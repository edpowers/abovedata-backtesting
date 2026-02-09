from __future__ import annotations

import datetime as dt
from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import product
from typing import Any, Self

import polars as pl

from abovedata_backtesting.entries.entry_context import (
    ENTRY_CONTEXT_COLUMNS,
    EntryContext,
)


class EntryRule(ABC):
    """Abstract base class for entry signal logic."""

    @abstractmethod
    def apply(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame,
    ) -> pl.DataFrame: ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def params(self) -> dict[str, Any]: ...

    @classmethod
    @abstractmethod
    def grid(cls, **param_lists: list[Any]) -> list[Self]: ...


def _resolve_entry_dates(
    market_data: pl.DataFrame,
    signal_dates: list[dt.date],
    entry_days_before: int,
) -> dict[dt.date, dt.date]:
    """Map each signal_date to an entry_date N trading days before it."""
    trading_dates = market_data["date"].to_list()
    date_to_idx = {d: i for i, d in enumerate(trading_dates)}

    entry_map: dict[dt.date, dt.date] = {}
    for sig_date in signal_dates:
        if sig_date not in date_to_idx:
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
    contexts: dict[dt.date, EntryContext],
) -> pl.DataFrame:
    """
    Apply sparse entry positions to market data, then forward-fill.

    Vectorized implementation: builds a sparse entries DataFrame,
    joins onto market_data by entry_date, then forward-fills.

    Writes:
        position, signal_strength, confidence, signal_id
        + entry context columns (if contexts provided)
    """
    # Build sparse entries DataFrame: one row per entry date
    rows: list[dict[str, Any]] = []
    for signal_id, entry_date in enumerate(sorted(entry_map.keys()), start=1):
        sig_date = entry_map[entry_date]
        row: dict[str, Any] = {
            "_entry_date": entry_date,
            "_position": directions.get(sig_date, 0.0),
            "_signal_strength": strengths.get(sig_date, 0.0),
            "_confidence": confidences.get(sig_date, 0.0),
            "_signal_id": signal_id,
        }
        # Add context columns
        ctx_row = _context_to_row(contexts.get(sig_date, EntryContext.make_empty()))
        for col in ENTRY_CONTEXT_COLUMNS:
            row[f"_{col}"] = ctx_row.get(col, None)

        rows.append(row)

    # Join onto market_data by date
    result = market_data.join(
        pl.DataFrame(rows),
        left_on="date",
        right_on="_entry_date",
        how="left",
    )

    # Forward-fill columns
    for src, dst, dtype in [
        ("_position", "position", pl.Float64),
        ("_signal_strength", "signal_strength", pl.Float64),
        ("_confidence", "confidence", pl.Float64),
        ("_signal_id", "signal_id", pl.Int32),
    ]:
        result = result.with_columns(
            pl.col(src)
            .forward_fill()
            .fill_null(0 if dtype != pl.Int32 else 0)
            .cast(dtype)
            .alias(dst),
        )

    # Forward-fill context columns
    for col in ENTRY_CONTEXT_COLUMNS:
        if f"_{col}" in result.columns:
            result = result.with_columns(
                pl.col(f"_{col}").forward_fill().alias(col),
            )

    # Drop temporary columns
    drop_cols = [c for c in result.columns if c.startswith("_")]
    result = result.drop(drop_cols)

    return result


def enforce_max_entries(
    daily: pl.DataFrame,
    max_entries_per_signal: int = 1,
) -> pl.DataFrame:
    """
    Prevent phantom re-entries after an exit fires within the same signal period.

    After an exit rule sets position to 0, the forward-filled position from
    _apply_entry_positions would re-enter the same direction on the next day.
    This function enforces that once a position is exited for a given signal_id,
    at most `max_entries_per_signal` entries are allowed per signal period.

    Parameters
    ----------
    daily : pl.DataFrame
        Must have columns: position, signal_id.
    max_entries_per_signal : int
        Maximum number of entry→exit round-trips allowed per signal period.
        1 = one trade per signal (default, prevents all re-entries).
        2 = allow one re-entry after the first exit, etc.

    Returns
    -------
    pl.DataFrame
        Same DataFrame with position zeroed out for excess re-entries.
    """
    if "signal_id" not in daily.columns or "position" not in daily.columns:
        return daily

    positions = daily["position"].to_list()
    signal_ids = daily["signal_id"].to_list()
    n = len(positions)

    # Track entry count per signal_id
    entries_by_signal: dict[int, int] = {}
    in_trade = False
    current_signal_id = 0
    suppressed = False  # True when we've exceeded max entries for this signal

    for i in range(n):
        sid = signal_ids[i]
        pos = positions[i]

        # New signal period — reset
        if sid != current_signal_id:
            current_signal_id = sid
            entries_by_signal[sid] = 0
            in_trade = False
            suppressed = False

        if suppressed:
            # We've exceeded max entries for this signal — force flat
            positions[i] = 0.0
            continue

        pos_active = abs(pos) > 0.01

        if pos_active and not in_trade:
            # New entry within this signal period
            entries_by_signal[sid] = entries_by_signal.get(sid, 0) + 1
            if entries_by_signal[sid] > max_entries_per_signal:
                # Exceeded max — suppress this and all subsequent entries
                suppressed = True
                positions[i] = 0.0
                continue
            in_trade = True
        elif not pos_active and in_trade:
            # Exit happened
            in_trade = False

    return daily.with_columns(
        pl.Series("position", positions, dtype=pl.Float64),
    )


