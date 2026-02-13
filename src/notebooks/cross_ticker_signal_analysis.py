"""Cross-ticker signal analysis and portfolio signal screening.

Evaluates ALL signal types per ticker — not just the UCC residual, but also:
- Contemporaneous and leading correlations (historical + MA + filtered)
- Correlation momentum
- Regime shift indicators
- Confidence scores
- Prediction signals (surprise direction, magnitude, calibrated predictions)

For each signal type, computes:
1. Per-ticker IC (Spearman rank correlation with forward returns)
2. Cross-ticker IC matrix (ticker A's signal → ticker B's forward returns)
3. Signal-signal correlation across tickers (for natural hedges)

Usage:
    python src/notebooks/cross_ticker_signal_analysis.py
    python src/notebooks/cross_ticker_signal_analysis.py --horizon 60
    python src/notebooks/cross_ticker_signal_analysis.py --min-obs 8
"""

from __future__ import annotations

import argparse
import warnings
from datetime import date
from pathlib import Path

import numpy as np
import polars as pl
from scipy import stats

from abovedata_backtesting.data_loaders.load_market_data import MarketDataLoaders
from abovedata_backtesting.data_loaders.load_signal_data import (
    list_visible_cols,
    load_signal_data,
)
from abovedata_backtesting.data_loaders.utils import data_root

# ─────────────────────────────────────────────────────────────────────────────
# Signal column definitions
# ─────────────────────────────────────────────────────────────────────────────

# Signal columns that exist in every processed_data.parquet file.
# These are the columns we evaluate as potential cross-ticker predictors.
# Grouped by category for readability.

CORRELATION_SIGNALS = [
    "contemp_corr_historical",
    "leading_corr_historical",
    "contemp_corr_ma",
    "leading_corr_ma",
    "filtered_contemp_corr",
    "filtered_leading_corr",
    "ucc_consensus_corr_historical",
    "consensus_revenue_corr_historical",
    "ucc_surprise_corr_historical",
]

MOMENTUM_SIGNALS = [
    "contemp_corr_momentum",
    "leading_corr_momentum",
]

CONFIDENCE_SIGNALS = [
    "contemp_confidence",
    "leading_confidence",
]

PREDICTION_SIGNALS = [
    "predicted_surprise_direction",
    "predicted_surprise_magnitude",
    "predicted_surprise_magnitude_v2",
    "predicted_rev_resid_calibrated",
    "predicted_surprise_calibrated",
]

BETA_SIGNALS = [
    "ucc_to_rev_beta",
    "ucc_to_surprise_beta",
]

# The regime shift columns are string ("Regime Shift" / null) — we encode as 0/1.
REGIME_SHIFT_SIGNALS = [
    "contemp_regime_shift",
    "leading_regime_shift",
]

# Combined: all float signals (regime shifts handled separately).
ALL_NUMERIC_SIGNALS = (
    CORRELATION_SIGNALS
    + MOMENTUM_SIGNALS
    + CONFIDENCE_SIGNALS
    + PREDICTION_SIGNALS
    + BETA_SIGNALS
)

# Short readable labels for printing.
SIGNAL_LABELS: dict[str, str] = {
    "contemp_corr_historical": "contemp_corr",
    "leading_corr_historical": "lead_corr",
    "contemp_corr_ma": "contemp_ma",
    "leading_corr_ma": "lead_ma",
    "filtered_contemp_corr": "filt_contemp",
    "filtered_leading_corr": "filt_lead",
    "ucc_consensus_corr_historical": "ucc_cons_corr",
    "consensus_revenue_corr_historical": "cons_rev_corr",
    "ucc_surprise_corr_historical": "ucc_surp_corr",
    "contemp_corr_momentum": "contemp_mom",
    "leading_corr_momentum": "lead_mom",
    "contemp_confidence": "contemp_conf",
    "leading_confidence": "lead_conf",
    "predicted_surprise_direction": "pred_dir",
    "predicted_surprise_magnitude": "pred_mag",
    "predicted_surprise_magnitude_v2": "pred_mag_v2",
    "predicted_rev_resid_calibrated": "pred_rev_cal",
    "predicted_surprise_calibrated": "pred_surp_cal",
    "ucc_to_rev_beta": "ucc_rev_beta",
    "ucc_to_surprise_beta": "ucc_surp_beta",
    "contemp_regime_shift": "contemp_regime",
    "leading_regime_shift": "lead_regime",
}


