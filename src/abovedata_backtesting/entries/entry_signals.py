"""Entry signal definitions for strategy grid search.

Each EntryRule produces positions ONLY on signal-derived dates
(earnings_date minus entry_days_before trading days). Between
signal dates, position is 0 unless held by an exit rule.

This prevents the compounding illusion from daily position × return.
"""

from __future__ import annotations

import datetime as dt
from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import product
from typing import Any, Self

import polars as pl


class EntryRule(ABC):
    """
    Abstract base class for entry signal logic.

    Entry rules produce positions ONLY on specific dates derived from
    signal/earnings dates. The entry_days_before parameter controls
    how many trading days before the signal date to enter.
    """

    @abstractmethod
    def apply(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame,
    ) -> pl.DataFrame:
        """
        Compute positions from market data and signals.

        Parameters
        ----------
        market_data : pl.DataFrame
            Daily OHLCV with at least: date, close. Sorted by date.
        signals : pl.DataFrame
            Fundamental signal data with earnings_date and signal columns.

        Returns
        -------
        pl.DataFrame
            market_data with added columns: position, signal_strength, confidence.
            position is non-zero ONLY on entry dates, then forward-filled
            until the next signal or end of data. Exit rules trim from there.
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable identifier including parameter values."""

    @abstractmethod
    def params(self) -> dict[str, Any]:
        """Return current parameters as a flat dict (for results DataFrame)."""

    @classmethod
    @abstractmethod
    def grid(cls, **param_lists: list[Any]) -> list[Self]:
        """Generate all parameter combinations from lists of values."""


def _resolve_entry_dates(
    market_data: pl.DataFrame,
    signal_dates: list[dt.date],
    entry_days_before: int,
) -> dict[dt.date, dt.date]:
    """
    Map each signal_date to an entry_date that is N trading days before it.

    Returns dict of {entry_date: signal_date}.
    If entry_date falls before the market data range, it's skipped.
    """
    trading_dates = market_data["date"].to_list()
    date_to_idx = {d: i for i, d in enumerate(trading_dates)}

    entry_map: dict[dt.date, dt.date] = {}
    for sig_date in signal_dates:
        if sig_date not in date_to_idx:
            # Find nearest prior trading day
            candidates = [d for d in trading_dates if d <= sig_date]
            if not candidates:
                continue
            sig_idx = date_to_idx[candidates[-1]]
        else:
            sig_idx = date_to_idx[sig_date]

        entry_idx = sig_idx - entry_days_before
        if entry_idx >= 0:
            entry_map[trading_dates[entry_idx]] = sig_date

    return entry_map


def _apply_entry_positions(
    market_data: pl.DataFrame,
    entry_map: dict[dt.date, dt.date],
    directions: dict[dt.date, float],
    strengths: dict[dt.date, float],
    confidences: dict[dt.date, float],
) -> pl.DataFrame:
    """
    Apply sparse entry positions to market data, then forward-fill.

    Entry dates get their computed position. Between entries, the most
    recent non-zero position is held (forward-filled). Exit rules
    then trim positions based on their logic.
    """
    entry_dates_set = set(entry_map.keys())
    dates = market_data["date"].to_list()

    positions: list[float] = []
    signal_strengths: list[float] = []
    confs: list[float] = []
    current_pos = 0.0
    current_strength = 0.0
    current_conf = 0.0

    for d in dates:
        if d in entry_dates_set:
            sig_date = entry_map[d]
            new_pos = directions.get(sig_date, 0.0)
            current_pos = new_pos
            current_strength = strengths.get(sig_date, 0.0)
            current_conf = confidences.get(sig_date, 0.0)

        positions.append(current_pos)
        signal_strengths.append(current_strength)
        confs.append(current_conf)

    return market_data.with_columns(
        pl.Series("position", positions, dtype=pl.Float64),
        pl.Series("signal_strength", signal_strengths, dtype=pl.Float64),
        pl.Series("confidence", confs, dtype=pl.Float64),
    )


# =============================================================================
# Momentum (price-based entry, timed to signal dates)
# =============================================================================