def _context_to_row(ctx: EntryContext) -> dict[str, Any]:
    """Convert an EntryContext to a dict matching ENTRY_CONTEXT_COLUMNS."""
    return {
        "entry_type": ctx.entry_type,
        "entry_signal_col": ctx.signal_col,
        "entry_signal_value": ctx.signal_value,
        "entry_signal_date": ctx.signal_date,
        "entry_raw_direction": ctx.raw_direction,
        "entry_final_direction": ctx.final_direction,
        "entry_flipped": ctx.flipped,
        "entry_corr_col_used": ctx.corr_col_used,
        "entry_corr_value_used": ctx.corr_value_used,
        "entry_prior_quarter_corr": ctx.prior_quarter_corr,
        "entry_confidence_col_used": ctx.confidence_col_used,
        "entry_confidence_value_used": ctx.confidence_value_used,
        "entry_correlation_regime": ctx.correlation_regime,
        "entry_regime_shift_detected": ctx.regime_shift_detected,
        "entry_regime_shift_skipped": ctx.regime_shift_skipped,
        "entry_momentum_zscore": ctx.momentum_zscore,
        "entry_lookback_days": ctx.lookback_days,
    }


# =============================================================================
# Momentum (price-based entry, timed to signal dates)
# =============================================================================


@dataclass(frozen=True, slots=True)
class MomentumEntry(EntryRule):
    """Enter based on price momentum z-score, timed to signal dates."""

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
        contexts: dict[dt.date, EntryContext] = {}

        for entry_date, sig_date in entry_map.items():
            z = zscore_lookup.get(entry_date)
            if z is None or z != z:
                continue

            if z > self.zscore_threshold:
                direction = 1.0
            elif z < -self.zscore_threshold:
                direction = -1.0
            else:
                direction = 0.0

            directions[sig_date] = direction
            strengths[sig_date] = z if z == z else 0.0
            confidences[sig_date] = min(1.0, abs(z) / 3.0) if z == z else 0.0

            contexts[sig_date] = EntryContext(
                entry_type="momentum",
                signal_date=sig_date,
                raw_direction=int(direction),
                final_direction=int(direction),
                flipped=False,
                momentum_zscore=z if z == z else None,
                lookback_days=self.lookback_days,
            )

        return _apply_entry_positions(
            market_data, entry_map, directions, strengths, confidences, contexts
        )


# =============================================================================
# Signal threshold (fundamental only)
# =============================================================================


@dataclass(frozen=True, slots=True)
class SignalThresholdEntry(EntryRule):
    """Enter based on fundamental signal crossing a threshold."""

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
        contexts: dict[dt.date, EntryContext] = {}

        for _entry_date, sig_date in entry_map.items():
            val = signal_vals.get(sig_date)
            if val is None or val != val:
                continue
            if val >= self.long_threshold:
                direction = 1.0
            elif val <= self.short_threshold:
                direction = -1.0
            else:
                direction = 0.0

            directions[sig_date] = direction
            strengths[sig_date] = val
            conf = signal_confs.get(sig_date)
            conf_val = (
                min(1.0, abs(conf))
                if conf is not None and conf == conf
                else min(1.0, abs(val) / 3.0)
            )
            confidences[sig_date] = conf_val

            contexts[sig_date] = EntryContext(
                entry_type="signal_threshold",
                signal_col=self.signal_col,
                signal_value=val,
                signal_date=sig_date,
                raw_direction=int(direction),
                final_direction=int(direction),
                flipped=False,
                confidence_value_used=conf_val,
            )

        return _apply_entry_positions(
            market_data, entry_map, directions, strengths, confidences, contexts
        )


# =============================================================================
# Divergence (price vs fundamental)
# =============================================================================


@dataclass(frozen=True, slots=True)
class DivergenceEntry(EntryRule):
    """Enter when price momentum diverges from fundamental signal."""

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
        contexts: dict[dt.date, EntryContext] = {}

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
            conf_val = (mom_f * fund_f) ** 0.5 * weight
            confidences[sig_date] = conf_val

            contexts[sig_date] = EntryContext(
                entry_type="divergence",
                signal_col=self.signal_col,
                signal_value=val,
                signal_date=sig_date,
                raw_direction=int(_sign(val)),
                final_direction=int(direction),
                flipped=(_sign(val) != direction and direction != 0),
                momentum_zscore=z if z == z else None,
                lookback_days=self.lookback_days,
                confidence_value_used=conf_val,
            )

        return _apply_entry_positions(
            market_data, entry_map, directions, strengths, confidences, contexts
        )


# =============================================================================
# Signal + Momentum Confirmation
# =============================================================================


@dataclass(frozen=True, slots=True)
class SignalMomentumEntry(EntryRule):
    """Enter when fundamental signal AND price momentum agree."""

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
        contexts: dict[dt.date, EntryContext] = {}

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
                direction = 1.0
            elif short_sig and short_mom:
                direction = -1.0
            else:
                direction = 0.0

            directions[sig_date] = direction
            strengths[sig_date] = val
            mom_f = min(1.0, abs(z) / 3.0)
            fund_f = min(1.0, abs(val) / 3.0)
            conf_val = (mom_f * fund_f) ** 0.5
            confidences[sig_date] = conf_val

            contexts[sig_date] = EntryContext(
                entry_type="signal_momentum_confirmation",
                signal_col=self.signal_col,
                signal_value=val,
                signal_date=sig_date,
                raw_direction=int(_sign(val)),
                final_direction=int(direction),
                flipped=False,
                momentum_zscore=z if z == z else None,
                lookback_days=self.lookback_days,
                confidence_value_used=conf_val,
            )

        return _apply_entry_positions(
            market_data, entry_map, directions, strengths, confidences, contexts
        )


def _sign(x: float) -> float:
    return 1.0 if x > 0 else -1.0 if x < 0 else 0.0