def _label(col: str) -> str:
    return SIGNAL_LABELS.get(col, col)


# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Load all signals + market data
# ─────────────────────────────────────────────────────────────────────────────


def _discover_tickers() -> list[str]:
    """Return all tickers that have signal data."""
    signal_dir = data_root / "signal-data"
    return sorted(
        d.name.removeprefix("ticker=")
        for d in signal_dir.iterdir()
        if d.is_dir() and d.name.startswith("ticker=")
    )


def _best_visible_col(ticker: str, method: str) -> tuple[str, str]:
    """Pick the visible_col with the most non-null residual observations.

    Returns (visible_col, resid_col_name).
    """
    vcs = list_visible_cols(ticker, method=method)
    if not vcs:
        raise ValueError(f"No visible_col variants for {ticker}")

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

    return best_vc, f"{best_vc}_resid"


def build_signal_panel(
    tickers: list[str],
    method: str = "stl_p4_s7_robustTrue",
) -> pl.DataFrame:
    """Build a panel with ALL signal columns per (ticker, earnings_date).

    One row per (ticker, earnings_date) with the UCC residual plus every
    correlation, confidence, regime, momentum, and prediction signal.

    Returns DataFrame with columns:
        [ticker, date, visible_col, resid, <all signal cols>...]
    """
    rows: list[pl.DataFrame] = []
    skipped: list[str] = []

    for ticker in tickers:
        try:
            vc, resid_col = _best_visible_col(ticker, method)
        except ValueError:
            skipped.append(ticker)
            continue

        df = load_signal_data(
            ticker, method=method, name="processed_data", visible_col=vc
        )
        if resid_col not in df.columns or "earnings_date" not in df.columns:
            skipped.append(ticker)
            continue

        # Start with core columns.
        select_exprs: list[pl.Expr] = [
            pl.col("earnings_date").cast(pl.Date).alias("date"),
            pl.lit(ticker).alias("ticker"),
            pl.col(resid_col).alias("resid"),
            pl.lit(vc).alias("visible_col"),
        ]

        # Add all numeric signal columns that exist in this file.
        for sig_col in ALL_NUMERIC_SIGNALS:
            if sig_col in df.columns:
                select_exprs.append(pl.col(sig_col).cast(pl.Float64))
            else:
                select_exprs.append(pl.lit(None, dtype=pl.Float64).alias(sig_col))

        # Encode regime shifts as binary (0 = no shift, 1 = regime shift).
        for rs_col in REGIME_SHIFT_SIGNALS:
            if rs_col in df.columns:
                select_exprs.append(
                    pl.col(rs_col).is_not_null().cast(pl.Float64).alias(rs_col)
                )
            else:
                select_exprs.append(pl.lit(None, dtype=pl.Float64).alias(rs_col))

        panel = df.select(select_exprs).filter(
            pl.col("date").is_not_null() & pl.col("resid").is_not_null()
        )

        if panel.height > 0:
            rows.append(panel)
        else:
            skipped.append(ticker)

    if skipped:
        print(f"  Skipped {len(skipped)} tickers (no usable signal): {skipped}")

    return pl.concat(rows, how="diagonal_relaxed").sort("ticker", "date")


def load_all_market_data(
    tickers: list[str],
    start_date: date = date(2015, 1, 1),
) -> dict[str, pl.DataFrame]:
    """Load daily market data for all tickers."""
    print(f"  Loading market data for {len(tickers)} tickers...")
    loaders = MarketDataLoaders.for_tickers(
        tickers=tickers,
        benchmark_ticker=None,
        start_date=start_date,
        with_returns=True,
    )
    return {t: loaders[t] for t in loaders.keys() if t in tickers}


# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Per-ticker signal quality screening (all signals)
# ─────────────────────────────────────────────────────────────────────────────


