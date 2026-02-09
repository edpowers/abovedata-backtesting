"""
Entry context: records the decision state at entry time.

Created by the entry rule during apply(), propagated through
TradeLog.from_daily() → Trade → TradeAnalyzer.

This eliminates post-hoc reconstruction of which correlation was used,
whether a flip occurred, etc.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EntryContext:
    """
    Immutable record of the entry decision for a single trade.

    Created by the entry rule at apply() time, attached to each Trade.
    The TradeAnalyzer reads this directly instead of re-deriving.
    """

    # What entry type produced this trade
    entry_type: str  # "momentum", "corr_aware", "signal_threshold", etc.

    # Signal
    signal_col: str | None = None  # e.g., "visible_revenue_resid"
    signal_value: float | None = None  # the residual value at signal time
    signal_date: dt.date | None = None  # earnings date this trade is tied to

    # Direction derivation
    raw_direction: int = 0  # sign(signal) before any flip: +1, -1, 0
    final_direction: int = 0  # after flip (or same as raw if no flip)
    flipped: bool = False  # whether correlation flip was applied

    # Correlation context (only populated for corr_aware entries)
    corr_col_used: str | None = None  # "contemp", "leading", "contemp_ma", etc.
    corr_value_used: float | None = None  # actual correlation value used for direction
    prior_quarter_corr: bool = False  # whether we used prior quarter's correlation

    # Confidence
    confidence_col_used: str | None = None  # "contemp", "leading"
    confidence_value_used: float | None = None  # actual confidence score

    # Regime
    correlation_regime: str | None = None  # "strong_positive", "weak_negative", etc.
    regime_shift_detected: bool = False  # whether a regime shift was flagged
    regime_shift_skipped: bool = False  # whether we skipped due to regime shift

    # Momentum context (only populated for momentum/signal_momentum entries)
    momentum_zscore: float | None = None
    lookback_days: int | None = None

    @property
    def is_correlation_aware(self) -> bool:
        return self.corr_col_used is not None

    @property
    def has_signal(self) -> bool:
        return self.signal_value is not None

    @classmethod
    def make_empty(cls) -> EntryContext:
        return cls(entry_type="none")

    @classmethod
    def from_row(cls, row: dict) -> EntryContext | None:
        """Build EntryContext from a daily DataFrame row with entry_* columns."""
        if row.get("entry_type") is None:
            return None
        kwargs = {
            k.removeprefix("entry_"): v  # type: ignore
            for k, v in row.items()
            if (k.startswith("entry_") and k not in ["entry_type"])
        }
        kwargs["entry_type"] = row.get('entry_type')

        # Strip "entry_" prefix to match EntryContext field names
        return cls(**kwargs)


# Column name constants for daily DataFrame propagation
# Entry rules write these columns; TradeLog.from_daily() reads them.
ENTRY_CONTEXT_COLUMNS = [
    "entry_type",
    "entry_signal_col",
    "entry_signal_value",
    "entry_signal_date",
    "entry_raw_direction",
    "entry_final_direction",
    "entry_flipped",
    "entry_corr_col_used",
    "entry_corr_value_used",
    "entry_prior_quarter_corr",
    "entry_confidence_col_used",
    "entry_confidence_value_used",
    "entry_correlation_regime",
    "entry_regime_shift_detected",
    "entry_regime_shift_skipped",
    "entry_momentum_zscore",
    "entry_lookback_days",
]
