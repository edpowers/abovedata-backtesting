"""
Strategy Models - Core abstractions for multi-strategy backtesting.

Provides the Strategy protocol and supporting types for expressing
multi-leg, multi-ticker trading strategies.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Any

import polars as pl


class StrategyType(Enum):
    """Classification of strategy types."""

    DIRECTIONAL = "directional"  # Long or short single asset
    LONG_SHORT_EQUITY = "long_short"  # Long asset, short hedge
    PAIRS = "pairs"  # Pairs trading
    STATISTICAL_ARB = "stat_arb"  # Multi-leg statistical arbitrage
    CROSS_TICKER = "cross_ticker"  # Signal from one ticker, trade another


@dataclass
class Leg:
    """
    Single leg of a multi-leg strategy position.

    Parameters
    ----------
    ticker : str
        Ticker symbol for this leg
    weight : float
        Position weight: +1 = full long, -1 = full short, fractional for partial
    role : str
        Role in the strategy: "primary", "hedge", "pair"
    """

    ticker: str
    weight: float
    role: str = "primary"

    def __post_init__(self) -> None:
        if not self.ticker:
            raise ValueError("Leg ticker cannot be empty")

    @property
    def is_long(self) -> bool:
        return self.weight > 0

    @property
    def is_short(self) -> bool:
        return self.weight < 0

    @property
    def abs_weight(self) -> float:
        return abs(self.weight)


@dataclass
class StrategySignal:
    """
    Output of strategy evaluation at a point in time.

    Represents the desired position(s) based on strategy logic.

    Parameters
    ----------
    date : date
        Date of the signal
    legs : list[Leg]
        Position legs (can be multi-leg)
    signal_strength : float
        Directional strength, typically -1 to +1
    confidence : float
        Confidence in the signal, 0 to 1
    metadata : dict
        Additional strategy-specific information
    """

    date: date
    legs: list[Leg]
    signal_strength: float
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.legs:
            raise ValueError("StrategySignal must have at least one leg")
        self.confidence = max(0.0, min(1.0, self.confidence))

    @property
    def is_long(self) -> bool:
        """Primary direction is long."""
        return self.signal_strength > 0

    @property
    def is_short(self) -> bool:
        """Primary direction is short."""
        return self.signal_strength < 0

    @property
    def primary_leg(self) -> Leg | None:
        """Get the primary leg if one exists."""
        for leg in self.legs:
            if leg.role == "primary":
                return leg
        return self.legs[0] if self.legs else None

    @property
    def gross_exposure(self) -> float:
        """Sum of absolute weights."""
        return sum(abs(leg.weight) for leg in self.legs)

    @property
    def net_exposure(self) -> float:
        """Sum of signed weights."""
        return sum(leg.weight for leg in self.legs)

    @property
    def tickers(self) -> list[str]:
        """All tickers in this signal."""
        return [leg.ticker for leg in self.legs]


class Strategy(ABC):
    """
    Abstract base class for trading strategies.

    A Strategy encapsulates the logic for:
    1. What tickers it needs data for
    2. How to evaluate signals and generate positions
    3. What type of strategy it is (for categorization)

    Subclasses implement specific trading logic (directional, pairs, etc.)
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this strategy instance."""

    @property
    @abstractmethod
    def strategy_type(self) -> StrategyType:
        """Type of strategy for categorization and reporting."""

    @property
    @abstractmethod
    def required_tickers(self) -> list[str]:
        """
        List of tickers this strategy needs data for.

        The orchestrator uses this to load required market data
        and signal data before evaluation.
        """

    @abstractmethod
    def evaluate(
        self,
        signals: dict[str, pl.DataFrame],
        market_data: dict[str, pl.DataFrame],
        as_of_date: date,
    ) -> StrategySignal | None:
        """
        Evaluate the strategy at a specific point in time.

        Parameters
        ----------
        signals : dict[str, pl.DataFrame]
            Processed signal data keyed by ticker.
            Each DataFrame contains signal columns with earnings_date.
        market_data : dict[str, pl.DataFrame]
            Daily market data keyed by ticker.
            Each DataFrame has date, close, volume, etc.
        as_of_date : date
            The date to evaluate (typically an earnings date or signal date)

        Returns
        -------
        StrategySignal | None
            The signal/position to take, or None if no trade
        """

    @abstractmethod
    def compute_positions(
        self,
        market_data: pl.DataFrame,
        signals: pl.DataFrame | None = None,
    ) -> pl.DataFrame:
        """
        Vectorized batch position computation for fast backtesting.

        Mirrors the logic in `evaluate` but operates over the full DataFrame.
        All implementations must avoid look-ahead bias.

        Parameters
        ----------
        market_data : pl.DataFrame
            Daily OHLCV data with columns: date, close, volume, etc.
        signals : pl.DataFrame | None
            Signal data (earnings dates, scores, etc.). Required for
            signal-based strategies, ignored by price-only strategies.

        Returns
        -------
        pl.DataFrame
            Input DataFrame with added columns:
            - position: float (1.0 / -1.0 / 0.0)
            - signal_strength: float
            - confidence: float (0.0 to 1.0)
        """

    def get_signal_value(
        self,
        signals: dict[str, pl.DataFrame],
        ticker: str,
        signal_col: str,
        as_of_date: date,
        date_col: str = "earnings_date",
    ) -> float | None:
        """
        Helper to extract a signal value for a ticker at a date.

        Parameters
        ----------
        signals : dict[str, pl.DataFrame]
            Signal data keyed by ticker
        ticker : str
            Ticker to get signal for
        signal_col : str
            Column name containing the signal
        as_of_date : date
            Date to look up
        date_col : str
            Date column name in the signal DataFrame

        Returns
        -------
        float | None
            Signal value, or None if not found
        """
        if ticker not in signals:
            return None

        df = signals[ticker]
        if signal_col not in df.columns:
            return None

        # Find the signal at or before as_of_date
        filtered = df.filter(pl.col(date_col).cast(pl.Date) <= as_of_date).sort(
            date_col, descending=True
        )

        if len(filtered) == 0:
            return None

        val = filtered[signal_col][0]
        return float(val) if val is not None else None

    def get_price_return(
        self,
        market_data: dict[str, pl.DataFrame],
        ticker: str,
        as_of_date: date,
        lookback_days: int = 20,
        date_col: str = "date",
        price_col: str = "close",
    ) -> float | None:
        """
        Helper to calculate price return over a lookback period.

        Parameters
        ----------
        market_data : dict[str, pl.DataFrame]
            Market data keyed by ticker
        ticker : str
            Ticker to calculate return for
        as_of_date : date
            End date for return calculation
        lookback_days : int
            Number of trading days to look back
        date_col : str
            Date column name
        price_col : str
            Price column name

        Returns
        -------
        float | None
            Return over the period, or None if insufficient data
        """
        if ticker not in market_data:
            return None

        df = market_data[ticker]
        filtered = df.filter(pl.col(date_col).cast(pl.Date) <= as_of_date).sort(
            date_col, descending=True
        )

        if len(filtered) < lookback_days:
            return None

        current_price = filtered[price_col][0]
        past_price = filtered[price_col][lookback_days - 1]

        if past_price is None or past_price == 0:
            return None

        return float((current_price / past_price) - 1)