def _forward_return(
    market_df: pl.DataFrame,
    signal_date: date,
    horizon_days: int,
) -> float | None:
    """Compute forward return from signal_date over horizon_days trading days.

    No lookahead: ``signal_date`` is the **earnings_date** — the date the
    signal became publicly known.  Forward returns start from the *first
    trading day on or after* that date, so we only use future prices.
    """
    future = market_df.filter(pl.col("date") >= signal_date).sort("date")
    if future.height < 2:
        return None

    close_0 = future["close"][0]
    if close_0 is None or close_0 == 0:
        return None

    idx = min(horizon_days, future.height - 1)
    close_t = future["close"][idx]
    if close_t is None:
        return None

    return float((close_t - close_0) / close_0)


def _compute_ic(
    signal_vals: np.ndarray,
    fwd_vals: np.ndarray,
) -> tuple[float | None, float | None]:
    """Spearman IC + p-value; returns (ic, pval) or (None, None)."""
    if len(signal_vals) < 5:
        return None, None
    # Remove NaN pairs.
    mask = np.isfinite(signal_vals) & np.isfinite(fwd_vals)
    s, f = signal_vals[mask], fwd_vals[mask]
    if len(s) < 5:
        return None, None
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ic, pval = stats.spearmanr(s, f)
    if not np.isfinite(ic):
        return None, None
    return float(ic), float(pval)


# All signal columns we evaluate (numeric + regime).
ALL_SIGNAL_COLS = ALL_NUMERIC_SIGNALS + REGIME_SHIFT_SIGNALS


def screen_ticker_signals(
    signal_panel: pl.DataFrame,
    market_data: dict[str, pl.DataFrame],
    horizon: int = 30,
    min_obs: int = 5,
) -> pl.DataFrame:
    """Compute per-ticker, per-signal IC at the given horizon.

    Returns DataFrame with:
        ticker, visible_col, n_obs, signal_col, ic, pval, accuracy, ls_spread, n_paired
    One row per (ticker, signal_col) combination.
    """
    results: list[dict] = []
    tickers = signal_panel["ticker"].unique().sort().to_list()

    for ticker in tickers:
        if ticker not in market_data:
            continue

        mkt = market_data[ticker]
        signals = signal_panel.filter(pl.col("ticker") == ticker)
        vc = signals["visible_col"][0]

        # Pre-compute forward returns for all earnings dates.
        dates = signals["date"].to_list()
        fwd_rets: dict[date, float | None] = {}
        for d in dates:
            fwd_rets[d] = _forward_return(mkt, d, horizon)

        # Evaluate the UCC residual first.
        signal_cols_to_test = ["resid"] + [
            c for c in ALL_SIGNAL_COLS if c in signals.columns
        ]

        for sig_col in signal_cols_to_test:
            sig_vals: list[float] = []
            fwd_vals: list[float] = []

            for row in signals.iter_rows(named=True):
                fwd = fwd_rets[row["date"]]
                sig_val = row.get(sig_col)
                if fwd is not None and sig_val is not None and np.isfinite(sig_val):
                    sig_vals.append(float(sig_val))
                    fwd_vals.append(fwd)

            n = len(sig_vals)
            ic, pval = _compute_ic(np.array(sig_vals), np.array(fwd_vals))

            # Direction accuracy and long-short spread.
            accuracy = None
            ls_spread = None
            if n >= min_obs:
                sig_arr = np.array(sig_vals)
                fwd_arr = np.array(fwd_vals)
                same_sign = np.sum(np.sign(sig_arr) == np.sign(fwd_arr))
                accuracy = float(same_sign / n)

                long_mask = sig_arr > 0
                short_mask = sig_arr < 0
                long_ret = (
                    float(np.mean(fwd_arr[long_mask])) if long_mask.sum() > 0 else 0.0
                )
                short_ret = (
                    float(np.mean(fwd_arr[short_mask])) if short_mask.sum() > 0 else 0.0
                )
                ls_spread = long_ret - short_ret

            results.append(
                {
                    "ticker": ticker,
                    "visible_col": vc,
                    "signal_col": sig_col,
                    "n_obs": signals.height,
                    "n_paired": n,
                    "ic": ic,
                    "pval": pval,
                    "accuracy": accuracy,
                    "ls_spread": ls_spread,
                }
            )

    return (
        pl.DataFrame(results)
        .with_columns(pl.col("ic").abs().alias("abs_ic"))
        .sort("abs_ic", descending=True, nulls_last=True)
    )


# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Cross-ticker signal matrices (for significant signals only)
# ─────────────────────────────────────────────────────────────────────────────


def identify_significant_signals(
    screening: pl.DataFrame,
    pval_thresh: float = 0.20,
    min_abs_ic: float = 0.05,
) -> pl.DataFrame:
    """Filter screening results for statistically significant signals.

    Returns rows where |IC| >= min_abs_ic AND p-value <= pval_thresh.
    """
    return screening.filter(
        pl.col("ic").is_not_null()
        & pl.col("pval").is_not_null()
        & (pl.col("abs_ic") >= min_abs_ic)
        & (pl.col("pval") <= pval_thresh)
    )


def build_cross_ic_matrix(
    signal_panel: pl.DataFrame,
    market_data: dict[str, pl.DataFrame],
    signal_col: str,
    horizon: int = 30,
    min_obs: int = 8,
) -> tuple[pl.DataFrame, list[str]]:
    """Build NxN cross-signal IC matrix for a given signal column.

    cross_ic[A][B] = rank correlation between ticker A's signal
    and ticker B's forward return at A's signal dates.

    **Lookahead protection**: the reference date is ticker A's
    ``earnings_date`` — the date A's signal became public.  Forward
    returns for ticker B are measured from that same public date
    forward.  We never use any signal before its earnings_date.

    Only includes tickers that have non-null values for signal_col.
    Returns (matrix_df, ticker_list).
    """
    # Filter to tickers that have this signal column with enough data.
    ticker_signals: dict[str, list[tuple[date, float]]] = {}

    for ticker in sorted(signal_panel["ticker"].unique().to_list()):
        if ticker not in market_data:
            continue
        rows = signal_panel.filter(pl.col("ticker") == ticker)
        if signal_col not in rows.columns:
            continue

        pairs = []
        for r in rows.iter_rows(named=True):
            val = r.get(signal_col)
            if val is not None and np.isfinite(val):
                pairs.append((r["date"], float(val)))
        if len(pairs) >= min_obs:
            ticker_signals[ticker] = pairs

    tickers = sorted(ticker_signals.keys())
    n = len(tickers)
    if n < 2:
        return pl.DataFrame(), tickers

    matrix = np.full((n, n), np.nan)

    for i, ticker_a in enumerate(tickers):
        for j, ticker_b in enumerate(tickers):
            if ticker_b not in market_data:
                continue

            mkt_b = market_data[ticker_b]
            sigs: list[float] = []
            fwds: list[float] = []

            for sig_date, sig_val in ticker_signals[ticker_a]:
                fwd = _forward_return(mkt_b, sig_date, horizon)
                if fwd is not None:
                    sigs.append(sig_val)
                    fwds.append(fwd)

            if len(sigs) >= min_obs:
                ic, _ = _compute_ic(np.array(sigs), np.array(fwds))
                if ic is not None:
                    matrix[i, j] = ic

    matrix_df = pl.DataFrame(
        {"signal_ticker": tickers}
        | {t: matrix[:, j].tolist() for j, t in enumerate(tickers)}
    )

    return matrix_df, tickers


