"""Strategy grid search using raw STL processor output.

Compares three entry approaches:
1. Momentum (price-only baseline)
2. Correlation-aware (fundamental signal + correlation regime for direction)
3. Signal-based (threshold, confirmation, divergence)

Uses raw STL output with contemp_corr_historical, leading_corr_historical,
confidence scores, and regime shift detection.

Sweeps all available visible_col variants (total_universe, visible_revenue,
visible_count) to find which signal source yields the best performance.
"""

import argparse
from datetime import date

import polars as pl
from IPython.display import display

from abovedata_backtesting.data_loaders.load_signal_data import (
    list_visible_cols,
    load_signal_data,
)
from abovedata_backtesting.entries.correlation_aware_entry import CorrelationAwareEntry
from abovedata_backtesting.entries.entry_signals import (
    DivergenceEntry,
    MomentumEntry,
    SignalMomentumEntry,
    SignalThresholdEntry,
)
from abovedata_backtesting.entries.multi_horizon_entry import MultiHorizonEntry
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
from abovedata_backtesting.processors.signal_preprocessor import (
    IdentityPreprocessor,
    SignalPreprocessor,
)
from abovedata_backtesting.processors.signal_transforms import (
    RateOfChangeTransform,
    TimeShiftTransform,
    WeightedBlendTransform,
)
from abovedata_backtesting.processors.strategy_processor import (
    GridSearchResult,
    GridSearchResults,
    StrategyProcessor,
)
from abovedata_backtesting.trades.analysis_utils import (
    analyze_best_strategies,
    compare_entry_types,
)
from abovedata_backtesting.trades.trade_save_results import save_results