@dataclass(frozen=True, slots=True)
class MomentumEntry(EntryRule):
    """
    Enter based on price momentum z-score, timed to signal dates.

    Momentum is evaluated at entry_date (N trading days before earnings).
    Long when momentum z-score > threshold, short when < -threshold.
    """

    lookback_days: int = 20
    zscore_threshold: float = 1.0
    zscore_window: int = 60
    entry_days_before: int = 0
    date_col: str = "earnings_date"

    @property
    def name(self) -> str:
        return f"momentum_lb{self.lookback_days}_z{self.zscore_threshold}_e{self.entry_days_before}d"

    def params(self) -> dict[str, Any]:
        return {
            "entry_type": "momentum",
            "lookback_days": self.lookback_days,
            "zscore_threshold": self.zscore_threshold,
            "zscore_window": self.zscore_window,
            "entry_days_before": self.entry_days_before,
        }

    @classmethod
    def grid(
        cls,
        lookback_days: list[int] | None = None,
        zscore_threshold: list[float] | None = None,
        zscore_window: list[int] | None = None,
        entry_days_before: list[int] | None = None,
        date_col: list[str] | None = None,
    ) -> list[Self]:
        return [
            cls(lb, zt, zw, edb, dc)
            for lb, zt, zw, edb, dc in product(
                lookback_days or [20],
                zscore_threshold or [1.0],
                zscore_window or [60],
                entry_days_before or [0],
                date_col or ["earnings_date"],
            )
        ]

    def apply(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame,
    ) -> pl.DataFrame:
        signal_dates = (
            signals[self.date_col].cast(pl.Date).drop_nulls().unique().sort().to_list()
        )
        entry_map = _resolve_entry_dates(
            market_data, signal_dates, self.entry_days_before
        )

        # Compute momentum z-score on full market data
        momentum = pl.col("close") / pl.col("close").shift(self.lookback_days) - 1
        lagged_momentum = momentum.shift(1)

        scored = (
            market_data.sort("date")
            .with_columns(momentum.alias("_momentum"))
            .with_columns(
                lagged_momentum.rolling_mean(self.zscore_window).alias("_mom_mean"),
                lagged_momentum.rolling_std(self.zscore_window).alias("_mom_std"),
            )
            .with_columns(
                (
                    (pl.col("_momentum") - pl.col("_mom_mean")) / pl.col("_mom_std")
                ).alias("_mom_zscore"),
            )
        )

        zscore_lookup = dict(
            zip(scored["date"].to_list(), scored["_mom_zscore"].to_list())
        )

        directions: dict[dt.date, float] = {}
        strengths: dict[dt.date, float] = {}
        confidences: dict[dt.date, float] = {}

        for entry_date, sig_date in entry_map.items():
            z = zscore_lookup.get(entry_date)
            if z is None or z != z:  # NaN check
                continue
            if z > self.zscore_threshold:
                directions[sig_date] = 1.0
            elif z < -self.zscore_threshold:
                directions[sig_date] = -1.0
            else:
                directions[sig_date] = 0.0
            strengths[sig_date] = z if z == z else 0.0
            confidences[sig_date] = min(1.0, abs(z) / 3.0) if z == z else 0.0

        return _apply_entry_positions(
            market_data, entry_map, directions, strengths, confidences
        )


# =============================================================================
# Signal threshold (fundamental only)
# =============================================================================


