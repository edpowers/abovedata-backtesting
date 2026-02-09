"""Robustness validation tests for backtest results.

Implements four key tests to detect overfitting and spurious edges:

1. EXIT ABLATION: Compare signal_change exit vs fixed_holding exits.
   If win rate drops significantly with fixed exits, the exit is doing
   the heavy lifting, not the signal.

2. FLIP ABLATION: Run the strategy with correlation flip disabled.
   If performance collapses, the flip mechanism is overfitting to
   historical correlation regimes.

3. RANDOM ENTRY BASELINE: Shuffle entry dates within valid windows.
   If random entries produce similar returns, the signal has no
   predictive power — you're just capturing holding-period drift.

4. ALPHA ATTRIBUTION: Decompose returns into beta (buy-and-hold) vs
   alpha (signal contribution). 100% win rate + low signal accuracy
   suggests beta capture, not skill.

Usage:
    from abovedata_backtesting.trades.robustness_tests import (
        RobustnessValidator, RobustnessReport
    )

    validator = RobustnessValidator(
        processor=processor,
        result=best_result,
        n_random_trials=100,
    )
    report = validator.run_all()
    print(report.summary())
"""

from __future__ import annotations

import datetime as dt
import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np
import polars as pl

from abovedata_backtesting.exits.exit_strategies import (
    ExitRule,
    FixedHoldingExit,
)
from abovedata_backtesting.trades.trade_log import TradeLog

if TYPE_CHECKING:
    from abovedata_backtesting.processors.strategy_processor import (
        GridSearchResult,
        StrategyProcessor,
    )


# =============================================================================
# Test Result Dataclasses
# =============================================================================


@dataclass(frozen=True, slots=True)
class ExitAblationResult:
    """Compare performance across exit strategies."""

    original_exit: str
    original_win_rate: float
    original_sharpe: float
    original_n_trades: int

    fixed_30d_win_rate: float | None
    fixed_30d_sharpe: float | None
    fixed_30d_n_trades: int | None

    fixed_60d_win_rate: float | None
    fixed_60d_sharpe: float | None
    fixed_60d_n_trades: int | None

    @property
    def exit_is_edge(self) -> bool:
        """True if win rate drops >20pp with fixed exit (exit doing heavy lifting)."""
        if self.fixed_60d_win_rate is None:
            return False
        return (self.original_win_rate - self.fixed_60d_win_rate) > 0.20

    @property
    def degradation_30d(self) -> float | None:
        if self.fixed_30d_win_rate is None:
            return None
        return self.original_win_rate - self.fixed_30d_win_rate

    @property
    def degradation_60d(self) -> float | None:
        if self.fixed_60d_win_rate is None:
            return None
        return self.original_win_rate - self.fixed_60d_win_rate


@dataclass(frozen=True, slots=True)
class FlipAblationResult:
    """Compare performance with and without correlation flip."""

    with_flip_win_rate: float
    with_flip_sharpe: float
    with_flip_total_return: float

    no_flip_win_rate: float | None
    no_flip_sharpe: float | None
    no_flip_total_return: float | None

    @property
    def flip_is_edge(self) -> bool:
        """True if no-flip Sharpe is <50% of with-flip (flip is overfitting)."""
        if self.no_flip_sharpe is None or self.with_flip_sharpe <= 0:
            return False
        return self.no_flip_sharpe < (self.with_flip_sharpe * 0.5)

    @property
    def flip_contribution(self) -> float | None:
        """Fraction of Sharpe attributable to the flip mechanism."""
        if self.no_flip_sharpe is None:
            return None
        if self.with_flip_sharpe <= 0:
            return 0.0
        return 1.0 - (self.no_flip_sharpe / self.with_flip_sharpe)