def build_signal_signal_correlation(
    signal_panel: pl.DataFrame,
    signal_col: str,
    min_obs: int = 8,
) -> tuple[pl.DataFrame, list[str]]:
    """Build NxN signal-signal correlation matrix for a given signal column.

    Correlates ticker A's signal with ticker B's signal on overlapping
    earnings dates.

    **Lookahead protection**: uses ``strategy="backward"`` so that for each
    of A's earnings dates we only match B's *most recent prior* earnings
    date (within 60 days).  This avoids using B's signal before it was
    publicly released.
    """
    # Filter tickers with enough data for this signal.
    ticker_data: dict[str, pl.DataFrame] = {}
    for t in sorted(signal_panel["ticker"].unique().to_list()):
        rows = signal_panel.filter(pl.col("ticker") == t)
        if signal_col not in rows.columns:
            continue
        sub = rows.select("date", pl.col(signal_col).alias("sig")).drop_nulls()
        if sub.height >= min_obs:
            ticker_data[t] = sub

    tickers = sorted(ticker_data.keys())
    n = len(tickers)
    if n < 2:
        return pl.DataFrame(), tickers

    matrix = np.full((n, n), np.nan)

    for i, ta in enumerate(tickers):
        for j, tb in enumerate(tickers):
            if j < i:
                matrix[i, j] = matrix[j, i]
                continue
            if i == j:
                matrix[i, j] = 1.0
                continue

            # A → B: for each of A's earnings dates, find B's most recent
            # prior earnings date (strategy="backward").  Then also compute
            # B → A the same way.  Average the two directions for the
            # symmetric matrix entry.
            da = ticker_data[ta].rename({"sig": "sig_a"})
            db = ticker_data[tb].rename({"sig": "sig_b", "date": "date_b"})

            joined_ab = da.join_asof(
                db.sort("date_b"),
                left_on="date",
                right_on="date_b",
                strategy="backward",
                tolerance="60d",
            ).drop_nulls()

            # B → A direction
            da2 = ticker_data[ta].rename({"sig": "sig_a", "date": "date_a"})
            db2 = ticker_data[tb].rename({"sig": "sig_b"})

            joined_ba = db2.join_asof(
                da2.sort("date_a"),
                left_on="date",
                right_on="date_a",
                strategy="backward",
                tolerance="60d",
            ).drop_nulls()

            # Use the direction with more observations; fall back to the other.
            if joined_ab.height >= min_obs and joined_ba.height >= min_obs:
                ic_ab, _ = _compute_ic(
                    joined_ab["sig_a"].to_numpy().astype(np.float64),
                    joined_ab["sig_b"].to_numpy().astype(np.float64),
                )
                ic_ba, _ = _compute_ic(
                    joined_ba["sig_b"].to_numpy().astype(np.float64),
                    joined_ba["sig_a"].to_numpy().astype(np.float64),
                )
                vals = [v for v in (ic_ab, ic_ba) if v is not None]
                if vals:
                    corr = float(np.mean(vals))
                    matrix[i, j] = corr
                    matrix[j, i] = corr
            elif joined_ab.height >= min_obs:
                ic_ab, _ = _compute_ic(
                    joined_ab["sig_a"].to_numpy().astype(np.float64),
                    joined_ab["sig_b"].to_numpy().astype(np.float64),
                )
                if ic_ab is not None:
                    matrix[i, j] = ic_ab
                    matrix[j, i] = ic_ab
            elif joined_ba.height >= min_obs:
                ic_ba, _ = _compute_ic(
                    joined_ba["sig_b"].to_numpy().astype(np.float64),
                    joined_ba["sig_a"].to_numpy().astype(np.float64),
                )
                if ic_ba is not None:
                    matrix[i, j] = ic_ba
                    matrix[j, i] = ic_ba

    matrix_df = pl.DataFrame(
        {"ticker": tickers} | {t: matrix[:, j].tolist() for j, t in enumerate(tickers)}
    )

    return matrix_df, tickers


# ─────────────────────────────────────────────────────────────────────────────
# Step 4: Extract portfolio opportunities
# ─────────────────────────────────────────────────────────────────────────────


def extract_cross_pairs(
    cross_ic_df: pl.DataFrame,
    tickers: list[str],
    signal_col: str,
    min_abs_ic: float = 0.15,
) -> pl.DataFrame:
    """Extract strongest cross-predictive pairs from an IC matrix."""
    pairs: list[dict] = []

    for i, ta in enumerate(tickers):
        for j, tb in enumerate(tickers):
            if i == j:
                continue
            ic_val = cross_ic_df[tb][i]
            if ic_val is not None and abs(ic_val) >= min_abs_ic:
                pairs.append(
                    {
                        "signal_ticker": ta,
                        "target_ticker": tb,
                        "signal_col": signal_col,
                        "cross_ic": ic_val,
                        "abs_ic": abs(ic_val),
                        "direction": "positive" if ic_val > 0 else "negative",
                    }
                )

    if not pairs:
        return pl.DataFrame(
            schema={
                "signal_ticker": pl.Utf8,
                "target_ticker": pl.Utf8,
                "signal_col": pl.Utf8,
                "cross_ic": pl.Float64,
                "abs_ic": pl.Float64,
                "direction": pl.Utf8,
            }
        )

    return pl.DataFrame(pairs).sort("abs_ic", descending=True)


