from dataclasses import dataclass, field
from datetime import date

import numpy as np
import polars as pl

from abovedata_backtesting.model.strategy_models import (
    Leg,
    Strategy,
    StrategySignal,
    StrategyType,
)

# =============================================================================
# Passive Benchmarks
# =============================================================================
"""Benchmark and naive trading strategies."""

# =============================================================================
# Benchmarks
# =============================================================================


@dataclass
class BuyAndHoldStrategy(Strategy):
    """
    100% long the entire period. The simplest benchmark.

    If your signal-based strategy can't beat this, the signal isn't adding value.
    """

    ticker: str

    @property
    def name(self) -> str:
        return f"buyhold_{self.ticker}"

    @property
    def strategy_type(self) -> StrategyType:
        return StrategyType.DIRECTIONAL

    @property
    def required_tickers(self) -> list[str]:
        return [self.ticker]

    def evaluate(
        self,
        signals: dict[str, pl.DataFrame],
        market_data: dict[str, pl.DataFrame],
        as_of_date: date,
    ) -> StrategySignal | None:
        return StrategySignal(
            date=as_of_date,
            legs=[Leg(self.ticker, 1.0, "primary")],
            signal_strength=1.0,
            confidence=1.0,
            metadata={"strategy": "buy_and_hold"},
        )

    def compute_positions(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame | None = None,
    ) -> pl.DataFrame:
        return market_data.with_columns(
            pl.lit(1.0).alias("position"),
            pl.lit(1.0).alias("signal_strength"),
            pl.lit(1.0).alias("confidence"),
        )


# =============================================================================
# Random Baselines
# =============================================================================


@dataclass
class RandomSignalStrategy(Strategy):
    """
    Random entry/exit with configurable frequency.
    Use to test if your strategy beats random chance.
    """

    ticker: str
    trade_probability: float = 0.3
    seed: int = 42
    long_bias: float = 0.5

    def __post_init__(self) -> None:
        self._rng = np.random.default_rng(self.seed)

    @property
    def name(self) -> str:
        return f"random_{self.ticker}_p{self.trade_probability:.0%}"

    @property
    def strategy_type(self) -> StrategyType:
        return StrategyType.DIRECTIONAL

    @property
    def required_tickers(self) -> list[str]:
        return [self.ticker]

    def evaluate(
        self,
        signals: dict[str, pl.DataFrame],
        market_data: dict[str, pl.DataFrame],
        as_of_date: date,
    ) -> StrategySignal | None:
        if self._rng.random() > self.trade_probability:
            return None

        direction = 1.0 if self._rng.random() < self.long_bias else -1.0
        return StrategySignal(
            date=as_of_date,
            legs=[Leg(self.ticker, direction, "primary")],
            signal_strength=direction,
            confidence=0.5,
            metadata={"strategy": "random"},
        )

    def compute_positions(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame | None = None,
    ) -> pl.DataFrame:
        """Vectorized random positions. Uses fresh RNG from same seed for reproducibility."""
        n = len(market_data)
        rng = np.random.default_rng(self.seed)

        # Two draws per row, matching evaluate's two rng.random() calls
        trade_draws = rng.random(n)
        direction_draws = rng.random(n)

        positions = np.where(
            trade_draws <= self.trade_probability,
            np.where(direction_draws < self.long_bias, 1.0, -1.0),
            0.0,
        )

        return market_data.with_columns(
            pl.Series("position", positions, dtype=pl.Float64),
            pl.Series("signal_strength", positions, dtype=pl.Float64),
            pl.lit(0.5).alias("confidence"),
        )