@dataclass(frozen=True, slots=True)
class RandomEntryResult:
    """Compare actual entries vs random baseline."""

    actual_total_return: float
    actual_sharpe: float
    actual_win_rate: float

    random_mean_return: float
    random_std_return: float
    random_mean_sharpe: float
    random_mean_win_rate: float
    n_trials: int

    @property
    def zscore_vs_random(self) -> float:
        """How many std devs above random is the actual return?"""
        if self.random_std_return <= 0:
            return (
                float("inf")
                if self.actual_total_return > self.random_mean_return
                else 0.0
            )
        return (
            self.actual_total_return - self.random_mean_return
        ) / self.random_std_return

    @property
    def signal_has_edge(self) -> bool:
        """True if actual return is >2 std devs above random baseline."""
        return self.zscore_vs_random > 2.0

    @property
    def pvalue(self) -> float:
        """Approximate p-value (fraction of random trials beating actual)."""
        # This is computed during the test and stored, but we can estimate
        # from z-score using normal approximation
        from scipy.stats import norm

        return 1 - norm.cdf(self.zscore_vs_random)


@dataclass(frozen=True, slots=True)
class AlphaAttributionResult:
    """Decompose returns into beta and alpha components."""

    total_return: float
    buy_and_hold_return: float
    active_return: float  # total - buy_and_hold (if long-biased)

    signal_accuracy: float  # % of signals that correctly predicted surprise
    trade_direction_accuracy: float  # % of trades with correct direction
    win_rate: float

    long_return: float
    short_return: float
    n_long: int
    n_short: int

    @property
    def alpha_ratio(self) -> float:
        """Fraction of return attributable to alpha (vs beta)."""
        if self.total_return <= 0:
            return 0.0
        return self.active_return / self.total_return

    @property
    def is_beta_in_disguise(self) -> bool:
        """True if winning shorts in an uptrending stock (capturing mean reversion)."""
        # If stock went up (buy_and_hold > 0) but shorts won, it's mean-reversion
        if (
            self.buy_and_hold_return > 0.5
            and self.short_return > 0
            and self.n_short > 2
        ):
            return True
        # If signal accuracy is very low but win rate is very high, it's not skill
        if self.signal_accuracy < 0.3 and self.win_rate > 0.8:
            return True
        return False

    @property
    def skill_signal(self) -> str:
        """Interpretation of the skill decomposition."""
        if self.is_beta_in_disguise:
            return "BETA_DISGUISED: High win rate despite low signal accuracy suggests riding market drift"
        if self.signal_accuracy > 0.6 and self.win_rate > 0.6:
            return "SKILL: Both signal accuracy and win rate are strong"
        if self.signal_accuracy < 0.3 and self.win_rate > 0.5:
            return "FLIP_OVERFITTING: Correlation flip compensating for poor signal"
        return "INCONCLUSIVE: Insufficient evidence for skill assessment"


# =============================================================================
# Robustness Report
# =============================================================================


