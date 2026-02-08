from datetime import date

import polars as pl
from IPython.display import display

from abovedata_backtesting.processors.benchmark_processor import (
    BenchmarkConfig,
    BenchmarkProcessor,
)

if __name__ == "__main__":
    pl.Config.set_tbl_cols(15)

    benchmark_ticker = "SPY"
    signal_col = "signal_zscore"

    config = BenchmarkConfig(
        tickers=("DE", "CAT"),
        signal_col=signal_col,
        start_date=date(2020, 1, 1),
        end_date=date(2025, 1, 1),
        benchmark_ticker=benchmark_ticker,
    )
    processor = BenchmarkProcessor(config)
    results = processor.run()
    # results = run_benchmarks("AAPL", start_date=date(2020, 1, 1))
    display(results.to_dataframe())
    comparison = results.compare_strategy(strategy_sharpe=1.8, strategy_return=0.45)

    display(comparison)
