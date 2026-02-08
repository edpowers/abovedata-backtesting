from pathlib import Path
from typing import cast

import polars as pl

from abovedata_backtesting.data_loaders.utils import data_root


def make_signal_data_path(ticker: str, method: str, name: str = "signal_data") -> Path:
    # Preprocessing method.
    return cast(
        Path,
        data_root.joinpath(
            "signal-data", f"ticker={ticker}", f"method={method}", f"{name}.parquet"
        ),
    )


def load_signal_data(
    ticker: str, method: str = "stl_p4_s7_robustTrue", name: str = "signal_data"
) -> pl.DataFrame:
    """Load the signal data used in the backtesting strategy."""
    return pl.read_parquet(make_signal_data_path(ticker, method, name))
