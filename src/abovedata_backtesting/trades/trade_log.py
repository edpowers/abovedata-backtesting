"""Trade log for round-trip trade tracking.

Converts daily position data into discrete trades with entry/exit dates,
holding periods, and P&L. This avoids the compounding illusion from
daily position × return calculations.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

import numpy as np
import polars as pl
from numpy.typing import NDArray


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
        Optional columns: signal_strength, confidence.

        A trade starts when position goes from 0 to non-zero,
        and ends when position returns to 0 or changes direction.
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

        trades: list[Trade] = []
        in_trade = False
        entry_date: dt.date | None = None
        entry_price: float = 0.0
        direction: float = 0.0
        entry_strength: float = 0.0
        entry_confidence: float = 0.0

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
                    )
                )

                # If direction reversed, immediately start new trade
                if pos_active and _sign(pos) != direction:
                    entry_date = d
                    entry_price = close
                    direction = 1.0 if pos > 0 else -1.0
                    entry_strength = strength if strength is not None else 0.0
                    entry_confidence = conf if conf is not None else 0.0
                else:
                    in_trade = False
                    entry_date = None

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
                )
            )

        return cls(trades=trades)

    def to_dataframe(self) -> pl.DataFrame:
        """Convert trade log to Polars DataFrame."""
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
        return pl.DataFrame(
            [
                {
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
                for t in self.trades
            ]
        )

    @property
    def n_trades(self) -> int:
        return len(self.trades)

    @property
    def returns(self) -> NDArray[np.float64]:
        """Array of per-trade returns."""
        if not self.trades:
            return np.array([], dtype=np.float64)
        return np.array([t.trade_return for t in self.trades], dtype=np.float64)

    @property
    def total_return(self) -> float:
        """Compounded return across all trades."""
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
        """Gross profits / gross losses."""
        r = self.returns
        gains = r[r > 0].sum()
        losses = abs(r[r < 0].sum())
        return (
            float(gains / losses) if losses > 0 else float("inf") if gains > 0 else 0.0
        )

    @property
    def max_consecutive_losses(self) -> int:
        """Longest streak of losing trades."""
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
        """Summary stats as a flat dict (for grid search DataFrame)."""
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
    """Count trading days between start and end (inclusive of end)."""
    # Since dates list is the actual trading calendar, just count rows
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
