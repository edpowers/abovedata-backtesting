"""
Backtest metric dataclasses.

Each dataclass owns its computation via a `from_returns()` classmethod.
BacktestMetrics composes them all and replaces the flat dict.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import numpy as np
import polars as pl
from numpy.typing import NDArray
from typing_extensions import Self

# =============================================================================
# Required columns for BacktestMetrics.from_dataframe
# =============================================================================

REQUIRED_COLUMNS = frozenset(
    {"date", "strategy_return", "asset_return", "benchmark_return", "position"}
)


# =============================================================================
# Core Metric Groups
# =============================================================================


@dataclass(frozen=True, slots=True)
class ReturnMetrics:
    """Compounded return statistics."""

    total_return: float
    annualized_return: float
    avg_period_return: float
    best_period: float
    worst_period: float
    n_periods: int

    @classmethod
    def from_returns(
        cls,
        returns: NDArray[np.floating],
        periods_per_year: float = 252,
    ) -> "Self":
        n = len(returns)
        if n < 1:
            return cls(0, 0, 0, 0, 0, 0)

        total = float(np.prod(1 + returns) - 1)
        n_years = n / periods_per_year
        ann = float((1 + total) ** (1 / max(n_years, 0.01)) - 1)

        return cls(
            total_return=total,
            annualized_return=ann,
            avg_period_return=float(np.mean(returns)),
            best_period=float(np.max(returns)),
            worst_period=float(np.min(returns)),
            n_periods=n,
        )


@dataclass(frozen=True, slots=True)
class RiskMetrics:
    """Risk and risk-adjusted return statistics."""

    annualized_volatility: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    calmar_ratio: float
    win_rate: float

    @classmethod
    def from_returns(
        cls,
        returns: NDArray[np.floating],
        annualized_return: float,
        ann_factor: float = np.sqrt(252),
    ) -> "Self":
        n = len(returns)
        if n < 2:
            return cls(0, 0, 0, 0, 0, 0)

        vol = float(np.std(returns, ddof=1)) * ann_factor
        sharpe = annualized_return / vol if vol > 0 else 0.0

        downside = returns[returns < 0]
        downside_vol = (
            float(np.std(downside, ddof=1)) * ann_factor if len(downside) > 1 else vol
        )
        sortino = annualized_return / downside_vol if downside_vol > 0 else 0.0

        cumulative = np.cumprod(1 + returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdowns = (cumulative - running_max) / running_max
        max_dd = float(np.min(drawdowns)) if len(drawdowns) > 0 else 0.0
        calmar = annualized_return / abs(max_dd) if abs(max_dd) > 0.001 else 0.0

        win_rate = float(np.sum(returns > 0) / n)

        return cls(
            annualized_volatility=vol,
            sharpe_ratio=sharpe,
            sortino_ratio=sortino,
            max_drawdown=max_dd,
            calmar_ratio=calmar,
            win_rate=win_rate,
        )


@dataclass(frozen=True, slots=True)
class ExposureMetrics:
    """Time-in-market and capital deployment stats."""

    time_in_market: float
    days_invested: int
    total_days: int

    @classmethod
    def from_positions(cls, positions: NDArray[np.floating]) -> "Self":
        invested_mask = np.abs(positions) > 0.01
        return cls(
            time_in_market=float(np.mean(invested_mask)),
            days_invested=int(np.sum(invested_mask)),
            total_days=len(positions),
        )


@dataclass(frozen=True, slots=True)
class BenchmarkMetrics:
    """Full-period benchmark (e.g. SPY) statistics."""

    ticker: str
    returns: ReturnMetrics
    risk: RiskMetrics

    @classmethod
    def from_returns(
        cls,
        benchmark_returns: NDArray[np.floating],
        ticker: str = "SPY",
        periods_per_year: float = 252,
        ann_factor: float = np.sqrt(252),
    ) -> "Self":
        ret = ReturnMetrics.from_returns(benchmark_returns, periods_per_year)
        risk = RiskMetrics.from_returns(
            benchmark_returns, ret.annualized_return, ann_factor
        )
        return cls(ticker=ticker, returns=ret, risk=risk)


@dataclass(frozen=True, slots=True)
class CapitalAdjustedMetrics:
    """
    Compares strategy vs asset/benchmark returns on invested days only,
    annualized so they're comparable to full-period metrics.

    Raw compounded returns on invested-only days are misleading when
    time-in-market is low (e.g., 20%). Annualizing normalizes for this.
    """

    strategy_return_invested: float
    asset_return_invested: float
    benchmark_return_invested: float

    strategy_return_annualized: float
    asset_return_annualized: float
    benchmark_return_annualized: float

    avg_daily_alpha: float
    n_invested_days: int
    n_total_days: int

    @property
    def timing_alpha(self) -> float:
        """Annualized strategy return minus annualized asset return on invested days."""
        return self.strategy_return_annualized - self.asset_return_annualized

    @property
    def vs_benchmark(self) -> float:
        """Annualized strategy return minus annualized benchmark on invested days."""
        return self.strategy_return_annualized - self.benchmark_return_annualized

    @property
    def capital_efficiency(self) -> float:
        """Fraction of total days that were invested."""
        return (
            self.n_invested_days / self.n_total_days if self.n_total_days > 0 else 0.0
        )

    @classmethod
    def from_returns(
        cls,
        strategy_returns: NDArray[np.floating],
        asset_returns: NDArray[np.floating],
        benchmark_returns: NDArray[np.floating],
        positions: NDArray[np.floating],
        periods_per_year: float = 252,
    ) -> CapitalAdjustedMetrics:
        invested = np.abs(positions) > 0.01
        n_invested = int(np.sum(invested))
        n_total = len(positions)

        def _compound(arr: NDArray[np.floating], mask: NDArray[np.bool_]) -> float:
            subset = arr[mask] if np.any(mask) else arr
            return float(np.prod(1 + subset) - 1) if len(subset) > 0 else 0.0

        def _annualize(total_return: float, n_days: int) -> float:
            if n_days < 1:
                return 0.0
            n_years = n_days / periods_per_year
            if n_years < 0.01:
                return 0.0
            try:
                return float((1 + total_return) ** (1 / n_years) - 1)
            except (OverflowError, ValueError):
                return 0.0

        strat_ret = _compound(strategy_returns, invested)
        asset_ret = _compound(asset_returns, invested)
        bench_ret = _compound(benchmark_returns, invested)

        if n_invested > 0:
            daily_alpha = strategy_returns[invested] - asset_returns[invested]
            avg_alpha = float(np.mean(daily_alpha))
        else:
            avg_alpha = 0.0

        return cls(
            strategy_return_invested=strat_ret,
            asset_return_invested=asset_ret,
            benchmark_return_invested=bench_ret,
            strategy_return_annualized=_annualize(strat_ret, n_invested),
            asset_return_annualized=_annualize(asset_ret, n_invested),
            benchmark_return_annualized=_annualize(bench_ret, n_invested),
            avg_daily_alpha=avg_alpha,
            n_invested_days=n_invested,
            n_total_days=n_total,
        )


# =============================================================================
# Composite
# =============================================================================


@dataclass(frozen=True, slots=True)
class BacktestMetrics:
    """All backtest metrics, composed from typed sub-groups."""

    start_date: date | None
    end_date: date | None
    returns: ReturnMetrics
    risk: RiskMetrics
    exposure: ExposureMetrics
    benchmark: BenchmarkMetrics
    capital_adjusted: CapitalAdjustedMetrics

    @classmethod
    def from_dataframe(
        cls,
        daily_df: pl.DataFrame,
        benchmark_ticker: str = "SPY",
        periods_per_year: float = 252,
        ann_factor: float = np.sqrt(252),
    ) -> "Self":
        """
        Build all metrics from a single aligned DataFrame.

        Parameters
        ----------
        daily_df : pl.DataFrame
            Must contain columns: date, strategy_return, asset_return,
            benchmark_return, position. All return columns must be non-null.
        benchmark_ticker : str
            Ticker label for benchmark metrics.
        periods_per_year : float
            Trading days per year for annualization.
        ann_factor : float
            Annualization factor for volatility (sqrt of periods_per_year).

        Raises
        ------
        ValueError
            If required columns are missing or DataFrame is empty after
            dropping nulls/non-finite values.
        """

        def convert_to_array(series: pl.Series) -> np.ndarray:
            return series.to_numpy(allow_copy=True).astype(np.float64)

        # ── Validate schema ─────────────────────────────────────────────
        if missing := (REQUIRED_COLUMNS - set(daily_df.columns)):
            raise ValueError(f"Missing required columns: {missing}")

        # ── Clean: drop nulls and non-finite returns ────────────────────
        return_cols = ["strategy_return", "asset_return", "benchmark_return"]
        clean = daily_df.drop_nulls(subset=return_cols).filter(
            pl.all_horizontal(pl.col(c).is_finite() for c in return_cols)
        )

        if clean.is_empty():
            raise ValueError(
                "DataFrame is empty after dropping nulls and non-finite values"
            )

        dates = clean["date"].to_list()

        return cls.from_daily(
            strategy_returns=convert_to_array(clean["strategy_return"]),
            asset_returns=convert_to_array(clean["asset_return"]),
            benchmark_returns=convert_to_array(clean["benchmark_return"]),
            positions=convert_to_array(clean["position"]),
            start_date=dates[0] if dates else None,
            end_date=dates[-1] if dates else None,
            benchmark_ticker=benchmark_ticker,
            periods_per_year=periods_per_year,
            ann_factor=ann_factor,
        )

    @classmethod
    def from_daily(
        cls,
        strategy_returns: NDArray[np.floating],
        asset_returns: NDArray[np.floating],
        benchmark_returns: NDArray[np.floating],
        positions: NDArray[np.floating],
        start_date: date | None = None,
        end_date: date | None = None,
        benchmark_ticker: str = "SPY",
        periods_per_year: float = 252,
        ann_factor: float = np.sqrt(252),
    ) -> "Self":
        """Build all metrics from pre-aligned numpy arrays."""
        ret = ReturnMetrics.from_returns(strategy_returns, periods_per_year)

        return cls(
            start_date=start_date,
            end_date=end_date,
            returns=ret,
            risk=RiskMetrics.from_returns(
                strategy_returns, ret.annualized_return, ann_factor
            ),
            exposure=ExposureMetrics.from_positions(positions),
            benchmark=BenchmarkMetrics.from_returns(
                benchmark_returns, benchmark_ticker, periods_per_year, ann_factor
            ),
            capital_adjusted=CapitalAdjustedMetrics.from_returns(
                strategy_returns, asset_returns, benchmark_returns, positions
            ),
        )

    def extract_metric(self, name: str) -> float:
        lookup: dict[str, float] = {
            "sharpe_ratio": self.risk.sharpe_ratio,
            "sortino_ratio": self.risk.sortino_ratio,
            "calmar_ratio": self.risk.calmar_ratio,
            "total_return": self.returns.total_return,
            "annualized_return": self.returns.annualized_return,
            "max_drawdown": self.risk.max_drawdown,
            "timing_alpha": self.capital_adjusted.timing_alpha,
            "vs_benchmark": self.capital_adjusted.vs_benchmark,
            "capital_efficiency": self.capital_adjusted.capital_efficiency,
            "avg_daily_alpha": self.capital_adjusted.avg_daily_alpha,
        }
        return lookup.get(name, 0.0)

    def make_dict(self) -> dict[str, float]:
        return {
            # Return metrics
            "total_return": self.returns.total_return,
            "annualized_return": self.returns.annualized_return,
            "n_periods": self.returns.n_periods,
            # Risk metrics
            "sharpe_ratio": self.risk.sharpe_ratio,
            "sortino_ratio": self.risk.sortino_ratio,
            "max_drawdown": self.risk.max_drawdown,
            "calmar_ratio": self.risk.calmar_ratio,
            "annualized_volatility": self.risk.annualized_volatility,
            "win_rate": self.risk.win_rate,
            # Exposure
            "time_in_market": self.exposure.time_in_market,
            "days_invested": self.exposure.days_invested,
            # Capital adjusted (annualized)
            "timing_alpha": self.capital_adjusted.timing_alpha,
            "vs_benchmark": self.capital_adjusted.vs_benchmark,
            "capital_efficiency": self.capital_adjusted.capital_efficiency,
            "avg_daily_alpha": self.capital_adjusted.avg_daily_alpha,
            "strategy_return_annualized_invested": self.capital_adjusted.strategy_return_annualized,
            "asset_return_annualized_invested": self.capital_adjusted.asset_return_annualized,
        }
