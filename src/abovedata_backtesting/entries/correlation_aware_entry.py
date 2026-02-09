"""Correlation-aware entry rule with intra-quarter signal estimation.

Uses correlation context to determine trade direction, and estimates
the signal value at entry time based on how far into the quarter we are.

Now records full decision context via EntryContext for downstream analysis.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from itertools import product
from typing import Any, Self

import polars as pl

from abovedata_backtesting.entries.entry_context import EntryContext
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
    """Estimate signal value at entry_date based on quarter progress."""
    if daily_cumulative is not None:
        if entry_date in daily_cumulative:
            actual = daily_cumulative[entry_date]
            frac = abs(actual / final_signal) if final_signal != 0 else 0.0
            return actual, min(frac, 1.0)
        prior_dates = sorted(d for d in daily_cumulative if d <= entry_date)
        if prior_dates:
            actual = daily_cumulative[prior_dates[-1]]
            frac = abs(actual / final_signal) if final_signal != 0 else 0.0
            return actual, min(frac, 1.0)
        return 0.0, 0.0

    total_span = (earnings_date - quarter_start).days
    if total_span <= 0:
        return final_signal, 1.0

    days_elapsed = (entry_date - quarter_start).days

    if days_elapsed <= 0:
        return 0.0, 0.0
    elif days_elapsed >= total_span:
        return final_signal, 1.0
    else:
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
    """Get correlation context from the most recently completed quarter."""
    prior = None
    for row in signal_rows:
        row_ed = row["_parsed_date"]
        if row_ed < earnings_date:
            prior = row
        else:
            break

    if prior is None:
        return {"correlation": None, "confidence": None, "regime_shift": None}

    return {
        "correlation": _safe_float(prior.get(corr_col_name)),
        "confidence": _safe_float(prior.get(conf_col_name)),
        "regime_shift": prior.get(regime_col_name),
    }


def _classify_regime(corr: float | None) -> str:
    """Classify correlation value into a regime string."""
    if corr is None:
        return "unknown"
    if corr > 0.5:
        return "strong_positive"
    elif corr > 0:
        return "weak_positive"
    elif corr > -0.5:
        return "weak_negative"
    else:
        return "strong_negative"


# =============================================================================
# Entry rule
# =============================================================================


@dataclass(frozen=True, slots=True)
class CorrelationAwareEntry(EntryRule):
    """
    Enter on every signal date, using correlation context for direction.

    Now records full EntryContext for each trade decision.
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
            # When not scaling, confidence_col doesn't affect position sizing,
            # but it DOES affect signal quality classification and context recording.
            # Default to matching the correlation column's family.
            if not sbc:
                effective_cfc = "leading" if cc.startswith("leading") else "contemp"
            else:
                effective_cfc = cfc
            effective_upqc = upqc if edb > 0 else True
            key = (sc, cc, msa, srs, sbc, effective_cfc, edb, effective_upqc, dc)
            if key in seen:
                continue
            seen.add(key)
            results.append(
                cls(sc, cc, msa, srs, sbc, effective_cfc, edb, effective_upqc, dc)
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

        corr_col_name = _CORR_COL_MAP.get(self.corr_col, self.corr_col)
        conf_col_name = _CONF_COL_MAP.get(self.confidence_col, self.confidence_col)
        regime_col_name = _REGIME_COL_MAP.get(self.corr_col, "contemp_regime_shift")

        daily_cum_lookup: dict[dt.date, float] | None = None
        if daily_cumulative is not None and self.signal_col in daily_cumulative.columns:
            daily_cum_lookup = dict(
                zip(
                    daily_cumulative["date"].to_list(),
                    daily_cumulative[self.signal_col].to_list(),
                )
            )

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
        contexts: dict[dt.date, EntryContext] = {}

        for entry_date, sig_date in entry_map.items():
            row = sig_date_to_row.get(sig_date)
            if row is None:
                continue

            # ── Signal estimation ───────────────────────────────────
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
            regime_shift_detected = regime_shift is not None and regime_shift != ""
            regime_shift_skipped = self.skip_regime_shifts and regime_shift_detected

            if abs(estimated_signal) < self.min_signal_abs or regime_shift_skipped:
                directions[sig_date] = 0.0
                strengths[sig_date] = estimated_signal
                confidences[sig_date] = 0.0

                # Still record context for skipped entries
                contexts[sig_date] = EntryContext(
                    entry_type="correlation_aware",
                    signal_col=self.signal_col,
                    signal_value=estimated_signal,
                    signal_date=sig_date,
                    raw_direction=int(_sign(estimated_signal)),
                    final_direction=0,
                    flipped=False,
                    corr_col_used=self.corr_col,
                    corr_value_used=corr,
                    prior_quarter_corr=self.use_prior_quarter_corr
                    and self.entry_days_before > 0,
                    confidence_col_used=self.confidence_col,
                    confidence_value_used=conf,
                    correlation_regime=_classify_regime(corr)
                    if not regime_shift_detected
                    else "regime_shift",
                    regime_shift_detected=regime_shift_detected,
                    regime_shift_skipped=regime_shift_skipped,
                )
                continue

            # Direction: sign(estimated_signal) * sign(correlation)
            raw_dir = _sign(estimated_signal)
            if corr is not None and abs(corr) > 0.01:
                final_dir = raw_dir * _sign(corr)
            else:
                final_dir = raw_dir

            flipped = (int(raw_dir) != int(final_dir)) and final_dir != 0

            position = final_dir
            if self.scale_by_confidence and conf is not None:
                position *= conf

            directions[sig_date] = position
            strengths[sig_date] = estimated_signal
            confidences[sig_date] = conf if conf is not None else 0.0

            # Record the full decision context
            contexts[sig_date] = EntryContext(
                entry_type="correlation_aware",
                signal_col=self.signal_col,
                signal_value=estimated_signal,
                signal_date=sig_date,
                raw_direction=int(raw_dir),
                final_direction=int(final_dir),
                flipped=flipped,
                corr_col_used=self.corr_col,
                corr_value_used=corr,
                prior_quarter_corr=self.use_prior_quarter_corr
                and self.entry_days_before > 0,
                confidence_col_used=self.confidence_col,
                confidence_value_used=conf,
                correlation_regime=_classify_regime(corr)
                if not regime_shift_detected
                else "regime_shift",
                regime_shift_detected=regime_shift_detected,
                regime_shift_skipped=False,
            )

        return _apply_entry_positions(
            market_data, entry_map, directions, strengths, confidences, contexts
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
