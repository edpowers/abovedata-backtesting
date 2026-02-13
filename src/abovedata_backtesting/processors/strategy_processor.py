"""Strategy processor for grid search optimization over entry × exit combinations.

Two-phase architecture for scalability to 100K+ permutations:
  Phase 1: Build entry cache — one entry.apply() per unique (preprocessor, entry, pos_filter).
  Phase 2: Apply exits — Cython-accelerated exit kernels over cached entry DataFrames.
"""

from __future__ import annotations

import datetime as dt
import os
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from itertools import product as itertools_product
from typing import Any, Literal

import numpy as np
import polars as pl
from numpy.typing import NDArray
from tqdm import tqdm
from typing_extensions import Self

from abovedata_backtesting.benchmarks.benchmark_results import (
    BenchmarkResults,
)
from abovedata_backtesting.data_loaders.load_market_data import MarketDataLoader
from abovedata_backtesting.entries.entry_signals import (
    EntryRule,
    enforce_max_entries_fast,
)
from abovedata_backtesting.exits.cython_exits import (
    enforce_max_entries_cy,
    fixed_holding_exit_cy,
    stop_loss_take_profit_exit_cy,
    trailing_stop_exit_cy,
)
from abovedata_backtesting.exits.exit_strategies import (
    ExitRule,
    FixedHoldingExit,
    SignalChangeExit,
    StopLossTakeProfitExit,
    TrailingStopExit,
)
from abovedata_backtesting.model.metrics import BacktestMetrics
from abovedata_backtesting.processors.signal_preprocessor import (
    IdentityPreprocessor,
    SignalPreprocessor,
)
from abovedata_backtesting.trades.trade_log import TradeLog

Preprocessor = SignalPreprocessor | IdentityPreprocessor


