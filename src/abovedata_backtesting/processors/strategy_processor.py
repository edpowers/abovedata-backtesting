"""Strategy processor for grid search optimization over entry × exit combinations."""

import datetime as dt
import warnings
from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import product
from typing import Any

import polars as pl
from typing_extensions import Self

from abovedata_backtesting.data_loaders.load_market_data import MarketDataLoader
from abovedata_backtesting.entries.entry_signals import EntryRule
from abovedata_backtesting.exits.exit_strategies import ExitRule, SignalChangeExit
from abovedata_backtesting.model.metrics import BacktestMetrics
from abovedata_backtesting.trades.trade_log import TradeLog

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
    metrics: BacktestMetrics
    trade_log: TradeLog
    daily_df: pl.DataFrame
    entry_params: dict[str, Any]
    exit_params: dict[str, Any]
    sanity: SanityFlags

    @property
    def trade_count(self) -> int:
        return self.trade_log.n_trades


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
    visible_col: str = "visible_revenue"
    benchmark_ticker: str = "SPY"
    start_date: dt.date | None = None
    end_date: dt.date | None = None
    sanity_config: SanityConfig = field(default_factory=SanityConfig)
    debug: bool = False

    _entry_rules: list[EntryRule] = field(default_factory=list, init=False, repr=False)
    _exit_rules: list[ExitRule] = field(default_factory=list, init=False, repr=False)
    _market_data: pl.DataFrame | None = field(default=None, init=False, repr=False)
    _benchmark_data: pl.DataFrame | None = field(default=None, init=False, repr=False)

    def add_entries(self, rules: Sequence[EntryRule]) -> None:
        """Add entry rules to the search space."""
        self._entry_rules.extend(rules)

    def add_exits(self, rules: Sequence[ExitRule]) -> None:
        """Add exit rules to the search space."""
        self._exit_rules.extend(rules)

    def run(
        self,
        optimize_by: str = "sharpe_ratio",
        exclude_suspicious: bool = False,
    ) -> tuple[pl.DataFrame, list[GridSearchResult]]:
        """
        Run full cartesian product of entry × exit rules.

        Parameters
        ----------
        optimize_by : str
            Metric to sort results by.
        exclude_suspicious : bool
            If True, filter out results that fail sanity checks.

        Returns
        -------
        tuple[pl.DataFrame, list[GridSearchResult]]
            Summary DataFrame + structured results, both sorted by optimize_by.
        """
        self._load_data()

        if not self._entry_rules:
            raise ValueError("No entry rules defined. Call add_entries() first.")
        if not self._exit_rules:
            self._exit_rules = [SignalChangeExit()]

        results: list[GridSearchResult] = []
        n_combos = len(self._entry_rules) * len(self._exit_rules)

        if self.debug:
            print(
                f"🔍 Running grid search: {len(self._entry_rules)} entries "
                f"× {len(self._exit_rules)} exits = {n_combos} combinations"
            )

        for i, (entry, exit_rule) in enumerate(
            product(self._entry_rules, self._exit_rules)
        ):
            if self.debug and (i + 1) % 10 == 0:
                print(f"  [{i + 1}/{n_combos}] {entry.name} × {exit_rule.name}")

            result = self._evaluate_combination(entry, exit_rule)
            if result is not None:
                results.append(result)

        if not results:
            raise ValueError(
                "No valid results produced. Check entry/exit rules and data."
            )

        if exclude_suspicious:
            clean = [r for r in results if not r.sanity.is_suspicious]
            n_removed = len(results) - len(clean)
            if n_removed > 0 and self.debug:
                print(f"⚠️  Excluded {n_removed} suspicious results")
            if not clean:
                warnings.warn(
                    "All results failed sanity checks. Returning all results unfiltered.",
                    stacklevel=2,
                )
            else:
                results = clean

        summary_df = self._build_summary(results, optimize_by)
        sort_idx = summary_df["_original_idx"].to_list()
        results = [results[i] for i in sort_idx]
        summary_df = summary_df.drop("_original_idx")

        if self.debug:
            best = results[0]
            print(
                f"\n🏆 Best: {best.entry_rule.name} × {best.exit_rule.name}"
                f" ({optimize_by}={_get_col_val(summary_df, optimize_by, 0):.4f})"
                f" | trades={best.trade_count}"
            )
            if best.sanity.is_suspicious:
                print(f"   ⚠️  Flags: {', '.join(best.sanity.flags_list)}")

        return summary_df, results

    # ── Internal ─────────────────────────────────────────────────────────

    def _load_data(self) -> None:
        """Load and prepare market data."""
        if self._market_data is not None:
            return

        self._market_data = (
            MarketDataLoader(self.ticker)
            .with_returns()
            .filter_dates(start_date=self.start_date, end_date=self.end_date)
            .collect()
        )
        self._benchmark_data = (
            MarketDataLoader(self.benchmark_ticker)
            .with_returns()
            .filter_dates(start_date=self.start_date, end_date=self.end_date)
            .collect()
        )

    def _evaluate_combination(
        self, entry: EntryRule, exit_rule: ExitRule
    ) -> GridSearchResult | None:
        """Run one entry × exit combination and compute metrics."""
        assert self._market_data is not None

        # 1. Entry rule computes positions (sparse, on signal-derived dates)
        daily = entry.apply(self._market_data.clone(), self.signals)

        if "position" not in daily.columns:
            return None

        # 2. Exit rule modifies positions (trims holding periods)
        daily = exit_rule.apply(daily)

        # 3. Compute daily returns
        daily = daily.with_columns(
            (pl.col("asset_return") * pl.col("position")).alias("strategy_return"),
        )

        # 4. Build trade log
        trade_log = TradeLog.from_daily(daily)

        if trade_log.n_trades == 0:
            return None

        # 5. Join benchmark
        daily = self._join_benchmark(daily)
        # 6. Compute metrics
        metrics = BacktestMetrics.from_dataframe(
            daily, benchmark_ticker=self.benchmark_ticker
        )
        # 7. Sanity check
        sanity = SanityFlags.from_result(
            metrics, trade_log.n_trades, self.sanity_config
        )

        return GridSearchResult(
            entry_rule=entry,
            exit_rule=exit_rule,
            metrics=metrics,
            trade_log=trade_log,
            daily_df=daily,
            entry_params=entry.params(),
            exit_params={"exit_type": exit_rule.name},
            sanity=sanity,
        )

    def _join_benchmark(self, daily: pl.DataFrame) -> pl.DataFrame:
        """Join benchmark returns onto daily DataFrame."""
        if self._benchmark_data is not None and "benchmark_return" not in daily.columns:
            bm = self._benchmark_data.select(
                "date",
                pl.col("asset_return").alias("benchmark_return"),
            )
            daily = daily.join(bm, on="date", how="inner")
        elif "benchmark_return" not in daily.columns:
            daily = daily.with_columns(
                pl.col("asset_return").alias("benchmark_return"),
            )
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


def _get_col_val(df: pl.DataFrame, col: str, row: int) -> float:
    """Safely get a float value from a DataFrame."""
    resolved = _resolve_metric_col(col, df.columns)
    val = df[resolved][row]
    return float(val) if val is not None else 0.0
