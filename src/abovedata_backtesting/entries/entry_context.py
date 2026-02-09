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


def entry_context_from_row(row: dict) -> EntryContext | None:
    """
    Build EntryContext from a daily DataFrame row.

    Returns None if no entry context columns are present.
    """
    entry_type = row.get("entry_type")
    if entry_type is None:
        return None

    return EntryContext(
        entry_type=str(entry_type),
        signal_col=row.get("entry_signal_col"),
        signal_value=_safe_float(row.get("entry_signal_value")),
        signal_date=row.get("entry_signal_date"),
        raw_direction=int(row.get("entry_raw_direction", 0)),
        final_direction=int(row.get("entry_final_direction", 0)),
        flipped=bool(row.get("entry_flipped", False)),
        corr_col_used=row.get("entry_corr_col_used"),
        corr_value_used=_safe_float(row.get("entry_corr_value_used")),
        prior_quarter_corr=bool(row.get("entry_prior_quarter_corr", False)),
        confidence_col_used=row.get("entry_confidence_col_used"),
        confidence_value_used=_safe_float(row.get("entry_confidence_value_used")),
        correlation_regime=row.get("entry_correlation_regime"),
        regime_shift_detected=bool(row.get("entry_regime_shift_detected", False)),
        regime_shift_skipped=bool(row.get("entry_regime_shift_skipped", False)),
        momentum_zscore=_safe_float(row.get("entry_momentum_zscore")),
        lookback_days=_safe_int(row.get("entry_lookback_days")),
    )


def _safe_float(val: object) -> float | None:
    if val is None:
        return None
    try:
        f = float(val)  # type: ignore[arg-type]
        return f if f == f else None  # NaN check
    except (ValueError, TypeError):
        return None


def _safe_int(val: object) -> int | None:
    if val is None:
        return None
    try:
        return int(val)  # type: ignore[arg-type]
    except (ValueError, TypeError):
        return None