@dataclass(slots=True)
class _CachedArrays:
    """Pre-extracted numpy arrays from a daily DataFrame for fast exit evaluation."""

    positions: NDArray[np.float64]
    closes: NDArray[np.float64]
    highs: NDArray[np.float64]
    lows: NDArray[np.float64]
    asset_returns: NDArray[np.float64]
    benchmark_returns: NDArray[np.float64]
    signal_ids: NDArray[np.int32]
    strengths: NDArray[np.float64]
    confs: NDArray[np.float64]
    dates: list[dt.date]
    signal_date_mask: NDArray[np.uint8]

    @classmethod
    def from_daily(
        cls,
        daily: pl.DataFrame,
        signal_dates: frozenset[dt.date] | None = None,
    ) -> _CachedArrays:
        """Extract all arrays from a daily DataFrame once."""
        dates = daily["date"].to_list()

        signal_mask = np.zeros(len(dates), dtype=np.uint8)
        if signal_dates:
            for i, d in enumerate(dates):
                if d in signal_dates:
                    signal_mask[i] = 1

        return cls(
            positions=np.array(
                daily["position"].to_numpy(), dtype=np.float64, copy=True
            ),
            closes=np.array(daily["close"].to_numpy(), dtype=np.float64, copy=True),
            highs=np.array(daily["high"].to_numpy(), dtype=np.float64, copy=True),
            lows=np.array(daily["low"].to_numpy(), dtype=np.float64, copy=True),
            asset_returns=np.array(
                daily["asset_return"].to_numpy(), dtype=np.float64, copy=True
            ),
            benchmark_returns=np.array(
                daily["benchmark_return"].to_numpy(), dtype=np.float64, copy=True
            ),
            signal_ids=(
                np.array(daily["signal_id"].to_numpy(), dtype=np.int32, copy=True)
                if "signal_id" in daily.columns
                else np.zeros(daily.height, dtype=np.int32)
            ),
            strengths=(
                np.array(
                    daily["signal_strength"].to_numpy(),
                    dtype=np.float64,
                    copy=True,
                )
                if "signal_strength" in daily.columns
                else np.zeros(daily.height, dtype=np.float64)
            ),
            confs=(
                np.array(daily["confidence"].to_numpy(), dtype=np.float64, copy=True)
                if "confidence" in daily.columns
                else np.zeros(daily.height, dtype=np.float64)
            ),
            dates=dates,
            signal_date_mask=signal_mask,
        )


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
    daily_df: pl.DataFrame | None
    entry_params: dict[str, Any]
    exit_params: dict[str, Any]
    sanity: SanityFlags
    max_entries_per_signal: int = 1
    preprocessor_name: str = "identity"
    preprocessor_params: dict[str, Any] = field(default_factory=dict)

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
    _preprocessors: list[Preprocessor] = field(
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

    def add_preprocessors(self, preprocessors: Sequence[Preprocessor]) -> None:
        """Add signal preprocessors to the search space."""
        self._preprocessors.extend(preprocessors)

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
        """Run full cartesian product of preprocessor × entry × exit rules.

        Two-phase architecture for performance:
          Phase 1: Build entry cache — one entry.apply() per unique
                   (preprocessor, entry_rule, position_filter) triple.
          Phase 2: Apply all (exit_rule, max_entries) variants to each
                   cached entry result using Cython-accelerated exit kernels.
        """
        self._load_data()
        self._set_defaults()

        results: list[GridSearchResult] = []

        # ── Phase 1: Build entry cache (parallel) ────────────────────
        # Preprocessors run sequentially (few, fast, may share state),
        # then entry.apply() calls run in parallel via ThreadPoolExecutor.
        # Polars releases the GIL during C-level operations, so threads
        # give real parallelism without serialization overhead.
        preprocessed_cache: dict[str, pl.DataFrame] = {}
        # Key: (pp_name, entry_name, pos_filter) → (daily_df, entry, preprocessor)
        entry_cache: dict[
            tuple[str, str, PositionFilter],
            tuple[pl.DataFrame, EntryRule, Preprocessor],
        ] = {}

        # Pre-compute preprocessor outputs (few, fast — no parallelism needed)
        for pp in self._preprocessors:
            if pp.name not in preprocessed_cache:
                preprocessed_cache[pp.name] = pp.apply(self.signals.clone())

        # Deduplicate entry combos
        entry_combos: list[tuple[str, EntryRule, PositionFilter, Preprocessor]] = []
        seen_keys: set[tuple[str, str, PositionFilter]] = set()
        for preprocessor, entry, pos_filter in itertools_product(
            self._preprocessors,
            self._entry_rules,
            self._position_filters,
        ):
            cache_key = (preprocessor.name, entry.name, pos_filter)
            if cache_key not in seen_keys:
                seen_keys.add(cache_key)
                entry_combos.append(
                    (preprocessor.name, entry, pos_filter, preprocessor)
                )

        n_workers = min(os.cpu_count() or 4, len(entry_combos))

        def _compute_entry(
            pp_name: str,
            entry: EntryRule,
            pos_filter: PositionFilter,
        ) -> tuple[
            tuple[str, str, PositionFilter],
            pl.DataFrame | None,
        ]:
            pp_signals = preprocessed_cache[pp_name]
            daily = entry.apply(self._market_data.clone(), pp_signals)
            if "position" not in daily.columns:
                return (pp_name, entry.name, pos_filter), None
            daily = self._apply_position_filter(daily, pos_filter)
            return (pp_name, entry.name, pos_filter), daily

        with ThreadPoolExecutor(max_workers=n_workers) as pool:
            futures = {
                pool.submit(_compute_entry, pp_name, entry, pos_filter): (
                    pp_name,
                    entry,
                    pos_filter,
                    preprocessor,
                )
                for pp_name, entry, pos_filter, preprocessor in entry_combos
            }
            with tqdm(
                total=len(futures),
                desc=f"Building entry cache ({n_workers} threads)",
                disable=not self.debug,
            ) as pbar:
                for future in as_completed(futures):
                    pp_name, entry, pos_filter, preprocessor = futures[future]
                    cache_key, daily = future.result()
                    if daily is not None:
                        entry_cache[cache_key] = (daily, entry, preprocessor)
                    pbar.update(1)

        # ── Phase 2: Apply exits to cached entries ───────────────────
        # Collect signal_dates from FixedHoldingExit rules for cache extraction
        signal_dates: frozenset[dt.date] | None = None
        for er in self._exit_rules:
            if isinstance(er, FixedHoldingExit) and er.signal_dates:
                signal_dates = er.signal_dates
                break

        total_combos = (
            len(entry_cache) * len(self._exit_rules) * len(self.max_entries_per_signal)
        )

        with tqdm(
            total=total_combos, desc="Evaluating exits", disable=not self.debug
        ) as pbar:
            for (
                _pp_name,
                _entry_name,
                pos_filter,
            ), (base_daily, entry, preprocessor) in entry_cache.items():
                # Pre-extract arrays once per entry cache key
                arrays = _CachedArrays.from_daily(base_daily, signal_dates)

                for exit_rule in self._exit_rules:
                    for max_entries in self.max_entries_per_signal:
                        pbar.update(1)
                        if result := self._evaluate_arrays(
                            arrays,
                            base_daily,
                            entry,
                            exit_rule,
                            pos_filter,
                            max_entries,
                            preprocessor,
                        ):
                            results.append(result)

        summary_df = self._build_summary(results, optimize_by)

        # ── Phase 3: Reconstruct daily_df for top results ────────────
        # Rebuild DataFrames only for results that need them (robustness
        # tests, reports). The rest stay as daily_df=None for memory.
        sorted_results = [results[i] for i in summary_df["_original_idx"].to_list()]
        self._rebuild_daily_df(sorted_results, entry_cache)

        return summary_df.drop("_original_idx"), sorted_results

    @staticmethod
    def _rebuild_daily_df(
        sorted_results: list[GridSearchResult],
        entry_cache: dict[
            tuple[str, str, PositionFilter],
            tuple[pl.DataFrame, EntryRule, Preprocessor],
        ],
        max_rebuild: int = 50,
    ) -> None:
        """Reconstruct daily_df for the top results that need it.

        Only rebuilds up to `max_rebuild` results to avoid O(N) overhead
        when N is large. Downstream analysis (robustness tests, reports)
        typically uses only the top 5-10 results.
        """
        rebuilt = 0
        for result in sorted_results:
            if rebuilt >= max_rebuild:
                break
            if result.daily_df is not None:
                rebuilt += 1
                continue
            cache_key = (
                result.preprocessor_name,
                result.entry_rule.name,
                result.position_filter,
            )
            if cache_key not in entry_cache:
                continue
            base_daily = entry_cache[cache_key][0]
            daily = result.exit_rule.apply_fast(base_daily)
            daily = enforce_max_entries_fast(
                daily,
                max_entries_per_signal=result.max_entries_per_signal,
            )
            result.daily_df = daily.with_columns(
                (pl.col("asset_return") * pl.col("position")).alias("strategy_return"),
            )
            rebuilt += 1

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
        if not self._preprocessors:
            self._preprocessors = [IdentityPreprocessor()]

    def _evaluate_arrays(
        self,
        arrays: _CachedArrays,
        base_daily: pl.DataFrame,
        entry: EntryRule,
        exit_rule: ExitRule,
        pos_filter: PositionFilter,
        max_entries: int,
        preprocessor: Preprocessor | None = None,
    ) -> GridSearchResult | None:
        """Evaluate one exit variant using pre-extracted numpy arrays.

        Operates entirely on numpy arrays, bypassing Polars overhead for
        exit application, strategy return computation, trade log building,
        and metrics calculation.
        """
        positions = arrays.positions

        # 3. Apply exit rule directly on numpy arrays
        exit_prices: NDArray[np.float64] | None = None
        if isinstance(exit_rule, SignalChangeExit):
            new_pos = positions
        elif isinstance(exit_rule, FixedHoldingExit):
            new_pos = fixed_holding_exit_cy(
                positions, arrays.signal_date_mask, exit_rule.holding_days
            )
        elif isinstance(exit_rule, TrailingStopExit):
            new_pos, exit_prices = trailing_stop_exit_cy(
                positions,
                arrays.closes,
                arrays.highs,
                arrays.lows,
                exit_rule.trailing_stop_pct,
            )
        elif isinstance(exit_rule, StopLossTakeProfitExit):
            new_pos, exit_prices = stop_loss_take_profit_exit_cy(
                positions,
                arrays.closes,
                arrays.highs,
                arrays.lows,
                exit_rule.stop_loss_pct,
                exit_rule.take_profit_pct,
            )
        else:
            # Fallback for unknown exit types
            daily = exit_rule.apply_fast(base_daily)
            daily = enforce_max_entries_fast(daily, max_entries_per_signal=max_entries)
            daily = daily.with_columns(
                (pl.col("asset_return") * pl.col("position")).alias("strategy_return"),
            )
            trade_log = TradeLog.from_daily(daily)
            if trade_log.n_trades == 0:
                return None
            metrics = BacktestMetrics.from_dataframe(
                daily, benchmark_ticker=self.benchmark_ticker
            )
            sanity = SanityFlags.from_result(
                metrics, trade_log.n_trades, self.sanity_config
            )
            pp_name = preprocessor.name if preprocessor is not None else "identity"
            pp_params = preprocessor.params() if preprocessor is not None else {}
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
                preprocessor_name=pp_name,
                preprocessor_params=pp_params,
            )

        # 4. Enforce max entries
        new_pos = enforce_max_entries_cy(new_pos, arrays.signal_ids, max_entries)

        # 5. Strategy return = asset_return * position (numpy multiply)
        strategy_returns = arrays.asset_returns * new_pos

        # 6. Build trade log from arrays (fast path, no Polars)
        # Use exit_prices for close if available (stop/trailing exits)
        trade_closes = exit_prices if exit_prices is not None else arrays.closes
        trade_log = TradeLog.from_arrays(
            new_pos, arrays.dates, trade_closes, arrays.strengths, arrays.confs
        )

        if trade_log.n_trades == 0:
            return None

        # 7. Compute metrics from numpy arrays directly (skip Polars conversion)
        metrics = BacktestMetrics.from_daily(
            strategy_returns=strategy_returns,
            asset_returns=arrays.asset_returns,
            benchmark_returns=arrays.benchmark_returns,
            positions=new_pos,
            start_date=arrays.dates[0] if arrays.dates else None,
            end_date=arrays.dates[-1] if arrays.dates else None,
            benchmark_ticker=self.benchmark_ticker,
        )

        # 8. Sanity check
        sanity = SanityFlags.from_result(
            metrics, trade_log.n_trades, self.sanity_config
        )

        pp_name = preprocessor.name if preprocessor is not None else "identity"
        pp_params = preprocessor.params() if preprocessor is not None else {}

        return GridSearchResult(
            entry_rule=entry,
            exit_rule=exit_rule,
            position_filter=pos_filter,
            metrics=metrics,
            trade_log=trade_log,
            daily_df=None,  # Defer DataFrame construction to top-N only
            entry_params=entry.params(),
            exit_params={"exit_type": exit_rule.name},
            sanity=sanity,
            max_entries_per_signal=max_entries,
            preprocessor_name=pp_name,
            preprocessor_params=pp_params,
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
                "pp_name": r.preprocessor_name,
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