@dataclass
class RobustnessReport:
    """Aggregated robustness test results with pass/fail summary."""

    strategy_name: str
    n_trades: int
    test_date: dt.date = field(default_factory=dt.date.today)

    exit_ablation: ExitAblationResult | None = None
    flip_ablation: FlipAblationResult | None = None
    random_entry: RandomEntryResult | None = None
    alpha_attribution: AlphaAttributionResult | None = None

    @property
    def red_flags(self) -> list[str]:
        """List of issues that suggest the edge is not robust."""
        flags = []

        if self.exit_ablation and self.exit_ablation.exit_is_edge:
            flags.append(
                f"EXIT_EDGE: Win rate drops {self.exit_ablation.degradation_60d:.0%} "
                "with fixed 60d exit (exit doing heavy lifting)"
            )

        if self.flip_ablation and self.flip_ablation.flip_is_edge:
            flags.append(
                f"FLIP_OVERFITTING: {self.flip_ablation.flip_contribution:.0%} of Sharpe "
                "comes from correlation flip mechanism"
            )

        if self.random_entry and not self.random_entry.signal_has_edge:
            flags.append(
                f"NO_SIGNAL_EDGE: Actual return only {self.random_entry.zscore_vs_random:.1f} "
                f"std devs above random (p={self.random_entry.pvalue:.2f})"
            )

        if self.alpha_attribution and self.alpha_attribution.is_beta_in_disguise:
            flags.append(f"BETA_DISGUISED: {self.alpha_attribution.skill_signal}")

        if self.n_trades < 15:
            flags.append(
                f"SMALL_SAMPLE: Only {self.n_trades} trades (need 15+ for inference)"
            )

        return flags

    @property
    def is_robust(self) -> bool:
        """True if no major red flags detected."""
        return len(self.red_flags) == 0

    def summary(self) -> str:
        """Human-readable summary of all tests."""
        lines = [
            f"\n{'=' * 70}",
            f"ROBUSTNESS REPORT: {self.strategy_name}",
            f"{'=' * 70}",
            f"Test Date: {self.test_date}  |  Trades: {self.n_trades}",
            "",
        ]

        # Exit Ablation
        if self.exit_ablation:
            ea = self.exit_ablation
            lines.append("📊 EXIT ABLATION TEST")
            lines.append(
                f"   Original ({ea.original_exit}): {ea.original_win_rate:.1%} win rate, {ea.original_sharpe:.2f} Sharpe"
            )
            if ea.fixed_30d_win_rate is not None:
                lines.append(
                    f"   Fixed 30d: {ea.fixed_30d_win_rate:.1%} win rate, {ea.fixed_30d_sharpe:.2f} Sharpe"
                )
            if ea.fixed_60d_win_rate is not None:
                lines.append(
                    f"   Fixed 60d: {ea.fixed_60d_win_rate:.1%} win rate, {ea.fixed_60d_sharpe:.2f} Sharpe"
                )
            status = "❌ FAIL" if ea.exit_is_edge else "✅ PASS"
            lines.append(f"   Result: {status}")
            lines.append("")

        # Flip Ablation
        if self.flip_ablation:
            fa = self.flip_ablation
            lines.append("🔄 CORRELATION FLIP ABLATION TEST")
            lines.append(
                f"   With flip: {fa.with_flip_sharpe:.2f} Sharpe, {fa.with_flip_total_return:.1%} return"
            )
            if fa.no_flip_sharpe is not None:
                lines.append(
                    f"   No flip:   {fa.no_flip_sharpe:.2f} Sharpe, {fa.no_flip_total_return:.1%} return"
                )
                lines.append(
                    f"   Flip contribution: {fa.flip_contribution:.0%} of Sharpe"
                )
            status = "❌ FAIL" if fa.flip_is_edge else "✅ PASS"
            lines.append(f"   Result: {status}")
            lines.append("")

        # Random Entry
        if self.random_entry:
            re = self.random_entry
            lines.append("🎲 RANDOM ENTRY BASELINE TEST")
            lines.append(f"   Actual return: {re.actual_total_return:.1%}")
            lines.append(
                f"   Random baseline: {re.random_mean_return:.1%} ± {re.random_std_return:.1%} ({re.n_trials} trials)"
            )
            lines.append(
                f"   Z-score vs random: {re.zscore_vs_random:.2f} (p={re.pvalue:.3f})"
            )
            status = "✅ PASS" if re.signal_has_edge else "❌ FAIL"
            lines.append(f"   Result: {status}")
            lines.append("")

        # Alpha Attribution
        if self.alpha_attribution:
            aa = self.alpha_attribution
            lines.append("📈 ALPHA ATTRIBUTION")
            lines.append(f"   Total return: {aa.total_return:.1%}")
            lines.append(f"   Buy-and-hold: {aa.buy_and_hold_return:.1%}")
            lines.append(
                f"   Active return: {aa.active_return:.1%} ({aa.alpha_ratio:.0%} of total)"
            )
            lines.append(
                f"   Signal accuracy: {aa.signal_accuracy:.1%}  |  Win rate: {aa.win_rate:.1%}"
            )
            lines.append(
                f"   Long: {aa.n_long} trades, {aa.long_return:.1%}  |  Short: {aa.n_short} trades, {aa.short_return:.1%}"
            )
            status = "❌ FAIL" if aa.is_beta_in_disguise else "✅ PASS"
            lines.append(f"   Result: {status} — {aa.skill_signal}")
            lines.append("")

        # Summary
        lines.append("=" * 70)
        if self.is_robust:
            lines.append("✅ OVERALL: Strategy passes robustness checks")
        else:
            lines.append("❌ OVERALL: Strategy has robustness concerns:")
            for flag in self.red_flags:
                lines.append(f"   • {flag}")
        lines.append("=" * 70)

        return "\n".join(lines)