@dataclass(frozen=True, slots=True)
class SignalThresholdEntry(EntryRule):
    """
    Enter based on fundamental signal crossing a threshold.
    Entry is timed to entry_days_before the earnings date.
    """

    signal_col: str = "visible_revenue_resid"
    long_threshold: float = 0.5
    short_threshold: float = -0.5
    entry_days_before: int = 0
    date_col: str = "earnings_date"
    confidence_col: str | None = None

    @property
    def name(self) -> str:
        col_short = self.signal_col.replace("_to_total_revenue", "").replace(
            "visible_revenue_", "vr_"
        )
        return f"signal_{col_short}_l{self.long_threshold}_s{self.short_threshold}_e{self.entry_days_before}d"

    def params(self) -> dict[str, Any]:
        return {
            "entry_type": "signal_threshold",
            "signal_col": self.signal_col,
            "long_threshold": self.long_threshold,
            "short_threshold": self.short_threshold,
            "entry_days_before": self.entry_days_before,
        }

    @classmethod
    def grid(
        cls,
        signal_col: list[str] | None = None,
        long_threshold: list[float] | None = None,
        short_threshold: list[float] | None = None,
        entry_days_before: list[int] | None = None,
        date_col: list[str] | None = None,
        confidence_col: list[str | None] | None = None,
    ) -> list[Self]:
        return [
            cls(sc, lt, st, edb, dc, cc)
            for sc, lt, st, edb, dc, cc in product(
                signal_col or ["visible_revenue_resid"],
                long_threshold or [0.5],
                short_threshold or [-0.5],
                entry_days_before or [0],
                date_col or ["earnings_date"],
                confidence_col or [None],
            )
        ]

    def apply(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame,
    ) -> pl.DataFrame:
        if self.signal_col not in signals.columns:
            return market_data.with_columns(
                pl.lit(0.0).alias("position"),
                pl.lit(0.0).alias("signal_strength"),
                pl.lit(0.0).alias("confidence"),
            )

        sig_rows = signals.select(
            pl.col(self.date_col).cast(pl.Date).alias("sig_date"),
            pl.col(self.signal_col).alias("sig_val"),
            *(
                [pl.col(self.confidence_col).alias("sig_conf")]
                if self.confidence_col and self.confidence_col in signals.columns
                else []
            ),
        ).drop_nulls(subset=["sig_date", "sig_val"])

        signal_dates = sig_rows["sig_date"].to_list()
        signal_vals = dict(zip(signal_dates, sig_rows["sig_val"].to_list()))
        signal_confs = (
            dict(zip(signal_dates, sig_rows["sig_conf"].to_list()))
            if "sig_conf" in sig_rows.columns
            else {}
        )

        entry_map = _resolve_entry_dates(
            market_data, signal_dates, self.entry_days_before
        )

        directions: dict[dt.date, float] = {}
        strengths: dict[dt.date, float] = {}
        confidences: dict[dt.date, float] = {}

        for _entry_date, sig_date in entry_map.items():
            val = signal_vals.get(sig_date)
            if val is None or val != val:
                continue
            if val >= self.long_threshold:
                directions[sig_date] = 1.0
            elif val <= self.short_threshold:
                directions[sig_date] = -1.0
            else:
                directions[sig_date] = 0.0
            strengths[sig_date] = val
            conf = signal_confs.get(sig_date)
            confidences[sig_date] = (
                min(1.0, abs(conf))
                if conf is not None and conf == conf
                else min(1.0, abs(val) / 3.0)
            )

        return _apply_entry_positions(
            market_data, entry_map, directions, strengths, confidences
        )


# =============================================================================
# Divergence (price vs fundamental)
# =============================================================================


