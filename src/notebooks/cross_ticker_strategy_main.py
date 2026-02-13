"""Cross-ticker strategy grid search.

Uses peer tickers' UCC signals to inform trade direction for a target ticker.
Compares against CorrelationAwareEntry (own signal only) and MomentumEntry
(price-only) baselines.

Auto-selects peers from cross_predictive_pairs.csv produced by
cross_ticker_signal_analysis.py.

Usage:
    python src/notebooks/cross_ticker_strategy_main.py --ticker PCAR
    python src/notebooks/cross_ticker_strategy_main.py --ticker DE --top-peers 3
"""

from __future__ import annotations

import argparse
from datetime import date

import polars as pl

from abovedata_backtesting.data_loaders.load_signal_data import (
    list_visible_cols,
    load_signal_data,
)
from abovedata_backtesting.entries.correlation_aware_entry import CorrelationAwareEntry
from abovedata_backtesting.entries.cross_ticker_entry import (
    CrossTickerEntry,
    discover_peer_config,
)
from abovedata_backtesting.entries.entry_signals import MomentumEntry
from abovedata_backtesting.exits.exit_strategies import (
    FixedHoldingExit,
    SignalChangeExit,
    StopLossTakeProfitExit,
    TrailingStopExit,
)
from abovedata_backtesting.processors.benchmark_processor import (
    BenchmarkConfig,
    BenchmarkProcessor,
)
from abovedata_backtesting.processors.signal_preprocessor import IdentityPreprocessor
from abovedata_backtesting.processors.strategy_processor import (
    GridSearchResult,
    StrategyProcessor,
)
from abovedata_backtesting.trades.trade_save_results import save_results


# ─────────────────────────────────────────────────────────────────────────────
# Grid search
# ─────────────────────────────────────────────────────────────────────────────


def _best_visible_col(ticker: str, method: str = "stl_p4_s7_robustTrue") -> str:
    """Pick the visible_col with the most non-null residual observations."""
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

    return best_vc


def run_cross_ticker_search(
    ticker: str,
    top_n_peers: int = 5,
    signal_method: str = "stl_p4_s7_robustTrue",
    start_date: date | None = date(2018, 1, 1),
    end_date: date | None = None,
    debug: bool = True,
) -> tuple[pl.DataFrame, list[GridSearchResult], StrategyProcessor]:
    """Run grid search comparing cross-ticker vs baseline entries."""

    # 1. Pick best visible_col.
    visible_col = _best_visible_col(ticker, method=signal_method)
    resid_col = f"{visible_col}_resid"
    print(f"  Using visible_col={visible_col} (resid_col={resid_col})")

    # 2. Load signals.
    signals = load_signal_data(
        ticker, method=signal_method, name="processed_data", visible_col=visible_col
    )

    if resid_col not in signals.columns:
        raise ValueError(f"Expected column '{resid_col}' not found.")

    # 3. Discover peers.
    peer_config = discover_peer_config(ticker, top_n_peers=top_n_peers)
    peer_tickers = peer_config["peer_tickers"]
    peer_signal_cols = peer_config["peer_signal_cols"]

    # 4. Set up processor.
    bm_config = BenchmarkConfig.for_ticker(ticker, signal_col=visible_col)
    benchmarks = BenchmarkProcessor(bm_config).run()

    processor = StrategyProcessor(
        ticker=ticker,
        benchmark_ticker=ticker,
        signals=signals,
        visible_col=visible_col,
        start_date=start_date,
        end_date=end_date,
        debug=debug,
        max_entries_per_signal=[3],
        benchmarks=benchmarks,
    )

    processor.add_preprocessors([IdentityPreprocessor()])

    # ═══════════════════════════════════════════════════════════════════════
    # Entry rules
    # ═══════════════════════════════════════════════════════════════════════

    entry_days_before = [5, 15, 20, 30]

    # ── Cross-ticker entries ─────────────────────────────────────────────
    if peer_tickers:
        # Build peer tuples: individual peers + combined.
        peer_sets: list[tuple[str, ...]] = []
        for pt in peer_tickers[:3]:
            peer_sets.append((pt,))
        if len(peer_tickers) >= 2:
            peer_sets.append(tuple(peer_tickers[:3]))
        if len(peer_tickers) >= 4:
            peer_sets.append(tuple(peer_tickers[:5]))

        # Ensure "resid" is always in the signal cols to try.
        peer_sig_cols = list(set(peer_signal_cols + ["resid"]))

        cross_entries = CrossTickerEntry.grid(
            target_ticker=[ticker],
            peer_tickers=peer_sets,
            peer_signal_col=peer_sig_cols,
            own_signal_col=[resid_col],
            aggregation=["mean", "strongest", "majority"],
            min_peer_signals=[1, 2],
            max_peer_signal_age_days=[90],
            entry_days_before=entry_days_before,
            min_own_signal_abs=[0.0],
            rolling_ic_window=[4, 6, 8],
        )
        print(f"\n  Cross-ticker entry rules: {len(cross_entries)}")
        processor.add_entries(cross_entries)

    # ── Correlation-aware baseline ───────────────────────────────────────
    corr_aware = CorrelationAwareEntry.grid(
        signal_col=[resid_col],
        corr_col=["contemp", "leading"],
        min_signal_abs=[0.0],
        min_confidence=[0.0, 0.3],
        skip_regime_shifts=[True, False],
        scale_by_confidence=[False],
        entry_days_before=entry_days_before,
        use_prior_quarter_corr=[True],
    )
    print(f"  Correlation-aware baseline rules: {len(corr_aware)}")
    processor.add_entries(corr_aware)

    # ── Momentum baseline ────────────────────────────────────────────────
    momentum = MomentumEntry.grid(
        lookback_days=[10, 20],
        zscore_threshold=[0.5, 1.0],
        entry_days_before=entry_days_before,
    )
    print(f"  Momentum baseline rules: {len(momentum)}")
    processor.add_entries(momentum)

    # ═══════════════════════════════════════════════════════════════════════
    # Position filters
    # ═══════════════════════════════════════════════════════════════════════
    processor.add_position_filters(["long_short", "long_only"])

    # ═══════════════════════════════════════════════════════════════════════
    # Exit rules
    # ═══════════════════════════════════════════════════════════════════════
    signal_dates = signals["earnings_date"].cast(pl.Date).unique().to_list()

    processor.add_exits(
        [
            SignalChangeExit(),
            FixedHoldingExit(holding_days=30, signal_dates=frozenset(signal_dates)),
            FixedHoldingExit(holding_days=60, signal_dates=frozenset(signal_dates)),
            FixedHoldingExit(holding_days=90, signal_dates=frozenset(signal_dates)),
            StopLossTakeProfitExit(stop_loss_pct=-0.05, take_profit_pct=0.10),
            StopLossTakeProfitExit(stop_loss_pct=-0.10, take_profit_pct=0.20),
            TrailingStopExit(trailing_stop_pct=0.05),
            TrailingStopExit(trailing_stop_pct=0.10),
        ]
    )

    # ═══════════════════════════════════════════════════════════════════════
    # Run
    # ═══════════════════════════════════════════════════════════════════════
    summary_df, results = processor.run(optimize_by="sharpe_ratio")
    summary_df = summary_df.with_columns(pl.lit(visible_col).alias("visible_col"))

    return summary_df, results, processor


