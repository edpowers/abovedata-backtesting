"""Strategy grid search using raw STL processor output.

Compares three entry approaches:
1. Momentum (price-only baseline)
2. Correlation-aware (fundamental signal + correlation regime for direction)
3. Signal-based (threshold, confirmation, divergence)

Uses raw STL output with contemp_corr_historical, leading_corr_historical,
confidence scores, and regime shift detection.
"""

import argparse
from datetime import date

import polars as pl
from IPython.display import display

from abovedata_backtesting.data_loaders.load_signal_data import load_signal_data
from abovedata_backtesting.entries.correlation_aware_entry import CorrelationAwareEntry
from abovedata_backtesting.entries.entry_signals import (
    DivergenceEntry,
    MomentumEntry,
    SignalMomentumEntry,
    SignalThresholdEntry,
)
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
    signal_method: str = "stl_p4_s7_robustTrue",
    start_date: date | None = date(2018, 1, 1),
    end_date: date | None = None,
    debug: bool = True,
) -> tuple[pl.DataFrame, list[GridSearchResult], StrategyProcessor]:
    """
    Run grid search with correlation-gated entry rules.

    Uses raw STL processor output (not df_fc_joined) so we have access
    to contemp_corr_historical, leading_corr_historical, regime shifts, etc.
    """
    # Load RAW STL processor output (not the joined/renamed version)
    signals = load_signal_data(ticker, method=signal_method, name="processed_data")

    visible_col = None
    for visible_col in ["visible_revenue", "total_universe"]:
        if visible_col in signals:
            break

    if not visible_col:
        raise ValueError("need a valid visible col")

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
    entry_days_before = [0, 1, 5, 15, 20, 30]

    base_momentum = MomentumEntry.grid(
        lookback_days=[10, 20],
        zscore_threshold=[0.5, 1.0, 1.5],
        entry_days_before=entry_days_before,
    )

    base_signal = SignalThresholdEntry.grid(
        signal_col=[f"{visible_col}_resid"],
        long_threshold=[0.3, 0.5, 1.0],
        short_threshold=[-0.3, -0.5, -1.0],
        entry_days_before=entry_days_before,
        confidence_col=["contemp", "leading"],
    )

    base_confirm = SignalMomentumEntry.grid(
        signal_col=[f"{visible_col}_resid"],
        signal_threshold=[0.0, 0.3, 0.5],
        lookback_days=[10, 20],
        momentum_zscore_threshold=[0.3, 0.5],
        entry_days_before=entry_days_before,
    )

    base_divergence = DivergenceEntry.grid(
        signal_col=[f"{visible_col}_resid"],
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
        signal_col=[f"{visible_col}_resid"],
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

    return summary_df, results, processor


def main(ticker: str = "DE") -> None:
    pl.Config.set_tbl_cols(12)
    pl.Config.set_tbl_rows(20)

    print(f"\n{'=' * 60}")
    print(f"Strategy Grid Search: {ticker}")
    print(f"{'=' * 60}\n")

    summary_df, results, processor = run_grid_search(
        ticker=ticker,
        start_date=date(2015, 1, 1),
        debug=True,
    )

    # Top 10 by Sharpe
    print("\n📊 Top 10 Strategies by Sharpe Ratio:\n")
    display(summary_df.head(10))

    # Top 10 by total return
    print("\n📊 Top 10 Strategies by Total Return:\n")
    by_return = summary_df.sort("trade_total_return", descending=True)
    display(by_return.head(10))

    # Entry type comparison
    print("\n📊 Entry Type Performance:")
    display(compare_entry_types(summary_df))

    # Corr-aware variant comparison
    print("\n📊 Correlation-Aware Variant Performance:")
    display(
        compare_entry_types(
            summary_df.filter(pl.col("entry_entry_type") == "correlation_aware")
        )
    )
    # Analyze top strategies
    print("\n" + "=" * 60)
    print("DETAILED TRADE ANALYSIS")
    print("=" * 60)
    analyze_best_strategies(GridSearchResults(results), processor, summary_df, top_n=5)

    # Direct comparison: best momentum vs best corr_aware
    print("\n" + "=" * 60)
    print("HEAD-TO-HEAD: BEST MOMENTUM vs BEST CORRELATION-AWARE")
    print("=" * 60)

    # best_momentum =

    best_momentum = next(
        (
            r
            for r in results
            if "momentum" in r.entry_rule.name and r.trade_log.total_return > 0
        ),
        None,
    )
    best_corr = next(
        (
            r
            for r in results
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

    # Save results
    save_results(
        ticker=ticker,
        summary_df=summary_df,
        results=results,
        processor=processor,
        output_dir="results",
        top_n=5,
    )


if __name__ == "__main__":
    # from pyinstrument import Profiler

    # profiler = Profiler(interval=0.01)
    # profiler.reset()
    # profiler.start()

    parser = argparse.ArgumentParser(
        description="Run correlation-aware strategy grid search"
    )
    parser.add_argument(
        "--ticker", type=str, default="DE", help="Stock ticker symbol (default: DE)"
    )
    args = parser.parse_args()
    main(ticker=args.ticker)

    # profiler.stop()
    # profiler.open_in_browser()