def run_grid_search(
    ticker: str,
    visible_col: str,
    signal_method: str = "stl_p4_s7_robustTrue",
    start_date: date | None = date(2018, 1, 1),
    end_date: date | None = None,
    debug: bool = True,
) -> tuple[pl.DataFrame, list[GridSearchResult], StrategyProcessor]:
    """
    Run grid search with correlation-gated entry rules.

    Uses raw STL processor output from the visible_col-specific parquet file
    so we have access to contemp_corr_historical, leading_corr_historical,
    regime shifts, etc. — all recomputed against the given visible_col.
    """
    signals = load_signal_data(
        ticker, method=signal_method, name="processed_data", visible_col=visible_col
    )

    resid_col = f"{visible_col}_resid"
    if resid_col not in signals.columns:
        raise ValueError(
            f"Expected column '{resid_col}' not found in "
            f"visible_col={visible_col} data. "
            f"Available columns: {signals.columns}"
        )

    bm_config = BenchmarkConfig.for_ticker(ticker, signal_col=visible_col)
    benchmarks = BenchmarkProcessor(bm_config).run()

    processor = StrategyProcessor(
        ticker=ticker,
        benchmark_ticker=ticker,  # Will default to buy and hold
        signals=signals,
        visible_col=visible_col,
        start_date=start_date,
        end_date=end_date,
        debug=debug,
        max_entries_per_signal=[3],
        benchmarks=benchmarks,
    )

    # =========================================================================
    # Define base entry rules
    # =========================================================================
    # THESE ARE TRADING DAYS, NOT CALENDAR DAYS.
    entry_days_before = [5, 15, 20, 30]

    base_momentum = MomentumEntry.grid(
        lookback_days=[10, 20],
        zscore_threshold=[0.5, 1.0, 1.5],
        entry_days_before=entry_days_before,
    )

    base_signal = SignalThresholdEntry.grid(
        signal_col=[resid_col],
        long_threshold=[0.3, 0.5, 1.0],
        short_threshold=[-0.3, -0.5, -1.0],
        entry_days_before=entry_days_before,
        confidence_col=["contemp", "leading"],
    )

    base_confirm = SignalMomentumEntry.grid(
        signal_col=[resid_col],
        signal_threshold=[0.0, 0.3, 0.5],
        lookback_days=[10, 20],
        momentum_zscore_threshold=[0.3, 0.5],
        entry_days_before=entry_days_before,
    )

    base_divergence = DivergenceEntry.grid(
        signal_col=[resid_col],
        lookback_days=[5, 10, 20, 30],
        divergence_zscore=[0.5, 1.0],
        fundamental_threshold=[0.0, 0.5, 1.0],
        require_strong_divergence=[False, True],
        entry_days_before=entry_days_before,
    )

    # =========================================================================
    # Correlation-aware entries (use corr context for direction, not filtering)
    # =========================================================================

    corr_aware = CorrelationAwareEntry.grid(
        signal_col=[resid_col],
        corr_col=["contemp", "leading"],
        min_signal_abs=[0.0, 0.1],
        min_confidence=[0.0, 0.3, 0.4],
        skip_regime_shifts=[True, False],
        scale_by_confidence=[False, True],
        confidence_col=["contemp", "leading"],
        entry_days_before=entry_days_before,
        use_prior_quarter_corr=[True, False],
    )

    # =========================================================================
    # Signal preprocessors (transform signals before entry rules)
    # =========================================================================

    preprocessors = [
        IdentityPreprocessor(),  # baseline: no transforms
        # Lag-1 and lag-2: use prior quarter's signal
        *SignalPreprocessor.grid(
            [
                TimeShiftTransform.grid(
                    source_cols=[(resid_col,)],
                    shift_quarters=[1, 2],
                ),
            ]
        ),
        # Lag + rate-of-change
        *SignalPreprocessor.grid(
            [
                TimeShiftTransform.grid(
                    source_cols=[(resid_col,)],
                    shift_quarters=[1],
                ),
                RateOfChangeTransform.grid(
                    source_col=[resid_col],
                    lookback_quarters=[1],
                ),
            ]
        ),
        # Blend current + lagged
        *SignalPreprocessor.grid(
            [
                TimeShiftTransform.grid(
                    source_cols=[(resid_col,)],
                    shift_quarters=[1],
                ),
                WeightedBlendTransform.grid(
                    col_a=[resid_col],
                    col_b=[f"{resid_col}_lag1q"],
                    weight_a=[0.7, 0.5, 0.3],
                ),
            ]
        ),
    ]
    processor.add_preprocessors(preprocessors)

    # =========================================================================
    # Multi-horizon entries (examine T, T-1, T-2 simultaneously)
    # =========================================================================
    multi_horizon = MultiHorizonEntry.grid(
        signal_col=[resid_col],
        horizons=[(0, 1), (0, 1, 2)],
        strategy=["consensus", "momentum", "reversal"],
        min_signal_abs=[0.0, 0.1],
        corr_col=["contemp", None],
        entry_days_before=entry_days_before,
    )

    # Correlation-aware entries targeting lagged signals
    corr_aware_lagged = CorrelationAwareEntry.grid(
        signal_col=[f"{resid_col}_lag1q"],
        corr_col=["contemp", "leading", "contemp_ma", "leading_ma"],
        min_signal_abs=[0.0, 0.1],
        min_confidence=[0.0, 0.3],
        skip_regime_shifts=[False, True],
        entry_days_before=entry_days_before,
    )

    # =========================================================================
    # Add entries to processor
    # =========================================================================

    # Momentum baseline (price-only, no fundamental input)
    processor.add_entries(base_momentum)

    # Correlation-aware (fundamental signal + correlation regime for direction)

    # Ungated signal-based entries for comparison
    processor.add_entries(base_signal)
    processor.add_entries(base_confirm)
    processor.add_entries(base_divergence)

    processor.add_entries(corr_aware)

    # Multi-horizon and lagged entries
    processor.add_entries(multi_horizon)
    processor.add_entries(corr_aware_lagged)

    processor.add_position_filters(["long_short", "long_only"])

    # =========================================================================
    # Define exit rules
    # =========================================================================

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

    # =========================================================================
    # Run grid search
    # =========================================================================
    summary_df, results = processor.run(
        optimize_by="sharpe_ratio",
    )

    # Tag results with visible_col for cross-comparison
    summary_df = summary_df.with_columns(
        pl.lit(visible_col).alias("visible_col"),
    )

    return summary_df, results, processor


