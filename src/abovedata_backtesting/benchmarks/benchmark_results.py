from dataclasses import dataclass, field
from typing import Iterator

import polars as pl

from abovedata_backtesting.model.metrics import (
    BacktestMetrics,
)

# =============================================================================
# Benchmark Result
# =============================================================================


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    """Result for a single benchmark strategy."""

    strategy_name: str
    ticker: str
    metrics: BacktestMetrics
    daily_returns: pl.DataFrame  # date, close, return, position, strategy_return

    @property
    def sharpe(self) -> float:
        return self.metrics.risk.sharpe_ratio

    @property
    def total_return(self) -> float:
        return self.metrics.returns.total_return

    def to_row(self) -> dict[str, float | str | int | None]:
        """Flatten to dict for DataFrame conversion."""
        m = self.metrics
        return {
            "strategy": self.strategy_name,
            "ticker": self.ticker,
            "total_return": m.returns.total_return,
            "annualized_return": m.returns.annualized_return,
            "sharpe_ratio": m.risk.sharpe_ratio,
            "sortino_ratio": m.risk.sortino_ratio,
            "max_drawdown": m.risk.max_drawdown,
            "win_rate": m.risk.win_rate,
            "volatility": m.risk.annualized_volatility,
            "time_in_market": m.exposure.time_in_market,
            "n_periods": m.returns.n_periods,
        }


@dataclass
class BenchmarkResults:
    """Container for all benchmark results."""

    _results: dict[str, BenchmarkResult] = field(default_factory=dict)

    def __iter__(self) -> Iterator[BenchmarkResult]:
        return iter(self._results.values())

    def __len__(self) -> int:
        return len(self._results)

    def __getitem__(self, key: str) -> BenchmarkResult:
        return self._results[key]

    def add(self, result: BenchmarkResult) -> None:
        self._results[result.strategy_name] = result

    def get(self, name: str) -> BenchmarkResult | None:
        return self._results.get(name)

    def to_dataframe(self) -> pl.DataFrame:
        """Convert all results to a sorted DataFrame."""
        if not self._results:
            return pl.DataFrame()
        rows = [r.to_row() for r in self._results.values()]
        return pl.DataFrame(rows).sort("sharpe_ratio", descending=True)

    def compare_strategy(
        self,
        strategy_sharpe: float,
        strategy_return: float,
    ) -> pl.DataFrame:
        """
        Compare a strategy against all benchmarks.

        Returns DataFrame with benchmark stats + comparison columns.
        """
        df = self.to_dataframe()
        if df.is_empty():
            return df

        return df.with_columns(
            pl.lit(strategy_sharpe).alias("strategy_sharpe"),
            pl.lit(strategy_return).alias("strategy_return"),
            (pl.lit(strategy_sharpe) - pl.col("sharpe_ratio")).alias("sharpe_alpha"),
            (pl.lit(strategy_return) - pl.col("total_return")).alias("return_alpha"),
            (pl.lit(strategy_sharpe) > pl.col("sharpe_ratio")).alias("beats_benchmark"),
        )
