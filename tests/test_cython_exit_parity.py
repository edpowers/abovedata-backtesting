"""Parity tests: Cython exit kernels produce identical results to Python originals."""

from datetime import date, timedelta

import numpy as np
import polars as pl
import pytest

from abovedata_backtesting.entries.entry_signals import (
    enforce_max_entries,
    enforce_max_entries_fast,
)
from abovedata_backtesting.exits.exit_strategies import (
    FixedHoldingExit,
    StopLossTakeProfitExit,
    TrailingStopExit,
)


def _make_daily(n: int = 2500, seed: int = 42) -> pl.DataFrame:
    """Build a realistic daily DataFrame with position blocks."""
    rng = np.random.default_rng(seed)
    positions = np.zeros(n, dtype=np.float64)
    for start in range(0, n, 80):
        end = min(start + 50, n)
        positions[start:end] = rng.choice([-1.0, 1.0])

    closes = 100.0 + np.cumsum(rng.standard_normal(n) * 0.5)
    highs = closes + np.abs(rng.standard_normal(n) * 0.3)
    lows = closes - np.abs(rng.standard_normal(n) * 0.3)

    dates = [date(2015, 1, 1) + timedelta(days=i) for i in range(n)]
    signal_ids = np.zeros(n, dtype=np.int32)
    sid = 0
    for i in range(n):
        if i % 80 == 0:
            sid += 1
        signal_ids[i] = sid

    return pl.DataFrame(
        {
            "date": dates,
            "position": positions,
            "close": closes,
            "high": highs,
            "low": lows,
            "signal_id": signal_ids,
        }
    )


@pytest.fixture
def daily() -> pl.DataFrame:
    return _make_daily()


class TestFixedHoldingExitParity:
    @pytest.mark.parametrize("holding_days", [10, 30, 60, 90])
    def test_parity(self, daily: pl.DataFrame, holding_days: int) -> None:
        dates = daily["date"].to_list()
        signal_dates = frozenset(dates[::80])
        exit_rule = FixedHoldingExit(
            holding_days=holding_days, signal_dates=signal_dates
        )

        py_result = exit_rule.apply(daily)
        cy_result = exit_rule.apply_fast(daily)

        np.testing.assert_array_almost_equal(
            py_result["position"].to_numpy(),
            cy_result["position"].to_numpy(),
            decimal=10,
        )


class TestTrailingStopExitParity:
    @pytest.mark.parametrize("pct", [0.02, 0.05, 0.10, 0.20])
    def test_parity(self, daily: pl.DataFrame, pct: float) -> None:
        exit_rule = TrailingStopExit(trailing_stop_pct=pct)

        py_result = exit_rule.apply(daily)
        cy_result = exit_rule.apply_fast(daily)

        np.testing.assert_array_almost_equal(
            py_result["position"].to_numpy(),
            cy_result["position"].to_numpy(),
            decimal=10,
        )
        np.testing.assert_array_almost_equal(
            py_result["exit_price"].to_numpy(),
            cy_result["exit_price"].to_numpy(),
            decimal=6,
        )


class TestStopLossTakeProfitExitParity:
    @pytest.mark.parametrize(
        "sl,tp",
        [(-0.05, 0.10), (-0.10, 0.20), (-0.03, 0.05), (-0.15, 0.30)],
    )
    def test_parity(self, daily: pl.DataFrame, sl: float, tp: float) -> None:
        exit_rule = StopLossTakeProfitExit(stop_loss_pct=sl, take_profit_pct=tp)

        py_result = exit_rule.apply(daily)
        cy_result = exit_rule.apply_fast(daily)

        np.testing.assert_array_almost_equal(
            py_result["position"].to_numpy(),
            cy_result["position"].to_numpy(),
            decimal=10,
        )
        np.testing.assert_array_almost_equal(
            py_result["exit_price"].to_numpy(),
            cy_result["exit_price"].to_numpy(),
            decimal=6,
        )


class TestEnforceMaxEntriesParity:
    @pytest.mark.parametrize("max_entries", [1, 2, 3])
    def test_parity(self, daily: pl.DataFrame, max_entries: int) -> None:
        # Apply a trailing stop first to create exit gaps (re-entry opportunities)
        ts = TrailingStopExit(trailing_stop_pct=0.05)
        exited = ts.apply(daily)

        py_result = enforce_max_entries(exited, max_entries)
        cy_result = enforce_max_entries_fast(exited, max_entries)

        np.testing.assert_array_almost_equal(
            py_result["position"].to_numpy(),
            cy_result["position"].to_numpy(),
            decimal=10,
        )


class TestEdgeCases:
    def test_all_zero_positions(self) -> None:
        """All-flat positions should produce all-flat output."""
        daily = _make_daily(100, seed=99)
        daily = daily.with_columns(pl.lit(0.0).alias("position"))

        for ExitCls, kwargs in [
            (TrailingStopExit, {"trailing_stop_pct": 0.05}),
            (StopLossTakeProfitExit, {"stop_loss_pct": -0.10, "take_profit_pct": 0.20}),
            (FixedHoldingExit, {"holding_days": 30, "signal_dates": frozenset()}),
        ]:
            exit_rule = ExitCls(**kwargs)
            result = exit_rule.apply_fast(daily)
            assert (result["position"].to_numpy() == 0.0).all()

    def test_single_row(self) -> None:
        """Single-row DataFrame should work without errors."""
        daily = pl.DataFrame(
            {
                "date": [date(2020, 1, 1)],
                "position": [1.0],
                "close": [100.0],
                "high": [101.0],
                "low": [99.0],
                "signal_id": [1],
            }
        )
        ts = TrailingStopExit(trailing_stop_pct=0.05)
        result = ts.apply_fast(daily)
        assert result.height == 1
