"""Multi-horizon entry rule.

Examines signals at multiple time horizons (T, T-1, T-2) to determine
trade direction. Expects lagged columns to already exist on the signals
DataFrame, created by SignalPreprocessor with TimeShiftTransform.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from itertools import product
from typing import Any, Literal, Self

import polars as pl

from abovedata_backtesting.entries.entry_context import EntryContext
from abovedata_backtesting.entries.entry_signals import (
    EntryRule,
    _apply_entry_positions,
    _resolve_entry_dates,
    _short_signal_col,
)

MultiHorizonStrategy = Literal["consensus", "momentum", "reversal", "weighted"]


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


@dataclass(frozen=True, slots=True)
class MultiHorizonEntry(EntryRule):
    """Entry rule examining signals at multiple time horizons.

    Looks at signal[T], signal[T-1], signal[T-2] (all past data)
    to determine trade direction, strength, and confidence.

    Strategies:
    - "consensus": All horizons agree on direction -> enter
    - "momentum": Signal is improving across horizons -> enter
    - "reversal": Signal reversed from prior quarter -> enter contrarian
    - "weighted": Weighted score across horizons -> enter based on sum

    Expects lagged columns (e.g., {signal_col}_lag1q) to already exist
    on the signals DataFrame.
    """

    signal_col: str = "visible_revenue_resid"
    horizons: tuple[int, ...] = (0, 1)
    strategy: MultiHorizonStrategy = "consensus"
    weights: tuple[float, ...] | None = None
    min_signal_abs: float = 0.0
    corr_col: str | None = None
    entry_days_before: int = 0
    date_col: str = "earnings_date"

    @property
    def name(self) -> str:
        h = "h" + "_".join(str(h) for h in self.horizons)
        col = _short_signal_col(self.signal_col)
        parts = [f"multi_{self.strategy}_{h}_{col}"]
        if self.min_signal_abs > 0:
            parts.append(f"min{self.min_signal_abs}")
        if self.corr_col:
            parts.append(f"corr_{self.corr_col}")
        parts.append(f"e{self.entry_days_before}d")
        return "_".join(parts)

    def params(self) -> dict[str, Any]:
        return {
            "entry_type": "multi_horizon",
            "signal_col": self.signal_col,
            "horizons": list(self.horizons),
            "strategy": self.strategy,
            "weights": list(self.weights) if self.weights else None,
            "min_signal_abs": self.min_signal_abs,
            "corr_col": self.corr_col,
            "entry_days_before": self.entry_days_before,
        }

    @classmethod
    def grid(
        cls,
        signal_col: list[str] | None = None,
        horizons: list[tuple[int, ...]] | None = None,
        strategy: list[MultiHorizonStrategy] | None = None,
        weights: list[tuple[float, ...] | None] | None = None,
        min_signal_abs: list[float] | None = None,
        corr_col: list[str | None] | None = None,
        entry_days_before: list[int] | None = None,
        date_col: list[str] | None = None,
    ) -> list[Self]:
        results: list[Self] = []
        for sc, h, s, w, msa, cc, edb, dc in product(
            signal_col or ["visible_revenue_resid"],
            horizons or [(0, 1)],
            strategy or ["consensus"],
            weights or [None],
            min_signal_abs or [0.0],
            corr_col or [None],
            entry_days_before or [0],
            date_col or ["earnings_date"],
        ):
            # "weighted" strategy requires weights matching horizons
            if s == "weighted" and w is not None and len(w) != len(h):
                continue
            results.append(cls(sc, h, s, w, msa, cc, edb, dc))
        return results

    def apply(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame,
    ) -> pl.DataFrame:
        # Resolve column names for each horizon
        col_map: dict[int, str] = {}
        for h in self.horizons:
            if h == 0:
                col_map[h] = self.signal_col
            else:
                col_map[h] = f"{self.signal_col}_lag{h}q"

        # Validate columns exist
        missing = [c for c in col_map.values() if c not in signals.columns]
        if missing:
            # Fall back to single-horizon if lagged columns don't exist
            if self.signal_col in signals.columns and 0 in col_map:
                col_map = {0: self.signal_col}
            else:
                return market_data.with_columns(
                    pl.lit(0.0).alias("position"),
                    pl.lit(0.0).alias("signal_strength"),
                    pl.lit(0.0).alias("confidence"),
                )

        # Optional correlation column
        corr_col_name = None
        if self.corr_col:
            from abovedata_backtesting.entries.correlation_aware_entry import (
                _CORR_COL_MAP,
            )

            corr_col_name = _CORR_COL_MAP.get(self.corr_col, self.corr_col)

        # Parse signal rows
        sig_rows = signals.sort(self.date_col).to_dicts()
        signal_dates: list[dt.date] = []
        for row in sig_rows:
            ed = row.get(self.date_col)
            if ed is None:
                continue
            if isinstance(ed, dt.datetime):
                ed = ed.date()
            row["_parsed_date"] = ed
            signal_dates.append(ed)

        entry_map = _resolve_entry_dates(
            market_data, signal_dates, self.entry_days_before
        )

        # Build lookup: date -> row
        row_lookup = {r["_parsed_date"]: r for r in sig_rows if "_parsed_date" in r}

        directions: dict[dt.date, float] = {}
        strengths: dict[dt.date, float] = {}
        confidences: dict[dt.date, float] = {}
        contexts: dict[dt.date, EntryContext] = {}

        for _entry_date, sig_date in entry_map.items():
            row = row_lookup.get(sig_date)
            if row is None:
                continue

            # Collect signal values at each horizon
            vals: dict[int, float] = {}
            for h, col in col_map.items():
                v = _safe_float(row.get(col))
                if v is not None:
                    vals[h] = v

            if not vals:
                continue

            # Apply min_signal_abs on current horizon
            current_val = vals.get(0)
            if current_val is not None and abs(current_val) < self.min_signal_abs:
                continue

            # Determine direction based on strategy
            direction, strength, conf = self._compute_strategy(vals)

            if direction == 0.0:
                directions[sig_date] = 0.0
                strengths[sig_date] = strength
                confidences[sig_date] = 0.0
                continue

            # Optional correlation flip
            final_dir = direction
            corr_value = None
            flipped = False
            if corr_col_name and corr_col_name in row:
                corr_value = _safe_float(row.get(corr_col_name))
                if corr_value is not None and abs(corr_value) > 0.01:
                    final_dir = direction * _sign(corr_value)
                    flipped = direction != final_dir

            directions[sig_date] = final_dir
            strengths[sig_date] = strength
            confidences[sig_date] = conf

            contexts[sig_date] = EntryContext(
                entry_type="multi_horizon",
                signal_col=self.signal_col,
                signal_value=current_val,
                signal_date=sig_date,
                raw_direction=int(direction),
                final_direction=int(final_dir),
                flipped=flipped,
                corr_col_used=self.corr_col,
                corr_value_used=corr_value,
                confidence_value_used=conf,
            )

        return _apply_entry_positions(
            market_data, entry_map, directions, strengths, confidences, contexts
        )

    def _compute_strategy(self, vals: dict[int, float]) -> tuple[float, float, float]:
        """Compute direction, strength, confidence from multi-horizon values.

        Returns (direction, strength, confidence).
        """
        sorted_horizons = sorted(vals.keys())
        sorted_vals = [vals[h] for h in sorted_horizons]

        if self.strategy == "consensus":
            return self._consensus(sorted_vals)
        elif self.strategy == "momentum":
            return self._momentum(sorted_horizons, sorted_vals)
        elif self.strategy == "reversal":
            return self._reversal(sorted_vals)
        elif self.strategy == "weighted":
            return self._weighted(sorted_horizons, sorted_vals)
        else:
            return 0.0, 0.0, 0.0

    def _consensus(self, vals: list[float]) -> tuple[float, float, float]:
        """Enter only when all horizons agree on direction."""
        signs = [_sign(v) for v in vals]
        if len(set(signs)) == 1 and signs[0] != 0.0:
            direction = signs[0]
            strength = sum(abs(v) for v in vals) / len(vals)
            conf = min(1.0, strength / 2.0)
            return direction, vals[0], conf
        return 0.0, vals[0] if vals else 0.0, 0.0

    def _momentum(
        self, horizons: list[int], vals: list[float]
    ) -> tuple[float, float, float]:
        """Enter when signal is consistently improving.

        For long: vals[T] > vals[T-1] > vals[T-2] and vals[T] > 0
        For short: vals[T] < vals[T-1] < vals[T-2] and vals[T] < 0
        """
        if len(vals) < 2:
            return 0.0, vals[0] if vals else 0.0, 0.0

        # Check if monotonically increasing (current is horizon 0 = smallest index)
        increasing = all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
        decreasing = all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))

        if increasing and vals[0] > 0:
            strength = vals[0]
            conf = min(1.0, abs(vals[0] - vals[-1]) / (abs(vals[-1]) + 1e-9))
            return 1.0, strength, conf
        elif decreasing and vals[0] < 0:
            strength = vals[0]
            conf = min(1.0, abs(vals[0] - vals[-1]) / (abs(vals[-1]) + 1e-9))
            return -1.0, strength, conf

        return 0.0, vals[0], 0.0

    def _reversal(self, vals: list[float]) -> tuple[float, float, float]:
        """Enter when signal reversed from prior quarter."""
        if len(vals) < 2:
            return 0.0, vals[0] if vals else 0.0, 0.0

        current = vals[0]
        prior = vals[1]  # horizon 1 = T-1 (next in sorted order)

        if _sign(current) != _sign(prior) and _sign(current) != 0.0:
            direction = _sign(current)
            conf = min(1.0, abs(current - prior) / (abs(prior) + 1e-9))
            return direction, current, conf

        return 0.0, current, 0.0

    def _weighted(
        self, horizons: list[int], vals: list[float]
    ) -> tuple[float, float, float]:
        """Enter based on weighted score across horizons."""
        if self.weights is not None:
            # Match weights to horizons by index
            w = list(self.weights)
        else:
            # Default: linearly decreasing weights
            n = len(vals)
            w = [(n - i) / sum(range(1, n + 1)) for i in range(n)]

        # Ensure weights align with available values
        w = w[: len(vals)]
        if len(w) < len(vals):
            w.extend([0.0] * (len(vals) - len(w)))

        score = sum(v * wt for v, wt in zip(vals, w))
        direction = _sign(score)
        strength = score
        conf = min(1.0, abs(score) / 2.0)

        return direction, strength, conf
