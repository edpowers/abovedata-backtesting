"""Save the trade results."""

import datetime
import json
import shutil
from pathlib import Path
from typing import Any

import polars as pl
from pydantic import BaseModel, computed_field

from abovedata_backtesting.processors.benchmark_processor import buy_and_hold_from_data
from abovedata_backtesting.trades.report_generator import StrategyReport
from abovedata_backtesting.trades.trade_analyzer import TradeAnalyzer


def _sanitize(obj: Any) -> Any:
    """Convert non-JSON-serializable values (inf, nan)."""
    if isinstance(obj, float):
        if obj != obj:  # NaN
            return None
        if obj == float("inf") or obj == float("-inf"):
            return str(obj)
        return obj
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj


def save_json(path: Path, data: list[dict[str, Any]] | dict[str, Any]) -> None:
    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with open(path, "w") as f:
        json.dump(_sanitize(data), f, indent=2, default=str)


class TradeSummaryPaths(BaseModel):
    ticker: str
    output_dir: Path

    @computed_field
    @property
    def ts(self) -> str:
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    @computed_field
    @property
    def run_dir(self) -> Path:
        return self.output_dir.joinpath(f"ticker={self.ticker}", f"time={self.ts}")

    @computed_field
    @property
    def latest_dir(self) -> Path:
        return self.output_dir.joinpath(f"ticker={self.ticker}", "time=latest")

    def write_dataframe(self, df: pl.DataFrame, path: Path) -> None:
        df.write_parquet(path.with_suffix(".parquet"), mkdir=True)
        df.write_csv(path.with_suffix(".csv"))