@dataclass(frozen=True, slots=True)
class DivergenceEntry(EntryRule):
    """
    Enter when price momentum diverges from fundamental signal.
    Price up + fundamental weak → Short. Price down + fundamental strong → Long.
    """

    signal_col: str = "visible_revenue_resid"
    lookback_days: int = 20
    divergence_zscore: float = 1.0
    fundamental_threshold: float = 1.0
    zscore_window: int = 60
    require_strong_divergence: bool = False
    entry_days_before: int = 0
    date_col: str = "earnings_date"

    @property
    def name(self) -> str:
        strength = "strong" if self.require_strong_divergence else "any"
        return (
            f"divergence_lb{self.lookback_days}_dz{self.divergence_zscore}"
            f"_ft{self.fundamental_threshold}_{strength}_e{self.entry_days_before}d"
        )

    def params(self) -> dict[str, Any]:
        return {
            "entry_type": "divergence",
            "signal_col": self.signal_col,
            "lookback_days": self.lookback_days,
            "divergence_zscore": self.divergence_zscore,
            "fundamental_threshold": self.fundamental_threshold,
            "require_strong_divergence": self.require_strong_divergence,
            "entry_days_before": self.entry_days_before,
        }

    @classmethod
    def grid(
        cls,
        signal_col: list[str] | None = None,
        lookback_days: list[int] | None = None,
        divergence_zscore: list[float] | None = None,
        fundamental_threshold: list[float] | None = None,
        require_strong_divergence: list[bool] | None = None,
        entry_days_before: list[int] | None = None,
        date_col: list[str] | None = None,
    ) -> list[Self]:
        return [
            cls(sc, lb, dz, ft, 60, rsd, edb, dc)
            for sc, lb, dz, ft, rsd, edb, dc in product(
                signal_col or ["visible_revenue_resid"],
                lookback_days or [20],
                divergence_zscore or [1.0],
                fundamental_threshold or [1.0],
                require_strong_divergence or [False],
                entry_days_before or [0],
                date_col or ["earnings_date"],
            )
        ]

    def apply(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame,
    ) -> pl.DataFrame:
        if self.signal_col not in signals.columns:
            return market_data.with_columns(
                pl.lit(0.0).alias("position"),
                pl.lit(0.0).alias("signal_strength"),
                pl.lit(0.0).alias("confidence"),
            )

        momentum = pl.col("close") / pl.col("close").shift(self.lookback_days) - 1
        lagged_momentum = momentum.shift(1)

        scored = (
            market_data.sort("date")
            .with_columns(momentum.alias("_momentum"))
            .with_columns(
                lagged_momentum.rolling_mean(self.zscore_window).alias("_mom_mean"),
                lagged_momentum.rolling_std(self.zscore_window).alias("_mom_std"),
            )
            .with_columns(
                (
                    (pl.col("_momentum") - pl.col("_mom_mean")) / pl.col("_mom_std")
                ).alias("_mom_zscore"),
            )
        )

        zscore_lookup = dict(
            zip(scored["date"].to_list(), scored["_mom_zscore"].to_list())
        )

        sig_rows = signals.select(
            pl.col(self.date_col).cast(pl.Date).alias("sig_date"),
            pl.col(self.signal_col).alias("sig_val"),
        ).drop_nulls()

        signal_dates = sig_rows["sig_date"].to_list()
        signal_vals = dict(zip(signal_dates, sig_rows["sig_val"].to_list()))

        entry_map = _resolve_entry_dates(
            market_data, signal_dates, self.entry_days_before
        )

        directions: dict[dt.date, float] = {}
        strengths: dict[dt.date, float] = {}
        confidences: dict[dt.date, float] = {}

        for entry_date, sig_date in entry_map.items():
            z = zscore_lookup.get(entry_date)
            val = signal_vals.get(sig_date)
            if z is None or z != z or val is None or val != val:
                continue

            price_high = z > self.divergence_zscore
            price_low = z < -self.divergence_zscore
            fund_strong = val > self.fundamental_threshold
            fund_weak = val < -self.fundamental_threshold

            direction = 0.0
            weight = 1.0
            if price_high and fund_weak:
                direction = -1.0
            elif price_low and fund_strong:
                direction = 1.0
            elif not self.require_strong_divergence:
                if price_high and val < 0:
                    direction, weight = -1.0, 0.5
                elif price_low and val > 0:
                    direction, weight = 1.0, 0.5

            directions[sig_date] = direction * weight
            strengths[sig_date] = val
            mom_f = min(1.0, abs(z) / 3.0)
            fund_f = min(1.0, abs(val) / 3.0)
            confidences[sig_date] = (mom_f * fund_f) ** 0.5 * weight

        return _apply_entry_positions(
            market_data, entry_map, directions, strengths, confidences
        )


# =============================================================================
# Signal + Momentum Confirmation
# =============================================================================


