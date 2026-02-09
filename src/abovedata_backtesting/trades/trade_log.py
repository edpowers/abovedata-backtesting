"""
Trade log: round-trip trades built from daily position data.

Trade now carries an optional EntryContext that records the entry
decision state (which correlation was used, whether a flip occurred, etc.).
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

import numpy as np
import polars as pl
from numpy.typing import NDArray

from abovedata_backtesting.entries.entry_context import (
    ENTRY_CONTEXT_COLUMNS,
    EntryContext,
    entry_context_from_row,
)


@dataclass(frozen=True, slots=True)
class Trade:
    """Single round-trip trade."""

    entry_date: dt.date
    exit_date: dt.date
    direction: float  # 1.0 or -1.0
    entry_price: float
    exit_price: float
    holding_days: int  # trading days
    trade_return: float  # (exit/entry - 1) * direction
    signal_strength: float
    confidence: float

    # Entry decision context — populated when entry rules write context columns
    entry_context: EntryContext | None = None


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
    def from_daily(cls, daily: pl.DataFrame) -> TradeLog:
        """
        Build trade log from daily DataFrame with positions.

        Required columns: date, close, position.
        Optional columns: signal_strength, confidence, entry_* context columns.
        """
        dates = daily["date"].to_list()
        closes = daily["close"].to_list()
        positions = daily["position"].to_list()
        strengths = (
            daily["signal_strength"].to_list()
            if "signal_strength" in daily.columns
            else [0.0] * len(dates)
        )
        confidences = (
            daily["confidence"].to_list()
            if "confidence" in daily.columns
            else [0.0] * len(dates)
        )

        # Check if entry context columns are available
        has_context = any(col in daily.columns for col in ENTRY_CONTEXT_COLUMNS)

        # Pre-extract context rows if available (avoid repeated dict building)
        context_rows: list[dict | None] = []
        if has_context:
            available_ctx_cols = [
                c for c in ENTRY_CONTEXT_COLUMNS if c in daily.columns
            ]
            ctx_df = daily.select(available_ctx_cols)
            for row in ctx_df.iter_rows(named=True):
                context_rows.append(row)
        else:
            context_rows = [None] * len(dates)

        trades: list[Trade] = []
        in_trade = False
        entry_date: dt.date | None = None
        entry_price: float = 0.0
        direction: float = 0.0
        entry_strength: float = 0.0
        entry_confidence: float = 0.0
        entry_ctx: EntryContext | None = None

        for i, (d, close, pos, strength, conf) in enumerate(
            zip(dates, closes, positions, strengths, confidences, strict=True)
        ):
            pos_active = abs(pos) > 0.01

            if pos_active and not in_trade:
                # New trade entry
                in_trade = True
                entry_date = d
                entry_price = close
                direction = 1.0 if pos > 0 else -1.0
                entry_strength = strength if strength is not None else 0.0
                entry_confidence = conf if conf is not None else 0.0
                entry_ctx = (
                    entry_context_from_row(context_rows[i])
                    if context_rows[i] is not None
                    else None
                )

            elif in_trade and (
                not pos_active or (pos_active and _sign(pos) != direction)
            ):
                # Trade exit: position went flat or reversed direction
                assert entry_date is not None
                trade_return = (close / entry_price - 1) * direction
                holding = _trading_days_between(dates, entry_date, d)

                trades.append(
                    Trade(
                        entry_date=entry_date,
                        exit_date=d,
                        direction=direction,
                        entry_price=entry_price,
                        exit_price=close,
                        holding_days=holding,
                        trade_return=trade_return,
                        signal_strength=entry_strength,
                        confidence=entry_confidence,
                        entry_context=entry_ctx,
                    )
                )

                # If direction reversed, immediately start new trade
                if pos_active and _sign(pos) != direction:
                    entry_date = d
                    entry_price = close
                    direction = 1.0 if pos > 0 else -1.0
                    entry_strength = strength if strength is not None else 0.0
                    entry_confidence = conf if conf is not None else 0.0
                    entry_ctx = (
                        entry_context_from_row(context_rows[i])
                        if context_rows[i] is not None
                        else None
                    )
                else:
                    in_trade = False
                    entry_date = None
                    entry_ctx = None

        # Close any open trade at end of period
        if in_trade and entry_date is not None and len(dates) > 0:
            trade_return = (closes[-1] / entry_price - 1) * direction
            holding = _trading_days_between(dates, entry_date, dates[-1])
            trades.append(
                Trade(
                    entry_date=entry_date,
                    exit_date=dates[-1],
                    direction=direction,
                    entry_price=entry_price,
                    exit_price=closes[-1],
                    holding_days=holding,
                    trade_return=trade_return,
                    signal_strength=entry_strength,
                    confidence=entry_confidence,
                    entry_context=entry_ctx,
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
            row: dict = {
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


def _sign(x: float) -> float:
    return 1.0 if x > 0 else -1.0 if x < 0 else 0.0


def _trading_days_between(dates: list[dt.date], start: dt.date, end: dt.date) -> int:
    in_range = False
    count = 0
    for d in dates:
        if d == start:
            in_range = True
            continue
        if in_range:
            count += 1
            if d >= end:
                break
    return max(count, 1)
