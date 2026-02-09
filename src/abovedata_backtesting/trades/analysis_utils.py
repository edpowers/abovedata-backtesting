from typing import Any

import polars as pl
from IPython.display import display

from abovedata_backtesting.processors.strategy_processor import (
    GridSearchResult,
    StrategyProcessor,
)
from abovedata_backtesting.trades.trade_analyzer import (
    TradeAnalyzer,
)


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
        visible_col=processor.visible_col,
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


def compare_entry_types(summary_df: pl.DataFrame) -> pl.DataFrame:
    """Compare performance across entry types."""
    return (
        summary_df.group_by("entry_entry_type")
        .agg(
            pl.len().alias("count"),
            pl.col("sharpe_ratio").mean().alias("avg_sharpe"),
            pl.col("sharpe_ratio").max().alias("max_sharpe"),
            pl.col("sharpe_ratio").median().alias("median_sharpe"),
            pl.col("trade_n_trades").mean().alias("avg_trades"),
            pl.col("trade_win_rate").mean().alias("avg_win_rate"),
            pl.col("trade_total_return").mean().alias("avg_total_return"),
            pl.col("trade_total_return").max().alias("max_total_return"),
            pl.col("annualized_return").mean().alias("avg_ann_return"),
        )
        .sort("avg_sharpe", descending=True)
    )


def compare_corr_aware_variants(summary_df: pl.DataFrame) -> pl.DataFrame:
    """Compare corr_aware variants by corr_col type."""
    corr = summary_df.filter(pl.col("entry_entry_type") == "correlation_aware")
    if corr.is_empty():
        return pl.DataFrame({"note": ["No correlation_aware entries found"]})

    corr_col = "entry_corr_col"
    if corr_col not in corr.columns:
        return corr

    return (
        corr.group_by(corr_col)
        .agg(
            pl.len().alias("count"),
            pl.col("sharpe_ratio").mean().alias("avg_sharpe"),
            pl.col("sharpe_ratio").max().alias("max_sharpe"),
            pl.col("trade_n_trades").mean().alias("avg_trades"),
            pl.col("trade_win_rate").mean().alias("avg_win_rate"),
            pl.col("trade_total_return").max().alias("max_total_return"),
        )
        .sort("avg_sharpe", descending=True)
    )