# ─────────────────────────────────────────────────────────────────────────────
# Analysis and display
# ─────────────────────────────────────────────────────────────────────────────


def print_entry_type_comparison(
    summary_df: pl.DataFrame,
    min_trades: int = 5,
) -> None:
    """Compare performance across entry types: cross_ticker vs baselines."""
    df = summary_df.filter(pl.col("trade_n_trades") >= min_trades)

    # Classify entry type.
    df = df.with_columns(
        pl.when(pl.col("entry_name").str.contains("cross_"))
        .then(pl.lit("cross_ticker"))
        .when(pl.col("entry_name").str.contains("corr_aware"))
        .then(pl.lit("corr_aware"))
        .when(pl.col("entry_name").str.contains("momentum"))
        .then(pl.lit("momentum"))
        .otherwise(pl.lit("other"))
        .alias("entry_type_group")
    )

    comparison = (
        df.group_by("entry_type_group")
        .agg(
            pl.col("sharpe_ratio").mean().alias("mean_sharpe"),
            pl.col("sharpe_ratio").max().alias("max_sharpe"),
            pl.col("sharpe_ratio").median().alias("median_sharpe"),
            pl.col("trade_total_return").mean().alias("mean_return"),
            pl.col("trade_total_return").max().alias("max_return"),
            pl.col("trade_n_trades").mean().alias("mean_trades"),
            pl.len().alias("n_strategies"),
        )
        .sort("mean_sharpe", descending=True)
    )

    print("\n" + "=" * 70)
    print("ENTRY TYPE COMPARISON")
    print("=" * 70)
    print(comparison)

    # Top 5 per entry type.
    for group in df["entry_type_group"].unique().sort().to_list():
        subset = df.filter(pl.col("entry_type_group") == group).sort(
            "sharpe_ratio", descending=True
        )
        print(f"\n  Top 5 {group}:")
        for row in subset.head(5).iter_rows(named=True):
            print(
                f"    {row['entry_name'][:60]} × {row['exit_name']}: "
                f"sharpe={row['sharpe_ratio']:.3f}  "
                f"return={row['trade_total_return']:.1%}  "
                f"trades={row['trade_n_trades']}"
            )


