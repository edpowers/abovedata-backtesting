from pprint import pprint

import polars as pl
from IPython.display import display

from abovedata_backtesting.processors.strategy_processor import (
    GridSearchResults,
    StrategyProcessor,
)
from abovedata_backtesting.trades.robustness_tests import (
    RobustnessValidator,
)
from abovedata_backtesting.trades.trade_analyzer import (
    TradeAnalyzer,
)


def analyze_best_strategies(
    grid_search_results: GridSearchResults,
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

    for ranking, result in grid_search_results.top_results_queued():
        label = "📈 TOP BY SHARPE" if ranking == "sharpe" else "💰 TOP BY TOTAL RETURN"
        print(f"\n{'=' * 70}")
        print(f"{label}: {result.entry_rule.name} × {result.exit_rule.name}")
        print(f"{'=' * 70}")

        analysis = analyzer.analyze(result.trade_log, processor._market_data)
        summary = analysis.full_summary()

        pprint(map(lambda x: round(x, 2) if isinstance(x, float) else x, summary))

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
        print(f"\n  All {trades_df.height} Trades:")
        display(trades_df)

        # Robustness validation for suspicious results
        if result.trade_log.win_rate > 0.9 or result.metrics.risk.sharpe_ratio > 0.5:
            validator = RobustnessValidator(
                processor=processor,
                result=result,
                trade_analysis=analysis,
                buy_hold_return=processor.get_buy_hold_return(
                    start_date=analysis.min_date,
                    end_date=analysis.max_date,
                ),
                n_random_trials=100,
            )
            print(validator.run_all().summary())


def compare_entry_types(
    summary_df: pl.DataFrame,
    group_by: str = "entry_entry_type",
    sort_by: str = "avg_sharpe",
) -> pl.DataFrame:
    """Compare performance across entry types."""
    return (
        summary_df.group_by(group_by)
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
        .sort(sort_by, descending=True)
    )
