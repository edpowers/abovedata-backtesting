from pathlib import Path
from typing import cast

import polars as pl

from abovedata_backtesting.data_loaders.utils import data_root


def make_signal_data_path(
    ticker: str,
    method: str,
    name: str = "signal_data",
    visible_col: str | None = None,
) -> Path:
    """Build path to signal data parquet file.

    When ``visible_col`` is provided the path includes the
    ``visible_col={visible_col}/`` subdirectory, which contains
    STL decomposition recomputed against that specific UCC column.
    """
    parts = ["signal-data", f"ticker={ticker}", f"method={method}"]
    if visible_col is not None:
        parts.append(f"visible_col={visible_col}")
    parts.append(f"{name}.parquet")
    return cast(Path, data_root.joinpath(*parts))


def load_signal_data(
    ticker: str,
    method: str = "stl_p4_s7_robustTrue",
    name: str = "signal_data",
    visible_col: str | None = None,
) -> pl.DataFrame:
    """Load the signal data used in the backtesting strategy."""
    return pl.read_parquet(
        make_signal_data_path(ticker, method, name, visible_col=visible_col)
    )


def list_visible_cols(
    ticker: str,
    method: str = "stl_p4_s7_robustTrue",
) -> list[str]:
    """Return available visible_col variants for a ticker.

    Scans ``data/signal-data/ticker={ticker}/method={method}/`` for
    ``visible_col=*/processed_data.parquet`` subdirectories.
    """
    method_dir = data_root / "signal-data" / f"ticker={ticker}" / f"method={method}"
    if not method_dir.exists():
        return []
    return sorted(
        d.name.removeprefix("visible_col=")
        for d in method_dir.iterdir()
        if d.is_dir()
        and d.name.startswith("visible_col=")
        and (d / "processed_data.parquet").exists()
    )
