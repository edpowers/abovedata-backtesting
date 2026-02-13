"""Atomic signal transforms for the signal preprocessing pipeline.

Each transform adds new columns to the quarterly signal DataFrame.
All transforms enforce look-ahead bias safety:
- TimeShiftTransform requires shift_quarters >= 1
- All Polars shift() calls use positive N (row T gets value from T-N)
- ZScoreNormalizeTransform uses shift(1) on expanding mean/std
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import product
from typing import Any, Self

import polars as pl


class SignalTransform(ABC):
    """A single atomic transformation on the quarterly signal DataFrame."""

    @abstractmethod
    def apply(
        self, signals: pl.DataFrame, date_col: str = "earnings_date"
    ) -> pl.DataFrame:
        """Transform signals, returning DataFrame with new columns added.

        MUST NOT use future data. All shifts must be backward-looking.
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Short, unique identifier for this transform."""
        ...

    @abstractmethod
    def params(self) -> dict[str, Any]:
        """All parameters as a dict for audit trail."""
        ...

    @classmethod
    @abstractmethod
    def grid(cls, **param_lists: list[Any]) -> list[Self]:
        """Generate cartesian product of parameter variations."""
        ...

    @abstractmethod
    def output_columns(self) -> list[str]:
        """Names of columns this transform adds to the DataFrame."""
        ...


# =============================================================================
# TimeShiftTransform
# =============================================================================


@dataclass(frozen=True, slots=True)
class TimeShiftTransform(SignalTransform):
    """Shift signal column(s) by N quarters.

    shift_quarters=1 means: for each row at time T, use the value from T-1.
    This is SAFE because we're using past data.

    The result column is named: {col}_lag{N}q

    LOOK-AHEAD SAFETY: shift_quarters must be >= 1.
    """

    source_cols: tuple[str, ...]
    shift_quarters: int = 1

    def __post_init__(self) -> None:
        if self.shift_quarters < 1:
            raise ValueError(
                f"shift_quarters must be >= 1 (got {self.shift_quarters}). "
                "Shifting by 0 is a no-op; negative shifts create look-ahead bias."
            )

    @property
    def name(self) -> str:
        cols = "_".join(c.replace("_resid", "R") for c in self.source_cols)
        return f"lag{self.shift_quarters}q_{cols}"

    def output_columns(self) -> list[str]:
        return [f"{col}_lag{self.shift_quarters}q" for col in self.source_cols]

    def params(self) -> dict[str, Any]:
        return {
            "transform": "time_shift",
            "source_cols": list(self.source_cols),
            "shift_quarters": self.shift_quarters,
        }

    @classmethod
    def grid(
        cls,
        source_cols: list[tuple[str, ...]] | None = None,
        shift_quarters: list[int] | None = None,
    ) -> list[Self]:
        return [
            cls(sc, sq)
            for sc, sq in product(
                source_cols or [("visible_revenue_resid",)],
                shift_quarters or [1],
            )
        ]

    def apply(
        self, signals: pl.DataFrame, date_col: str = "earnings_date"
    ) -> pl.DataFrame:
        signals = signals.sort(date_col)
        for col in self.source_cols:
            if col in signals.columns:
                signals = signals.with_columns(
                    pl.col(col)
                    .shift(self.shift_quarters)
                    .alias(f"{col}_lag{self.shift_quarters}q")
                )
        return signals


# =============================================================================
# RateOfChangeTransform
# =============================================================================


@dataclass(frozen=True, slots=True)
class RateOfChangeTransform(SignalTransform):
    """Compute quarter-over-quarter rate of change.

    roc = (X[T] - X[T-n]) / (|X[T-n]| + eps)

    Output column: {col}_roc{n}q
    """

    source_col: str = "visible_revenue_resid"
    lookback_quarters: int = 1

    @property
    def name(self) -> str:
        col_short = self.source_col.replace("_resid", "R")
        return f"roc{self.lookback_quarters}q_{col_short}"

    def output_columns(self) -> list[str]:
        return [f"{self.source_col}_roc{self.lookback_quarters}q"]

    def params(self) -> dict[str, Any]:
        return {
            "transform": "rate_of_change",
            "source_col": self.source_col,
            "lookback_quarters": self.lookback_quarters,
        }

    @classmethod
    def grid(
        cls,
        source_col: list[str] | None = None,
        lookback_quarters: list[int] | None = None,
    ) -> list[Self]:
        return [
            cls(sc, lq)
            for sc, lq in product(
                source_col or ["visible_revenue_resid"],
                lookback_quarters or [1],
            )
        ]

    def apply(
        self, signals: pl.DataFrame, date_col: str = "earnings_date"
    ) -> pl.DataFrame:
        signals = signals.sort(date_col)
        if self.source_col not in signals.columns:
            return signals
        lagged = pl.col(self.source_col).shift(self.lookback_quarters)
        roc = (pl.col(self.source_col) - lagged) / (lagged.abs() + 1e-9)
        return signals.with_columns(
            roc.alias(f"{self.source_col}_roc{self.lookback_quarters}q")
        )


# =============================================================================
# AccelerationTransform
# =============================================================================


@dataclass(frozen=True, slots=True)
class AccelerationTransform(SignalTransform):
    """Second derivative: RoC[T] - RoC[T-1].

    Computes rate-of-change inline, then takes the difference.
    Output column: {col}_accel{n}q
    """

    source_col: str = "visible_revenue_resid"
    lookback_quarters: int = 1

    @property
    def name(self) -> str:
        col_short = self.source_col.replace("_resid", "R")
        return f"accel{self.lookback_quarters}q_{col_short}"

    def output_columns(self) -> list[str]:
        return [f"{self.source_col}_accel{self.lookback_quarters}q"]

    def params(self) -> dict[str, Any]:
        return {
            "transform": "acceleration",
            "source_col": self.source_col,
            "lookback_quarters": self.lookback_quarters,
        }

    @classmethod
    def grid(
        cls,
        source_col: list[str] | None = None,
        lookback_quarters: list[int] | None = None,
    ) -> list[Self]:
        return [
            cls(sc, lq)
            for sc, lq in product(
                source_col or ["visible_revenue_resid"],
                lookback_quarters or [1],
            )
        ]

    def apply(
        self, signals: pl.DataFrame, date_col: str = "earnings_date"
    ) -> pl.DataFrame:
        signals = signals.sort(date_col)
        if self.source_col not in signals.columns:
            return signals

        n = self.lookback_quarters
        lagged = pl.col(self.source_col).shift(n)
        roc = (pl.col(self.source_col) - lagged) / (lagged.abs() + 1e-9)

        out_col = f"{self.source_col}_accel{n}q"
        return (
            signals.with_columns(roc.alias("_roc_tmp"))
            .with_columns(
                (pl.col("_roc_tmp") - pl.col("_roc_tmp").shift(1)).alias(out_col)
            )
            .drop("_roc_tmp")
        )


# =============================================================================
# CrossSignalRatioTransform
# =============================================================================


@dataclass(frozen=True, slots=True)
class CrossSignalRatioTransform(SignalTransform):
    """Ratio of two signal columns: numerator / (|denominator| + eps).

    Output column: {numerator}_over_{denominator}
    """

    numerator_col: str = "visible_revenue_resid"
    denominator_col: str = "consensus_resid"

    @property
    def name(self) -> str:
        num_short = self.numerator_col.replace("_resid", "R")
        den_short = self.denominator_col.replace("_resid", "R")
        return f"{num_short}_over_{den_short}"

    def output_columns(self) -> list[str]:
        return [f"{self.numerator_col}_over_{self.denominator_col}"]

    def params(self) -> dict[str, Any]:
        return {
            "transform": "cross_signal_ratio",
            "numerator_col": self.numerator_col,
            "denominator_col": self.denominator_col,
        }

    @classmethod
    def grid(
        cls,
        numerator_col: list[str] | None = None,
        denominator_col: list[str] | None = None,
    ) -> list[Self]:
        return [
            cls(nc, dc)
            for nc, dc in product(
                numerator_col or ["visible_revenue_resid"],
                denominator_col or ["consensus_resid"],
            )
        ]

    def apply(
        self, signals: pl.DataFrame, date_col: str = "earnings_date"
    ) -> pl.DataFrame:
        if (
            self.numerator_col not in signals.columns
            or self.denominator_col not in signals.columns
        ):
            return signals
        ratio = pl.col(self.numerator_col) / (pl.col(self.denominator_col).abs() + 1e-9)
        return signals.with_columns(
            ratio.alias(f"{self.numerator_col}_over_{self.denominator_col}")
        )


# =============================================================================
# WeightedBlendTransform
# =============================================================================


@dataclass(frozen=True, slots=True)
class WeightedBlendTransform(SignalTransform):
    """Weighted blend: w * col_a + (1-w) * col_b.

    Primary use case: blending current-quarter and prior-quarter signals.
    Output column: blend_{col_a}_{col_b}_w{weight}
    """

    col_a: str = "visible_revenue_resid"
    col_b: str = "visible_revenue_resid_lag1q"
    weight_a: float = 0.5

    @property
    def name(self) -> str:
        a_short = self.col_a.replace("_resid", "R")
        b_short = self.col_b.replace("_resid", "R")
        return f"blend_{a_short}_{b_short}_w{self.weight_a}"

    def output_columns(self) -> list[str]:
        return [f"blend_{self.col_a}_{self.col_b}_w{self.weight_a}"]

    def params(self) -> dict[str, Any]:
        return {
            "transform": "weighted_blend",
            "col_a": self.col_a,
            "col_b": self.col_b,
            "weight_a": self.weight_a,
        }

    @classmethod
    def grid(
        cls,
        col_a: list[str] | None = None,
        col_b: list[str] | None = None,
        weight_a: list[float] | None = None,
    ) -> list[Self]:
        return [
            cls(a, b, w)
            for a, b, w in product(
                col_a or ["visible_revenue_resid"],
                col_b or ["visible_revenue_resid_lag1q"],
                weight_a or [0.5],
            )
        ]

    def apply(
        self, signals: pl.DataFrame, date_col: str = "earnings_date"
    ) -> pl.DataFrame:
        if self.col_a not in signals.columns or self.col_b not in signals.columns:
            return signals
        blend = pl.col(self.col_a) * self.weight_a + pl.col(self.col_b) * (
            1.0 - self.weight_a
        )
        return signals.with_columns(
            blend.alias(f"blend_{self.col_a}_{self.col_b}_w{self.weight_a}")
        )


# =============================================================================
# DifferenceTransform
# =============================================================================


@dataclass(frozen=True, slots=True)
class DifferenceTransform(SignalTransform):
    """Difference between two columns: col_a - col_b.

    Output column: diff_{col_a}_{col_b}
    """

    col_a: str = "visible_revenue_resid"
    col_b: str = "visible_revenue_resid_lag1q"

    @property
    def name(self) -> str:
        a_short = self.col_a.replace("_resid", "R")
        b_short = self.col_b.replace("_resid", "R")
        return f"diff_{a_short}_{b_short}"

    def output_columns(self) -> list[str]:
        return [f"diff_{self.col_a}_{self.col_b}"]

    def params(self) -> dict[str, Any]:
        return {
            "transform": "difference",
            "col_a": self.col_a,
            "col_b": self.col_b,
        }

    @classmethod
    def grid(
        cls,
        col_a: list[str] | None = None,
        col_b: list[str] | None = None,
    ) -> list[Self]:
        return [
            cls(a, b)
            for a, b in product(
                col_a or ["visible_revenue_resid"],
                col_b or ["visible_revenue_resid_lag1q"],
            )
        ]

    def apply(
        self, signals: pl.DataFrame, date_col: str = "earnings_date"
    ) -> pl.DataFrame:
        if self.col_a not in signals.columns or self.col_b not in signals.columns:
            return signals
        diff = pl.col(self.col_a) - pl.col(self.col_b)
        return signals.with_columns(diff.alias(f"diff_{self.col_a}_{self.col_b}"))


# =============================================================================
# ZScoreNormalizeTransform
# =============================================================================


@dataclass(frozen=True, slots=True)
class ZScoreNormalizeTransform(SignalTransform):
    """Expanding-window z-score normalization.

    z[T] = (X[T] - mean(X[0:T-1])) / std(X[0:T-1])

    Uses shift(1) on expanding mean/std to prevent look-ahead bias.
    Output column: {col}_znorm
    """

    source_col: str = "visible_revenue_resid"
    min_periods: int = 4

    @property
    def name(self) -> str:
        col_short = self.source_col.replace("_resid", "R")
        return f"znorm_{col_short}"

    def output_columns(self) -> list[str]:
        return [f"{self.source_col}_znorm"]

    def params(self) -> dict[str, Any]:
        return {
            "transform": "zscore_normalize",
            "source_col": self.source_col,
            "min_periods": self.min_periods,
        }

    @classmethod
    def grid(
        cls,
        source_col: list[str] | None = None,
        min_periods: list[int] | None = None,
    ) -> list[Self]:
        return [
            cls(sc, mp)
            for sc, mp in product(
                source_col or ["visible_revenue_resid"],
                min_periods or [4],
            )
        ]

    def apply(
        self, signals: pl.DataFrame, date_col: str = "earnings_date"
    ) -> pl.DataFrame:
        signals = signals.sort(date_col)
        if self.source_col not in signals.columns:
            return signals

        col = pl.col(self.source_col)
        # Expanding mean: cum_sum / cum_count, shifted by 1 to exclude current
        expanding_mean = (col.cum_sum() / col.cum_count()).shift(1)
        # Expanding std via rolling with full window, shifted by 1
        n = signals.height
        expanding_std = col.rolling_std(
            window_size=n, min_samples=self.min_periods
        ).shift(1)

        z = (col - expanding_mean) / (expanding_std + 1e-9)

        return signals.with_columns(z.alias(f"{self.source_col}_znorm"))
