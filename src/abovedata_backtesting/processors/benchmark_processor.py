"""
Benchmark Processor

Pre-computes benchmark returns and metrics for strategy comparison.
Results are cached and can be compared against live strategies.
"""

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
from abovedata_backtesting.model.metrics import (
    BacktestMetrics,
)

# =============================================================================
# Configuration
# =============================================================================


@dataclass(frozen=True, slots=True)
class BenchmarkConfig:
    """Configuration for benchmark processing."""

    tickers: tuple[str, ...]
    strategies: tuple[Strategy, ...] | None = None  # None = use defaults
    signal_col: str | None = None  # For shuffled/always-in strategies
    start_date: date | None = None
    end_date: date | None = None
    benchmark_ticker: str = "SPY"
    trade_probability: float = 0.3  # For random strategy
    seed: int = 42

    @classmethod
    def for_ticker(
        cls,
        ticker: str,
        signal_col: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> BenchmarkConfig:
        """Create config for a single ticker with default benchmarks."""
        return cls(
            tickers=(ticker,),
            signal_col=signal_col,
            start_date=start_date,
            end_date=end_date,
        )


# =============================================================================
# Benchmark Processor
# =============================================================================


@dataclass
class BenchmarkProcessor:
    """
    Processes benchmark strategies and caches results for comparison.

    Usage
    -----
    >>> config = BenchmarkConfig.for_ticker("AAPL", signal_col="signal_zscore")
    >>> processor = BenchmarkProcessor(config)
    >>> results = processor.run()
    >>> print(results.to_dataframe())
    >>>
    >>> # Later, compare your strategy
    >>> comparison = results.compare_strategy(strategy_sharpe=1.5, strategy_return=0.25)
    """

    config: BenchmarkConfig
    _market_data: dict[str, pl.DataFrame] = field(default_factory=dict, init=False)
    _results: BenchmarkResults = field(default_factory=BenchmarkResults, init=False)

    def run(self) -> BenchmarkResults:
        """Execute benchmark processing pipeline."""
        self._load_market_data()
        self._build_and_evaluate_strategies()
        return self._results

    # =========================================================================
    # Internal: Data Loading
    # =========================================================================
    def _load_market_data(self) -> None:
        """Load market data for all required tickers."""
        loaders = MarketDataLoaders.for_tickers(
            tickers=list(self.config.tickers),
            benchmark_ticker=self.config.benchmark_ticker,
            start_date=self.config.start_date,
            end_date=self.config.end_date,
        )
        self._market_data = {t: loaders[t] for t in loaders.keys()}

    # =========================================================================
    # Internal: Strategy Evaluation
    # =========================================================================

    def _build_and_evaluate_strategies(self) -> None:
        """Build and evaluate all benchmark strategies."""
        strategies = self._get_strategies()

        for strategy in strategies:
            result = self._evaluate_strategy(strategy)
            if result is not None:
                self._results.add(result)

    def _get_strategies(self) -> list[Strategy]:
        """Get strategies to evaluate (configured or defaults)."""
        if self.config.strategies:
            return list(self.config.strategies)

        # Build default strategies for each ticker
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
        """Evaluate a single strategy and compute metrics."""
        primary_ticker = strategy.required_tickers[0]
        market_df = self._market_data[primary_ticker]
        # Compute daily returns for the asset
        daily_df = self._compute_daily_returns(market_df, strategy)

        return BenchmarkResult(
            strategy_name=strategy.name,
            ticker=primary_ticker,
            metrics=self._compute_metrics(daily_df, primary_ticker),
            daily_returns=daily_df,
        )

    def _compute_daily_returns(
        self, market_df: pl.DataFrame, strategy: Strategy
    ) -> pl.DataFrame:
        """Compute daily returns with positions based on strategy type."""
        # Strategy computes its own positions — no isinstance needed
        return strategy.compute_positions(market_df).with_columns(
            (pl.col("asset_return") * pl.col("position")).alias("strategy_return"),
        )

    def _compute_metrics(self, daily_df: pl.DataFrame, ticker: str) -> BacktestMetrics:
        """Compute full metrics from daily returns."""
        bm_ticker = self.config.benchmark_ticker

        # Join benchmark returns on date (already has asset_return from MarketDataLoaders)
        if bm_ticker in self._market_data:
            bm_df = self._market_data[bm_ticker].select(
                "date",
                pl.col("asset_return").alias("benchmark_return"),
            )
            daily_df = daily_df.join(bm_df, on="date", how="inner")
        else:
            daily_df = daily_df.with_columns(
                pl.col("asset_return").alias("benchmark_return"),
            )

        return BacktestMetrics.from_dataframe(daily_df, benchmark_ticker=bm_ticker)



__all__ = [
    "BenchmarkConfig",
    "BenchmarkProcessor",
    "BenchmarkResult",
    "BenchmarkResults",
]
