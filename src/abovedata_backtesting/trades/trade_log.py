"""
Trade log: builds round-trip trades from daily position data.

Vectorized implementation:
- Trade boundaries detected via numpy array operations (no row iteration)
- EntryContext read only at entry points via column-oriented reader
- Holding days computed by index difference (O(1) per trade)
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Any

import numpy as np
import polars as pl
from numpy.typing import NDArray

from abovedata_backtesting.entries.entry_context import (
    ENTRY_CONTEXT_COLUMNS,
    EntryContext,
)


@dataclass(frozen=True, slots=True)
class Trade:
    """Single round-trip trade."""

    entry_date: dt.date
    exit_date: dt.date
    direction: float  # +1.0 (long) or -1.0 (short)
    entry_price: float
    exit_price: float
    holding_days: int
    trade_return: float  # (exit/entry - 1) * direction
    signal_strength: float = 0.0
    confidence: float = 0.0
    entry_context: EntryContext | None = None


class _ContextReader:
    """
    Column-oriented context reader for O(1) row access without iter_rows.

    Extracts each context column as a Python list once at init time,
    then builds EntryContext from column arrays at any index.
    """

    __slots__ = ("_columns", "_col_names")

    def __init__(self, daily: pl.DataFrame, col_names: list[str]) -> None:
        self._col_names = col_names
        self._columns: dict[str, list[Any]] = {
            col: daily[col].to_list() for col in col_names
        }

    def read(self, idx: int) -> EntryContext | None:
        """Build EntryContext at row index from pre-extracted columns."""
        return EntryContext.from_row(
            {col: self._columns[col][idx] for col in self._col_names}
        )


@dataclass
class TradeLog:
    """
    Collection of round-trip trades built from daily position data.

    Assumes:
    - Enter on day T close price
    - Exit on day T+k close price
    - One position at a time (no overlapping trades)
    """

    trades: list[Trade]

    @classmethod
    def from_arrays(
        cls,
        positions: NDArray[np.float64],
        dates: list[Any],
        closes: NDArray[np.float64],
        strengths: NDArray[np.float64],
        confs: NDArray[np.float64],
    ) -> TradeLog:
        """Build trade log from pre-extracted numpy arrays (fast path).

        Skips Polars extraction overhead. No EntryContext support (not needed
        during grid search ranking — contexts are read only for top-N results).
        """
        if len(positions) == 0:
            return cls(trades=[])

        prev_positions = np.empty_like(positions)
        prev_positions[0] = 0.0
        prev_positions[1:] = positions[:-1]

        active = np.abs(positions) > 0.01
        prev_active = np.abs(prev_positions) > 0.01
        direction = np.sign(positions)
        prev_direction = np.sign(prev_positions)
        direction_changed = direction != prev_direction

        entries_mask = active & (~prev_active | (prev_active & direction_changed))
        exits_mask = prev_active & (~active | (active & direction_changed))

        entry_indices = np.flatnonzero(entries_mask)
        exit_indices = np.flatnonzero(exits_mask)

        if len(entry_indices) == 0:
            return cls(trades=[])

        n_rows = len(dates)
        trades: list[Trade] = []
        exit_ptr = 0

        for entry_idx in entry_indices:
            entry_idx = int(entry_idx)
            while exit_ptr < len(exit_indices) and exit_indices[exit_ptr] <= entry_idx:
                exit_ptr += 1

            if exit_ptr < len(exit_indices):
                exit_idx = int(exit_indices[exit_ptr])
            else:
                exit_idx = n_rows - 1

            entry_price = float(closes[entry_idx])
            exit_price = float(closes[exit_idx])
            trade_dir = float(direction[entry_idx])
            holding = max(exit_idx - entry_idx, 1)
            trade_return = (exit_price / entry_price - 1) * trade_dir

            s = float(strengths[entry_idx])
            c = float(confs[entry_idx])

            trades.append(
                Trade(
                    entry_date=dates[entry_idx],
                    exit_date=dates[exit_idx],
                    direction=trade_dir,
                    entry_price=entry_price,
                    exit_price=exit_price,
                    holding_days=holding,
                    trade_return=trade_return,
                    signal_strength=s if s == s else 0.0,
                    confidence=c if c == c else 0.0,
                    entry_context=None,
                )
            )

        return cls(trades=trades)

    @classmethod
    def from_daily(cls, daily: pl.DataFrame) -> TradeLog:
        """
        Build trade log from daily DataFrame with positions.

        Vectorized implementation:
        1. Detect trade boundaries using numpy array ops (no row iteration)
        2. Match entry→exit pairs via sorted index scan
        3. Build Trade objects with O(1) holding day calc
        4. Read EntryContext only at entry rows via column-oriented reader

        Required columns: date, close, position.
        Optional columns: signal_strength, confidence, entry_* context columns.
        """
        if daily.height == 0 or "position" not in daily.columns:
            return cls(trades=[])

        # Extract arrays once (numpy for numeric, list for dates)
        positions = daily["position"].to_numpy()
        dates = daily["date"].to_list()
        closes = daily["close"].to_numpy()

        strengths = (
            daily["signal_strength"].to_numpy()
            if "signal_strength" in daily.columns
            else np.zeros(len(dates))
        )
        confs = (
            daily["confidence"].to_numpy()
            if "confidence" in daily.columns
            else np.zeros(len(dates))
        )

        # Vectorized boundary detection
        prev_positions = np.empty_like(positions)
        prev_positions[0] = 0.0
        prev_positions[1:] = positions[:-1]

        active = np.abs(positions) > 0.01
        prev_active = np.abs(prev_positions) > 0.01
        direction = np.sign(positions)
        prev_direction = np.sign(prev_positions)
        direction_changed = direction != prev_direction

        # Entry: was inactive → active, or active but direction reversed
        entries_mask = active & (~prev_active | (prev_active & direction_changed))
        # Exit: was active → inactive, or active but direction reversed
        exits_mask = prev_active & (~active | (active & direction_changed))

        entry_indices = np.flatnonzero(entries_mask)
        exit_indices = np.flatnonzero(exits_mask)

        if len(entry_indices) == 0:
            return cls(trades=[])

        # Context reader: column-oriented, reads only at entry points
        has_context = any(col in daily.columns for col in ENTRY_CONTEXT_COLUMNS)
        ctx_reader: _ContextReader | None = None
        if has_context:
            available_cols = [c for c in ENTRY_CONTEXT_COLUMNS if c in daily.columns]
            ctx_reader = _ContextReader(daily, available_cols)

        # Match entries to exits and build trades
        n_rows = len(dates)
        trades: list[Trade] = []
        exit_ptr = 0

        for entry_idx in entry_indices:
            entry_idx = int(entry_idx)

            # Advance exit pointer past this entry
            while exit_ptr < len(exit_indices) and exit_indices[exit_ptr] <= entry_idx:
                exit_ptr += 1

            if exit_ptr < len(exit_indices):
                exit_idx = int(exit_indices[exit_ptr])
            else:
                # No exit found — close at end of data
                exit_idx = n_rows - 1

            entry_price = float(closes[entry_idx])
            exit_price = float(closes[exit_idx])
            trade_dir = float(direction[entry_idx])
            holding = max(exit_idx - entry_idx, 1)
            trade_return = (exit_price / entry_price - 1) * trade_dir

            # NaN-safe strength/confidence
            s = float(strengths[entry_idx])
            c = float(confs[entry_idx])

            trades.append(
                Trade(
                    entry_date=dates[entry_idx],
                    exit_date=dates[exit_idx],
                    direction=trade_dir,
                    entry_price=entry_price,
                    exit_price=exit_price,
                    holding_days=holding,
                    trade_return=trade_return,
                    signal_strength=s if s == s else 0.0,
                    confidence=c if c == c else 0.0,
                    entry_context=(
                        ctx_reader.read(entry_idx) if ctx_reader is not None else None
                    ),
                )
            )

        return cls(trades=trades)

    def to_dataframe(self) -> pl.DataFrame:
        """Convert trade log to Polars DataFrame, including context fields."""
        if not self.trades:
            return pl.DataFrame(
                schema={
                    "entry_date": pl.Date,
                    "exit_date": pl.Date,
                    "direction": pl.Float64,
                    "entry_price": pl.Float64,
                    "exit_price": pl.Float64,
                    "holding_days": pl.Int64,
                    "trade_return": pl.Float64,
                    "signal_strength": pl.Float64,
                    "confidence": pl.Float64,
                }
            )

        rows = []
        for t in self.trades:
            row: dict[str, Any] = {
                "entry_date": t.entry_date,
                "exit_date": t.exit_date,
                "direction": t.direction,
                "entry_price": t.entry_price,
                "exit_price": t.exit_price,
                "holding_days": t.holding_days,
                "trade_return": t.trade_return,
                "signal_strength": t.signal_strength,
                "confidence": t.confidence,
            }

            # Flatten entry context into columns
            ctx = t.entry_context
            if ctx is not None:
                row["entry_type"] = ctx.entry_type
                row["signal_col"] = ctx.signal_col
                row["signal_value"] = ctx.signal_value
                row["signal_date"] = ctx.signal_date
                row["raw_direction"] = ctx.raw_direction
                row["final_direction"] = ctx.final_direction
                row["flipped"] = ctx.flipped
                row["corr_col_used"] = ctx.corr_col_used
                row["corr_value_used"] = ctx.corr_value_used
                row["confidence_col_used"] = ctx.confidence_col_used
                row["confidence_value_used"] = ctx.confidence_value_used
                row["correlation_regime"] = ctx.correlation_regime
                row["regime_shift_detected"] = ctx.regime_shift_detected
                row["momentum_zscore"] = ctx.momentum_zscore

            rows.append(row)

        return pl.DataFrame(rows)

    @property
    def n_trades(self) -> int:
        return len(self.trades)

    @property
    def returns(self) -> NDArray[np.float64]:
        if not self.trades:
            return np.array([], dtype=np.float64)
        return np.array([t.trade_return for t in self.trades], dtype=np.float64)

    @property
    def total_return(self) -> float:
        r = self.returns
        return float(np.prod(1 + r) - 1) if len(r) > 0 else 0.0

    @property
    def win_rate(self) -> float:
        r = self.returns
        return float(np.mean(r > 0)) if len(r) > 0 else 0.0

    @property
    def avg_return(self) -> float:
        r = self.returns
        return float(np.mean(r)) if len(r) > 0 else 0.0

    @property
    def avg_holding_days(self) -> float:
        if not self.trades:
            return 0.0
        return float(np.mean([t.holding_days for t in self.trades]))

    @property
    def profit_factor(self) -> float:
        r = self.returns
        gains = r[r > 0].sum()
        losses = abs(r[r < 0].sum())
        return (
            float(gains / losses) if losses > 0 else float("inf") if gains > 0 else 0.0
        )

    @property
    def max_consecutive_losses(self) -> int:
        r = self.returns
        max_streak = 0
        current = 0
        for ret in r:
            if ret < 0:
                current += 1
                max_streak = max(max_streak, current)
            else:
                current = 0
        return max_streak

    def summary(self) -> dict[str, float | int]:
        return {
            "n_trades": self.n_trades,
            "total_return": self.total_return,
            "win_rate": self.win_rate,
            "avg_return": self.avg_return,
            "avg_holding_days": self.avg_holding_days,
            "profit_factor": self.profit_factor,
            "max_consecutive_losses": self.max_consecutive_losses,
        }
