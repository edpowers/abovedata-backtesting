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
from typing import Any

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
from abovedata_backtesting.processors.strategy_processor import (
    GridSearchResult,
    StrategyProcessor,
)
from abovedata_backtesting.trades.trade_analyzer import (
    TradeAnalyzer,
    compare_corr_aware_variants,
    compare_entry_types,
)
from abovedata_backtesting.trades.trade_save_results import save_results


def run_gated_grid_search(
    ticker: str = "DE",
    signal_method: str = "stl_p4_s7_robustTrue",
    start_date: date | None = date(2015, 1, 1),
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

    processor = StrategyProcessor(
        ticker=ticker,
        signals=signals,
        visible_col="visible_revenue",
        start_date=start_date,
        end_date=end_date,
        debug=debug,
    )

    # =========================================================================
    # Define base entry rules (ungated)
    # =========================================================================
    # THESE ARE TRADING DAYS, NOT CALENDAR DAYS.
    entry_days_before = [0, 1, 3, 5, 10, 15, 20, 25, 30]

    base_momentum = MomentumEntry.grid(
        lookback_days=[10, 20, 40],
        zscore_threshold=[0.5, 1.0, 1.5],
        entry_days_before=entry_days_before,
    )

    base_signal = SignalThresholdEntry.grid(
        signal_col=["visible_revenue_resid"],
        long_threshold=[0.3, 0.5, 1.0],
        short_threshold=[-0.3, -0.5, -1.0],
        entry_days_before=entry_days_before,
    )

    base_confirm = SignalMomentumEntry.grid(
        signal_col=["visible_revenue_resid"],
        signal_threshold=[0.3, 0.5],
        lookback_days=[10, 20],
        momentum_zscore_threshold=[0.3, 0.5],
        entry_days_before=entry_days_before,
    )

    base_divergence = DivergenceEntry.grid(
        signal_col=["visible_revenue_resid"],
        lookback_days=[20],
        divergence_zscore=[0.5, 1.0],
        fundamental_threshold=[0.5, 1.0],
        require_strong_divergence=[False, True],
        entry_days_before=entry_days_before,
    )

    # =========================================================================
    # Correlation-aware entries (use corr context for direction, not filtering)
    # =========================================================================

    corr_aware = CorrelationAwareEntry.grid(
        signal_col=["visible_revenue_resid"],
        corr_col=["contemp", "leading", "contemp_ma", "leading_ma"],
        min_signal_abs=[0.0, 0.1],
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
    processor.add_entries(corr_aware)

    # Ungated signal-based entries for comparison
    processor.add_entries(base_signal)
    processor.add_entries(base_confirm)
    processor.add_entries(base_divergence)

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
        exclude_suspicious=False,
    )

    return summary_df, results, processor


def analyze_best_strategies(
    results: list[GridSearchResult],
    processor: StrategyProcessor,
    summary_df: pl.DataFrame,
    top_n: int = 5,
) -> None:
    """Analyze top N by Sharpe and top N by total return, showing trades."""
    analyzer = TradeAnalyzer(
        signals=processor.signals,
        benchmark_data=processor._benchmark_data,
        visible_col="visible_revenue",
    )

    # Top by total return — re-sort
    return_sorted = sorted(
        [r for r in results if r.trade_log.n_trades >= 10],
        key=lambda r: r.trade_log.total_return,
        reverse=True,
    )

    # Merge unique (avoid analyzing same strategy twice)
    seen_names: set[str] = set()
    analysis_queue: list[tuple[str, Any]] = []

    # Top by Sharpe (already sorted)
    for r in results[:top_n]:
        key = f"{r.entry_rule.name} × {r.exit_rule.name}"
        if key not in seen_names:
            seen_names.add(key)
            analysis_queue.append(("sharpe", r))

    for r in return_sorted[:top_n]:
        key = f"{r.entry_rule.name} × {r.exit_rule.name}"
        if key not in seen_names:
            seen_names.add(key)
            analysis_queue.append(("total_return", r))

    for ranking, result in analysis_queue:
        label = "📈 TOP BY SHARPE" if ranking == "sharpe" else "💰 TOP BY TOTAL RETURN"
        print(f"\n{'=' * 70}")
        print(f"{label}: {result.entry_rule.name} × {result.exit_rule.name}")
        print(f"{'=' * 70}")

        analysis = analyzer.analyze(result.trade_log, processor._market_data)
        summary = analysis.full_summary()

        # Headline metrics
        sharpe = result.metrics.risk.sharpe_ratio
        total_ret = result.trade_log.total_return
        ann_ret = result.metrics.returns.annualized_return
        max_dd = result.metrics.risk.max_drawdown

        print(
            f"  Sharpe: {sharpe:.3f}  |  Total Return: {total_ret:.1%}  |  "
            f"Ann Return: {ann_ret:.1%}  |  Max DD: {max_dd:.1%}"
        )
        print(
            f"  Trades: {summary['n_trades']}  |  Win Rate: {summary['win_rate']:.1%}  |  "
            f"Direction Accuracy: {summary['direction_accuracy']:.1%}  |  "
            f"Signal Accuracy: {summary['signal_accuracy']:.1%}  |  "
            f"Skill Ratio: {summary['skill_ratio']:.1%}"
        )

        # Diversity metrics
        print("\n  📊 Diversity & Concentration:")
        print(
            f"    HHI: {summary['hhi']:.4f}  (1/{summary['n_trades']}="
            f"{1 / summary['n_trades']:.4f} = perfectly diverse)"
        )
        print(
            f"    Top-1 trade: {summary['top1_pct']:.1%} of gross profit  |  "
            f"Top-3: {summary['top3_pct']:.1%}  |  Top-5: {summary['top5_pct']:.1%}"
        )
        print(
            f"    Return ex-top-1: {summary['return_ex_top1']:.1%}  |  "
            f"ex-top-3: {summary['return_ex_top3']:.1%}"
        )
        print(f"    Max single trade: {summary['max_single_contribution']:.1%}")
        print(
            f"    Profit factor: {summary['profit_factor']:.2f}  |  "
            f"Expectancy: {summary['expectancy']:.4f}  |  "
            f"Tail ratio: {summary['tail_ratio']:.2f}"
        )
        print()

        # Outcome breakdown
        print("  Outcome Breakdown:")
        display(analysis.outcome_summary())

        # Regime breakdown
        print("  Correlation Regime:")
        display(analysis.regime_summary())

        # Trade list — show all trades with key fields
        trades_df = analysis.to_dataframe()
        trade_display_cols = [
            "entry_date",
            "exit_date",
            "direction",
            "holding_days",
            "trade_return",
            "signal_date",
            "signal_value",
            "correlation_regime",
            "signal_quality",
            "actual_beat_consensus",
            "signal_correct",
            "trade_direction_correct",
            "outcome",
            "benchmark_return",
            "alpha_contribution",
        ]
        available = [c for c in trade_display_cols if c in trades_df.columns]
        print(f"\n  All {trades_df.height} Trades:")
        display(trades_df.select(available))


def main(ticker: str = "DE") -> None:
    pl.Config.set_tbl_cols(12)
    pl.Config.set_tbl_rows(20)

    print(f"\n{'=' * 60}")
    print(f"Gated Strategy Grid Search: {ticker}")
    print(f"{'=' * 60}\n")

    summary_df, results, processor = run_gated_grid_search(
        ticker=ticker,
        start_date=date(2015, 1, 1),
        debug=True,
    )

    # Top 10 by Sharpe
    print("\n📊 Top 10 Strategies by Sharpe Ratio:\n")
    top_cols = [
        "entry_name",
        "exit_name",
        "sharpe_ratio",
        "annualized_return",
        "trade_n_trades",
        "trade_win_rate",
        "trade_total_return",
        "max_drawdown",
        "is_suspicious",
    ]
    display(
        summary_df.select([c for c in top_cols if c in summary_df.columns]).head(10)
    )

    # Top 10 by total return
    print("\n📊 Top 10 Strategies by Total Return:\n")
    by_return = summary_df.sort("trade_total_return", descending=True)
    display(by_return.select([c for c in top_cols if c in by_return.columns]).head(10))

    # Entry type comparison
    print("\n📊 Entry Type Performance:")
    display(compare_entry_types(summary_df))

    # Corr-aware variant comparison
    print("\n📊 Correlation-Aware Variant Performance:")
    display(compare_corr_aware_variants(summary_df))

    # Exit type comparison
    print("\n📊 Exit Type Performance:")
    exit_perf = (
        summary_df.group_by("exit_exit_type")
        .agg(
            pl.len().alias("count"),
            pl.col("sharpe_ratio").mean().alias("avg_sharpe"),
            pl.col("sharpe_ratio").max().alias("max_sharpe"),
        )
        .sort("avg_sharpe", descending=True)
    )
    display(exit_perf)

    # Analyze top strategies
    print("\n" + "=" * 60)
    print("DETAILED TRADE ANALYSIS")
    print("=" * 60)
    analyze_best_strategies(results, processor, summary_df, top_n=5)

    # Direct comparison: best momentum vs best corr_aware
    print("\n" + "=" * 60)
    print("HEAD-TO-HEAD: BEST MOMENTUM vs BEST CORRELATION-AWARE")
    print("=" * 60)

    best_momentum = next(
        (
            r
            for r in results
            if "momentum" in r.entry_rule.name and "gated" not in r.entry_rule.name
        ),
        None,
    )
    best_corr = next(
        (r for r in results if "corr_aware" in r.entry_rule.name),
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
    parser = argparse.ArgumentParser(description="Run correlation-aware strategy grid search")
    parser.add_argument("--ticker", type=str, default="DE", help="Stock ticker symbol (default: DE)")
    args = parser.parse_args()
    main(ticker=args.ticker)
