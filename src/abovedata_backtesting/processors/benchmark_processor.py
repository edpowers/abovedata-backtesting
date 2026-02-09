from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

import polars as pl

from abovedata_backtesting.benchmarks.benchmark_models import (
    Strategy,
    create_benchmark_strategies,
)
from abovedata_backtesting.benchmarks.benchmark_results import (
    BenchmarkResult,
    BenchmarkResults,
)
from abovedata_backtesting.data_loaders.load_market_data import MarketDataLoaders
from abovedata_backtesting.model.metrics import BacktestMetrics

# =============================================================================
# Configuration
# =============================================================================


@dataclass(frozen=True, slots=True)
class BenchmarkConfig:
    """Configuration for benchmark processing."""

    tickers: tuple[str, ...]
    strategies: tuple[Strategy, ...] | None = None
    signal_col: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    benchmark_ticker: str = "SPY"
    trade_probability: float = 0.3
    seed: int = 42

    @classmethod
    def for_ticker(
        cls,
        ticker: str,
        signal_col: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        benchmark_ticker: str = "SPY",
    ) -> BenchmarkConfig:
        return cls(
            tickers=(ticker,),
            signal_col=signal_col,
            start_date=start_date,
            end_date=end_date,
            benchmark_ticker=benchmark_ticker,
        )


# =============================================================================
# Benchmark Processor
# =============================================================================


@dataclass
class BenchmarkProcessor:
    """
    Processes benchmark strategies and produces BenchmarkResults.

    Run once, then pass results to StrategyProcessor for comparison.

    Usage
    -----
    >>> config = BenchmarkConfig.for_ticker("DE", signal_col="visible_revenue")
    >>> benchmarks = BenchmarkProcessor(config).run()
    >>> processor = StrategyProcessor(ticker="DE", benchmarks=benchmarks, ...)
    """

    config: BenchmarkConfig
    _market_data: dict[str, pl.DataFrame] = field(default_factory=dict, init=False)
    _results: BenchmarkResults = field(default_factory=BenchmarkResults, init=False)

    def run(self) -> BenchmarkResults:
        """Execute benchmark processing pipeline."""
        self._load_market_data()
        self._build_and_evaluate_strategies()
        return self._results

    def _load_market_data(self) -> None:
        """Load market data for all required tickers (including benchmark)."""
        all_tickers = set(self.config.tickers)
        all_tickers.add(self.config.benchmark_ticker)

        loaders = MarketDataLoaders.for_tickers(
            tickers=list(all_tickers),
            benchmark_ticker=self.config.benchmark_ticker,
            start_date=self.config.start_date,
            end_date=self.config.end_date,
        )
        self._market_data = {t: loaders[t] for t in loaders.keys()}

    def _build_and_evaluate_strategies(self) -> None:
        strategies = self._get_strategies()
        for strategy in strategies:
            result = self._evaluate_strategy(strategy)
            if result is not None:
                self._results.add(result)

    def _get_strategies(self) -> list[Strategy]:
        if self.config.strategies:
            return list(self.config.strategies)

        all_strategies: list[Strategy] = []
        for ticker in self.config.tickers:
            all_strategies.extend(
                create_benchmark_strategies(
                    ticker=ticker,
                    signal_col=self.config.signal_col,
                    trade_probability=self.config.trade_probability,
                    seed=self.config.seed,
                )
            )
        return all_strategies

    def _evaluate_strategy(self, strategy: Strategy) -> BenchmarkResult | None:
        primary_ticker = strategy.required_tickers[0]
        if primary_ticker not in self._market_data:
            return None

        market_df = self._market_data[primary_ticker]
        daily_df = strategy.compute_positions(market_df).with_columns(
            (pl.col("asset_return") * pl.col("position")).alias("strategy_return"),
        )
        daily_df = self._join_benchmark(daily_df)

        return BenchmarkResult(
            strategy_name=strategy.name,
            ticker=primary_ticker,
            metrics=BacktestMetrics.from_dataframe(
                daily_df,
                benchmark_ticker=self.config.benchmark_ticker,
            ),
            daily_returns=daily_df,
        )

    def _join_benchmark(self, daily_df: pl.DataFrame) -> pl.DataFrame:
        """Join benchmark returns onto a daily DataFrame."""
        bm_ticker = self.config.benchmark_ticker
        if bm_ticker in self._market_data:
            bm_df = self._market_data[bm_ticker].select(
                "date",
                pl.col("asset_return").alias("benchmark_return"),
            )
            return daily_df.join(bm_df, on="date", how="inner")
        return daily_df.with_columns(
            pl.col("asset_return").alias("benchmark_return"),
        )


__all__ = [
    "BenchmarkConfig",
    "BenchmarkProcessor",
    "BenchmarkResult",
    "BenchmarkResults",
]