@dataclass
class ShuffledSignalStrategy(Strategy):
    """
    Uses real signal values but shuffled in time.
    Destroys temporal relationship while preserving signal distribution.
    """

    ticker: str
    signal_col: str
    long_threshold: float = 0.5
    short_threshold: float = -0.5
    seed: int = 42
    date_col: str = "earnings_date"

    _shuffled_signals: dict[date, float] | None = field(
        default=None, init=False, repr=False
    )

    @property
    def name(self) -> str:
        return f"shuffled_{self.ticker}"

    @property
    def strategy_type(self) -> StrategyType:
        return StrategyType.DIRECTIONAL

    @property
    def required_tickers(self) -> list[str]:
        return [self.ticker]

    def evaluate(
        self,
        signals: dict[str, pl.DataFrame],
        market_data: dict[str, pl.DataFrame],
        as_of_date: date,
    ) -> StrategySignal | None:
        if self._shuffled_signals is None:
            self._build_shuffled_signals(signals)

        if self._shuffled_signals is None:
            return None

        signal_val = self._shuffled_signals.get(as_of_date)
        if signal_val is None:
            return None

        if signal_val >= self.long_threshold:
            direction = 1.0
        elif signal_val <= self.short_threshold:
            direction = -1.0
        else:
            return None

        return StrategySignal(
            date=as_of_date,
            legs=[Leg(self.ticker, direction, "primary")],
            signal_strength=signal_val,
            confidence=min(1.0, abs(signal_val) / 3.0),
            metadata={"strategy": "shuffled", "original_signal": signal_val},
        )

    def compute_positions(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame | None = None,
    ) -> pl.DataFrame:
        """Shuffle signal values across signal dates, then join onto market data."""
        if signals is None or self.signal_col not in signals.columns:
            return market_data.with_columns(
                pl.lit(0.0).alias("position"),
                pl.lit(0.0).alias("signal_strength"),
                pl.lit(0.0).alias("confidence"),
            )

        # Extract and shuffle signal values
        sig = signals.select(
            pl.col(self.date_col).cast(pl.Date).alias("_signal_date"),
            pl.col(self.signal_col).alias("_signal_val"),
        ).drop_nulls()

        values = sig["_signal_val"].to_numpy().copy()
        np.random.default_rng(self.seed).shuffle(values)

        sig = sig.with_columns(
            pl.Series("_shuffled_signal", values, dtype=pl.Float64),
        ).select("_signal_date", "_shuffled_signal")

        # asof join: each market date gets the most recent shuffled signal
        result = (
            market_data.sort("date")
            .join_asof(
                sig.sort("_signal_date"),
                left_on="date",
                right_on="_signal_date",
                strategy="backward",
            )
            .with_columns(
                pl.when(pl.col("_shuffled_signal") >= self.long_threshold)
                .then(1.0)
                .when(pl.col("_shuffled_signal") <= self.short_threshold)
                .then(-1.0)
                .otherwise(0.0)
                .alias("position"),
                pl.col("_shuffled_signal").fill_null(0.0).alias("signal_strength"),
                (pl.col("_shuffled_signal").abs() / 3.0)
                .clip(0.0, 1.0)
                .fill_null(0.0)
                .alias("confidence"),
            )
            .drop("_shuffled_signal")
        )

        return result


# =============================================================================
# Naive Strategies
# =============================================================================


@dataclass
class MomentumOnlyStrategy(Strategy):
    """
    Pure price momentum - no fundamental signal.
    Go long when price momentum is positive, short when negative.
    """

    ticker: str
    lookback_days: int = 20
    zscore_threshold: float = 1.0
    zscore_window: int = 60

    @property
    def name(self) -> str:
        return f"momentum_{self.ticker}_{self.lookback_days}d"

    @property
    def strategy_type(self) -> StrategyType:
        return StrategyType.DIRECTIONAL

    @property
    def required_tickers(self) -> list[str]:
        return [self.ticker]

    def evaluate(
        self,
        signals: dict[str, pl.DataFrame],
        market_data: dict[str, pl.DataFrame],
        as_of_date: date,
    ) -> StrategySignal | None:
        if self.ticker not in market_data:
            return None

        df = market_data[self.ticker]
        df = df.filter(pl.col("date").cast(pl.Date) <= as_of_date).sort("date")

        if len(df) < self.lookback_days * 2:
            return None

        prices = df["close"].to_numpy()

        current_ret = (prices[-1] / prices[-self.lookback_days]) - 1

        n_samples = min(self.zscore_window, len(prices) - self.lookback_days)
        historical_rets = []
        for i in range(n_samples):
            idx = len(prices) - self.lookback_days - 1 - i
            if idx >= self.lookback_days:
                ret = (prices[idx] / prices[idx - self.lookback_days]) - 1
                historical_rets.append(ret)

        if len(historical_rets) < 10:
            return None

        mean_ret = float(np.mean(historical_rets))
        std_ret = float(np.std(historical_rets))

        if std_ret < 1e-9:
            return None

        zscore = (current_ret - mean_ret) / std_ret

        if abs(zscore) <= self.zscore_threshold:
            return None

        direction = 1.0 if zscore > self.zscore_threshold else -1.0
        return StrategySignal(
            date=as_of_date,
            legs=[Leg(self.ticker, direction, "primary")],
            signal_strength=zscore,
            confidence=min(1.0, abs(zscore) / 3.0),
            metadata={"strategy": "momentum", "momentum_zscore": zscore},
        )

    def compute_positions(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame | None = None,
    ) -> pl.DataFrame:
        momentum = pl.col("close") / pl.col("close").shift(self.lookback_days) - 1
        lagged_momentum = momentum.shift(1)

        return (
            market_data.sort("date")
            .with_columns(momentum.alias("_momentum"))
            .with_columns(
                lagged_momentum.rolling_mean(self.zscore_window).alias("_mom_mean"),
                lagged_momentum.rolling_std(self.zscore_window).alias("_mom_std"),
            )
            .with_columns(
                (
                    (pl.col("_momentum") - pl.col("_mom_mean")) / pl.col("_mom_std")
                ).alias("_mom_zscore"),
            )
            .with_columns(
                pl.when(pl.col("_mom_zscore") > self.zscore_threshold)
                .then(1.0)
                .when(pl.col("_mom_zscore") < -self.zscore_threshold)
                .then(-1.0)
                .otherwise(0.0)
                .alias("position"),
                pl.col("_mom_zscore").alias("signal_strength"),
                (pl.col("_mom_zscore").abs() / 3.0).clip(0.0, 1.0).alias("confidence"),
            )
            .drop(["_momentum", "_mom_mean", "_mom_std", "_mom_zscore"])
        )


