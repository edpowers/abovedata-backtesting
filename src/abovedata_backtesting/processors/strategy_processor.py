"""Strategy processor for grid search optimization over entry × exit combinations."""

import datetime as dt
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Literal

import polars as pl
from tqdm.contrib.itertools import product
from typing_extensions import Self

from abovedata_backtesting.benchmarks.benchmark_results import (
    BenchmarkResults,
)
from abovedata_backtesting.data_loaders.load_market_data import MarketDataLoader
from abovedata_backtesting.entries.entry_signals import EntryRule, enforce_max_entries
from abovedata_backtesting.exits.exit_strategies import ExitRule, SignalChangeExit
from abovedata_backtesting.model.metrics import BacktestMetrics
from abovedata_backtesting.trades.trade_log import TradeLog

# =============================================================================
# Position Filter
# =============================================================================

PositionFilter = Literal["long_short", "long_only", "short_only"]

# =============================================================================
# Sanity Validation
# =============================================================================


@dataclass(frozen=True, slots=True)
class SanityConfig:
    """Thresholds for flagging suspicious results."""

    max_annualized_return: float = 2.0  # 200%
    max_sharpe_ratio: float = 3.0
    min_trade_count: int = 10
    min_time_in_market: float = 0.05  # 5%


@dataclass(frozen=True, slots=True)
class SanityFlags:
    """Validation flags for a single result."""

    excessive_return: bool = False
    excessive_sharpe: bool = False
    too_few_trades: bool = False
    too_little_exposure: bool = False

    @property
    def is_suspicious(self) -> bool:
        return any(
            [
                self.excessive_return,
                self.excessive_sharpe,
                self.too_few_trades,
                self.too_little_exposure,
            ]
        )

    @property
    def flags_list(self) -> list[str]:
        flags = []
        if self.excessive_return:
            flags.append("excessive_return")
        if self.excessive_sharpe:
            flags.append("excessive_sharpe")
        if self.too_few_trades:
            flags.append("too_few_trades")
        if self.too_little_exposure:
            flags.append("too_little_exposure")
        return flags

    @classmethod
    def from_result(
        cls, metrics: BacktestMetrics, trade_count: int, config: SanityConfig
    ) -> "Self":
        return cls(
            excessive_return=abs(metrics.returns.annualized_return)
            > config.max_annualized_return,
            excessive_sharpe=abs(metrics.risk.sharpe_ratio) > config.max_sharpe_ratio,
            too_few_trades=trade_count < config.min_trade_count,
            too_little_exposure=metrics.exposure.time_in_market
            < config.min_time_in_market,
        )


# =============================================================================
# Grid Search Result
# =============================================================================


@dataclass
class GridSearchResult:
    """Single result from one entry × exit combination."""

    entry_rule: EntryRule
    exit_rule: ExitRule
    position_filter: PositionFilter
    metrics: BacktestMetrics
    trade_log: TradeLog
    daily_df: pl.DataFrame
    entry_params: dict[str, Any]
    exit_params: dict[str, Any]
    sanity: SanityFlags
    max_entries_per_signal: int = 1

    @property
    def trade_count(self) -> int:
        return self.trade_log.n_trades

    def summarize(self) -> dict[str, str | int | float | dict[str, Any]]:
        return {
            "entry": self.entry_rule.name,
            "exit": self.exit_rule.name,
            "entry_params": self.entry_params,
            "exit_params": self.exit_params,
            "sharpe": self.metrics.risk.sharpe_ratio,
            "total_return": self.trade_log.total_return,
            "annualized_return": self.metrics.returns.annualized_return,
            "max_drawdown": self.metrics.risk.max_drawdown,
        }

    def make_key(self) -> str:
        return f"{self.entry_rule.name} × {self.exit_rule.name}"

    def make_safe_name(self) -> str:
        return (
            self.make_key().replace(" × ", "__").replace("/", "_").replace("%", "pct")
        )


@dataclass
class GridSearchResults:
    results: list[GridSearchResult]

    def return_sorted(
        self, sort_by: str = "total_return", min_trades: int = 5
    ) -> list[GridSearchResult]:
        eligible = [r for r in self.results if r.trade_log.n_trades >= min_trades]

        if sort_by == "sharpe":

            def get_sort_by(r: Any) -> float:
                return r.metrics.risk.sharpe_ratio
        else:

            def get_sort_by(r: Any) -> float:
                return getattr(r.trade_log, sort_by)

        return sorted(eligible, key=lambda r: get_sort_by(r), reverse=True)

    def top_results_queued(
        self, top_n: int = 5, min_trades: int = 5
    ) -> list[tuple[str, GridSearchResult]]:
        """Top results by sharpe and total_return, deduplicated."""
        seen: set[str] = set()
        queue: list[tuple[str, GridSearchResult]] = []
        for sort_by in (
            "total_return",
            "sharpe",
        ):
            for r in self.return_sorted(sort_by, min_trades=min_trades)[:top_n]:
                if (key := r.make_key()) not in seen:
                    seen.add(key)
                    queue.append((sort_by, r))
        return queue


