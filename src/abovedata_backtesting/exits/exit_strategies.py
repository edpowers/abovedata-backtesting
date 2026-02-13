"""Exit strategy implementations.

Each exit strategy modifies positions computed by a trading strategy,
applying exit logic (holding periods, stop losses, etc.) to determine
when to close positions.
"""

from __future__ import annotations

import bisect
import datetime as dt
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import polars as pl


class ExitRule(ABC):
    """
    Abstract base class for exit strategies.

    An ExitRule takes a DataFrame that already has positions from a
    trading strategy and modifies them based on exit logic.

    Required input columns: date, position, close.
    Some subclasses require additional columns (e.g., signal dates).
    """

    @abstractmethod
    def apply(self, daily: pl.DataFrame) -> pl.DataFrame:
        """
        Apply exit logic to modify positions.

        Parameters
        ----------
        daily : pl.DataFrame
            Must contain: date, position, close.
            May require additional columns per subclass.

        Returns
        -------
        pl.DataFrame
            Same DataFrame with position column modified by exit logic.
        """

    def apply_fast(self, daily: pl.DataFrame) -> pl.DataFrame:
        """Cython-accelerated exit logic. Falls back to apply() by default."""
        return self.apply(daily)

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable identifier for this exit rule."""


@dataclass(frozen=True, slots=True)
class SignalChangeExit(ExitRule):
    """
    No-op exit: positions change only when the underlying signal changes.
    This is the default — the trading strategy's positions are used as-is.
    """

    @property
    def name(self) -> str:
        return "signal_change"

    def apply(self, daily: pl.DataFrame) -> pl.DataFrame:
        return daily


@dataclass(frozen=True, slots=True)
class FixedHoldingExit(ExitRule):
    """
    Exit after a fixed number of days, resetting if a new signal fires.

    Parameters
    ----------
    holding_days : int
        Maximum days to hold a position before exiting.
    signal_dates : list[dt.date]
        Dates on which new signals were generated (e.g., earnings dates).
        Position timer resets on these dates.
    """

    holding_days: int = 60
    signal_dates: frozenset[dt.date] = frozenset()

    @property
    def name(self) -> str:
        return f"fixed_holding_{self.holding_days}d"

    def apply(self, daily: pl.DataFrame) -> pl.DataFrame:
        dates = daily["date"].to_list()
        positions = daily["position"].to_list()

        new_positions: list[float] = []
        days_held = 0
        in_position = False

        for d, pos in zip(dates, positions, strict=True):
            if abs(pos) > 0.01:
                if not in_position:
                    # New entry
                    in_position, days_held = True, 1
                    new_positions.append(pos)
                elif d in self.signal_dates:
                    # New signal resets the clock
                    days_held = 1
                    new_positions.append(pos)
                elif days_held >= self.holding_days:
                    # Time's up
                    new_positions.append(0.0)
                    in_position, days_held = False, 0
                else:
                    days_held += 1
                    new_positions.append(pos)
            else:
                new_positions.append(0.0)
                in_position, days_held = False, 0

        return daily.with_columns(pl.Series("position", new_positions))

    def apply_fast(self, daily: pl.DataFrame) -> pl.DataFrame:
        from abovedata_backtesting.exits.cython_exits import fixed_holding_exit_cy

        positions = daily["position"].to_numpy(allow_copy=True)
        dates = daily["date"].to_list()
        signal_mask = np.array(
            [1 if d in self.signal_dates else 0 for d in dates], dtype=np.uint8
        )
        new_pos = fixed_holding_exit_cy(positions, signal_mask, self.holding_days)
        return daily.with_columns(pl.Series("position", new_pos))


@dataclass(frozen=True, slots=True)
class NextEarningsExit(ExitRule):
    """
    Exit N days before the next earnings date.

    Parameters
    ----------
    days_before : int
        Number of calendar days before next earnings to exit.
    earnings_dates : list[dt.date]
        Sorted list of known earnings dates.
    """

    days_before: int = 1
    earnings_dates: tuple[dt.date, ...] = ()

    @property
    def name(self) -> str:
        return f"next_earnings_{self.days_before}d_before"

    def apply(self, daily: pl.DataFrame) -> pl.DataFrame:
        dates = daily["date"].to_list()
        positions = daily["position"].to_list()
        sorted_earnings = sorted(self.earnings_dates)

        new_positions: list[float] = []
        for d, pos in zip(dates, positions, strict=True):
            if abs(pos) < 0.01:
                new_positions.append(0.0)
                continue

            # Binary search for next earnings after current date
            idx = bisect.bisect_right(sorted_earnings, d)
            next_earnings = sorted_earnings[idx] if idx < len(sorted_earnings) else None

            if (
                next_earnings is not None
                and (next_earnings - d).days <= self.days_before
            ):
                new_positions.append(0.0)
            else:
                new_positions.append(pos)

        return daily.with_columns(pl.Series("position", new_positions))


@dataclass(frozen=True, slots=True)
class StopLossTakeProfitExit(ExitRule):
    """
    Exit when intraday price hits stop-loss or take-profit.

    Uses high/low prices for realistic trigger detection.
    When both trigger on the same bar, stop-loss takes priority
    (conservative assumption: adverse move likely happened first).

    Parameters
    ----------
    stop_loss_pct : float
        Maximum loss before exit (negative, e.g., -0.10 for 10% loss).
    take_profit_pct : float
        Target profit for exit (positive, e.g., 0.20 for 20% gain).
    """

    stop_loss_pct: float = -0.10
    take_profit_pct: float = 0.20

    @property
    def name(self) -> str:
        return f"sl{self.stop_loss_pct:.0%}_tp{self.take_profit_pct:.0%}"

    def apply(self, daily: pl.DataFrame) -> pl.DataFrame:
        positions = daily["position"].to_list()
        closes = daily["close"].to_list()
        highs = daily["high"].to_list()
        lows = daily["low"].to_list()

        new_positions: list[float] = []
        exit_prices: list[float] = []
        entry_price: float | None = None
        in_position = False
        direction = 0.0

        for pos, close, high, low in zip(positions, closes, highs, lows, strict=True):
            if abs(pos) > 0.01 and not in_position:
                # New entry — use close as entry price
                in_position = True
                entry_price = close
                direction = 1.0 if pos > 0 else -1.0
                new_positions.append(pos)
                exit_prices.append(close)
            elif in_position and entry_price is not None:
                # Check intraday extremes for stop/TP triggers
                if direction > 0:
                    # Long: low can trigger stop, high can trigger TP
                    stop_ret = low / entry_price - 1
                    tp_ret = high / entry_price - 1
                else:
                    # Short: high can trigger stop (adverse), low can trigger TP
                    stop_ret = -(high / entry_price - 1)
                    tp_ret = -(low / entry_price - 1)

                stop_hit = stop_ret <= self.stop_loss_pct
                tp_hit = tp_ret >= self.take_profit_pct

                if stop_hit:
                    # Exit at the stop price, not close
                    stop_price = entry_price * (1 + self.stop_loss_pct * direction)
                    new_positions.append(0.0)
                    exit_prices.append(stop_price)
                    in_position, entry_price = False, None
                elif tp_hit:
                    tp_price = entry_price * (1 + self.take_profit_pct * direction)
                    new_positions.append(0.0)
                    exit_prices.append(tp_price)
                    in_position, entry_price = False, None
                elif abs(pos) < 0.01:
                    # Signal says exit (no stop/TP, just signal change)
                    new_positions.append(0.0)
                    exit_prices.append(close)
                    in_position, entry_price = False, None
                else:
                    new_positions.append(pos)
                    exit_prices.append(close)
            else:
                new_positions.append(pos)
                exit_prices.append(close)
                if abs(pos) < 0.01:
                    in_position, entry_price = False, None

        return daily.with_columns(
            pl.Series("position", new_positions),
            pl.Series("exit_price", exit_prices),
        )

    def apply_fast(self, daily: pl.DataFrame) -> pl.DataFrame:
        from abovedata_backtesting.exits.cython_exits import (
            stop_loss_take_profit_exit_cy,
        )

        positions = daily["position"].to_numpy(allow_copy=True)
        closes = daily["close"].to_numpy(allow_copy=True)
        highs = daily["high"].to_numpy(allow_copy=True)
        lows = daily["low"].to_numpy(allow_copy=True)
        new_pos, exit_prices = stop_loss_take_profit_exit_cy(
            positions, closes, highs, lows, self.stop_loss_pct, self.take_profit_pct
        )
        return daily.with_columns(
            pl.Series("position", new_pos),
            pl.Series("exit_price", exit_prices),
        )


@dataclass(frozen=True, slots=True)
class TrailingStopExit(ExitRule):
    """
    Exit when intraday price retraces by a percentage from peak/trough.

    Peak/trough updates from high/low BEFORE checking the stop on
    the same bar. This means a new high that then reverses intraday
    will correctly trigger the trailing stop from the new peak.

    Parameters
    ----------
    trailing_stop_pct : float
        Percentage retracement that triggers exit (e.g., 0.05 for 5%).
    """

    trailing_stop_pct: float = 0.05

    @property
    def name(self) -> str:
        return f"trailing_stop_{self.trailing_stop_pct:.0%}"

    def apply(self, daily: pl.DataFrame) -> pl.DataFrame:
        positions = daily["position"].to_list()
        closes = daily["close"].to_list()
        highs = daily["high"].to_list()
        lows = daily["low"].to_list()

        new_positions: list[float] = []
        exit_prices: list[float] = []
        peak: float | None = None
        trough: float | None = None
        in_position = False
        direction = 0.0

        for pos, close, high, low in zip(positions, closes, highs, lows, strict=True):
            if abs(pos) > 0.01 and not in_position:
                # New entry
                in_position = True
                direction = 1.0 if pos > 0 else -1.0
                if direction > 0:
                    peak = high  # Best price seen (use high, not close)
                    trough = None
                else:
                    trough = low  # Best price seen for short
                    peak = None
                new_positions.append(pos)
                exit_prices.append(close)

            elif in_position:
                should_exit = False
                stop_exit_price = close  # default

                if direction > 0 and peak is not None:
                    # Update peak from today's high FIRST
                    peak = max(peak, high)
                    # Then check if low breached trailing stop from peak
                    stop_price = peak * (1 - self.trailing_stop_pct)
                    if low <= stop_price:
                        should_exit = True
                        stop_exit_price = stop_price

                elif direction < 0 and trough is not None:
                    # Update trough from today's low FIRST
                    trough = min(trough, low)
                    # Then check if high breached trailing stop from trough
                    stop_price = trough * (1 + self.trailing_stop_pct)
                    if high >= stop_price:
                        should_exit = True
                        stop_exit_price = stop_price

                if should_exit or abs(pos) < 0.01:
                    new_positions.append(0.0)
                    exit_prices.append(stop_exit_price if should_exit else close)
                    in_position, peak, trough = False, None, None
                else:
                    new_positions.append(pos)
                    exit_prices.append(close)
            else:
                new_positions.append(pos)
                exit_prices.append(close)

        return daily.with_columns(
            pl.Series("position", new_positions),
            pl.Series("exit_price", exit_prices),
        )

    def apply_fast(self, daily: pl.DataFrame) -> pl.DataFrame:
        from abovedata_backtesting.exits.cython_exits import trailing_stop_exit_cy

        positions = daily["position"].to_numpy(allow_copy=True)
        closes = daily["close"].to_numpy(allow_copy=True)
        highs = daily["high"].to_numpy(allow_copy=True)
        lows = daily["low"].to_numpy(allow_copy=True)
        new_pos, exit_prices = trailing_stop_exit_cy(
            positions, closes, highs, lows, self.trailing_stop_pct
        )
        return daily.with_columns(
            pl.Series("position", new_pos),
            pl.Series("exit_price", exit_prices),
        )
