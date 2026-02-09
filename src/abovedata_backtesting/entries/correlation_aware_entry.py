"""
Correlation-aware entry rule.

Uses UCC signal + historical correlation context to determine trade direction.
Optionally filters by signal magnitude, confidence, and regime shifts.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field, fields
from itertools import product
from typing import Any, Self

import polars as pl

from abovedata_backtesting.entries.entry_context import EntryContext
from abovedata_backtesting.entries.entry_signals import (
    EntryRule,
    _apply_entry_positions,
    _resolve_entry_dates,
)

# ── Column name mappings ────────────────────────────────────────────────────

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


# ── Helpers ─────────────────────────────────────────────────────────────────


def _sign(x: float) -> float:
    return 1.0 if x > 0 else -1.0 if x < 0 else 0.0


def _safe_float(val: Any) -> float | None:
    if val is None:
        return None
    try:
        f = float(val)
        return f if f == f else None  # NaN check
    except (ValueError, TypeError):
        return None


def _classify_regime(corr: float | None) -> str:
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


# ── Intra-quarter signal estimation ─────────────────────────────────────────


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
        if row["_parsed_date"] < earnings_date:
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


# ── Entry rule ──────────────────────────────────────────────────────────────

# Fields excluded from grid dedup key (non-strategic)
_EXCLUDE_FROM_KEY = frozenset({"date_col"})


@dataclass
class RunningContext:
    corr_col: str
    confidence_col: str

    corr_col_name: str = field(init=False)
    conf_col_name: str = field(init=False)
    regime_col_name: str = field(init=False)

    directions: dict[dt.date, float] = field(default_factory=dict)
    strengths: dict[dt.date, float] = field(default_factory=dict)
    confidences: dict[dt.date, float] = field(default_factory=dict)
    contexts: dict[dt.date, EntryContext] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.corr_col_name = _CORR_COL_MAP.get(self.corr_col, self.corr_col)
        self.conf_col_name = _CONF_COL_MAP.get(self.confidence_col, self.confidence_col)
        self.regime_col_name = _REGIME_COL_MAP.get(
            self.corr_col, "contemp_regime_shift"
        )

    def add_empty(self, timing_date: dt.date) -> None:
        self.directions[timing_date] = 0.0
        self.strengths[timing_date] = 0.0
        self.confidences[timing_date] = 0.0

    def add_skip(self, timing_date: dt.date, signal: float) -> None:
        self.directions[timing_date] = 0.0
        self.strengths[timing_date] = signal
        self.confidences[timing_date] = 0.0


@dataclass(frozen=True, slots=True)
class CorrelationAwareEntry(EntryRule):
    """
    Enter on every signal date, using correlation context for direction.

    Direction = sign(signal) × sign(correlation).
    Filters: min_signal_abs, min_confidence, skip_regime_shifts.
    Optional: scale position by confidence score.
    """

    signal_col: str = "visible_revenue_resid"
    corr_col: str = "contemp"
    min_signal_abs: float = 0.0
    min_confidence: float = 0.0
    skip_regime_shifts: bool = True
    scale_by_confidence: bool = False
    confidence_col: str = "contemp"
    entry_days_before: int = 0
    use_prior_quarter_corr: bool = True
    target_next_quarter: bool = False
    date_col: str = "earnings_date"

    # ── Auto-generated from dataclass fields ────────────────────────────

    @property
    def name(self) -> str:
        parts = [f"corr_aware_{self.corr_col}"]
        if self.target_next_quarter:
            parts.append("tgtQ+1")
        if self.min_signal_abs > 0:
            parts.append(f"min{self.min_signal_abs}")
        if self.min_confidence > 0:
            parts.append(f"conf{self.min_confidence}")
        if self.skip_regime_shifts:
            parts.append("noshift")
        if self.scale_by_confidence:
            parts.append("scaled")
        if not self.use_prior_quarter_corr:
            parts.append("sameq")
        parts.append(f"e{self.entry_days_before}d")
        return "_".join(parts)

    def params(self) -> dict[str, Any]:
        """Auto-generate params dict from all dataclass fields."""
        return {"entry_type": "correlation_aware"} | {
            f.name: getattr(self, f.name) for f in fields(self)
        }

    @classmethod
    def grid(cls, **param_lists: list[Any]) -> list[Self]:
        """
        Generate grid of instances from parameter lists.

        Usage:
            CorrelationAwareEntry.grid(
                corr_col=["contemp", "leading"],
                min_confidence=[0.0, 0.3],
                entry_days_before=[5, 10, 20],
            )

        Any parameter not specified uses the dataclass default (as single-element list).
        Deduplication applied automatically.
        """
        field_defs = fields(cls)
        grid_axes: dict[str, list[Any]] = {}
        for f in field_defs:
            if f.name in param_lists:
                grid_axes[f.name] = param_lists[f.name]
            else:
                grid_axes[f.name] = [f.default]

        field_names = list(grid_axes.keys())
        seen: set[tuple[Any, ...]] = set()
        results: list[Self] = []

        for combo in product(*grid_axes.values()):
            kw = dict(zip(field_names, combo))

            # ── Semantic normalization (reduces redundant combos) ────
            # When not scaling by confidence, confidence_col defaults to
            # match correlation family
            if not kw["scale_by_confidence"]:
                kw["confidence_col"] = (
                    "leading" if kw["corr_col"].startswith("leading") else "contemp"
                )
            # use_prior_quarter_corr is irrelevant when entry_days_before=0
            if kw["entry_days_before"] == 0:
                kw["use_prior_quarter_corr"] = True
            # Auto-infer target_next_quarter from corr_col if not explicitly set:
            # leading correlations predict T+1, so trade should target T+1 earnings
            if "target_next_quarter" not in param_lists:
                kw["target_next_quarter"] = kw["corr_col"].startswith("leading")
            # target_next_quarter requires entry_days_before > 0
            # (can't enter "before next earnings" on earnings day itself)
            if kw["target_next_quarter"] and kw["entry_days_before"] == 0:
                continue

            # Dedup
            key = tuple(
                kw[f.name] for f in field_defs if f.name not in _EXCLUDE_FROM_KEY
            )
            if key in seen:
                continue
            seen.add(key)
            results.append(cls(**kw))

        return results

    # ── Core logic ──────────────────────────────────────────────────────

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

        running_context = RunningContext(
            corr_col=self.corr_col,
            confidence_col=self.confidence_col,
        )

        daily_cum_lookup = self._build_daily_cumulative(daily_cumulative)
        signal_rows = self._parse_signal_rows(signals)

        # Build entry timing and data source mappings
        if self.target_next_quarter:
            # Leading signal: data from row T, trade timed to row T+1's earnings
            # entry_map: {entry_date → T+1_earnings_date}
            # data_source: {T+1_earnings_date → row_T}
            timing_dates: list[dt.date] = []
            data_source: dict[dt.date, dict[str, Any]] = {}
            for i, row in enumerate(signal_rows[:-1]):  # skip last (no T+1)
                next_earnings = signal_rows[i + 1]["_parsed_date"]
                timing_dates.append(next_earnings)
                data_source[next_earnings] = row
        else:
            # Contemporaneous: data and timing from same row
            timing_dates = [r["_parsed_date"] for r in signal_rows]
            data_source = {r["_parsed_date"]: r for r in signal_rows}

        entry_map = _resolve_entry_dates(
            market_data,
            timing_dates,
            self.entry_days_before,
        )

        for entry_date, timing_date in entry_map.items():
            row = data_source.get(timing_date)
            if row is None:
                continue

            # sig_date for context recording: use the data row's earnings date
            # (the quarter whose UCC data we're using for the signal)
            # Signal estimation
            signal = self._estimate_signal(row, entry_date, daily_cum_lookup)
            if signal is None:
                running_context.add_empty(timing_date)
                continue

            # Correlation context
            corr, conf, regime_shift = self._get_corr_context(
                row,
                signal_rows,
                running_context.corr_col_name,
                running_context.conf_col_name,
                running_context.regime_col_name,
            )

            # Entry decision: should we skip?
            if skip_reason := self._check_skip(signal, conf, regime_shift):
                running_context.add_skip(timing_date, signal)
                running_context.contexts[timing_date] = self._build_context(
                    row["_parsed_date"],
                    signal,
                    corr,
                    conf,
                    regime_shift,
                    final_direction=0,
                    skip_reason=skip_reason,
                )
                continue

            # Direction: sign(signal) × sign(correlation)
            raw_dir = _sign(signal)
            final_dir = raw_dir * _sign(corr) if corr and abs(corr) > 0.01 else raw_dir

            position = final_dir
            if self.scale_by_confidence and conf is not None:
                position *= conf

            running_context.directions[timing_date] = position
            running_context.strengths[timing_date] = signal
            running_context.confidences[timing_date] = conf if conf is not None else 0.0
            running_context.contexts[timing_date] = self._build_context(
                row["_parsed_date"],
                signal,
                corr,
                conf,
                regime_shift,
                final_direction=int(final_dir),
            )

        return _apply_entry_positions(
            market_data,
            entry_map,
            running_context.directions,
            running_context.strengths,
            running_context.confidences,
            running_context.contexts,
        )

    # ── Private helpers ─────────────────────────────────────────────────

    def _build_daily_cumulative(
        self,
        daily_cumulative: pl.DataFrame | None,
    ) -> dict[dt.date, float] | None:
        if daily_cumulative is None or self.signal_col not in daily_cumulative.columns:
            return None
        return dict(
            zip(
                daily_cumulative["date"].to_list(),
                daily_cumulative[self.signal_col].to_list(),
            )
        )

    def _parse_signal_rows(self, signals: pl.DataFrame) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for row in signals.sort(self.date_col).iter_rows(named=True):
            ed = row.get(self.date_col)
            if ed is None:
                continue
            if isinstance(ed, dt.datetime):
                ed = ed.date()
            row_copy = dict(row)
            row_copy["_parsed_date"] = ed
            rows.append(row_copy)
        return rows

    def _estimate_signal(
        self,
        row: dict[str, Any],
        entry_date: dt.date,
        daily_cum_lookup: dict[dt.date, float] | None,
    ) -> float | None:
        """Returns estimated signal value, or None if no signal."""
        final_signal = _safe_float(row.get(self.signal_col))
        if final_signal is None:
            return None

        # When targeting next quarter, we're using completed quarter T data
        # to trade around T+1 earnings — we have the final signal, no estimation needed
        if self.target_next_quarter:
            return final_signal

        if self.entry_days_before == 0:
            return final_signal

        q_start = row.get("quarter_start")
        q_end = row.get("quarter_end")
        if q_start is None or q_end is None:
            return final_signal

        if isinstance(q_start, dt.datetime):
            q_start = q_start.date()
        if isinstance(q_end, dt.datetime):
            q_end = q_end.date()

        signal, _ = estimate_signal_at_entry(
            entry_date=entry_date,
            quarter_start=q_start,
            quarter_end=q_end,
            earnings_date=row["_parsed_date"],
            final_signal=final_signal,
            final_pct_complete=_safe_float(row.get("pct_count_complete")),
            daily_cumulative=daily_cum_lookup,
        )
        return signal

    def _get_corr_context(
        self,
        row: dict[str, Any],
        signal_rows: list[dict[str, Any]],
        corr_col_name: str,
        conf_col_name: str,
        regime_col_name: str,
    ) -> tuple[float | None, float | None, Any]:
        """Returns (correlation, confidence, regime_shift)."""
        if self.use_prior_quarter_corr and self.entry_days_before > 0:
            ctx = _get_prior_quarter_context(
                row["_parsed_date"],
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
        return ctx["correlation"], ctx["confidence"], ctx["regime_shift"]

    def _check_skip(
        self,
        signal: float,
        conf: float | None,
        regime_shift: Any,
    ) -> str | None:
        """Returns skip reason string, or None to proceed with entry."""
        if abs(signal) < self.min_signal_abs:
            return "below_min_signal"
        if self.min_confidence > 0 and (conf is None or conf < self.min_confidence):
            return "below_min_confidence"
        if self.skip_regime_shifts and regime_shift is not None and regime_shift != "":
            return "regime_shift"
        return None

    def _build_context(
        self,
        sig_date: dt.date,
        signal: float,
        corr: float | None,
        conf: float | None,
        regime_shift: Any,
        final_direction: int = 0,
        skip_reason: str | None = None,
    ) -> EntryContext:
        """Single place to build EntryContext — no copy-paste."""
        raw_dir = int(_sign(signal))
        regime_shift_detected = regime_shift is not None and regime_shift != ""

        return EntryContext(
            entry_type="correlation_aware",
            signal_col=self.signal_col,
            signal_value=signal,
            signal_date=sig_date,
            raw_direction=raw_dir,
            final_direction=final_direction,
            flipped=(raw_dir != final_direction) and final_direction != 0,
            corr_col_used=self.corr_col,
            corr_value_used=corr,
            prior_quarter_corr=(
                self.use_prior_quarter_corr and self.entry_days_before > 0
            ),
            confidence_col_used=self.confidence_col,
            confidence_value_used=conf,
            correlation_regime=(
                "regime_shift" if regime_shift_detected else _classify_regime(corr)
            ),
            regime_shift_detected=regime_shift_detected,
            regime_shift_skipped=skip_reason == "regime_shift",
        )