def run_all_visible_cols(
    ticker: str,
    signal_method: str = "stl_p4_s7_robustTrue",
    start_date: date | None = date(2018, 1, 1),
    end_date: date | None = None,
    debug: bool = True,
) -> tuple[pl.DataFrame, dict[str, list[GridSearchResult]], StrategyProcessor]:
    """Run grid search across all available visible_col variants.

    Returns combined summary, per-visible_col results, and last processor
    (for buy-and-hold comparison — market data is the same for all variants).
    """
    available = list_visible_cols(ticker, method=signal_method)
    if not available:
        raise ValueError(
            f"No visible_col variants found for {ticker} / {signal_method}"
        )

    print(f"Found {len(available)} visible_col variants: {available}")

    all_summaries: list[pl.DataFrame] = []
    all_results: dict[str, list[GridSearchResult]] = {}
    last_processor: StrategyProcessor | None = None

    for vc in available:
        print(f"\n{'─' * 60}")
        print(f"Running grid search: visible_col={vc}")
        print(f"{'─' * 60}")

        summary_df, results, processor = run_grid_search(
            ticker=ticker,
            visible_col=vc,
            signal_method=signal_method,
            start_date=start_date,
            end_date=end_date,
            debug=debug,
        )
        all_summaries.append(summary_df)
        all_results[vc] = results
        last_processor = processor

    assert last_processor is not None
    combined = pl.concat(all_summaries, how="diagonal_relaxed")

    return combined, all_results, last_processor


def print_visible_col_comparison(combined_df: pl.DataFrame) -> None:
    """Print per-visible_col performance summary."""
    print("\n" + "=" * 70)
    print("VISIBLE COLUMN COMPARISON")
    print("=" * 70)

    comparison = (
        combined_df.filter(pl.col("trade_n_trades") >= 5)
        .group_by("visible_col")
        .agg(
            pl.col("sharpe_ratio").mean().alias("mean_sharpe"),
            pl.col("sharpe_ratio").max().alias("max_sharpe"),
            pl.col("trade_total_return").mean().alias("mean_return"),
            pl.col("trade_total_return").max().alias("max_return"),
            pl.col("trade_n_trades").mean().alias("mean_trades"),
            pl.len().alias("n_strategies"),
        )
        .sort("mean_sharpe", descending=True)
    )
    display(comparison)

    # Top 5 per visible_col
    for vc in combined_df["visible_col"].unique().sort().to_list():
        subset = combined_df.filter(
            (pl.col("visible_col") == vc) & (pl.col("trade_n_trades") >= 5)
        ).sort("sharpe_ratio", descending=True)
        print(f"\n  Top 5 for visible_col={vc}:")
        for row in subset.head(5).iter_rows(named=True):
            print(
                f"    {row['entry_name']} × {row['exit_name']}: "
                f"sharpe={row['sharpe_ratio']:.3f}  "
                f"return={row['trade_total_return']:.1%}  "
                f"trades={row['trade_n_trades']}"
            )


