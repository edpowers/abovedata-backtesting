"""
Trade analyzer: enriches trades with ground truth and classifies outcomes.

Key design principle: the analyzer READS decision context from EntryContext
(recorded at entry time), never re-derives it. Post-hoc reconstruction is
only used as a fallback for legacy trades without context.

Accuracy Definitions
--------------------
signal_accuracy:
    Did sign(UCC residual) predict sign(earnings surprise)?
    Pure measure of UCC predictive power. Independent of any correlation
    flip or position sizing.

direction_accuracy:
    Did the final trade direction (after any correlation flip) match the
    actual price move over the holding period?
    Measures strategy execution quality.

flip_value:
    For trades where a correlation flip was applied: did the flip improve
    the outcome vs. what raw signal direction would have produced?
    Measures whether the correlation regime adds value.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from enum import Enum
from typing import Any

import numpy as np
import polars as pl

from abovedata_backtesting.entries.entry_context import EntryContext
from abovedata_backtesting.trades.trade_log import Trade, TradeLog

# =============================================================================
# Enums
# =============================================================================


class TradeOutcome(Enum):
    """Trade outcome based on TRADE DIRECTION correctness."""

    DIRECTION_RIGHT_PROFIT = "direction_right_profit"
    DIRECTION_RIGHT_LOSS = "direction_right_loss"
    DIRECTION_WRONG_PROFIT = "direction_wrong_profit"
    DIRECTION_WRONG_LOSS = "direction_wrong_loss"
    NO_SIGNAL = "no_signal"


class CorrelationRegime(Enum):
    STRONG_POSITIVE = "strong_positive"
    WEAK_POSITIVE = "weak_positive"
    WEAK_NEGATIVE = "weak_negative"
    STRONG_NEGATIVE = "strong_negative"
    REGIME_SHIFT = "regime_shift"
    UNKNOWN = "unknown"


class SignalQuality(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NO_DATA = "no_data"


# =============================================================================
# Analyzed Trade
# =============================================================================


@dataclass(frozen=True, slots=True)
class AnalyzedTrade:
    """A trade enriched with ground truth and outcome classification."""

    # Original trade data
    entry_date: dt.date
    exit_date: dt.date
    direction: float
    entry_price: float
    exit_price: float
    holding_days: int
    trade_return: float

    # Entry context (from the entry rule, not reconstructed)
    entry_context: EntryContext | None

    # Signal (from context or fallback lookup)
    signal_date: dt.date | None
    signal_value: float | None
    signal_confidence: float | None
    signal_direction: int  # +1, -1, 0  — raw signal, before any flip

    # Correlation (from context — what was actually used)
    corr_col_used: str | None
    corr_value_used: float | None
    correlation_regime: CorrelationRegime
    flipped: bool  # whether correlation flip was applied

    # Signal quality
    signal_quality: SignalQuality

    # Ground truth
    actual_beat_consensus: bool | None
    actual_surprise: float | None
    actual_surprise_direction: int  # +1 beat, -1 miss, 0 unknown
    prediction_error: float | None

    # Accuracy (three distinct measures)
    signal_correct: bool  # sign(residual) == sign(surprise)
    trade_direction_correct: bool  # final direction matched price move
    flip_helped: bool | None  # for flipped trades: did flip improve outcome?

    # Outcome
    outcome: TradeOutcome

    # Market context
    benchmark_return: float
    alpha_contribution: float


# =============================================================================
# Trade Analyzer
# =============================================================================


@dataclass
class TradeAnalyzer:
    """
    Enriches trades with signal ground truth and outcome classification.

    Reads EntryContext from each Trade to determine what was actually used
    for direction, correlation, and confidence decisions.

    Falls back to signal lookup only for ground truth (earnings surprise)
    and for legacy trades without EntryContext.
    """

    signals: pl.DataFrame
    benchmark_data: pl.DataFrame | None = None
    visible_col: str = "visible_revenue"
    date_col: str = "earnings_date"

    def analyze(
        self,
        trade_log: TradeLog,
        market_data: pl.DataFrame,
    ) -> TradeAnalysis:
        """Analyze all trades and return classified results."""
        ground_truth = self._build_ground_truth_lookup()
        bm_prices = (
            _build_price_lookup(self.benchmark_data)
            if self.benchmark_data is not None
            else None
        )

        analyzed: list[AnalyzedTrade] = []
        for trade in trade_log.trades:
            analyzed.append(self._analyze_trade(trade, ground_truth, bm_prices))

        return TradeAnalysis(trades=analyzed)

    def _build_ground_truth_lookup(self) -> dict[dt.date, dict[str, Any]]:
        """
        Build earnings_date → ground truth lookup.

        Only contains earnings surprise data (what actually happened),
        NOT signal/correlation decisions (those come from EntryContext).
        """
        col_map: dict[str, str] = {
            "signal_value": f"{self.visible_col}_resid",
            "contemp_corr": "contemp_corr_historical",
            "leading_corr": "leading_corr_historical",
            "contemp_confidence": "contemp_confidence",
            "leading_confidence": "leading_confidence",
            "pred_direction": "predicted_surprise_direction",
            "prediction_error": "surprise_prediction_error_calibrated",
            "contemp_regime_shift": "contemp_regime_shift",
            "leading_regime_shift": "leading_regime_shift",
            # Ground truth
            "total_revenue": "total_revenue",
            "consensus": "consensus",
            "consensus_surprise": "consensus_surprise",
            "consensus_beat": "consensus_beat",
        }

        available = set(self.signals.columns)
        lookup: dict[dt.date, dict[str, Any]] = {}

        for row in self.signals.iter_rows(named=True):
            ed = row.get(self.date_col)
            if ed is None:
                continue
            if isinstance(ed, dt.datetime):
                ed = ed.date()

            data: dict[str, Any] = {}
            for key, col_name in col_map.items():
                data[key] = row.get(col_name) if col_name in available else None

            # Compute consensus_beat if not present
            if data.get("consensus_beat") is None:
                total_rev = data.get("total_revenue")
                consensus = data.get("consensus")
                if total_rev is not None and consensus is not None and consensus != 0:
                    data["consensus_surprise"] = (total_rev - consensus) / consensus
                    data["consensus_beat"] = total_rev > consensus

            lookup[ed] = data

        return lookup

    def _analyze_trade(
        self,
        trade: Trade,
        ground_truth: dict[dt.date, dict[str, Any]],
        bm_prices: dict[dt.date, float] | None,
    ) -> AnalyzedTrade:
        """Classify a single trade using EntryContext + ground truth."""
        ctx = trade.entry_context

        # ── Signal context: from EntryContext if available ───────────
        if ctx is not None and ctx.has_signal:
            signal_date = ctx.signal_date
            signal_value = ctx.signal_value
            signal_direction = ctx.raw_direction
            confidence = ctx.confidence_value_used
            corr_col_used = ctx.corr_col_used
            corr_value_used = ctx.corr_value_used
            flipped = ctx.flipped
            correlation_regime = _parse_regime(ctx.correlation_regime)
        else:
            # Fallback: find signal from ground truth lookup
            signal_date, sig = self._find_signal_for_trade(trade, ground_truth)
            signal_value = _safe_float(sig.get("signal_value")) if sig else None
            signal_direction = (
                (1 if signal_value > 0 else -1 if signal_value < 0 else 0)
                if signal_value is not None
                else 0
            )
            confidence = None
            corr_col_used = None
            corr_value_used = None
            flipped = False
            correlation_regime = CorrelationRegime.UNKNOWN

        # ── Ground truth: always from lookup ────────────────────────
        gt_date = signal_date or self._find_nearest_earnings(trade, ground_truth)
        gt = ground_truth.get(gt_date) if gt_date else None

        consensus_beat = gt.get("consensus_beat") if gt else None
        consensus_surprise = _safe_float(gt.get("consensus_surprise")) if gt else None
        prediction_error = _safe_float(gt.get("prediction_error")) if gt else None

        if consensus_beat is True:
            actual_direction = 1
        elif consensus_beat is False:
            actual_direction = -1
        else:
            actual_direction = 0

        # ── Signal quality ──────────────────────────────────────────
        if ctx is not None:
            signal_quality = _classify_signal_quality_from_context(ctx)
        else:
            contemp_corr = _safe_float(gt.get("contemp_corr")) if gt else None
            leading_corr = _safe_float(gt.get("leading_corr")) if gt else None
            contemp_conf = _safe_float(gt.get("contemp_confidence")) if gt else None
            signal_quality = _classify_signal_quality(
                contemp_conf, contemp_corr, leading_corr
            )

        # ── Three accuracy measures ─────────────────────────────────

        # 1. Signal accuracy: did UCC residual predict the surprise?
        signal_correct = (
            signal_direction != 0
            and actual_direction != 0
            and signal_direction == actual_direction
        )

        # 2. Direction accuracy: did final trade direction match price move?
        raw_price_move = (
            (trade.exit_price / trade.entry_price - 1) if trade.entry_price > 0 else 0.0
        )
        trade_direction_correct = (trade.direction > 0 and raw_price_move > 0) or (
            trade.direction < 0 and raw_price_move < 0
        )

        # 3. Flip value: for flipped trades, did the flip help?
        #    Compare: actual outcome vs what would have happened with raw direction
        if flipped and signal_direction != 0:
            # What would raw direction have returned?
            raw_return = raw_price_move * signal_direction
            # What did the flipped direction actually return?
            actual_return = trade.trade_return
            flip_helped = actual_return > raw_return
        else:
            flip_helped = None

        # ── Outcome classification ──────────────────────────────────
        outcome = _classify_outcome(
            trade_direction_correct, trade.trade_return, actual_direction
        )

        # ── Benchmark ───────────────────────────────────────────────
        benchmark_return = (
            _holding_period_return(bm_prices, trade.entry_date, trade.exit_date)
            if bm_prices
            else 0.0
        )

        return AnalyzedTrade(
            entry_date=trade.entry_date,
            exit_date=trade.exit_date,
            direction=trade.direction,
            entry_price=trade.entry_price,
            exit_price=trade.exit_price,
            holding_days=trade.holding_days,
            trade_return=trade.trade_return,
            entry_context=ctx,
            signal_date=signal_date,
            signal_value=signal_value,
            signal_confidence=confidence,
            signal_direction=signal_direction,
            corr_col_used=corr_col_used,
            corr_value_used=corr_value_used,
            correlation_regime=correlation_regime,
            flipped=flipped,
            signal_quality=signal_quality,
            actual_beat_consensus=consensus_beat
            if isinstance(consensus_beat, bool)
            else None,
            actual_surprise=consensus_surprise,
            actual_surprise_direction=actual_direction,
            prediction_error=prediction_error,
            signal_correct=signal_correct,
            trade_direction_correct=trade_direction_correct,
            flip_helped=flip_helped,
            outcome=outcome,
            benchmark_return=benchmark_return,
            alpha_contribution=trade.trade_return - benchmark_return,
        )

    def _find_signal_for_trade(
        self,
        trade: Trade,
        ground_truth: dict[dt.date, dict[str, Any]],
    ) -> tuple[dt.date | None, dict[str, Any] | None]:
        """Find nearest earnings date >= entry within 120 calendar days."""
        for ed in sorted(ground_truth.keys()):
            if ed >= trade.entry_date:
                if (ed - trade.entry_date).days <= 120:
                    return ed, ground_truth[ed]
                break
        return None, None

    def _find_nearest_earnings(
        self,
        trade: Trade,
        ground_truth: dict[dt.date, dict[str, Any]],
    ) -> dt.date | None:
        """Find nearest earnings date for ground truth lookup."""
        for ed in sorted(ground_truth.keys()):
            if ed >= trade.entry_date:
                if (ed - trade.entry_date).days <= 120:
                    return ed
                break
        return None


# =============================================================================
# Trade Analysis (collection with accuracy properties)
# =============================================================================


@dataclass
class TradeAnalysis:
    """Collection of analyzed trades with properly defined accuracy measures."""

    trades: list[AnalyzedTrade]

    def to_dataframe(self) -> pl.DataFrame:
        if not self.trades:
            return pl.DataFrame()

        rows = []
        for t in self.trades:
            row: dict[str, Any] = {
                "entry_date": t.entry_date,
                "exit_date": t.exit_date,
                "direction": t.direction,
                "holding_days": t.holding_days,
                "trade_return": t.trade_return,
                "signal_date": t.signal_date,
                "signal_value": t.signal_value,
                "signal_confidence": t.signal_confidence,
                "signal_direction": t.signal_direction,
                "corr_col_used": t.corr_col_used,
                "corr_value_used": t.corr_value_used,
                "correlation_regime": t.correlation_regime.value,
                "flipped": t.flipped,
                "signal_quality": t.signal_quality.value,
                "actual_beat_consensus": t.actual_beat_consensus,
                "actual_surprise": t.actual_surprise,
                "actual_surprise_direction": t.actual_surprise_direction,
                "prediction_error": t.prediction_error,
                "signal_correct": t.signal_correct,
                "trade_direction_correct": t.trade_direction_correct,
                "flip_helped": t.flip_helped,
                "outcome": t.outcome.value,
                "benchmark_return": t.benchmark_return,
                "alpha_contribution": t.alpha_contribution,
            }

            # Include entry type if available
            if t.entry_context is not None:
                row["entry_type"] = t.entry_context.entry_type

            rows.append(row)

        return pl.DataFrame(rows, infer_schema_length=10_000)

    @property
    def n_trades(self) -> int:
        return len(self.trades)

    # ── Accuracy Properties (clearly defined) ─────────────────────

    @property
    def signal_accuracy(self) -> float:
        """
        Did sign(UCC residual) predict sign(earnings surprise)?

        Pure UCC predictive power. Denominator: trades with both
        a signal direction and a known earnings outcome.
        """
        eligible = [
            t
            for t in self.trades
            if t.signal_direction != 0 and t.actual_surprise_direction != 0
        ]
        if not eligible:
            return 0.0
        return sum(1 for t in eligible if t.signal_correct) / len(eligible)

    @property
    def direction_accuracy(self) -> float:
        """
        Did the final trade direction match the actual price move?

        Measures strategy execution (including any correlation flip).
        Denominator: all trades with a price move.
        """
        eligible = [
            t for t in self.trades if abs(t.exit_price / t.entry_price - 1) > 1e-6
        ]
        if not eligible:
            return 0.0
        return sum(1 for t in eligible if t.trade_direction_correct) / len(eligible)

    @property
    def flip_accuracy(self) -> float:
        """
        For flipped trades: what fraction were improved by the flip?

        Measures whether the correlation regime classification adds value
        over raw signal direction. Only defined for correlation-aware entries.
        """
        flipped = [t for t in self.trades if t.flip_helped is not None]
        if not flipped:
            return 0.0
        return sum(1 for t in flipped if t.flip_helped) / len(flipped)

    @property
    def flip_count(self) -> int:
        """Number of trades where a correlation flip was applied."""
        return sum(1 for t in self.trades if t.flipped)

    @property
    def skill_ratio(self) -> float:
        """direction_right_profit / (direction_right_profit + direction_wrong_loss)."""
        counts = self.outcome_counts()
        skill = counts.get(TradeOutcome.DIRECTION_RIGHT_PROFIT.value, 0)
        expected_loss = counts.get(TradeOutcome.DIRECTION_WRONG_LOSS.value, 0)
        total = skill + expected_loss
        return skill / total if total > 0 else 0.0

    @property
    def headwind_ratio(self) -> float:
        """Fraction of direction-correct trades that still lost."""
        right = [t for t in self.trades if t.trade_direction_correct]
        if not right:
            return 0.0
        return sum(1 for t in right if t.trade_return < 0) / len(right)

    @property
    def luck_ratio(self) -> float:
        """Fraction of direction-wrong trades that still profited."""
        wrong = [
            t
            for t in self.trades
            if not t.trade_direction_correct and t.actual_surprise_direction != 0
        ]
        if not wrong:
            return 0.0
        return sum(1 for t in wrong if t.trade_return > 0) / len(wrong)

    # ── Summaries ─────────────────────────────────────────────────

    def outcome_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for t in self.trades:
            key = t.outcome.value
            counts[key] = counts.get(key, 0) + 1
        return counts

    def outcome_summary(self) -> pl.DataFrame:
        df = self.to_dataframe()
        if df.is_empty():
            return df
        return (
            df.group_by("outcome")
            .agg(
                pl.len().alias("count"),
                pl.col("trade_return").mean().alias("avg_return"),
                pl.col("trade_return").sum().alias("total_return"),
                pl.col("alpha_contribution").mean().alias("avg_alpha"),
                pl.col("holding_days").mean().alias("avg_holding_days"),
            )
            .sort("count", descending=True)
        )

    def regime_summary(self) -> pl.DataFrame:
        df = self.to_dataframe()
        if df.is_empty():
            return df
        return (
            df.group_by("correlation_regime")
            .agg(
                pl.len().alias("count"),
                pl.col("signal_correct").mean().alias("signal_accuracy"),
                pl.col("trade_direction_correct").mean().alias("direction_accuracy"),
                pl.col("trade_return").mean().alias("avg_return"),
                pl.col("alpha_contribution").mean().alias("avg_alpha"),
                (pl.col("trade_return") > 0).mean().alias("win_rate"),
            )
            .sort("count", descending=True)
        )

    def quality_summary(self) -> pl.DataFrame:
        """Signal quality breakdown with accuracy and return stats."""
        df = self.to_dataframe()
        if df.is_empty():
            return df
        return (
            df.group_by("signal_quality")
            .agg(
                pl.len().alias("count"),
                pl.col("signal_correct").mean().alias("signal_accuracy"),
                pl.col("trade_direction_correct").mean().alias("direction_accuracy"),
                pl.col("trade_return").mean().alias("avg_return"),
                pl.col("alpha_contribution").mean().alias("avg_alpha"),
                (pl.col("trade_return") > 0).mean().alias("win_rate"),
            )
            .sort("signal_quality")
        )

    def flip_summary(self) -> pl.DataFrame:
        """Summary of flipped vs unflipped trades."""
        df = self.to_dataframe()
        if df.is_empty():
            return df
        return (
            df.group_by("flipped")
            .agg(
                pl.len().alias("count"),
                pl.col("signal_correct").mean().alias("signal_accuracy"),
                pl.col("trade_direction_correct").mean().alias("direction_accuracy"),
                pl.col("trade_return").mean().alias("avg_return"),
                pl.col("alpha_contribution").mean().alias("avg_alpha"),
                (pl.col("trade_return") > 0).mean().alias("win_rate"),
            )
            .sort("flipped")
        )

    def accuracy_summary(self) -> dict[str, float | int]:
        """All three accuracy measures in one dict."""
        return {
            "signal_accuracy": self.signal_accuracy,
            "direction_accuracy": self.direction_accuracy,
            "flip_accuracy": self.flip_accuracy,
            "flip_count": self.flip_count,
            "n_trades": self.n_trades,
            "win_rate": float(np.mean([t.trade_return > 0 for t in self.trades]))
            if self.trades
            else 0.0,
            "skill_ratio": self.skill_ratio,
            "headwind_ratio": self.headwind_ratio,
            "luck_ratio": self.luck_ratio,
        }

    # ── Diversity / Concentration ─────────────────────────────────

    def diversity_metrics(self) -> dict[str, Any]:
        """
        Concentration and robustness metrics.

        Returns
        -------
        dict with:
            hhi: Herfindahl index on |returns| (1/N = perfectly diverse, 1.0 = one trade)
            top1_pct / top3_pct / top5_pct: share of gross profit from top N trades
            return_ex_top1 / ex_top3: compounded return excluding top N trades
            profit_factor: gross_profit / gross_loss
            expectancy: avg_win * win_rate - avg_loss * loss_rate
            max_single_contribution: largest single trade return
            tail_ratio: mean(top 10% returns) / mean(|bottom 10% returns|)
        """
        returns = np.array([t.trade_return for t in self.trades])
        n = len(returns)
        if n == 0:
            return self._empty_diversity()

        # HHI on absolute return contributions
        abs_returns = np.abs(returns)
        total_abs = abs_returns.sum()
        if total_abs > 0:
            shares = abs_returns / total_abs
            hhi = float(np.sum(shares**2))
        else:
            hhi = 0.0

        # Top-N concentration (% of gross profit)
        gross_profits = returns[returns > 0]
        total_gross_profit = gross_profits.sum() if len(gross_profits) > 0 else 0.0

        sorted_desc = np.sort(returns)[::-1]
        if total_gross_profit > 0:
            top1_pct = float(sorted_desc[0] / total_gross_profit) if n >= 1 else 0.0
            top3_pct = (
                float(sorted_desc[:3].sum() / total_gross_profit)
                if n >= 3
                else top1_pct
            )
            top5_pct = (
                float(sorted_desc[:5].sum() / total_gross_profit)
                if n >= 5
                else top3_pct
            )
        else:
            top1_pct = top3_pct = top5_pct = 0.0

        # Compounded return excluding top-K trades
        sorted_idx = np.argsort(returns)[::-1]
        return_ex_top1 = (
            float(np.prod(1 + np.delete(returns, sorted_idx[:1])) - 1) if n > 1 else 0.0
        )
        return_ex_top3 = (
            float(np.prod(1 + np.delete(returns, sorted_idx[:3])) - 1) if n > 3 else 0.0
        )

        # Profit factor
        gross_loss = np.abs(returns[returns < 0]).sum()
        profit_factor = (
            float(total_gross_profit / gross_loss) if gross_loss > 0 else float("inf")
        )

        # Expectancy
        winners = returns[returns > 0]
        losers = returns[returns < 0]
        win_rate = len(winners) / n if n > 0 else 0.0
        loss_rate = len(losers) / n if n > 0 else 0.0
        avg_win = float(winners.mean()) if len(winners) > 0 else 0.0
        avg_loss = float(np.abs(losers).mean()) if len(losers) > 0 else 0.0
        expectancy = avg_win * win_rate - avg_loss * loss_rate

        # Tail ratio
        k = max(1, n // 10)
        sorted_asc = np.sort(returns)
        top_tail = float(sorted_asc[-k:].mean())
        bottom_tail = float(np.abs(sorted_asc[:k]).mean())
        tail_ratio = top_tail / bottom_tail if bottom_tail > 0 else float("inf")

        return {
            "hhi": hhi,
            "top1_pct": top1_pct,
            "top3_pct": top3_pct,
            "top5_pct": top5_pct,
            "return_ex_top1": return_ex_top1,
            "return_ex_top3": return_ex_top3,
            "profit_factor": profit_factor,
            "expectancy": expectancy,
            "max_single_contribution": float(sorted_desc[0]),
            "tail_ratio": tail_ratio,
        }

    @staticmethod
    def _empty_diversity() -> dict[str, Any]:
        return {
            "hhi": 0.0,
            "top1_pct": 0.0,
            "top3_pct": 0.0,
            "top5_pct": 0.0,
            "return_ex_top1": 0.0,
            "return_ex_top3": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
            "max_single_contribution": 0.0,
            "tail_ratio": 0.0,
        }

    def diversity_summary(self) -> pl.DataFrame:
        """Diversity metrics as a single-row DataFrame for display."""
        return pl.DataFrame([self.diversity_metrics()])

    def full_summary(self) -> dict[str, Any]:
        """Full summary including accuracy and diversity metrics."""
        returns = np.array([t.trade_return for t in self.trades])
        alphas = np.array([t.alpha_contribution for t in self.trades])

        base: dict[str, Any] = {
            "n_trades": self.n_trades,
            "avg_return": float(np.mean(returns)) if len(returns) > 0 else 0.0,
            "avg_alpha": float(np.mean(alphas)) if len(alphas) > 0 else 0.0,
            "total_return": float(np.prod(1 + returns) - 1)
            if len(returns) > 0
            else 0.0,
            "win_rate": float(np.mean(returns > 0)) if len(returns) > 0 else 0.0,
            "outcome_counts": self.outcome_counts(),
        }
        base.update(self.accuracy_summary())
        base.update(self.diversity_metrics())
        return base


# =============================================================================
# Helpers
# =============================================================================


def _safe_float(val: Any) -> float | None:
    if val is None:
        return None
    try:
        f = float(val)
        return f if f == f else None
    except (ValueError, TypeError):
        return None


def _parse_regime(regime_str: str | None) -> CorrelationRegime:
    """Parse a regime string into the enum, defaulting to UNKNOWN."""
    if regime_str is None:
        return CorrelationRegime.UNKNOWN
    try:
        return CorrelationRegime(regime_str)
    except ValueError:
        return CorrelationRegime.UNKNOWN


def _classify_signal_quality_from_context(ctx: EntryContext) -> SignalQuality:
    """Classify signal quality from what the entry actually used."""
    conf = ctx.confidence_value_used
    corr = abs(ctx.corr_value_used) if ctx.corr_value_used is not None else 0.0

    if conf is None:
        return SignalQuality.NO_DATA
    if conf > 0.5 and corr > 0.5:
        return SignalQuality.HIGH
    elif conf > 0.3 or corr > 0.3:
        return SignalQuality.MEDIUM
    else:
        return SignalQuality.LOW


def _classify_signal_quality(
    confidence: float | None,
    contemp_corr: float | None,
    leading_corr: float | None,
) -> SignalQuality:
    """Fallback for legacy trades without context."""
    if confidence is None:
        return SignalQuality.NO_DATA
    corr_strength = max(
        abs(leading_corr) if leading_corr is not None else 0.0,
        abs(contemp_corr) if contemp_corr is not None else 0.0,
    )
    if confidence > 0.5 and corr_strength > 0.5:
        return SignalQuality.HIGH
    elif confidence > 0.3 or corr_strength > 0.3:
        return SignalQuality.MEDIUM
    else:
        return SignalQuality.LOW


def _classify_outcome(
    direction_correct: bool,
    trade_return: float,
    actual_direction: int,
) -> TradeOutcome:
    if actual_direction == 0:
        return TradeOutcome.NO_SIGNAL
    profitable = trade_return > 0
    if direction_correct and profitable:
        return TradeOutcome.DIRECTION_RIGHT_PROFIT
    elif direction_correct and not profitable:
        return TradeOutcome.DIRECTION_RIGHT_LOSS
    elif not direction_correct and profitable:
        return TradeOutcome.DIRECTION_WRONG_PROFIT
    else:
        return TradeOutcome.DIRECTION_WRONG_LOSS


def _build_price_lookup(df: pl.DataFrame) -> dict[dt.date, float]:
    return dict(zip(df["date"].to_list(), df["close"].to_list()))


def _holding_period_return(
    prices: dict[dt.date, float],
    entry_date: dt.date,
    exit_date: dt.date,
) -> float:
    entry_price = prices.get(entry_date)
    exit_price = prices.get(exit_date)
    if entry_price is None or exit_price is None or entry_price == 0:
        return 0.0
    return (exit_price / entry_price) - 1
