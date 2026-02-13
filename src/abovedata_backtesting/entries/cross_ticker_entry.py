"""Cross-ticker entry rule.

Uses peer tickers' UCC signals to inform trade direction for a target ticker.
The cross-ticker relationship is tracked with a rolling cross-IC, so the
strategy adapts when relationships flip from positive to negative and back.

Lookahead protection:
  - Peer signals: only the most recent *prior* earnings date (backward search)
  - Rolling cross-IC: computed using only data up to the current earnings date
  - Forward returns in IC: from the target's *past* earnings dates only
"""

from __future__ import annotations

import datetime as dt
import warnings
from dataclasses import dataclass, fields
from itertools import product
from pathlib import Path
from typing import Any, Self

import numpy as np
import polars as pl
from scipy import stats

from abovedata_backtesting.data_loaders.load_signal_data import (
    list_visible_cols,
    load_signal_data,
)
from abovedata_backtesting.entries.entry_context import EntryContext
from abovedata_backtesting.entries.entry_signals import (
    EntryRule,
    _apply_entry_positions,
    _resolve_entry_dates,
    _short_signal_col,
)

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


# ── Peer data loading (cached) ──────────────────────────────────────────────

# Module-level cache for peer signal data.
# Key: (ticker, method, visible_col) → list of (earnings_date, {signal_col: value})
_peer_cache: dict[tuple[str, str, str], list[tuple[dt.date, dict[str, float]]]] = {}


def _load_peer_signals(
    ticker: str,
    signal_cols: list[str],
    method: str = "stl_p4_s7_robustTrue",
) -> list[tuple[dt.date, dict[str, float]]]:
    """Load peer's signal data.  Returns sorted list of (date, {col: value}).

    Picks the best visible_col for the ticker (most non-null resid obs).
    Caches the result at module level to avoid reloading across grid combos.
    """
    # Try the cache first.
    vcs = list_visible_cols(ticker, method=method)
    if not vcs:
        return []

    # Pick best visible_col (most non-null resid).
    best_vc, best_count = vcs[0], 0
    for vc in vcs:
        resid_col = f"{vc}_resid"
        try:
            df = load_signal_data(
                ticker, method=method, name="processed_data", visible_col=vc
            )
        except Exception:
            continue
        if resid_col in df.columns:
            count = df[resid_col].drop_nulls().len()
            if count > best_count:
                best_count = count
                best_vc = vc

    cache_key = (ticker, method, best_vc)
    if cache_key in _peer_cache:
        return _peer_cache[cache_key]

    try:
        df = load_signal_data(
            ticker, method=method, name="processed_data", visible_col=best_vc
        )
    except Exception:
        _peer_cache[cache_key] = []
        return []

    if "earnings_date" not in df.columns:
        _peer_cache[cache_key] = []
        return []

    resid_col = f"{best_vc}_resid"
    # Build the list of (date, signal_values).
    result: list[tuple[dt.date, dict[str, float]]] = []
    for row in df.sort("earnings_date").iter_rows(named=True):
        ed = row.get("earnings_date")
        if ed is None:
            continue
        if isinstance(ed, dt.datetime):
            ed = ed.date()

        vals: dict[str, float] = {}
        # Always include the resid column under "resid" key.
        resid_val = _safe_float(row.get(resid_col))
        if resid_val is not None:
            vals["resid"] = resid_val

        for col in signal_cols:
            v = _safe_float(row.get(col))
            if v is not None:
                vals[col] = v

        if vals:
            result.append((ed, vals))

    _peer_cache[cache_key] = result
    return result


# ── Peer selection helper ───────────────────────────────────────────────────