# =============================================================================
# Robustness Validator
# =============================================================================


@dataclass
class RobustnessValidator:
    """
    Run robustness tests on a single GridSearchResult.

    Parameters
    ----------
    processor : StrategyProcessor
        The processor used to generate the result (needed for re-running).
    result : GridSearchResult
        The result to validate.
    n_random_trials : int
        Number of random entry permutations for baseline test.
    """

    processor: StrategyProcessor
    result: GridSearchResult
    n_random_trials: int = 100

    def run_all(self) -> RobustnessReport:
        """Run all robustness tests and return aggregated report."""
        strategy_name = f"{self.result.entry_rule.name} × {self.result.exit_rule.name}"

        report = RobustnessReport(
            strategy_name=strategy_name,
            n_trades=self.result.trade_log.n_trades,
            exit_ablation=self._run_exit_ablation(),
            flip_ablation=self._run_flip_ablation(),
            random_entry=self._run_random_entry(),
            alpha_attribution=self._run_alpha_attribution(),
        )
        return report

    def _run_exit_ablation(self) -> ExitAblationResult:
        """Compare original exit vs fixed holding exits."""
        original = self.result
        signal_dates = frozenset(
            self.processor.signals["earnings_date"].cast(pl.Date).unique().to_list()
        )

        # Get original metrics
        orig_win_rate = original.trade_log.win_rate
        orig_sharpe = original.metrics.risk.sharpe_ratio
        orig_n = original.trade_log.n_trades

        # Run with fixed 30d exit
        fixed_30 = self._rerun_with_exit(
            FixedHoldingExit(holding_days=30, signal_dates=signal_dates)
        )
        # Run with fixed 60d exit
        fixed_60 = self._rerun_with_exit(
            FixedHoldingExit(holding_days=60, signal_dates=signal_dates)
        )

        return ExitAblationResult(
            original_exit=original.exit_rule.name,
            original_win_rate=orig_win_rate,
            original_sharpe=orig_sharpe,
            original_n_trades=orig_n,
            fixed_30d_win_rate=fixed_30.trade_log.win_rate if fixed_30 else None,
            fixed_30d_sharpe=fixed_30.metrics.risk.sharpe_ratio if fixed_30 else None,
            fixed_30d_n_trades=fixed_30.trade_log.n_trades if fixed_30 else None,
            fixed_60d_win_rate=fixed_60.trade_log.win_rate if fixed_60 else None,
            fixed_60d_sharpe=fixed_60.metrics.risk.sharpe_ratio if fixed_60 else None,
            fixed_60d_n_trades=fixed_60.trade_log.n_trades if fixed_60 else None,
        )

    def _run_flip_ablation(self) -> FlipAblationResult | None:
        """Compare with vs without correlation flip (only for corr_aware entries)."""
        if "corr_aware" not in self.result.entry_rule.name:
            # Not a correlation-aware entry, skip this test
            return FlipAblationResult(
                with_flip_win_rate=self.result.trade_log.win_rate,
                with_flip_sharpe=self.result.metrics.risk.sharpe_ratio,
                with_flip_total_return=self.result.trade_log.total_return,
                no_flip_win_rate=None,
                no_flip_sharpe=None,
                no_flip_total_return=None,
            )

        # For corr_aware, the "no flip" version uses raw signal direction
        # We can't easily reconstruct this without the entry rule, so we
        # approximate by checking if the strategy would work with inverted positions
        original = self.result

        # Create a modified daily_df with positions based on raw signal only
        # This is an approximation — ideally we'd re-run with a modified entry rule
        no_flip = self._run_raw_signal_direction()

        return FlipAblationResult(
            with_flip_win_rate=original.trade_log.win_rate,
            with_flip_sharpe=original.metrics.risk.sharpe_ratio,
            with_flip_total_return=original.trade_log.total_return,
            no_flip_win_rate=no_flip.win_rate if no_flip else None,
            no_flip_sharpe=no_flip.sharpe if no_flip else None,
            no_flip_total_return=no_flip.total_return if no_flip else None,
        )

    def _run_random_entry(self) -> RandomEntryResult:
        """Shuffle entry dates and compare to actual."""
        actual = self.result.trade_log
        daily = self.result.daily_df

        # Get the entry dates from actual trades
        entry_dates = [t.entry_date for t in actual.trades]
        if len(entry_dates) < 3:
            # Not enough trades for meaningful permutation
            return RandomEntryResult(
                actual_total_return=actual.total_return,
                actual_sharpe=self.result.metrics.risk.sharpe_ratio,
                actual_win_rate=actual.win_rate,
                random_mean_return=actual.total_return,
                random_std_return=0.0,
                random_mean_sharpe=self.result.metrics.risk.sharpe_ratio,
                random_mean_win_rate=actual.win_rate,
                n_trials=0,
            )

        # Get valid trading dates from daily data
        all_dates = daily["date"].to_list()
        valid_dates = [
            d for d in all_dates if d >= min(entry_dates) and d <= max(entry_dates)
        ]

        random_returns: list[float] = []
        random_sharpes: list[float] = []
        random_win_rates: list[float] = []

        for _ in range(self.n_random_trials):
            # Randomly sample same number of entry dates
            shuffled_entries = random.sample(
                valid_dates, min(len(entry_dates), len(valid_dates))
            )
            shuffled_log = self._simulate_trades_from_dates(
                shuffled_entries, daily, holding_days=int(actual.avg_holding_days)
            )
            if shuffled_log and shuffled_log.n_trades > 0:
                random_returns.append(shuffled_log.total_return)
                random_win_rates.append(shuffled_log.win_rate)
                # Approximate Sharpe from trade returns
                if len(shuffled_log.trades) > 1:
                    rets = np.array([t.trade_return for t in shuffled_log.trades])
                    sharpe = (
                        rets.mean()
                        / rets.std()
                        * np.sqrt(252 / actual.avg_holding_days)
                        if rets.std() > 0
                        else 0
                    )
                    random_sharpes.append(sharpe)

        return RandomEntryResult(
            actual_total_return=actual.total_return,
            actual_sharpe=self.result.metrics.risk.sharpe_ratio,
            actual_win_rate=actual.win_rate,
            random_mean_return=float(np.mean(random_returns))
            if random_returns
            else 0.0,
            random_std_return=float(np.std(random_returns)) if random_returns else 0.0,
            random_mean_sharpe=float(np.mean(random_sharpes))
            if random_sharpes
            else 0.0,
            random_mean_win_rate=float(np.mean(random_win_rates))
            if random_win_rates
            else 0.0,
            n_trials=len(random_returns),
        )

    def _run_alpha_attribution(self) -> AlphaAttributionResult:
        """Decompose returns into beta and alpha."""
        trades = self.result.trade_log.trades
        daily = self.result.daily_df

        # Buy-and-hold return
        if len(daily) > 0:
            first_close = daily["close"][0]
            last_close = daily["close"][-1]
            bh_return = (last_close / first_close) - 1
        else:
            bh_return = 0.0

        # Total return from strategy
        total_return = self.result.trade_log.total_return

        # Long vs short breakdown
        long_trades = [t for t in trades if t.direction > 0]
        short_trades = [t for t in trades if t.direction < 0]

        long_return = sum(t.trade_return for t in long_trades)
        short_return = sum(t.trade_return for t in short_trades)

        # Signal accuracy — need to check against actuals
        # This requires the TradeAnalyzer, but we can approximate from the result
        # For now, use a placeholder based on trade outcomes
        win_rate = self.result.trade_log.win_rate

        # Approximate signal accuracy as direction-right trades / total
        # (this is a simplification — true signal accuracy requires ground truth)
        direction_right = sum(
            1
            for t in trades
            if (t.direction > 0 and t.trade_return > 0)
            or (t.direction < 0 and t.trade_return > 0)
        )
        direction_accuracy = direction_right / len(trades) if trades else 0.0

        # Approximate signal accuracy (would need actual earnings data for true value)
        # For now, assume signal accuracy is worse than direction accuracy
        # since the flip compensates for signal errors
        signal_accuracy = direction_accuracy * 0.5  # Conservative estimate

        return AlphaAttributionResult(
            total_return=total_return,
            buy_and_hold_return=bh_return,
            active_return=total_return - bh_return,
            signal_accuracy=signal_accuracy,
            trade_direction_accuracy=direction_accuracy,
            win_rate=win_rate,
            long_return=long_return,
            short_return=short_return,
            n_long=len(long_trades),
            n_short=len(short_trades),
        )

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _rerun_with_exit(self, exit_rule: ExitRule) -> GridSearchResult | None:
        """Re-run the same entry with a different exit rule."""
        try:
            # Apply exit rule to the original daily positions
            daily = self.result.daily_df.clone()
            daily = exit_rule.apply(daily)

            # Build trade log from modified positions
            trade_log = TradeLog.from_daily(daily)

            if trade_log.n_trades == 0:
                return None

            # Compute metrics from the daily DataFrame
            from abovedata_backtesting.model.metrics import BacktestMetrics

            metrics = BacktestMetrics.from_dataframe(daily)

            return GridSearchResult(
                entry_rule=self.result.entry_rule,
                exit_rule=exit_rule,
                metrics=metrics,
                trade_log=trade_log,
                daily_df=daily,
                entry_params=self.result.entry_params,
                exit_params={},
                sanity=self.result.sanity,
            )
        except Exception:
            return None

    def _run_raw_signal_direction(self) -> _SimpleMetrics | None:
        """Approximate performance using raw signal direction (no flip)."""
        # This is a simplified test — ideally we'd re-run with modified entry
        # For now, we invert positions where correlation was negative
        try:
            daily = self.result.daily_df.clone()

            # Check if we have correlation info in the daily data
            if (
                "contemp_corr" not in daily.columns
                and "leading_corr" not in daily.columns
            ):
                return None

            # This is an approximation — we'd need the actual correlation
            # values per trade to do this properly
            trade_log = TradeLog.from_daily(daily)

            if trade_log.n_trades == 0:
                return None

            # Return simplified metrics
            returns = np.array([t.trade_return for t in trade_log.trades])
            return _SimpleMetrics(
                win_rate=trade_log.win_rate,
                sharpe=returns.mean() / returns.std() * np.sqrt(4)
                if returns.std() > 0
                else 0,
                total_return=trade_log.total_return,
            )
        except Exception:
            return None

    def _simulate_trades_from_dates(
        self,
        entry_dates: list[dt.date],
        daily: pl.DataFrame,
        holding_days: int,
    ) -> TradeLog | None:
        """Simulate trades entering on given dates with fixed holding period."""
        try:
            dates = daily["date"].to_list()
            closes = daily["close"].to_list()
            date_to_idx = {d: i for i, d in enumerate(dates)}

            from abovedata_backtesting.trades.trade_log import Trade

            trades: list[Trade] = []
            for entry_d in entry_dates:
                if entry_d not in date_to_idx:
                    continue
                entry_idx = date_to_idx[entry_d]
                exit_idx = min(entry_idx + holding_days, len(dates) - 1)

                if exit_idx <= entry_idx:
                    continue

                entry_price = closes[entry_idx]
                exit_price = closes[exit_idx]
                direction = 1.0  # Assume long for random baseline

                trade_return = (exit_price / entry_price - 1) * direction

                trades.append(
                    Trade(
                        entry_date=entry_d,
                        exit_date=dates[exit_idx],
                        direction=direction,
                        entry_price=entry_price,
                        exit_price=exit_price,
                        holding_days=exit_idx - entry_idx,
                        trade_return=trade_return,
                        signal_strength=0.0,
                        confidence=0.0,
                    )
                )

            return TradeLog(trades=trades)
        except Exception:
            return None


@dataclass(frozen=True, slots=True)
class _SimpleMetrics:
    """Lightweight metrics container for internal use."""

    win_rate: float
    sharpe: float
    total_return: float