def print_cross_ticker_details(
    summary_df: pl.DataFrame,
    min_trades: int = 5,
) -> None:
    """Show details of cross-ticker strategy variants."""
    cross = summary_df.filter(
        pl.col("entry_name").str.contains("cross_")
        & (pl.col("trade_n_trades") >= min_trades)
    ).sort("sharpe_ratio", descending=True)

    if cross.height == 0:
        print("\n  No cross-ticker strategies met the minimum trade count.")
        return

    print("\n" + "=" * 70)
    print(f"CROSS-TICKER STRATEGY DETAILS (top 20 of {cross.height})")
    print("=" * 70)

    for row in cross.head(20).iter_rows(named=True):
        print(f"  {row['entry_name'][:70]}")
        print(
            f"    exit={row['exit_name']}  "
            f"sharpe={row['sharpe_ratio']:.3f}  "
            f"return={row['trade_total_return']:.1%}  "
            f"trades={row['trade_n_trades']}  "
            f"win_rate={row.get('trade_win_rate', 0):.1%}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────


def main(ticker: str = "PCAR", top_n_peers: int = 5) -> None:
    pl.Config.set_tbl_cols(14)
    pl.Config.set_tbl_rows(25)

    print(f"\n{'=' * 60}")
    print(f"Cross-Ticker Strategy Grid Search: {ticker}")
    print(f"{'=' * 60}\n")

    summary_df, results, processor = run_cross_ticker_search(
        ticker=ticker,
        top_n_peers=top_n_peers,
        start_date=date(2015, 1, 1),
        debug=True,
    )

    # ── Entry type comparison ────────────────────────────────────────────
    print_entry_type_comparison(summary_df)

    # ── Cross-ticker details ─────────────────────────────────────────────
    print_cross_ticker_details(summary_df)

    # ── Overall top results ──────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("TOP 10 STRATEGIES BY SHARPE RATIO")
    print("=" * 70)
    top_sharpe = summary_df.filter(pl.col("trade_n_trades") >= 5).sort(
        "sharpe_ratio", descending=True
    )
    for row in top_sharpe.head(10).iter_rows(named=True):
        print(
            f"  {row['entry_name'][:55]:55s} × {row['exit_name']:15s} "
            f"sharpe={row['sharpe_ratio']:6.3f}  "
            f"ret={row['trade_total_return']:7.1%}  "
            f"trades={row['trade_n_trades']}"
        )

    print("\n" + "=" * 70)
    print("TOP 10 STRATEGIES BY TOTAL RETURN")
    print("=" * 70)
    top_ret = summary_df.filter(pl.col("trade_n_trades") >= 5).sort(
        "trade_total_return", descending=True
    )
    for row in top_ret.head(10).iter_rows(named=True):
        print(
            f"  {row['entry_name'][:55]:55s} × {row['exit_name']:15s} "
            f"sharpe={row['sharpe_ratio']:6.3f}  "
            f"ret={row['trade_total_return']:7.1%}  "
            f"trades={row['trade_n_trades']}"
        )

    # ── Head-to-head ─────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("HEAD-TO-HEAD: BEST CROSS-TICKER vs BEST CORR-AWARE vs BEST MOMENTUM")
    print("=" * 70)

    for label, pattern in [
        ("CROSS-TICKER", "cross_"),
        ("CORR-AWARE", "corr_aware"),
        ("MOMENTUM", "momentum"),
    ]:
        subset = summary_df.filter(
            pl.col("entry_name").str.contains(pattern) & (pl.col("trade_n_trades") >= 5)
        ).sort("sharpe_ratio", descending=True)

        if subset.height > 0:
            row = subset.row(0, named=True)
            print(f"\n  {label}: {row['entry_name'][:60]}")
            print(f"    Exit: {row['exit_name']}")
            print(f"    Sharpe: {row['sharpe_ratio']:.3f}")
            print(f"    Total Return: {row['trade_total_return']:.1%}")
            print(f"    Trades: {row['trade_n_trades']}")
            print(f"    Win Rate: {row.get('trade_win_rate', 0):.1%}")
            print(f"    Max DD: {row.get('max_drawdown', 0):.1%}")
        else:
            print(f"\n  {label}: No strategies with >=5 trades")

    # ── Save results ─────────────────────────────────────────────────────
    save_results(
        ticker=ticker,
        summary_df=summary_df,
        results=results,
        processor=processor,
        output_dir="results",
        top_n=5,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run cross-ticker strategy grid search"
    )
    parser.add_argument(
        "--ticker",
        type=str,
        default="PCAR",
        help="Target stock ticker (default: PCAR)",
    )
    parser.add_argument(
        "--top-peers",
        type=int,
        default=5,
        help="Number of top peer tickers to use (default: 5)",
    )
    args = parser.parse_args()
    main(ticker=args.ticker, top_n_peers=args.top_peers)
