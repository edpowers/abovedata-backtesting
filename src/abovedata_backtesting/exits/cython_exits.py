"""Cython-accelerated exit strategy kernels (pure-Python mode).

Works as regular Python when not compiled. When compiled with Cython,
the typed loops run as native C code (~50-100x faster).

Build: cythonize -i src/abovedata_backtesting/exits/cython_exits.py
"""

from __future__ import annotations

import cython
import numpy as np
from numpy.typing import NDArray


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
def _fixed_holding_exit(
    positions: cython.double[:],
    signal_date_mask: cython.uchar[:],
    holding_days: cython.int,
    out: cython.double[:],
) -> None:
    n: cython.Py_ssize_t = positions.shape[0]
    i: cython.Py_ssize_t
    days_held: cython.int = 0
    in_position: cython.bint = False
    pos: cython.double

    for i in range(n):
        pos = positions[i]
        if pos > 0.01 or pos < -0.01:
            if not in_position:
                in_position = True
                days_held = 1
                out[i] = pos
            elif signal_date_mask[i]:
                days_held = 1
                out[i] = pos
            elif days_held >= holding_days:
                out[i] = 0.0
                in_position = False
                days_held = 0
            else:
                days_held += 1
                out[i] = pos
        else:
            out[i] = 0.0
            in_position = False
            days_held = 0


def fixed_holding_exit_cy(
    positions: NDArray[np.float64],
    signal_date_mask: NDArray[np.uint8],
    holding_days: int,
) -> NDArray[np.float64]:
    """Apply fixed holding period exit logic.

    Parameters
    ----------
    positions : (N,) float64 array of raw positions from entry rule
    signal_date_mask : (N,) uint8 array, 1 where date is a signal_date
    holding_days : max days to hold before exiting

    Returns
    -------
    (N,) float64 array of modified positions
    """
    pos = np.array(positions, dtype=np.float64, copy=True)
    mask = np.array(signal_date_mask, dtype=np.uint8, copy=True)
    out = np.empty(pos.shape[0], dtype=np.float64)
    _fixed_holding_exit(pos, mask, holding_days, out)
    return out


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
def _trailing_stop_exit(
    positions: cython.double[:],
    closes: cython.double[:],
    highs: cython.double[:],
    lows: cython.double[:],
    trailing_stop_pct: cython.double,
    out_pos: cython.double[:],
    out_exit: cython.double[:],
) -> None:
    n: cython.Py_ssize_t = positions.shape[0]
    i: cython.Py_ssize_t
    peak: cython.double = 0.0
    trough: cython.double = 0.0
    in_position: cython.bint = False
    direction: cython.double = 0.0
    should_exit: cython.bint
    stop_price: cython.double
    stop_exit_price: cython.double
    pos: cython.double
    close: cython.double
    high: cython.double
    low: cython.double

    for i in range(n):
        pos = positions[i]
        close = closes[i]
        high = highs[i]
        low = lows[i]

        if (pos > 0.01 or pos < -0.01) and not in_position:
            # New entry
            in_position = True
            if pos > 0:
                direction = 1.0
                peak = high
            else:
                direction = -1.0
                trough = low
            out_pos[i] = pos
            out_exit[i] = close

        elif in_position:
            should_exit = False
            stop_exit_price = close

            if direction > 0:
                if high > peak:
                    peak = high
                stop_price = peak * (1.0 - trailing_stop_pct)
                if low <= stop_price:
                    should_exit = True
                    stop_exit_price = stop_price
            else:
                if low < trough:
                    trough = low
                stop_price = trough * (1.0 + trailing_stop_pct)
                if high >= stop_price:
                    should_exit = True
                    stop_exit_price = stop_price

            if should_exit or (pos > -0.01 and pos < 0.01):
                out_pos[i] = 0.0
                if should_exit:
                    out_exit[i] = stop_exit_price
                else:
                    out_exit[i] = close
                in_position = False
                peak = 0.0
                trough = 0.0
            else:
                out_pos[i] = pos
                out_exit[i] = close
        else:
            out_pos[i] = pos
            out_exit[i] = close