# =============================================================================
# Strategy Processor
# =============================================================================


@dataclass
class StrategyProcessor:
    """
    Grid search over entry × exit combinations for a single ticker.

    Entries only fire on signal-derived dates (earnings_date - N trading days).
    Returns are computed from the trade log (entry close → exit close),
    avoiding the daily compounding illusion.

    Usage:
        processor = StrategyProcessor(
            ticker="DE",
            signals=df_fc_joined,
            visible_col="visible_revenue",
            start_date=date(2015, 1, 1),
        )

        processor.add_entries(
            MomentumEntry.grid(
                lookback_days=[10, 20],
                zscore_threshold=[0.5, 1.0],
                entry_days_before=[0, 1, 5, 10, 20],
            ),
        )
        processor.add_exits([
            SignalChangeExit(),
            FixedHoldingExit(holding_days=30, signal_dates=...),
            TrailingStopExit(trailing_stop_pct=0.05),
        ])

        results_df, results = processor.run(optimize_by="sharpe_ratio")
    """

    ticker: str
    signals: pl.DataFrame
    benchmarks: BenchmarkResults
    benchmark_ticker: str = "SPY"
    visible_col: str = "visible_revenue"
    start_date: dt.date | None = None
    end_date: dt.date | None = None
    sanity_config: SanityConfig = field(default_factory=SanityConfig)
    debug: bool = False

    _entry_rules: list[EntryRule] = field(default_factory=list, init=False, repr=False)
    _exit_rules: list[ExitRule] = field(default_factory=list, init=False, repr=False)
    _position_filters: list[PositionFilter] = field(
        default_factory=list, init=False, repr=False
    )
    _market_data: pl.DataFrame = field(
        default_factory=pl.DataFrame, init=False, repr=False
    )
    _benchmark_data: pl.DataFrame | None = field(default=None, init=False, repr=False)

    _buy_hold_cache: dict[tuple[dt.date, dt.date], float] = field(
        default_factory=dict, init=False, repr=False
    )
    max_entries_per_signal: list[int] = field(default_factory=lambda: [1])

    def add_entries(self, rules: Sequence[EntryRule]) -> None:
        """Add entry rules to the search space."""
        self._entry_rules.extend(rules)

    def add_exits(self, rules: Sequence[ExitRule]) -> None:
        """Add exit rules to the search space."""
        self._exit_rules.extend(rules)

    def add_position_filters(self, filters: Sequence[PositionFilter]) -> None:
        """Add position filters to the search space."""
        self._position_filters.extend(filters)

    def run(
        self,
        optimize_by: str = "sharpe_ratio",
    ) -> tuple[pl.DataFrame, list[GridSearchResult]]:
        """Run full cartesian product of entry × exit rules."""
        self._load_data()
        self._set_defaults()

        results: list[GridSearchResult] = []

        combos = product(
            self._entry_rules,
            self._exit_rules,
            self._position_filters,
            self.max_entries_per_signal,
        )

        for entry, exit_rule, pos_filter, max_entries in combos:
            if result := self._evaluate_combination(
                entry, exit_rule, pos_filter, max_entries
            ):
                results.append(result)

        summary_df = self._build_summary(results, optimize_by)

        return summary_df.drop("_original_idx"), [
            results[i] for i in summary_df["_original_idx"].to_list()
        ]

    # ── Internal ─────────────────────────────────────────────────────────

    def _load_data(self) -> None:
        """Load and prepare market data."""
        if not self._market_data.is_empty():
            return

        self._market_data = (
            MarketDataLoader(self.ticker)
            .with_returns()
            .filter_dates(start_date=self.start_date, end_date=self.end_date)
            .collect()
        )
        # Pre-join benchmark returns once
        self._market_data = self._market_data.join(
            self.benchmarks.get_daily_returns(self.benchmark_ticker),
            on="date",
            how="inner",
        )

    def get_buy_hold_return(self, start_date: dt.date, end_date: dt.date) -> float:
        """Get buy-and-hold return for the primary ticker over a date range."""
        aligned = self._market_data.filter(
            (pl.col("date") >= start_date) & (pl.col("date") <= end_date)
        )
        return float(aligned["close"][-1] / aligned["close"][0] - 1)

    def get_buy_hold_return_dict(
        self, start_date: dt.date, end_date: dt.date
    ) -> dict[str, float]:
        """Get buy-and-hold total and annualized return for the primary ticker."""
        aligned = self._market_data.filter(
            (pl.col("date") >= start_date) & (pl.col("date") <= end_date)
        )
        total = float(aligned["close"][-1] / aligned["close"][0] - 1)
        n_trading_days = aligned.height
        annualized = (1 + total) ** (252 / max(n_trading_days, 1)) - 1
        return {
            "buy_hold_total_return": total,
            "buy_hold_annualized_return": annualized,
        }

    def _set_defaults(self) -> None:
        if not self._entry_rules:
            raise ValueError("No entry rules defined. Call add_entries() first.")
        if not self._exit_rules:
            self._exit_rules = [SignalChangeExit()]
        if not self._position_filters:
            self._position_filters = ["long_short"]  # Default: no filtering

    def _evaluate_combination(
        self,
        entry: EntryRule,
        exit_rule: ExitRule,
        pos_filter: PositionFilter,
        max_entries: int,
    ) -> GridSearchResult | None:
        """Run one entry × exit × position_filter combination and compute metrics."""
        assert self._market_data is not None

        # 1. Entry rule computes positions (sparse, on signal-derived dates)
        daily = entry.apply(self._market_data.clone(), self.signals)

        if "position" not in daily.columns:
            return None

        # 2. Apply position filter (long_only, short_only, or long_short)
        daily = self._apply_position_filter(daily, pos_filter)

        # 3. Exit rule modifies positions (trims holding periods)
        daily = exit_rule.apply(daily)

        daily = enforce_max_entries(
            daily,
            max_entries_per_signal=max_entries,
        )

        # 4. Compute daily returns
        daily = daily.with_columns(
            (pl.col("asset_return") * pl.col("position")).alias("strategy_return"),
        )

        # 5. Build trade log
        trade_log = TradeLog.from_daily(daily)

        if trade_log.n_trades == 0:
            return None

        # 7. Compute metrics
        metrics = BacktestMetrics.from_dataframe(
            daily, benchmark_ticker=self.benchmark_ticker
        )
        # 8. Sanity check
        sanity = SanityFlags.from_result(
            metrics, trade_log.n_trades, self.sanity_config
        )

        return GridSearchResult(
            entry_rule=entry,
            exit_rule=exit_rule,
            position_filter=pos_filter,
            metrics=metrics,
            trade_log=trade_log,
            daily_df=daily,
            entry_params=entry.params(),
            exit_params={"exit_type": exit_rule.name},
            sanity=sanity,
            max_entries_per_signal=max_entries,
        )

    def _apply_position_filter(
        self, daily: pl.DataFrame, pos_filter: PositionFilter
    ) -> pl.DataFrame:
        """
        Filter positions based on position_filter setting.

        - "long_short": No filtering (default), keep all positions
        - "long_only": Zero out negative positions (short → flat)
        - "short_only": Zero out positive positions (long → flat)
        """
        if pos_filter == "long_short":
            return daily

        if pos_filter == "long_only":
            # Keep only positive positions, zero out shorts
            return daily.with_columns(
                pl.when(pl.col("position") > 0)
                .then(pl.col("position"))
                .otherwise(0.0)
                .alias("position")
            )

        if pos_filter == "short_only":
            # Keep only negative positions, zero out longs
            return daily.with_columns(
                pl.when(pl.col("position") < 0)
                .then(pl.col("position"))
                .otherwise(0.0)
                .alias("position")
            )

        # Should not reach here due to Literal type, but defensive
        return daily

    def _build_summary(
        self, results: list[GridSearchResult], optimize_by: str
    ) -> pl.DataFrame:
        """Build summary DataFrame from results, sorted by optimization metric."""
        rows: list[dict[str, Any]] = []
        for i, r in enumerate(results):
            row: dict[str, Any] = {
                "_original_idx": i,
                "entry_name": r.entry_rule.name,
                "exit_name": r.exit_rule.name,
                "position_filter": r.position_filter,
                "max_entries_per_signal": r.max_entries_per_signal,
                # Trade log stats
                **{f"trade_{k}": v for k, v in r.trade_log.summary().items()},
                # Metrics
                # Sanity
                "is_suspicious": r.sanity.is_suspicious,
                "sanity_flags": ", ".join(r.sanity.flags_list)
                if r.sanity.is_suspicious
                else "",
            } | r.metrics.make_dict()
            # Flatten entry/exit params
            row.update({f"entry_{k}": v for k, v in r.entry_params.items()})
            row.update({f"exit_{k}": v for k, v in r.exit_params.items()})
            rows.append(row)

        df = pl.DataFrame(rows)

        sort_col = _resolve_metric_col(optimize_by, df.columns)
        return df.sort(sort_col, descending=True)


def _resolve_metric_col(name: str, columns: list[str]) -> str:
    """Resolve a metric name to a column name."""
    if name in columns:
        return name
    aliases = {
        "sharpe": "sharpe_ratio",
        "sortino": "sortino_ratio",
        "calmar": "calmar_ratio",
        "alpha": "timing_alpha",
        "return": "annualized_return",
        "trades": "trade_n_trades",
    }
    resolved = aliases.get(name, name)
    if resolved not in columns:
        raise ValueError(f"Unknown metric '{name}'. Available: {columns}")
    return resolved