@dataclass
class AlwaysInMarketStrategy(Strategy):
    """
    Always invested, signal only determines direction.
    Uses fundamental signal for direction but never exits to cash.
    """

    ticker: str
    signal_col: str
    date_col: str = "earnings_date"

    @property
    def name(self) -> str:
        return f"always_in_{self.ticker}"

    @property
    def strategy_type(self) -> StrategyType:
        return StrategyType.DIRECTIONAL

    @property
    def required_tickers(self) -> list[str]:
        return [self.ticker]

    def evaluate(
        self,
        signals: dict[str, pl.DataFrame],
        market_data: dict[str, pl.DataFrame],
        as_of_date: date,
    ) -> StrategySignal | None:
        if self.ticker not in signals:
            return StrategySignal(
                date=as_of_date,
                legs=[Leg(self.ticker, 1.0, "primary")],
                signal_strength=0.0,
                confidence=0.5,
                metadata={"strategy": "always_in", "direction": "default_long"},
            )

        df = signals[self.ticker]
        if self.signal_col not in df.columns:
            return StrategySignal(
                date=as_of_date,
                legs=[Leg(self.ticker, 1.0, "primary")],
                signal_strength=0.0,
                confidence=0.5,
                metadata={"strategy": "always_in", "direction": "default_long"},
            )

        filtered = df.filter(pl.col(self.date_col).cast(pl.Date) <= as_of_date).sort(
            self.date_col, descending=True
        )

        if len(filtered) == 0:
            direction = 1.0
            signal_val = 0.0
        else:
            signal_val = filtered[self.signal_col][0]
            if signal_val is None or np.isnan(signal_val):
                direction = 1.0
                signal_val = 0.0
            else:
                direction = 1.0 if signal_val >= 0 else -1.0

        return StrategySignal(
            date=as_of_date,
            legs=[Leg(self.ticker, direction, "primary")],
            signal_strength=float(signal_val),
            confidence=min(1.0, abs(float(signal_val)) / 3.0) if signal_val else 0.5,
            metadata={"strategy": "always_in", "signal_value": signal_val},
        )

    def compute_positions(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame | None = None,
    ) -> pl.DataFrame:
        """Always in market; direction from forward-filled signal, default long."""
        if signals is None or self.signal_col not in signals.columns:
            return market_data.with_columns(
                pl.lit(1.0).alias("position"),
                pl.lit(0.0).alias("signal_strength"),
                pl.lit(0.5).alias("confidence"),
            )

        # Get signal dates and values
        sig = signals.select(
            pl.col(self.date_col).cast(pl.Date).alias("_signal_date"),
            pl.col(self.signal_col).alias("_signal_val"),
        ).drop_nulls()

        # asof join: each market date gets the most recent signal
        result = (
            market_data.sort("date")
            .join_asof(
                sig.sort("_signal_date"),
                left_on="date",
                right_on="_signal_date",
                strategy="backward",
            )
            .with_columns(
                # Default long when no signal yet
                pl.when(pl.col("_signal_val").is_null())
                .then(1.0)
                .when(pl.col("_signal_val") >= 0)
                .then(1.0)
                .otherwise(-1.0)
                .alias("position"),
                pl.col("_signal_val").fill_null(0.0).alias("signal_strength"),
                pl.when(pl.col("_signal_val").is_null())
                .then(0.5)
                .otherwise((pl.col("_signal_val").abs() / 3.0).clip(0.0, 1.0))
                .alias("confidence"),
            )
            .drop("_signal_val")
        )

        return result


def create_benchmark_strategies(
    ticker: str,
    signal_col: str | None = None,
    trade_probability: float = 0.3,
    seed: int = 42,
) -> list[Strategy]:
    """
    Create standard set of benchmark strategies.

    Parameters
    ----------
    ticker : str
        Ticker to benchmark
    signal_col : str | None
        Signal column (needed for shuffled and always-in strategies)
    trade_probability : float
        Trade frequency for random strategy
    seed : int
        Random seed

    Returns
    -------
    list[Strategy]
        List of benchmark strategies
    """
    benchmarks: list[Strategy] = [
        BuyAndHoldStrategy(ticker=ticker),
        RandomSignalStrategy(
            ticker=ticker, trade_probability=trade_probability, seed=seed
        ),
        MomentumOnlyStrategy(ticker=ticker, lookback_days=20),
    ]

    if signal_col:
        benchmarks.extend(
            [
                ShuffledSignalStrategy(ticker=ticker, signal_col=signal_col, seed=seed),
                AlwaysInMarketStrategy(ticker=ticker, signal_col=signal_col),
            ]
        )

    return benchmarks