def trailing_stop_exit_cy(
    positions: NDArray[np.float64],
    closes: NDArray[np.float64],
    highs: NDArray[np.float64],
    lows: NDArray[np.float64],
    trailing_stop_pct: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Apply trailing stop exit logic.

    Returns
    -------
    (new_positions, exit_prices) — both (N,) float64 arrays
    """
    n = positions.shape[0]
    pos = np.array(positions, dtype=np.float64, copy=True)
    cl = np.array(closes, dtype=np.float64, copy=True)
    hi = np.array(highs, dtype=np.float64, copy=True)
    lo = np.array(lows, dtype=np.float64, copy=True)
    out_pos = np.empty(n, dtype=np.float64)
    out_exit = np.empty(n, dtype=np.float64)
    _trailing_stop_exit(pos, cl, hi, lo, trailing_stop_pct, out_pos, out_exit)
    return out_pos, out_exit


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
def _stop_loss_take_profit_exit(
    positions: cython.double[:],
    closes: cython.double[:],
    highs: cython.double[:],
    lows: cython.double[:],
    stop_loss_pct: cython.double,
    take_profit_pct: cython.double,
    out_pos: cython.double[:],
    out_exit: cython.double[:],
) -> None:
    n: cython.Py_ssize_t = positions.shape[0]
    i: cython.Py_ssize_t
    entry_price: cython.double = 0.0
    in_position: cython.bint = False
    direction: cython.double = 0.0
    pos: cython.double
    close: cython.double
    high: cython.double
    low: cython.double
    stop_ret: cython.double
    tp_ret: cython.double
    stop_hit: cython.bint
    tp_hit: cython.bint

    for i in range(n):
        pos = positions[i]
        close = closes[i]
        high = highs[i]
        low = lows[i]

        if (pos > 0.01 or pos < -0.01) and not in_position:
            # New entry
            in_position = True
            entry_price = close
            if pos > 0:
                direction = 1.0
            else:
                direction = -1.0
            out_pos[i] = pos
            out_exit[i] = close

        elif in_position:
            if direction > 0:
                stop_ret = low / entry_price - 1.0
                tp_ret = high / entry_price - 1.0
            else:
                stop_ret = -(high / entry_price - 1.0)
                tp_ret = -(low / entry_price - 1.0)

            stop_hit = stop_ret <= stop_loss_pct
            tp_hit = tp_ret >= take_profit_pct

            if stop_hit:
                out_pos[i] = 0.0
                out_exit[i] = entry_price * (1.0 + stop_loss_pct * direction)
                in_position = False
            elif tp_hit:
                out_pos[i] = 0.0
                out_exit[i] = entry_price * (1.0 + take_profit_pct * direction)
                in_position = False
            elif pos > -0.01 and pos < 0.01:
                out_pos[i] = 0.0
                out_exit[i] = close
                in_position = False
            else:
                out_pos[i] = pos
                out_exit[i] = close
        else:
            out_pos[i] = pos
            out_exit[i] = close
            if pos > -0.01 and pos < 0.01:
                in_position = False


def stop_loss_take_profit_exit_cy(
    positions: NDArray[np.float64],
    closes: NDArray[np.float64],
    highs: NDArray[np.float64],
    lows: NDArray[np.float64],
    stop_loss_pct: float,
    take_profit_pct: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Apply stop-loss / take-profit exit logic.

    Returns
    -------
    (new_positions, exit_prices) — both (N,) float64 arrays
    """
    n = positions.shape[0]
    pos = np.array(positions, dtype=np.float64, copy=True)
    cl = np.array(closes, dtype=np.float64, copy=True)
    hi = np.array(highs, dtype=np.float64, copy=True)
    lo = np.array(lows, dtype=np.float64, copy=True)
    out_pos = np.empty(n, dtype=np.float64)
    out_exit = np.empty(n, dtype=np.float64)
    _stop_loss_take_profit_exit(
        pos,
        cl,
        hi,
        lo,
        stop_loss_pct,
        take_profit_pct,
        out_pos,
        out_exit,
    )
    return out_pos, out_exit


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
def _enforce_max_entries(
    positions: cython.double[:],
    signal_ids: cython.int[:],
    max_entries_per_signal: cython.int,
    out: cython.double[:],
) -> None:
    n: cython.Py_ssize_t = positions.shape[0]
    i: cython.Py_ssize_t
    in_trade: cython.bint = False
    current_sid: cython.int = 0
    suppressed: cython.bint = False
    entry_count: cython.int = 0
    sid: cython.int
    pos: cython.double
    pos_active: cython.bint

    for i in range(n):
        sid = signal_ids[i]
        pos = positions[i]

        if sid != current_sid:
            current_sid = sid
            entry_count = 0
            in_trade = False
            suppressed = False

        if suppressed:
            out[i] = 0.0
            continue

        pos_active = pos > 0.01 or pos < -0.01

        if pos_active and not in_trade:
            entry_count += 1
            if entry_count > max_entries_per_signal:
                suppressed = True
                out[i] = 0.0
                continue
            in_trade = True
            out[i] = pos
        elif not pos_active and in_trade:
            in_trade = False
            out[i] = pos
        else:
            out[i] = pos


def enforce_max_entries_cy(
    positions: NDArray[np.float64],
    signal_ids: NDArray[np.int32],
    max_entries_per_signal: int,
) -> NDArray[np.float64]:
    """Enforce maximum entries per signal period.

    Returns
    -------
    (N,) float64 array of modified positions
    """
    pos = np.array(positions, dtype=np.float64, copy=True)
    sids = np.array(signal_ids, dtype=np.int32, copy=True)
    out = np.empty(pos.shape[0], dtype=np.float64)
    _enforce_max_entries(pos, sids, max_entries_per_signal, out)
    return out
