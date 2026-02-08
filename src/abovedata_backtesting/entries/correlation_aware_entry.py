"""Correlation-aware entry rule with intra-quarter signal estimation.

Uses correlation context to determine trade direction, and estimates
the signal value at entry time based on how far into the quarter we are.

Signal estimation logic:
- quarter_start to quarter_end: filings accumulate
- quarter_end to earnings_date (~20 days): remaining filings trickle in
- entry_date maps to a completion fraction based on position in quarter
- signal_at_entry = final_signal * completion_fraction

If a daily transaction DataFrame is provided, uses actual cumulative
values instead of linear interpolation.

Correlation context (contemp_corr, leading_corr, confidence) comes from
the most recently COMPLETED quarter — no look-ahead.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from itertools import product
from typing import Any, Self

import polars as pl

from abovedata_backtesting.entries.entry_signals import (
    EntryRule,
    _apply_entry_positions,
    _resolve_entry_dates,
)

_CORR_COL_MAP: dict[str, str] = {
    "contemp": "contemp_corr_historical",
    "leading": "leading_corr_historical",
    "contemp_ma": "contemp_corr_ma",
    "leading_ma": "leading_corr_ma",
}

_CONF_COL_MAP: dict[str, str] = {
    "contemp": "contemp_confidence",
    "leading": "leading_confidence",
}

_REGIME_COL_MAP: dict[str, str] = {
    "contemp": "contemp_regime_shift",
    "leading": "leading_regime_shift",
    "contemp_ma": "contemp_regime_shift",
    "leading_ma": "leading_regime_shift",
}


# =============================================================================
# Intra-quarter signal estimation
# =============================================================================


def estimate_signal_at_entry(
    entry_date: dt.date,
    quarter_start: dt.date,
    quarter_end: dt.date,
    earnings_date: dt.date,
    final_signal: float,
    final_pct_complete: float | None = None,
    daily_cumulative: dict[dt.date, float] | None = None,
) -> tuple[float, float]:
    """
    Estimate the signal value at entry_date based on quarter progress.

    Parameters
    ----------
    entry_date : dt.date
        The date we want to enter the trade.
    quarter_start : dt.date
        Start of the fiscal quarter.
    quarter_end : dt.date
        End of the fiscal quarter.
    earnings_date : dt.date
        Date of the earnings call (~20 days after quarter_end).
    final_signal : float
        The final signal value (visible_revenue_resid) at earnings_date.
    final_pct_complete : float | None
        The pct_count_complete at earnings_date (e.g., 0.90).
        If None, assumed to be 1.0.
    daily_cumulative : dict[dt.date, float] | None
        Optional: actual daily cumulative signal values keyed by date.
        If provided, uses exact values instead of linear interpolation.

    Returns
    -------
    tuple[float, float]
        (estimated_signal, completion_fraction)
        completion_fraction is in [0, 1] representing how much of
        the quarter's data is available at entry_date.
    """
    # If we have actual daily data, use it
    if daily_cumulative is not None:
        if entry_date in daily_cumulative:
            actual = daily_cumulative[entry_date]
            frac = abs(actual / final_signal) if final_signal != 0 else 0.0
            return actual, min(frac, 1.0)
        # Fall back to nearest prior date
        prior_dates = sorted(d for d in daily_cumulative if d <= entry_date)
        if prior_dates:
            actual = daily_cumulative[prior_dates[-1]]
            frac = abs(actual / final_signal) if final_signal != 0 else 0.0
            return actual, min(frac, 1.0)
        return 0.0, 0.0

    # Linear interpolation based on calendar position
    # Filing accumulation spans quarter_start → earnings_date
    total_span = (earnings_date - quarter_start).days
    if total_span <= 0:
        return final_signal, 1.0

    days_elapsed = (entry_date - quarter_start).days

    if days_elapsed <= 0:
        # Before quarter started — no signal from this quarter
        return 0.0, 0.0
    elif days_elapsed >= total_span:
        # At or past earnings_date — full signal
        return final_signal, 1.0
    else:
        # Linear interpolation
        max_coverage = final_pct_complete if final_pct_complete else 1.0
        raw_fraction = days_elapsed / total_span
        completion = raw_fraction * max_coverage
        estimated_signal = final_signal * raw_fraction
        return estimated_signal, completion


def _get_prior_quarter_context(
    earnings_date: dt.date,
    signal_rows: list[dict[str, Any]],
    corr_col_name: str,
    conf_col_name: str,
    regime_col_name: str,
) -> dict[str, Any]:
    """
    Get correlation context from the most recently completed quarter.

    For a trade entered during Q2, we use Q1's correlation context.
    This is fully causal — no look-ahead.
    """
    prior = None
    for row in signal_rows:
        row_ed = row["_parsed_date"]
        if row_ed < earnings_date:
            prior = row
        else:
            break  # rows are sorted by date

    if prior is None:
        return {"correlation": None, "confidence": None, "regime_shift": None}

    return {
        "correlation": _safe_float(prior.get(corr_col_name)),
        "confidence": _safe_float(prior.get(conf_col_name)),
        "regime_shift": prior.get(regime_col_name),
    }


# =============================================================================
# Entry rule
# =============================================================================


@dataclass(frozen=True, slots=True)
class CorrelationAwareEntry(EntryRule):
    """
    Enter on every signal date, using correlation context for direction
    and intra-quarter signal estimation for early entries.

    Signal estimation:
        At entry_days_before=N, estimates signal as a fraction of the
        final quarterly value based on calendar position within the quarter.
        Optional daily_cumulative DataFrame overrides with actual values.

    Direction logic:
        direction = sign(estimated_signal) * sign(correlation)

    Correlation context:
        use_prior_quarter_corr=True (default): correlation from the most
        recently completed quarter. Fully causal for early entries.
        use_prior_quarter_corr=False: same-row correlation (only safe
        for entry_days_before=0).
    """

    signal_col: str = "visible_revenue_resid"
    corr_col: str = "contemp"
    min_signal_abs: float = 0.0
    skip_regime_shifts: bool = True
    scale_by_confidence: bool = False
    confidence_col: str = "contemp"
    entry_days_before: int = 0
    use_prior_quarter_corr: bool = True
    date_col: str = "earnings_date"

    @property
    def name(self) -> str:
        parts = [f"corr_aware_{self.corr_col}"]
        if self.min_signal_abs > 0:
            parts.append(f"min{self.min_signal_abs}")
        if self.skip_regime_shifts:
            parts.append("noshift")
        if self.scale_by_confidence:
            parts.append("scaled")
        if not self.use_prior_quarter_corr:
            parts.append("sameq")
        parts.append(f"e{self.entry_days_before}d")
        return "_".join(parts)

    def params(self) -> dict[str, Any]:
        return {
            "entry_type": "correlation_aware",
            "signal_col": self.signal_col,
            "corr_col": self.corr_col,
            "min_signal_abs": self.min_signal_abs,
            "skip_regime_shifts": self.skip_regime_shifts,
            "scale_by_confidence": self.scale_by_confidence,
            "confidence_col": self.confidence_col,
            "entry_days_before": self.entry_days_before,
            "use_prior_quarter_corr": self.use_prior_quarter_corr,
        }

    @classmethod
    def grid(
        cls,
        signal_col: list[str] | None = None,
        corr_col: list[str] | None = None,
        min_signal_abs: list[float] | None = None,
        skip_regime_shifts: list[bool] | None = None,
        scale_by_confidence: list[bool] | None = None,
        confidence_col: list[str] | None = None,
        entry_days_before: list[int] | None = None,
        use_prior_quarter_corr: list[bool] | None = None,
        date_col: list[str] | None = None,
    ) -> list[Self]:
        seen: set[tuple] = set()
        results: list[Self] = []
        for sc, cc, msa, srs, sbc, cfc, edb, upqc, dc in product(
            signal_col or ["visible_revenue_resid"],
            corr_col or ["contemp", "leading"],
            min_signal_abs or [0.0],
            skip_regime_shifts or [True],
            scale_by_confidence or [False],
            confidence_col or ["contemp"],
            entry_days_before or [0],
            use_prior_quarter_corr or [True],
            date_col or ["earnings_date"],
        ):
            # Deduplicate: confidence_col irrelevant when not scaling
            effective_cfc = cfc if sbc else "contemp"
            # use_prior_quarter_corr irrelevant when entry_days_before=0
            effective_upqc = upqc if edb > 0 else True
            key = (sc, cc, msa, srs, sbc, effective_cfc, edb, effective_upqc, dc)
            if key in seen:
                continue
            seen.add(key)
            results.append(
                cls(
                    sc,
                    cc,
                    msa,
                    srs,
                    sbc,
                    effective_cfc,
                    edb,
                    effective_upqc,
                    dc,
                )
            )
        return results

    def apply(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame,
        daily_cumulative: pl.DataFrame | None = None,
    ) -> pl.DataFrame:
        if self.signal_col not in signals.columns:
            return market_data.with_columns(
                pl.lit(0.0).alias("position"),
                pl.lit(0.0).alias("signal_strength"),
                pl.lit(0.0).alias("confidence"),
            )

        # Resolve column names
        corr_col_name = _CORR_COL_MAP.get(self.corr_col, self.corr_col)
        conf_col_name = _CONF_COL_MAP.get(self.confidence_col, self.confidence_col)
        regime_col_name = _REGIME_COL_MAP.get(self.corr_col, "contemp_regime_shift")

        # Build daily cumulative lookup if provided
        daily_cum_lookup: dict[dt.date, float] | None = None
        if daily_cumulative is not None and self.signal_col in daily_cumulative.columns:
            daily_cum_lookup = dict(
                zip(
                    daily_cumulative["date"].to_list(),
                    daily_cumulative[self.signal_col].to_list(),
                )
            )

        # Parse all signal rows sorted chronologically
        signal_rows: list[dict[str, Any]] = []
        for row in signals.sort(self.date_col).iter_rows(named=True):
            ed = row.get(self.date_col)
            if ed is None:
                continue
            if isinstance(ed, dt.datetime):
                ed = ed.date()
            row_copy = dict(row)
            row_copy["_parsed_date"] = ed
            signal_rows.append(row_copy)

        signal_dates = [r["_parsed_date"] for r in signal_rows]
        entry_map = _resolve_entry_dates(
            market_data, signal_dates, self.entry_days_before
        )

        sig_date_to_row: dict[dt.date, dict[str, Any]] = {
            r["_parsed_date"]: r for r in signal_rows
        }

        directions: dict[dt.date, float] = {}
        strengths: dict[dt.date, float] = {}
        confidences: dict[dt.date, float] = {}

        for entry_date, sig_date in entry_map.items():
            row = sig_date_to_row.get(sig_date)
            if row is None:
                continue

            # ── Signal estimation at entry_date ─────────────────────
            final_signal = _safe_float(row.get(self.signal_col))
            if final_signal is None:
                directions[sig_date] = 0.0
                strengths[sig_date] = 0.0
                confidences[sig_date] = 0.0
                continue

            q_start = row.get("quarter_start")
            q_end = row.get("quarter_end")
            earnings_dt = row["_parsed_date"]
            pct_complete = _safe_float(row.get("pct_count_complete"))

            if isinstance(q_start, dt.datetime):
                q_start = q_start.date()
            if isinstance(q_end, dt.datetime):
                q_end = q_end.date()

            if self.entry_days_before == 0 or q_start is None or q_end is None:
                estimated_signal = final_signal
                completion = 1.0
            else:
                estimated_signal, completion = estimate_signal_at_entry(
                    entry_date=entry_date,
                    quarter_start=q_start,
                    quarter_end=q_end,
                    earnings_date=earnings_dt,
                    final_signal=final_signal,
                    final_pct_complete=pct_complete,
                    daily_cumulative=daily_cum_lookup,
                )

            # ── Correlation context ─────────────────────────────────
            if self.use_prior_quarter_corr and self.entry_days_before > 0:
                ctx = _get_prior_quarter_context(
                    earnings_dt,
                    signal_rows,
                    corr_col_name,
                    conf_col_name,
                    regime_col_name,
                )
            else:
                ctx = {
                    "correlation": _safe_float(row.get(corr_col_name)),
                    "confidence": _safe_float(row.get(conf_col_name)),
                    "regime_shift": row.get(regime_col_name),
                }

            corr = ctx["correlation"]
            conf = ctx["confidence"]
            regime_shift = ctx["regime_shift"]

            # ── Entry decision ──────────────────────────────────────
            if abs(estimated_signal) < self.min_signal_abs:
                directions[sig_date] = 0.0
                strengths[sig_date] = estimated_signal
                confidences[sig_date] = 0.0
                continue

            if self.skip_regime_shifts and regime_shift is not None:
                directions[sig_date] = 0.0
                strengths[sig_date] = estimated_signal
                confidences[sig_date] = 0.0
                continue

            # Direction: sign(estimated_signal) * sign(correlation)
            if corr is not None and abs(corr) > 0.01:
                direction = _sign(estimated_signal) * _sign(corr)
            else:
                direction = _sign(estimated_signal)

            position = direction
            if self.scale_by_confidence and conf is not None:
                position *= conf

            directions[sig_date] = position
            strengths[sig_date] = estimated_signal
            confidences[sig_date] = conf if conf is not None else 0.0

        return _apply_entry_positions(
            market_data, entry_map, directions, strengths, confidences
        )


# =============================================================================
# Helpers
# =============================================================================


def _sign(x: float) -> float:
    return 1.0 if x > 0 else -1.0 if x < 0 else 0.0


def _safe_float(val: Any) -> float | None:
    if val is None:
        return None
    try:
        f = float(val)
        return f if f == f else None
    except (ValueError, TypeError):
        return None