def main(ticker: str = "DE") -> None:
    pl.Config.set_tbl_cols(12)
    pl.Config.set_tbl_rows(20)

    print(f"\n{'=' * 60}")
    print(f"Strategy Grid Search: {ticker}")
    print(f"{'=' * 60}\n")

    combined_df, all_results, processor = run_all_visible_cols(
        ticker=ticker,
        start_date=date(2015, 1, 1),
        debug=True,
    )

    # =========================================================================
    # Cross-visible_col comparison
    # =========================================================================
    print_visible_col_comparison(combined_df)

    # =========================================================================
    # Overall top results (across all visible_cols)
    # =========================================================================
    print("\n📊 Top 10 Strategies by Sharpe Ratio (all visible_cols):\n")
    display(combined_df.sort("sharpe_ratio", descending=True).head(10))

    print("\n📊 Top 10 Strategies by Total Return (all visible_cols):\n")
    by_return = combined_df.sort("trade_total_return", descending=True)
    display(by_return.head(10))

    # Entry type comparison
    print("\n📊 Entry Type Performance:")
    display(compare_entry_types(combined_df))

    # Corr-aware variant comparison
    if combined_df.filter(pl.col("entry_name").str.contains("corr_aware")).height > 0:
        print("\n📊 Correlation-Aware Variant Performance:")
        display(
            compare_entry_types(
                combined_df.filter(pl.col("entry_name").str.contains("corr_aware"))
            )
        )

    # Use the best visible_col's results for detailed analysis
    best_vc = (
        combined_df.filter(pl.col("trade_n_trades") >= 5)
        .group_by("visible_col")
        .agg(pl.col("sharpe_ratio").max().alias("best_sharpe"))
        .sort("best_sharpe", descending=True)
        .row(0)[0]
    )
    print(f"\n⭐ Best visible_col: {best_vc}")
    best_results = all_results[best_vc]

    # Analyze top strategies from the best visible_col
    best_summary = combined_df.filter(pl.col("visible_col") == best_vc)
    print("\n" + "=" * 60)
    print(f"DETAILED TRADE ANALYSIS (visible_col={best_vc})")
    print("=" * 60)
    analyze_best_strategies(
        GridSearchResults(best_results), processor, best_summary, top_n=5
    )

    # Direct comparison: best momentum vs best corr_aware (across all visible_cols)
    all_flat = [r for rs in all_results.values() for r in rs]
    print("\n" + "=" * 60)
    print("HEAD-TO-HEAD: BEST MOMENTUM vs BEST CORRELATION-AWARE")
    print("=" * 60)

    best_momentum = next(
        (
            r
            for r in all_flat
            if "momentum" in r.entry_rule.name and r.trade_log.total_return > 0
        ),
        None,
    )
    best_corr = next(
        (
            r
            for r in all_flat
            if "corr_aware" in r.entry_rule.name and r.trade_log.total_return > 0
        ),
        None,
    )

    if best_momentum and best_corr:
        for label, r in [("MOMENTUM", best_momentum), ("CORR-AWARE", best_corr)]:
            print(f"\n  {label}: {r.entry_rule.name} × {r.exit_rule.name}")
            print(f"    Sharpe: {r.metrics.risk.sharpe_ratio:.3f}")
            print(f"    Total Return: {r.trade_log.total_return:.1%}")
            print(f"    Trades: {r.trade_log.n_trades}")
            print(f"    Win Rate: {r.trade_log.win_rate:.1%}")
            print(f"    Avg Return: {r.trade_log.avg_return:.4f}")
            print(f"    Max DD: {r.metrics.risk.max_drawdown:.1%}")
            print(f"    Avg Holding: {r.trade_log.avg_holding_days:.1f} days")

    # Save results (best visible_col)
    save_results(
        ticker=ticker,
        summary_df=best_summary,
        results=best_results,
        processor=processor,
        output_dir="results",
        top_n=5,
    )


if __name__ == "__main__":
    from pyinstrument import Profiler

    profiler = Profiler(interval=0.01)
    profiler.reset()
    profiler.start()

    parser = argparse.ArgumentParser(
        description="Run correlation-aware strategy grid search"
    )
    parser.add_argument(
        "--ticker", type=str, default="DE", help="Stock ticker symbol (default: DE)"
    )
    args = parser.parse_args()
    main(ticker=args.ticker)

    profiler.stop()
    profiler.open_in_browser()