def extract_signal_hedges(
    sig_corr_df: pl.DataFrame,
    tickers: list[str],
    signal_col: str,
    max_corr: float = -0.2,
) -> pl.DataFrame:
    """Find ticker pairs with negatively correlated signals (natural hedges)."""
    pairs: list[dict] = []

    for i, ta in enumerate(tickers):
        for j, tb in enumerate(tickers):
            if j <= i:
                continue
            corr_val = sig_corr_df[tb][i]
            if corr_val is not None and corr_val <= max_corr:
                pairs.append(
                    {
                        "ticker_a": ta,
                        "ticker_b": tb,
                        "signal_col": signal_col,
                        "signal_corr": corr_val,
                    }
                )

    if not pairs:
        return pl.DataFrame(
            schema={
                "ticker_a": pl.Utf8,
                "ticker_b": pl.Utf8,
                "signal_col": pl.Utf8,
                "signal_corr": pl.Float64,
            }
        )

    return pl.DataFrame(pairs).sort("signal_corr")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────


def main(
    horizon: int = 30,
    min_obs: int = 8,
    start_date: date = date(2018, 1, 1),
    pval_thresh: float = 0.20,
    min_abs_ic: float = 0.05,
) -> None:
    pl.Config.set_tbl_cols(20)
    pl.Config.set_tbl_rows(40)
    pl.Config.set_fmt_float("mixed")

    print("=" * 80)
    print("CROSS-TICKER MULTI-SIGNAL ANALYSIS")
    print("=" * 80)

    # ── Step 1: Load data ────────────────────────────────────────────────
    print("\n[1/4] Discovering tickers and loading ALL signals...")
    all_tickers = _discover_tickers()
    print(f"  Found {len(all_tickers)} tickers with signal data")

    signal_panel = build_signal_panel(all_tickers)
    used_tickers = signal_panel["ticker"].unique().sort().to_list()
    print(
        f"  Signal panel: {signal_panel.height} observations "
        f"across {len(used_tickers)} tickers"
    )
    print(f"  Signal columns loaded: {len(ALL_SIGNAL_COLS) + 1}")  # +1 for resid

    # Quick column availability check.
    available_signals = ["resid"] + [
        c for c in ALL_SIGNAL_COLS if c in signal_panel.columns
    ]
    print(f"  Available in panel: {len(available_signals)} signals")

    print("\n[1/4] Loading market data...")
    market_data = load_all_market_data(used_tickers, start_date=start_date)
    loaded_tickers = list(market_data.keys())
    print(f"  Loaded market data for {len(loaded_tickers)} tickers")

    # ── Step 2: Per-ticker × per-signal screening ────────────────────────
    print(f"\n[2/4] Screening all signal types per ticker (horizon={horizon}d)...")
    screening = screen_ticker_signals(
        signal_panel, market_data, horizon=horizon, min_obs=5
    )

    # ── 2a: Best signal per ticker ────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print(f"BEST SIGNAL PER TICKER (highest |IC| at {horizon}d)")
    print(f"{'=' * 80}")

    # For each ticker, find the signal with the highest |IC|.
    best_per_ticker = (
        screening.filter(pl.col("ic").is_not_null())
        .sort("abs_ic", descending=True)
        .group_by("ticker", maintain_order=True)
        .first()
        .sort("abs_ic", descending=True)
    )

    print(
        best_per_ticker.select(
            "ticker",
            "signal_col",
            "n_paired",
            "ic",
            "pval",
            "accuracy",
            "ls_spread",
        ).head(30)
    )

    # ── 2b: Best ticker per signal ────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print(f"BEST TICKER PER SIGNAL TYPE (highest |IC| at {horizon}d)")
    print(f"{'=' * 80}")

    best_per_signal = (
        screening.filter(pl.col("ic").is_not_null())
        .sort("abs_ic", descending=True)
        .group_by("signal_col", maintain_order=True)
        .first()
        .sort("abs_ic", descending=True)
    )

    print(
        best_per_signal.select(
            "signal_col",
            "ticker",
            "n_paired",
            "ic",
            "pval",
            "accuracy",
            "ls_spread",
        ).head(30)
    )

    # ── 2c: Statistically significant signals ────────────────────────────
    significant = identify_significant_signals(
        screening, pval_thresh=pval_thresh, min_abs_ic=min_abs_ic
    )

    print(f"\n{'=' * 80}")
    print(
        f"STATISTICALLY SIGNIFICANT SIGNALS (|IC| >= {min_abs_ic}, p <= {pval_thresh})"
    )
    print(f"{'=' * 80}")
    print(f"  Total significant (ticker, signal) pairs: {significant.height}")

    # Count by signal type.
    sig_counts = (
        significant.group_by("signal_col")
        .agg(
            pl.len().alias("n_tickers"),
            pl.col("ic").mean().alias("mean_ic"),
            pl.col("abs_ic").mean().alias("mean_abs_ic"),
        )
        .sort("n_tickers", descending=True)
    )
    print("\n  Significant signals by type:")
    print(sig_counts)

    # ── 2d: Signal-type summary across all tickers ────────────────────────
    print(f"\n{'=' * 80}")
    print("SIGNAL TYPE SUMMARY ACROSS ALL TICKERS")
    print(f"{'=' * 80}")

    signal_summary = (
        screening.filter(pl.col("ic").is_not_null())
        .group_by("signal_col")
        .agg(
            pl.len().alias("n_tickers"),
            pl.col("ic").mean().alias("mean_ic"),
            pl.col("abs_ic").mean().alias("mean_abs_ic"),
            pl.col("ic").median().alias("median_ic"),
            (pl.col("pval") <= pval_thresh).sum().alias("n_significant"),
            pl.col("accuracy").mean().alias("mean_accuracy"),
        )
        .sort("mean_abs_ic", descending=True)
    )
    print(signal_summary)

    # ── Step 3: Cross-ticker matrices for significant signal types ────────
    # Find the signal types that are significant for multiple tickers.
    sig_types_for_cross = sig_counts.filter(pl.col("n_tickers") >= 3)[
        "signal_col"
    ].to_list()

    # Always include the resid if it's not already there.
    if "resid" not in sig_types_for_cross:
        sig_types_for_cross.append("resid")

    # Limit to top N signal types to keep computation manageable.
    sig_types_for_cross = sig_types_for_cross[:8]

    # For cross-ticker analysis, use only tickers with enough market data.
    viable_tickers = [t for t in used_tickers if t in market_data]
    viable_panel = signal_panel.filter(pl.col("ticker").is_in(viable_tickers))
    viable_market = {t: market_data[t] for t in viable_tickers}

    all_cross_pairs: list[pl.DataFrame] = []
    all_hedges: list[pl.DataFrame] = []

    for sig_type in sig_types_for_cross:
        print(
            f"\n[3/4] Cross-ticker IC matrix for '{_label(sig_type)}' "
            f"({len(viable_tickers)} tickers, {horizon}d)..."
        )

        cross_ic_df, cross_tickers = build_cross_ic_matrix(
            viable_panel,
            viable_market,
            signal_col=sig_type,
            horizon=horizon,
            min_obs=min_obs,
        )

        if len(cross_tickers) < 2:
            print(f"  Skipped — fewer than 2 tickers have {sig_type}")
            continue

        # Print compact view.
        show_n = min(12, len(cross_tickers))
        compact = cross_ic_df.select("signal_ticker", *cross_tickers[:show_n]).head(
            show_n
        )

        print(
            f"\n  Cross-IC matrix ({_label(sig_type)}) — {len(cross_tickers)} tickers:"
        )
        print(compact)

        # Extract notable cross-predictive pairs.
        pairs = extract_cross_pairs(
            cross_ic_df, cross_tickers, signal_col=sig_type, min_abs_ic=0.15
        )
        if pairs.height == 0:
            pairs = extract_cross_pairs(
                cross_ic_df, cross_tickers, signal_col=sig_type, min_abs_ic=0.10
            )
        if pairs.height > 0:
            all_cross_pairs.append(pairs)

        # Signal-signal correlations.
        sig_corr_df, sig_tickers = build_signal_signal_correlation(
            viable_panel, signal_col=sig_type, min_obs=min_obs
        )

        hedges = extract_signal_hedges(
            sig_corr_df, sig_tickers, signal_col=sig_type, max_corr=-0.2
        )
        if hedges.height == 0:
            hedges = extract_signal_hedges(
                sig_corr_df, sig_tickers, signal_col=sig_type, max_corr=0.0
            )
        if hedges.height > 0:
            all_hedges.append(hedges)

    # ── Step 4: Combined results ─────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("CROSS-PREDICTIVE PAIRS — ALL SIGNAL TYPES (|cross-IC| ≥ 0.10)")
    print(f"{'=' * 80}")

    if all_cross_pairs:
        combined_pairs = pl.concat(all_cross_pairs).sort("abs_ic", descending=True)
        print(combined_pairs.head(40))
    else:
        combined_pairs = pl.DataFrame()
        print("  No cross-predictive pairs found.")

    print(f"\n{'=' * 80}")
    print("NATURAL HEDGES — ALL SIGNAL TYPES (signal correlation < -0.2)")
    print(f"{'=' * 80}")

    if all_hedges:
        combined_hedges = pl.concat(all_hedges).sort("signal_corr")
        print(combined_hedges.head(30))
    else:
        combined_hedges = pl.DataFrame()
        print("  No natural hedges found (relaxing to corr < 0).")

    # ── Summary ──────────────────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")

    print(f"\n  Total tickers: {len(used_tickers)}")
    print(f"  Total (ticker, signal) pairs evaluated: {screening.height}")
    print(
        f"  Statistically significant pairs "
        f"(|IC|≥{min_abs_ic}, p≤{pval_thresh}): {significant.height}"
    )
    print(f"  Signal types with ≥3 significant tickers: {len(sig_types_for_cross)}")

    if combined_pairs.height > 0:
        print(f"  Cross-predictive pairs (|IC|≥0.10): {combined_pairs.height}")
        # Show unique signal types that appear in cross-pairs.
        unique_sigs = combined_pairs["signal_col"].unique().to_list()
        print(f"  Signal types driving cross-prediction: {unique_sigs}")

    if combined_hedges.height > 0:
        print(f"  Natural hedge pairs: {combined_hedges.height}")

    # Top tickers by count of significant signals.
    ticker_sig_count = (
        significant.group_by("ticker")
        .agg(
            pl.len().alias("n_significant_signals"),
            pl.col("signal_col").alias("significant_signals"),
        )
        .sort("n_significant_signals", descending=True)
    )
    print("\n  Top tickers by # significant signals:")
    for row in ticker_sig_count.head(15).iter_rows(named=True):
        sigs = row["significant_signals"]
        short = [_label(s) for s in sigs[:5]]
        extra = f"... +{len(sigs) - 5}" if len(sigs) > 5 else ""
        print(
            f"    {row['ticker']:6s}: "
            f"{row['n_significant_signals']} signals — "
            f"{', '.join(short)}{extra}"
        )

    # ── Save results ─────────────────────────────────────────────────────
    output_dir = Path("results") / "cross_ticker_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    screening.write_csv(output_dir / "signal_screening_all.csv")
    significant.write_csv(output_dir / "significant_signals.csv")
    best_per_ticker.write_csv(output_dir / "best_signal_per_ticker.csv")
    signal_summary.write_csv(output_dir / "signal_type_summary.csv")

    if combined_pairs.height > 0:
        combined_pairs.write_csv(output_dir / "cross_predictive_pairs.csv")
    if combined_hedges.height > 0:
        combined_hedges.write_csv(output_dir / "natural_hedges.csv")

    print(f"\n  Results saved to {output_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cross-ticker multi-signal analysis")
    parser.add_argument(
        "--horizon",
        type=int,
        default=30,
        help="Forward return horizon in trading days",
    )
    parser.add_argument(
        "--min-obs",
        type=int,
        default=8,
        help="Minimum observations for correlation",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default="2018-01-01",
        help="Start date for market data",
    )
    parser.add_argument(
        "--pval",
        type=float,
        default=0.20,
        help="P-value threshold for significance",
    )
    parser.add_argument(
        "--min-ic",
        type=float,
        default=0.05,
        help="Minimum |IC| threshold for significance",
    )
    args = parser.parse_args()

    main(
        horizon=args.horizon,
        min_obs=args.min_obs,
        start_date=date.fromisoformat(args.start_date),
        pval_thresh=args.pval,
        min_abs_ic=args.min_ic,
    )