@dataclass(frozen=True, slots=True)
class SignalMomentumEntry(EntryRule):
    """
    Enter when fundamental signal AND price momentum agree.
    Both must exceed thresholds in the same direction.
    """

    signal_col: str = "visible_revenue_resid"
    signal_threshold: float = 0.5
    lookback_days: int = 20
    momentum_zscore_threshold: float = 0.5
    zscore_window: int = 60
    entry_days_before: int = 0
    date_col: str = "earnings_date"

    @property
    def name(self) -> str:
        return (
            f"confirm_st{self.signal_threshold}_mz{self.momentum_zscore_threshold}"
            f"_lb{self.lookback_days}_e{self.entry_days_before}d"
        )

    def params(self) -> dict[str, Any]:
        return {
            "entry_type": "signal_momentum_confirmation",
            "signal_col": self.signal_col,
            "signal_threshold": self.signal_threshold,
            "lookback_days": self.lookback_days,
            "momentum_zscore_threshold": self.momentum_zscore_threshold,
            "entry_days_before": self.entry_days_before,
        }

    @classmethod
    def grid(
        cls,
        signal_col: list[str] | None = None,
        signal_threshold: list[float] | None = None,
        lookback_days: list[int] | None = None,
        momentum_zscore_threshold: list[float] | None = None,
        entry_days_before: list[int] | None = None,
        date_col: list[str] | None = None,
    ) -> list[Self]:
        return [
            cls(sc, st, lb, mzt, 60, edb, dc)
            for sc, st, lb, mzt, edb, dc in product(
                signal_col or ["visible_revenue_resid"],
                signal_threshold or [0.5],
                lookback_days or [20],
                momentum_zscore_threshold or [0.5],
                entry_days_before or [0],
                date_col or ["earnings_date"],
            )
        ]

    def apply(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame,
    ) -> pl.DataFrame:
        if self.signal_col not in signals.columns:
            return market_data.with_columns(
                pl.lit(0.0).alias("position"),
                pl.lit(0.0).alias("signal_strength"),
                pl.lit(0.0).alias("confidence"),
            )

        momentum = pl.col("close") / pl.col("close").shift(self.lookback_days) - 1
        lagged_momentum = momentum.shift(1)

        scored = (
            market_data.sort("date")
            .with_columns(momentum.alias("_momentum"))
            .with_columns(
                lagged_momentum.rolling_mean(self.zscore_window).alias("_mom_mean"),
                lagged_momentum.rolling_std(self.zscore_window).alias("_mom_std"),
            )
            .with_columns(
                (
                    (pl.col("_momentum") - pl.col("_mom_mean")) / pl.col("_mom_std")
                ).alias("_mom_zscore"),
            )
        )

        zscore_lookup = dict(
            zip(scored["date"].to_list(), scored["_mom_zscore"].to_list())
        )

        sig_rows = signals.select(
            pl.col(self.date_col).cast(pl.Date).alias("sig_date"),
            pl.col(self.signal_col).alias("sig_val"),
        ).drop_nulls()

        signal_dates = sig_rows["sig_date"].to_list()
        signal_vals = dict(zip(signal_dates, sig_rows["sig_val"].to_list()))

        entry_map = _resolve_entry_dates(
            market_data, signal_dates, self.entry_days_before
        )

        directions: dict[dt.date, float] = {}
        strengths: dict[dt.date, float] = {}
        confidences: dict[dt.date, float] = {}

        for entry_date, sig_date in entry_map.items():
            z = zscore_lookup.get(entry_date)
            val = signal_vals.get(sig_date)
            if z is None or z != z or val is None or val != val:
                continue

            long_sig = val > self.signal_threshold
            short_sig = val < -self.signal_threshold
            long_mom = z > self.momentum_zscore_threshold
            short_mom = z < -self.momentum_zscore_threshold

            if long_sig and long_mom:
                directions[sig_date] = 1.0
            elif short_sig and short_mom:
                directions[sig_date] = -1.0
            else:
                directions[sig_date] = 0.0

            strengths[sig_date] = val
            mom_f = min(1.0, abs(z) / 3.0)
            fund_f = min(1.0, abs(val) / 3.0)
            confidences[sig_date] = (mom_f * fund_f) ** 0.5

        return _apply_entry_positions(
            market_data, entry_map, directions, strengths, confidences
        )
