"""Save the trade results."""

import datetime
import json
import shutil
from pathlib import Path
from typing import Any

import polars as pl
from pydantic import BaseModel, computed_field

from abovedata_backtesting.processors.strategy_processor import (
    GridSearchResult,
)
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


def print_top_summary(best_result: dict[str, Any], ticker: str) -> None:
    best_summary = best_result["strat_summary"]
    print(f"\n⭐ Top strategy: {best_summary['name']}")
    print(
        f"   Total Return: {best_summary['total_return']:.1%}  |  "
        f"Sharpe: {best_summary['sharpe']:.3f}  |  "
        f"Trades: {best_summary['n_trades']}  |  "
        f"HHI: {best_summary['hhi']:.4f}"
    )
    bh_total = best_summary["buy_hold_total_return"]
    bh_ann = best_summary["buy_hold_annualized_return"]
    print(
        f"   Buy & Hold ({ticker}): {bh_total:.1%} total  |  {bh_ann:.1%} ann.  |  "
        f"Strategy alpha: {(best_summary['total_return'] - bh_total):.1%} total"
    )


def save_json(path: Path, data: list[dict[str, Any]] | dict[str, Any]) -> None:
    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with open(path, "w") as f:
        json.dump(_sanitize(data), f, indent=2, default=str)


class TradeSummaryPaths(BaseModel):
    ticker: str
    output_dir: Path
    strategy_summaries: list[Any]
    summary_df: pl.DataFrame

    class Config:
        arbitrary_types_allowed = True

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

    @computed_field
    @property
    def top_dir(self) -> Path:
        return self.run_dir / "top_strategy"

    def write_dataframe(self, df: pl.DataFrame, path: Path) -> None:
        df.write_parquet(path.with_suffix(".parquet"), mkdir=True)
        df.write_csv(path.with_suffix(".csv"))

    def save_metadata(self, buy_hold: dict[str, Any]) -> None:
        save_json(
            self.run_dir / "metadata.json",
            {
                "ticker": self.ticker,
                "timestamp": self.ts,
                "total_strategies": self.summary_df.height,
                "top_strategies_saved": len(self.strategy_summaries),
                "strategies": self.strategy_summaries,
                **buy_hold,
            },
        )

    def print_summary(self) -> None:
        print(f"\n💾 Results saved to: {self.run_dir}")
        print(f"   summary.parquet: {self.summary_df.height} strategies")
        print(
            f"   trades_by_strategy/: {len(self.strategy_summaries)} strategy trade logs"
        )
        print("   metadata.json: run config + top strategy summaries")

    def copy_to_latest(self) -> None:
        # Then copy over all files from the run_dir to the latest:
        shutil.copytree(
            self.run_dir,
            self.latest_dir,
            dirs_exist_ok=True,
        )

    def get_top_names(self, top_n: int) -> set[str]:
        # Top N by Sharpe + top N by total return (deduped)
        by_sharpe = self.summary_df.sort("sharpe_ratio", descending=True).head(top_n)
        by_return = self.summary_df.sort("trade_total_return", descending=True).head(
            top_n
        )

        top_names: set[str] = set()
        for df_slice in [by_sharpe, by_return]:
            for row in df_slice.iter_rows(named=True):
                top_names.add(f"{row['entry_name']} × {row['exit_name']}")

        return top_names

    def write_trade_summary(self) -> None:
        self.summary_df.write_parquet(self.run_dir / "summary.parquet", mkdir=True)


def save_results(
    ticker: str,
    summary_df: pl.DataFrame,
    results: list[GridSearchResult],
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
    trade_summary_paths = TradeSummaryPaths(
        ticker=ticker,
        output_dir=Path(output_dir),
        strategy_summaries=[],
        summary_df=summary_df,
    )

    if trade_summary_paths.latest_dir.exists():
        shutil.rmtree(trade_summary_paths.latest_dir)

    # 1. Summary parquet — the full grid
    trade_summary_paths.write_trade_summary()

    # 2. Per-strategy trade-level analysis for top strategies
    analyzer = TradeAnalyzer(
        signals=processor.signals,
        benchmark_data=processor._benchmark_data,
        visible_col=processor.visible_col,
    )
    top_names = trade_summary_paths.get_top_names(top_n)

    strategy_summaries: list[dict[str, Any]] = []
    buy_hold: dict[str, Any] = {}

    for result in results:
        key = result.make_key()
        if key not in top_names:
            continue

        analysis = analyzer.analyze(result.trade_log, processor._market_data)
        trades_df = analysis.to_dataframe()

        strat_name_dir = (
            trade_summary_paths.run_dir
            / "trades_by_strategy"
            / f"name={result.make_safe_name()}"
        )

        trade_summary_paths.write_dataframe(
            trades_df,
            strat_name_dir / result.make_safe_name(),
        )
        # Strategy-level summary for metadata
        strat_summary = {
            "name": key,
            "trades_df": trades_df,
            "strat_summary": result.summarize()
            | analysis.full_summary()
            | processor.get_buy_hold_return_dict(
                start_date=trades_df["entry_date"].dt.min(),
                end_date=trades_df["exit_date"].dt.max(),
            )
            | {"name": key},
        }
        strategy_summaries.append(strat_summary)

        StrategyReport(
            metadata=strat_summary["strat_summary"],  # type: ignore
            trades_df=analysis.to_dataframe(),
            ticker=ticker,
        ).write(strat_name_dir / "README.md")

    best_result = max(
        strategy_summaries, key=lambda x: x["strat_summary"]["total_return"]
    )

    # 3. Top strategy folder — best by total return with full detail
    trade_summary_paths.write_dataframe(
        best_result["trades_df"], trade_summary_paths.top_dir / "trades"
    )
    save_json(
        trade_summary_paths.top_dir / "metadata.json", best_result["strat_summary"]
    )

    StrategyReport(
        metadata=best_result["strat_summary"],
        trades_df=best_result["trades_df"],
        ticker=ticker,
    ).write(trade_summary_paths.top_dir / "README.md")

    print_top_summary(best_result, ticker)

    # 4. Metadata JSON
    trade_summary_paths.strategy_summaries = strategy_summaries
    trade_summary_paths.save_metadata(buy_hold)
    trade_summary_paths.copy_to_latest()

    return trade_summary_paths.run_dir