def select_peers(
    target_ticker: str,
    signal_col: str | None = None,
    top_n: int = 5,
    csv_path: str | Path | None = None,
) -> list[tuple[str, str, float]]:
    """Select top peer tickers from cross_predictive_pairs.csv.

    Returns list of (peer_ticker, signal_col, cross_ic) sorted by |cross_ic|.

    Parameters
    ----------
    target_ticker : str
        The ticker to find peers for.
    signal_col : str | None
        If given, filter to peers where this signal column drives the prediction.
    top_n : int
        Maximum number of peers to return.
    csv_path : str | Path | None
        Path to cross_predictive_pairs.csv.  Defaults to
        ``results/cross_ticker_analysis/cross_predictive_pairs.csv``.
    """
    if csv_path is None:
        csv_path = (
            Path("results") / "cross_ticker_analysis" / "cross_predictive_pairs.csv"
        )
    csv_path = Path(csv_path)

    if not csv_path.exists():
        return []

    pairs = pl.read_csv(csv_path)

    # Filter to rows where this is the target.
    filtered = pairs.filter(pl.col("target_ticker") == target_ticker)

    if signal_col is not None:
        filtered = filtered.filter(pl.col("signal_col") == signal_col)

    # Sort by |cross_ic| descending, take top N.
    filtered = filtered.sort("abs_ic", descending=True).head(top_n)

    result: list[tuple[str, str, float]] = []
    for row in filtered.iter_rows(named=True):
        result.append((row["signal_ticker"], row["signal_col"], row["cross_ic"]))

    return result


def discover_peer_config(
    target_ticker: str,
    top_n_peers: int = 5,
    csv_path: str | Path | None = None,
) -> dict[str, Any]:
    """Discover best peers and signal columns for a target ticker.

    Reads cross_predictive_pairs.csv and returns:
        - peer_tickers: top peer ticker symbols ranked by |cross-IC|
        - peer_signal_cols: most common signal columns in cross-pairs
        - peer_details: full list of (peer, signal_col, cross_ic) triples
    """
    from collections import Counter

    all_peers = select_peers(
        target_ticker, signal_col=None, top_n=100, csv_path=csv_path
    )

    if not all_peers:
        return {"peer_tickers": [], "peer_signal_cols": [], "peer_details": []}

    # Unique peer tickers, ranked by their best |cross_ic|.
    ticker_best_ic: dict[str, float] = {}
    for pt, sc, ic in all_peers:
        if pt not in ticker_best_ic or abs(ic) > abs(ticker_best_ic[pt]):
            ticker_best_ic[pt] = ic

    ranked_tickers = sorted(
        ticker_best_ic.keys(), key=lambda t: abs(ticker_best_ic[t]), reverse=True
    )
    top_peer_tickers = ranked_tickers[:top_n_peers]

    # Most common signal columns across all pairs.
    sig_counts: Counter[str] = Counter()
    for _, sc, _ in all_peers:
        sig_counts[sc] += 1

    top_signal_cols = [sc for sc, _ in sig_counts.most_common(3)]

    print(f"\n  Peer discovery for {target_ticker}:")
    print(f"    Total cross-predictive pairs: {len(all_peers)}")
    print(f"    Top {top_n_peers} peers: {top_peer_tickers}")
    print(f"    Top signal columns: {top_signal_cols}")
    for pt in top_peer_tickers:
        ic = ticker_best_ic[pt]
        print(
            f"      {pt}: best |cross-IC| = {abs(ic):.3f} "
            f"({'positive' if ic > 0 else 'negative'})"
        )

    return {
        "peer_tickers": top_peer_tickers,
        "peer_signal_cols": top_signal_cols,
        "peer_details": all_peers,
    }


# ── Cross-ticker entry rule ────────────────────────────────────────────────

_EXCLUDE_FROM_KEY = frozenset({"date_col"})


