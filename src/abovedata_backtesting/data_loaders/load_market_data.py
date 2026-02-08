"""Load the market data for a given ticker."""

import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

import polars as pl
import yfinance as yf
from typing_extensions import Self

from abovedata_backtesting.data_loaders.utils import data_root


def make_market_data_path(ticker: str) -> Path:
    return cast(
        Path,
        data_root.joinpath(
            "market-data", "freq=daily", f"ticker={ticker}", "market_data.parquet"
        ),
    )


def load_market_data(
    ticker: str,
    refresh: bool = False,
    debug: bool = False,
) -> pl.DataFrame:
    fpath = make_market_data_path(ticker=ticker)

    if fpath.exists() and not refresh:
        if debug:
            print("📈 Loading cached prices...")
        prices = pl.read_parquet(fpath)
    else:
        if debug:
            print(f"📈 Fetching market data for {ticker}...")

        df_pd = yf.download(ticker, start="2010-01-01", progress=False).reset_index()
        df_pd.columns = df_pd.columns.droplevel(1)
        df_pd.columns = [c.lower() for c in df_pd.columns]

        if df_pd.empty:
            raise ValueError("No price data fetched!")

        prices = pl.from_pandas(df_pd)  # type: ignore
        prices.write_parquet(fpath, mkdir=True)

    if "ticker" not in prices.columns:
        prices = prices.with_columns(pl.lit(ticker).alias("ticker"))

    return prices.with_columns(pl.col("date").dt.date())


@dataclass
class MarketDataLoader:
    ticker: str
    refresh: bool = field(default=False)
    _df: pl.DataFrame = field(init=False)

    def __post_init__(self) -> None:
        self._ensure_loaded()

    def _ensure_loaded(self) -> pl.DataFrame:
        if not hasattr(self, "_df") or self._df is None:
            self._df = load_market_data(self.ticker)
        return self._df

    def with_returns(self) -> Self:
        """Add daily asset_return column (simple returns on close)."""
        df = self._ensure_loaded()
        self._df = (
            df.sort("date")
            .with_columns(
                (pl.col("close") / pl.col("close").shift(1) - 1).alias("asset_return"),
            )
            .drop_nulls(subset=["asset_return"])
        )
        return self

    def filter_dates(
        self,
        start_date: datetime.date | str | None = None,
        end_date: datetime.date | str | None = None,
    ) -> Self:
        """Filter by date range (inclusive)."""
        df = self._ensure_loaded()
        exprs: list[pl.Expr] = []
        if start_date is not None:
            exprs.append(pl.col("date") >= pl.lit(start_date).cast(pl.Date))
        if end_date is not None:
            exprs.append(pl.col("date") <= pl.lit(end_date).cast(pl.Date))
        if exprs:
            self._df = df.filter(pl.all_horizontal(exprs))
        return self

    def collect(self) -> pl.DataFrame:
        """Terminal method — return the built DataFrame."""
        return self._ensure_loaded()


@dataclass
class MarketDataLoaders:
    """
    Container for loading market data for multiple tickers.

    Provides a reusable pattern for processors that need market data
    for primary tickers plus a benchmark.

    Usage
    -----
    >>> data = MarketDataLoaders.for_tickers(
    ...     tickers=["AAPL", "MSFT"],
    ...     benchmark_ticker="SPY",
    ...     start_date=date(2020, 1, 1),
    ... )
    >>> aapl_df = data["AAPL"]
    >>> spy_df = data["SPY"]
    """

    _data: dict[str, pl.DataFrame] = field(default_factory=dict)

    def __getitem__(self, ticker: str) -> pl.DataFrame:
        return self._data[ticker]

    def __contains__(self, ticker: str) -> bool:
        return ticker in self._data

    def get(self, ticker: str) -> pl.DataFrame | None:
        return self._data.get(ticker)

    def keys(self) -> list[str]:
        return list(self._data.keys())

    @classmethod
    def for_tickers(
        cls,
        tickers: list[str] | tuple[str, ...],
        benchmark_ticker: str | None = "SPY",
        start_date: datetime.date | None = None,
        end_date: datetime.date | None = None,
        with_returns: bool = True,
    ) -> "MarketDataLoaders":
        """
        Load market data for multiple tickers with optional date filtering.

        Parameters
        ----------
        tickers : list[str] | tuple[str, ...]
            Primary tickers to load
        benchmark_ticker : str | None
            Benchmark ticker (default: SPY). Set to None to skip.
        start_date : date | None
            Start date filter (inclusive)
        end_date : date | None
            End date filter (inclusive)
        with_returns : bool
            If True, compute asset_return column (default: True)

        Returns
        -------
        MarketDataLoaders
            Container with loaded DataFrames accessible by ticker
        """
        all_tickers = set(tickers)
        if benchmark_ticker:
            all_tickers.add(benchmark_ticker)

        data: dict[str, pl.DataFrame] = {}
        for ticker in all_tickers:
            loader = MarketDataLoader(ticker)
            if with_returns:
                loader = loader.with_returns()
            loader = loader.filter_dates(start_date=start_date, end_date=end_date)
            data[ticker] = loader.collect()

        return cls(_data=data)