def save_results(
    ticker: str,
    summary_df: pl.DataFrame,
    results: list[Any],
    processor: Any,
    output_dir: str | Path = "results",
    top_n: int = 10,
) -> Path:
    """
    Save grid search results to disk for later analysis.

    Outputs
    -------
    {output_dir}/{ticker}_{timestamp}/
        summary.parquet          — full grid summary (all combos)
        trades_by_strategy/      — per-strategy trade-level parquet files
            {strategy_name}.parquet
        top_strategy/            — best strategy by total return (detailed)
            trades.parquet
            trades.csv
            metadata.json
        metadata.json            — run config, timestamps, top strategies
    """
    trade_summary_paths = TradeSummaryPaths(ticker=ticker, output_dir=Path(output_dir))
    top_dir = trade_summary_paths.run_dir / "top_strategy"
    if trade_summary_paths.latest_dir.exists():
        shutil.rmtree(trade_summary_paths.latest_dir)

    # 1. Summary parquet — the full grid
    summary_df.write_parquet(
        trade_summary_paths.run_dir / "summary.parquet", mkdir=True
    )

    # Buy-and-hold (same ticker) via benchmark processor for comparison
    buy_hold_result = None
    if processor._market_data is not None:
        buy_hold_result = buy_and_hold_from_data(
            processor._market_data,
            processor._benchmark_data,
            ticker=ticker,
            benchmark_ticker=getattr(processor, "benchmark_ticker", "SPY"),
        )
    buy_hold = {}
    if buy_hold_result is not None:
        buy_hold = {
            "buy_hold_total_return": buy_hold_result.metrics.returns.total_return,
            "buy_hold_annualized_return": buy_hold_result.metrics.returns.annualized_return,
        }

    # 2. Per-strategy trade-level analysis for top strategies
    analyzer = TradeAnalyzer(
        signals=processor.signals,
        benchmark_data=processor._benchmark_data,
        visible_col=processor.visible_col,
    )

    # Top N by Sharpe + top N by total return (deduped)
    by_sharpe = summary_df.sort("sharpe_ratio", descending=True).head(top_n)
    by_return = summary_df.sort("trade_total_return", descending=True).head(top_n)

    top_names: set[str] = set()
    for df_slice in [by_sharpe, by_return]:
        for row in df_slice.iter_rows(named=True):
            top_names.add(f"{row['entry_name']} × {row['exit_name']}")

    strategy_summaries: list[dict[str, Any]] = []
    best_result: tuple[float, Any, dict[str, Any], pl.DataFrame] | None = None

    for result in results:
        key = f"{result.entry_rule.name} × {result.exit_rule.name}"
        if key not in top_names:
            continue

        analysis = analyzer.analyze(result.trade_log, processor._market_data)
        full = analysis.full_summary()

        # Trade-level DataFrame
        trades_df = analysis.to_dataframe()
        safe_name = key.replace(" × ", "__").replace("/", "_").replace("%", "pct")
        strat_name_dir = (
            trade_summary_paths.run_dir / "trades_by_strategy" / f"name={safe_name}"
        )
        trade_summary_paths.write_dataframe(
            trades_df,
            strat_name_dir / safe_name,
        )

        # Strategy-level summary for metadata
        strat_summary = {
            "name": key,
            "entry": result.entry_rule.name,
            "exit": result.exit_rule.name,
            "entry_params": result.entry_params,
            "exit_params": result.exit_params,
            "sharpe": result.metrics.risk.sharpe_ratio,
            "total_return": result.trade_log.total_return,
            "annualized_return": result.metrics.returns.annualized_return,
            "max_drawdown": result.metrics.risk.max_drawdown,
            "n_trades": full["n_trades"],
            "win_rate": full["win_rate"],
            "signal_accuracy": full["signal_accuracy"],
            "direction_accuracy": full["direction_accuracy"],
            "skill_ratio": full["skill_ratio"],
            "hhi": full["hhi"],
            "top1_pct": full["top1_pct"],
            "top3_pct": full["top3_pct"],
            "return_ex_top1": full["return_ex_top1"],
            "return_ex_top3": full["return_ex_top3"],
            "profit_factor": full["profit_factor"],
            "expectancy": full["expectancy"],
            "tail_ratio": full["tail_ratio"],
            "max_single_contribution": full["max_single_contribution"],
            **buy_hold,
        }
        strategy_summaries.append(strat_summary)

        # Track best by total return
        total_ret = result.trade_log.total_return
        if best_result is None or total_ret > best_result[0]:
            best_result = (total_ret, result, strat_summary, trades_df)

        report = StrategyReport(
            metadata=strat_summary, trades_df=trades_df, ticker=ticker
        )
        report.write(strat_name_dir / "README.md")

    # 3. Top strategy folder — best by total return with full detail
    if best_result is not None:
        _, _, best_summary, best_trades = best_result

        trade_summary_paths.write_dataframe(best_trades, top_dir / "trades")
        save_json(top_dir / "metadata.json", best_summary)

        print(f"\n⭐ Top strategy: {best_summary['name']}")
        print(
            f"   Total Return: {best_summary['total_return']:.1%}  |  "
            f"Sharpe: {best_summary['sharpe']:.3f}  |  "
            f"Trades: {best_summary['n_trades']}  |  "
            f"HHI: {best_summary['hhi']:.4f}"
        )
        if buy_hold:
            bh_total = buy_hold["buy_hold_total_return"]
            bh_ann = buy_hold["buy_hold_annualized_return"]
            print(
                f"   Buy & Hold ({ticker}): {bh_total:.1%} total  |  {bh_ann:.1%} ann.  |  "
                f"Strategy alpha: {(best_summary['total_return'] - bh_total):.1%} total"
            )
        report = StrategyReport(
            metadata=best_summary, trades_df=best_trades, ticker=ticker
        )
        report.write(top_dir / "README.md")

    # 4. Metadata JSON
    metadata = {
        "ticker": ticker,
        "timestamp": trade_summary_paths.ts,
        "total_strategies": summary_df.height,
        "top_strategies_saved": len(strategy_summaries),
        "strategies": strategy_summaries,
        **buy_hold,
    }

    save_json(trade_summary_paths.run_dir / "metadata.json", metadata)

    print(f"\n💾 Results saved to: {trade_summary_paths.run_dir}")
    print(f"   summary.parquet: {summary_df.height} strategies")
    print(f"   trades_by_strategy/: {len(strategy_summaries)} strategy trade logs")
    print("   metadata.json: run config + top strategy summaries")

    # Then copy over all files from the run_dir to the latest:
    shutil.copytree(
        trade_summary_paths.run_dir, trade_summary_paths.latest_dir, dirs_exist_ok=True
    )

    return trade_summary_paths.run_dir