@dataclass(frozen=True, slots=True)
class CrossTickerEntry(EntryRule):
    """Enter using peer tickers' signals to determine direction.

    At each of the target ticker's earnings dates:
    1. Look up each peer's most recent prior signal (no lookahead)
    2. Compute a rolling cross-IC to track whether the relationship
       is currently positive or negative
    3. Weight/flip peer signals by sign(rolling_cross_ic)
    4. Aggregate across peers
    5. Direction = sign(own_signal) x sign(aggregated_peer_signal)

    The rolling IC adapts to regime switches — when a peer relationship
    flips from positive to negative, the rolling IC tracks the change
    and the peer signal contribution flips accordingly.
    """

    target_ticker: str = ""
    peer_tickers: tuple[str, ...] = ()
    peer_signal_col: str = "resid"
    own_signal_col: str = "resid"
    aggregation: str = "mean"  # "mean" | "strongest" | "majority"
    min_peer_signals: int = 1
    max_peer_signal_age_days: int = 90
    entry_days_before: int = 0
    min_own_signal_abs: float = 0.0
    rolling_ic_window: int = 6  # quarters
    date_col: str = "earnings_date"

    @property
    def name(self) -> str:
        n_peers = len(self.peer_tickers)
        peer_str = "_".join(self.peer_tickers[:3])
        if n_peers > 3:
            peer_str += f"+{n_peers - 3}"
        own_short = (
            _short_signal_col(self.own_signal_col)
            if self.own_signal_col != "resid"
            else "resid"
        )
        parts = [
            f"cross_{self.aggregation}",
            f"p{n_peers}_{peer_str}",
            f"ps_{_short_signal_col(self.peer_signal_col)}",
            f"own_{own_short}",
        ]
        if self.min_own_signal_abs > 0:
            parts.append(f"min{self.min_own_signal_abs}")
        parts.append(f"icw{self.rolling_ic_window}")
        parts.append(f"e{self.entry_days_before}d")
        return "_".join(parts)

    def params(self) -> dict[str, Any]:
        return {"entry_type": "cross_ticker"} | {
            f.name: getattr(self, f.name) for f in fields(self)
        }

    @classmethod
    def grid(cls, **param_lists: list[Any]) -> list[Self]:
        """Generate grid of instances from parameter lists.

        Usage:
            CrossTickerEntry.grid(
                target_ticker=["PCAR"],
                peer_tickers=[("BWAY", "WM"), ("BWAY",)],
                peer_signal_col=["filtered_leading_corr", "resid"],
                aggregation=["mean", "strongest"],
                entry_days_before=[5, 15, 20],
            )
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

            # Ensure peer_tickers is a tuple.
            if isinstance(kw["peer_tickers"], list):
                kw["peer_tickers"] = tuple(kw["peer_tickers"])

            # Semantic: min_peer_signals can't exceed # peers.
            if kw["min_peer_signals"] > len(kw["peer_tickers"]):
                continue

            # Dedup.
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
    ) -> pl.DataFrame:
        if not self.peer_tickers:
            return market_data.with_columns(
                pl.lit(0.0).alias("position"),
                pl.lit(0.0).alias("signal_strength"),
                pl.lit(0.0).alias("confidence"),
            )

        # 1. Load peer signal data.
        all_signal_cols = [self.peer_signal_col]
        if self.peer_signal_col != "resid":
            all_signal_cols.append("resid")

        peer_data: dict[str, list[tuple[dt.date, dict[str, float]]]] = {}
        for pt in self.peer_tickers:
            pd_list = _load_peer_signals(pt, signal_cols=all_signal_cols)
            if pd_list:
                peer_data[pt] = pd_list

        if not peer_data:
            return market_data.with_columns(
                pl.lit(0.0).alias("position"),
                pl.lit(0.0).alias("signal_strength"),
                pl.lit(0.0).alias("confidence"),
            )

        # 2. Parse own signal rows.
        own_rows = self._parse_own_rows(signals)
        if not own_rows:
            return market_data.with_columns(
                pl.lit(0.0).alias("position"),
                pl.lit(0.0).alias("signal_strength"),
                pl.lit(0.0).alias("confidence"),
            )

        timing_dates = [r["_date"] for r in own_rows]
        entry_map = _resolve_entry_dates(
            market_data, timing_dates, self.entry_days_before
        )

        # 3. Pre-compute forward returns for our ticker at past earnings dates.
        # Used for rolling cross-IC.  Computed once to avoid N^2 lookups.
        market_dates = market_data["date"].to_list()
        market_closes = market_data["close"].to_list()
        date_to_idx: dict[dt.date, int] = {d: i for i, d in enumerate(market_dates)}

        own_fwd_rets: dict[dt.date, float] = {}
        for row in own_rows:
            d = row["_date"]
            fwd = self._forward_return_fast(d, date_to_idx, market_closes, horizon=30)
            if fwd is not None:
                own_fwd_rets[d] = fwd

        # 4. Iterate over our earnings dates and compute entries.
        directions: dict[dt.date, float] = {}
        strengths: dict[dt.date, float] = {}
        confidences: dict[dt.date, float] = {}
        contexts: dict[dt.date, EntryContext] = {}

        for entry_date, timing_date in entry_map.items():
            row = next((r for r in own_rows if r["_date"] == timing_date), None)
            if row is None:
                continue

            own_signal = _safe_float(row.get(self.own_signal_col))
            if own_signal is None:
                continue
            if abs(own_signal) < self.min_own_signal_abs:
                continue

            # Collect peer contributions.
            peer_contributions: list[tuple[float, float]] = []
            # (adjusted_signal, rolling_ic_abs) per peer

            for pt, pt_data in peer_data.items():
                # a. Find peer's most recent prior signal.
                peer_sig = self._find_prior_peer_signal(
                    timing_date, pt_data, self.peer_signal_col
                )
                if peer_sig is None:
                    continue

                peer_date, peer_val = peer_sig

                # b. Compute rolling cross-IC: peer's past signals vs our past fwd returns.
                rolling_ic = self._rolling_cross_ic(
                    timing_date,
                    pt_data,
                    self.peer_signal_col,
                    own_fwd_rets,
                    self.rolling_ic_window,
                )

                # c. Adjust peer signal by relationship direction.
                if rolling_ic is not None and abs(rolling_ic) > 0.01:
                    adjusted = peer_val * _sign(rolling_ic)
                    peer_contributions.append((adjusted, abs(rolling_ic)))
                else:
                    # No IC history yet — use raw peer signal (assume positive relationship).
                    peer_contributions.append((peer_val, 0.0))

            # Check minimum peer count.
            if len(peer_contributions) < self.min_peer_signals:
                continue

            # d. Aggregate peer signals.
            agg_signal = self._aggregate(peer_contributions)
            if agg_signal is None or agg_signal == 0.0:
                continue

            # e. Final direction.
            raw_dir = _sign(own_signal)
            peer_dir = _sign(agg_signal)
            final_dir = raw_dir * peer_dir

            # Confidence: mean |rolling IC| across contributing peers.
            ics = [ic for _, ic in peer_contributions if ic > 0]
            conf = float(np.mean(ics)) if ics else 0.3  # default moderate confidence

            directions[timing_date] = final_dir
            strengths[timing_date] = own_signal
            confidences[timing_date] = min(1.0, conf)

            contexts[timing_date] = EntryContext(
                entry_type="cross_ticker",
                signal_col=self.own_signal_col,
                signal_value=own_signal,
                signal_date=timing_date,
                raw_direction=int(raw_dir),
                final_direction=int(final_dir),
                flipped=(raw_dir != final_dir),
                corr_col_used=self.peer_signal_col,
                corr_value_used=agg_signal,
                confidence_value_used=min(1.0, conf),
                preprocessor_name=f"peers={','.join(self.peer_tickers[:3])}",
            )

        return _apply_entry_positions(
            market_data, entry_map, directions, strengths, confidences, contexts
        )

    # ── Private helpers ─────────────────────────────────────────────────

    def _parse_own_rows(self, signals: pl.DataFrame) -> list[dict[str, Any]]:
        """Parse our own signal rows, extracting dates and signal values."""
        rows: list[dict[str, Any]] = []

        # Determine which columns to extract.
        # needed = {self.own_signal_col, self.date_col}

        for row in signals.sort(self.date_col).iter_rows(named=True):
            ed = row.get(self.date_col)
            if ed is None:
                continue
            if isinstance(ed, dt.datetime):
                ed = ed.date()

            parsed: dict[str, Any] = dict(row)
            parsed["_date"] = ed
            rows.append(parsed)

        return rows

    def _find_prior_peer_signal(
        self,
        our_date: dt.date,
        peer_data: list[tuple[dt.date, dict[str, float]]],
        signal_col: str,
    ) -> tuple[dt.date, float] | None:
        """Find the peer's most recent signal BEFORE our_date.

        Only matches within max_peer_signal_age_days.
        """
        best: tuple[dt.date, float] | None = None
        cutoff = our_date - dt.timedelta(days=self.max_peer_signal_age_days)

        for peer_date, peer_vals in peer_data:
            if peer_date >= our_date:
                continue  # No lookahead.
            if peer_date < cutoff:
                continue  # Too old.

            val = peer_vals.get(signal_col)
            if val is None:
                continue

            if best is None or peer_date > best[0]:
                best = (peer_date, val)

        return best

    def _rolling_cross_ic(
        self,
        current_date: dt.date,
        peer_data: list[tuple[dt.date, dict[str, float]]],
        signal_col: str,
        own_fwd_rets: dict[dt.date, float],
        window: int,
    ) -> float | None:
        """Compute rolling cross-IC: peer's signals vs our forward returns.

        Only uses data strictly before current_date (no lookahead).
        Returns the Spearman IC over the most recent `window` overlapping quarters.
        """
        # Collect (peer_signal, our_fwd_return) pairs at our earnings dates
        # where the peer had a recent signal.
        pairs: list[tuple[float, float]] = []

        # Get our earnings dates with forward returns (sorted, before current_date).
        our_dates_sorted = sorted(d for d in own_fwd_rets.keys() if d < current_date)

        for our_d in our_dates_sorted:
            # Find peer's most recent signal before our_d.
            peer_sig = self._find_prior_peer_signal(our_d, peer_data, signal_col)
            if peer_sig is None:
                continue

            fwd = own_fwd_rets[our_d]
            pairs.append((peer_sig[1], fwd))

        # Use only the most recent `window` pairs.
        if len(pairs) < 3:
            return None

        pairs = pairs[-window:]
        peer_arr = np.array([p[0] for p in pairs])
        fwd_arr = np.array([p[1] for p in pairs])

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ic, _ = stats.spearmanr(peer_arr, fwd_arr)

        if not np.isfinite(ic):
            return None
        return float(ic)

    def _aggregate(
        self,
        contributions: list[tuple[float, float]],
    ) -> float | None:
        """Aggregate peer signal contributions.

        Each contribution is (adjusted_signal, |rolling_ic|).
        """
        if not contributions:
            return None

        if self.aggregation == "mean":
            # IC-weighted mean if ICs are available; otherwise simple mean.
            total_weight = 0.0
            weighted_sum = 0.0
            for sig, ic_abs in contributions:
                w = max(ic_abs, 0.1)  # floor weight at 0.1
                weighted_sum += sig * w
                total_weight += w
            return weighted_sum / total_weight if total_weight > 0 else None

        elif self.aggregation == "strongest":
            # Take the signal from the peer with the highest |rolling IC|.
            best = max(contributions, key=lambda x: x[1])
            return best[0]

        elif self.aggregation == "majority":
            # Majority vote of sign(adjusted_signal).
            votes = [_sign(sig) for sig, _ in contributions]
            pos = sum(1 for v in votes if v > 0)
            neg = sum(1 for v in votes if v < 0)
            if pos > neg:
                return 1.0
            elif neg > pos:
                return -1.0
            else:
                return 0.0

        return None

    @staticmethod
    def _forward_return_fast(
        signal_date: dt.date,
        date_to_idx: dict[dt.date, int],
        closes: list[Any],
        horizon: int = 30,
    ) -> float | None:
        """Fast forward return computation using pre-built index."""
        idx = date_to_idx.get(signal_date)
        if idx is None:
            # Find nearest date on or after.
            candidates = [d for d in date_to_idx if d >= signal_date]
            if not candidates:
                return None
            idx = date_to_idx[min(candidates)]

        close_0 = closes[idx]
        if close_0 is None or close_0 == 0:
            return None

        end_idx = min(idx + horizon, len(closes) - 1)
        if end_idx <= idx:
            return None

        close_t = closes[end_idx]
        if close_t is None:
            return None

        return float((close_t - close_0) / close_0)
