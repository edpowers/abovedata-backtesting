"""Trade analysis and post-processing.

Classifies each trade by signal quality, correctness, and market context.
Column names are derived from the visible_col parameter to match the
output schema of load_signal_data / STLSignalProcessor.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from enum import Enum
from typing import Any

import numpy as np
import polars as pl

from abovedata_backtesting.trades.trade_log import Trade, TradeLog


def compare_entry_types(summary_df: pl.DataFrame) -> pl.DataFrame:
    """Compare performance across entry types."""
    return (
        summary_df.group_by("entry_entry_type")
        .agg(
            pl.len().alias("count"),
            pl.col("sharpe_ratio").mean().alias("avg_sharpe"),
            pl.col("sharpe_ratio").max().alias("max_sharpe"),
            pl.col("sharpe_ratio").median().alias("median_sharpe"),
            pl.col("trade_n_trades").mean().alias("avg_trades"),
            pl.col("trade_win_rate").mean().alias("avg_win_rate"),
            pl.col("trade_total_return").mean().alias("avg_total_return"),
            pl.col("trade_total_return").max().alias("max_total_return"),
            pl.col("annualized_return").mean().alias("avg_ann_return"),
        )
        .sort("avg_sharpe", descending=True)
    )


def compare_corr_aware_variants(summary_df: pl.DataFrame) -> pl.DataFrame:
    """Compare corr_aware variants by corr_col type."""
    corr = summary_df.filter(pl.col("entry_entry_type") == "correlation_aware")
    if corr.is_empty():
        return pl.DataFrame({"note": ["No correlation_aware entries found"]})

    corr_col = "entry_corr_col"
    if corr_col not in corr.columns:
        return corr

    return (
        corr.group_by(corr_col)
        .agg(
            pl.len().alias("count"),
            pl.col("sharpe_ratio").mean().alias("avg_sharpe"),
            pl.col("sharpe_ratio").max().alias("max_sharpe"),
            pl.col("trade_n_trades").mean().alias("avg_trades"),
            pl.col("trade_win_rate").mean().alias("avg_win_rate"),
            pl.col("trade_total_return").max().alias("max_total_return"),
        )
        .sort("avg_sharpe", descending=True)
    )


# =============================================================================
# Enums
# =============================================================================


class TradeOutcome(Enum):
    """Trade outcome based on TRADE DIRECTION correctness, not signal accuracy.

    For corr_aware strategies, the trade direction includes the correlation
    flip: direction = sign(signal) × sign(correlation). So the trade can be
    directionally correct even when the raw signal "missed" the surprise,
    because the correlation flip compensated.

    trade_direction_correct = (direction > 0 and price went up) or
                              (direction < 0 and price went down)
    """

    DIRECTION_RIGHT_PROFIT = "direction_right_profit"  # Skill: right direction + profit
    DIRECTION_RIGHT_LOSS = "direction_right_loss"  # Headwinds: right direction but lost
    DIRECTION_WRONG_PROFIT = (
        "direction_wrong_profit"  # Luck: wrong direction but profited
    )
    DIRECTION_WRONG_LOSS = "direction_wrong_loss"  # Expected: wrong direction + loss
    NO_SIGNAL = "no_signal"  # No ground truth available


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
    """A trade enriched with signal quality and outcome classification."""

    # Original trade
    entry_date: dt.date
    exit_date: dt.date
    direction: float
    entry_price: float
    exit_price: float
    holding_days: int
    trade_return: float

    # Signal context
    signal_date: dt.date | None
    signal_value: float | None
    signal_confidence: float | None
    signal_direction: int  # +1, -1, or 0

    # Correlation context
    contemp_corr: float | None
    leading_corr: float | None
    correlation_regime: CorrelationRegime
    signal_quality: SignalQuality

    # Ground truth
    actual_beat_consensus: bool | None
    actual_surprise: float | None  # (total_revenue - consensus) / consensus
    actual_surprise_direction: int  # +1 beat, -1 miss, 0 unknown
    prediction_error: float | None

    # Classification
    signal_correct: bool  # Did UCC predict earnings surprise direction?
    trade_direction_correct: bool  # Did trade direction match actual price move?
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
    Post-processor that enriches trades with signal quality and outcome data.

    Column names are derived dynamically from visible_col to match
    the df_fc_joined schema:
      - {visible_col}_resid
      - {visible_col}_to_total_revenue_contemp_corr
      - {visible_col}_to_total_revenue_lead1_corr
      - {visible_col}_to_total_revenue_contemp_confidence
      - {visible_col}_to_total_revenue_contemp_pred_direction
      - {visible_col}_to_total_revenue_contemp_pred_calibrated
      - {visible_col}_to_total_revenue_contemp_regime_shift
      - {visible_col}_to_total_revenue_contemp_hit
    """

    signals: pl.DataFrame
    benchmark_data: pl.DataFrame | None = None
    visible_col: str = "visible_revenue"
    date_col: str = "earnings_date"

    def _col(self, suffix: str) -> str:
        """Build column name from visible_col prefix."""
        return f"{self.visible_col}_{suffix}"

    def analyze(
        self,
        trade_log: TradeLog,
        market_data: pl.DataFrame,
    ) -> TradeAnalysis:
        """Analyze all trades and return classified results."""
        signal_lookup = self._build_signal_lookup()
        bm_prices = (
            _build_price_lookup(self.benchmark_data)
            if self.benchmark_data is not None
            else None
        )

        analyzed: list[AnalyzedTrade] = []
        for trade in trade_log.trades:
            analyzed.append(self._analyze_trade(trade, signal_lookup, bm_prices))

        return TradeAnalysis(trades=analyzed)

    def _build_signal_lookup(self) -> dict[dt.date, dict[str, Any]]:
        """Build earnings_date → signal data lookup using actual column names."""
        # Map logical names to actual column names in STL processor output.
        # The STL processor uses flat names like contemp_corr_historical,
        # NOT the relationship pattern visible_revenue_to_total_revenue_*.
        col_map: dict[str, str] = {
            "signal_value": self._col("resid"),  # visible_revenue_resid
            "contemp_confidence": "contemp_confidence",
            "leading_confidence": "leading_confidence",
            "contemp_corr": "contemp_corr_historical",
            "lead1_corr": "leading_corr_historical",
            "contemp_corr_ma": "contemp_corr_ma",
            "leading_corr_ma": "leading_corr_ma",
            "pred_direction": "predicted_surprise_direction",
            "pred_calibrated": "predicted_surprise_calibrated",
            "prediction_error": "surprise_prediction_error_calibrated",
            "contemp_regime_shift": "contemp_regime_shift",
            "leading_regime_shift": "leading_regime_shift",
            "signal_percentile": "signal_percentile",
            # Ground truth
            "total_revenue": "total_revenue",
            "consensus": "consensus",
            "consensus_surprise": "consensus_surprise",
            "consensus_beat": "consensus_beat",
        }

        available_cols = set(self.signals.columns)

        lookup: dict[dt.date, dict[str, Any]] = {}
        for row in self.signals.iter_rows(named=True):
            ed = row.get(self.date_col)
            if ed is None:
                continue
            if isinstance(ed, dt.datetime):
                ed = ed.date()

            data: dict[str, Any] = {}
            for key, col_name in col_map.items():
                if col_name in available_cols:
                    data[key] = row.get(col_name)
                else:
                    data[key] = None

            # Use consensus_beat/surprise from data if already present,
            # otherwise compute from total_revenue and consensus
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
        signal_lookup: dict[dt.date, dict[str, Any]],
        bm_prices: dict[dt.date, float] | None,
    ) -> AnalyzedTrade:
        """Classify a single trade."""
        signal_date, sig = self._find_signal_for_trade(trade, signal_lookup)

        # Signal context
        signal_value = _safe_float(sig.get("signal_value")) if sig else None
        contemp_conf = _safe_float(sig.get("contemp_confidence")) if sig else None
        leading_conf = _safe_float(sig.get("leading_confidence")) if sig else None
        # Prefer leading confidence if available
        signal_confidence = (
            leading_conf
            if leading_conf is not None and leading_conf > 0
            else contemp_conf
        )

        contemp_corr = _safe_float(sig.get("contemp_corr")) if sig else None
        leading_corr = _safe_float(sig.get("lead1_corr")) if sig else None

        # Signal direction from predicted direction, or sign of residual
        pred_dir = sig.get("pred_direction") if sig else None
        if pred_dir is not None and pred_dir != 0:
            signal_direction = int(pred_dir)
        elif signal_value is not None:
            signal_direction = 1 if signal_value > 0 else -1 if signal_value < 0 else 0
        else:
            signal_direction = 0

        # Correlation regime — check both contemp and leading regime shifts
        contemp_shift = sig.get("contemp_regime_shift") if sig else None
        leading_shift = sig.get("leading_regime_shift") if sig else None
        has_regime_shift = (contemp_shift is not None and contemp_shift != "") or (
            leading_shift is not None and leading_shift != ""
        )
        correlation_regime = _classify_correlation_regime(
            contemp_corr, leading_corr, has_regime_shift
        )

        # Signal quality
        signal_quality = _classify_signal_quality(
            signal_confidence, contemp_corr, leading_corr
        )

        # Ground truth
        consensus_beat = sig.get("consensus_beat") if sig else None
        consensus_surprise = _safe_float(sig.get("consensus_surprise")) if sig else None
        prediction_error = _safe_float(sig.get("prediction_error")) if sig else None

        if consensus_beat is True:
            actual_direction = 1
        elif consensus_beat is False:
            actual_direction = -1
        else:
            actual_direction = 0

        # Signal correctness: did UCC residual predict the surprise?
        signal_correct = (
            signal_direction != 0
            and actual_direction != 0
            and signal_direction == actual_direction
        )

        # Trade direction correctness: did the TRADE direction (after corr flip)
        # match the actual price move? This is what matters for corr_aware strategies.
        # For momentum entries, direction comes from price, so this measures timing.
        # For corr_aware entries, direction = sign(signal) × sign(corr), so this
        # measures whether the full signal+correlation logic got the price move right.
        price_went_up = (
            trade.trade_return > 0 if trade.direction > 0 else trade.trade_return < 0
        )
        # Actually: trade_return already incorporates direction. If trade_return > 0,
        # the trade direction was correct (we made money). But that conflates direction
        # correctness with magnitude. We want: did price move in the direction we bet?
        #
        # price_move = (exit_price / entry_price) - 1
        # trade_direction_correct = (direction > 0 and price_move > 0) or
        #                           (direction < 0 and price_move < 0)
        raw_price_move = (
            (trade.exit_price / trade.entry_price - 1) if trade.entry_price > 0 else 0.0
        )
        trade_direction_correct = (trade.direction > 0 and raw_price_move > 0) or (
            trade.direction < 0 and raw_price_move < 0
        )

        # Outcome classification based on trade direction (not signal accuracy)
        outcome = _classify_outcome(
            trade_direction_correct, trade.trade_return, actual_direction
        )

        # Benchmark return over holding period
        benchmark_return = (
            _holding_period_return(bm_prices, trade.entry_date, trade.exit_date)
            if bm_prices
            else 0.0
        )
        alpha = trade.trade_return - benchmark_return

        return AnalyzedTrade(
            entry_date=trade.entry_date,
            exit_date=trade.exit_date,
            direction=trade.direction,
            entry_price=trade.entry_price,
            exit_price=trade.exit_price,
            holding_days=trade.holding_days,
            trade_return=trade.trade_return,
            signal_date=signal_date,
            signal_value=signal_value,
            signal_confidence=signal_confidence,
            signal_direction=signal_direction,
            contemp_corr=contemp_corr,
            leading_corr=leading_corr,
            correlation_regime=correlation_regime,
            signal_quality=signal_quality,
            actual_beat_consensus=consensus_beat
            if isinstance(consensus_beat, bool)
            else None,
            actual_surprise=consensus_surprise,
            actual_surprise_direction=actual_direction,
            prediction_error=prediction_error,
            signal_correct=signal_correct,
            trade_direction_correct=trade_direction_correct,
            outcome=outcome,
            benchmark_return=benchmark_return,
            alpha_contribution=alpha,
        )

    def _find_signal_for_trade(
        self,
        trade: Trade,
        signal_lookup: dict[dt.date, dict[str, Any]],
    ) -> tuple[dt.date | None, dict[str, Any] | None]:
        """
        Find the signal (earnings date) this trade is associated with.

        The trade was entered N days before an earnings date.
        Find the nearest earnings_date >= entry_date within 120 calendar days.
        """
        if not signal_lookup:
            return None, None

        earnings_dates = sorted(signal_lookup.keys())
        for ed in earnings_dates:
            if ed >= trade.entry_date:
                delta = (ed - trade.entry_date).days
                if delta <= 120:
                    return ed, signal_lookup[ed]
                break

        return None, None


# =============================================================================
# Trade Analysis (collection)
# =============================================================================


@dataclass
class TradeAnalysis:
    """Collection of analyzed trades with summary statistics."""

    trades: list[AnalyzedTrade]

    def to_dataframe(self) -> pl.DataFrame:
        if not self.trades:
            return pl.DataFrame()

        rows = []
        for t in self.trades:
            rows.append(
                {
                    "entry_date": t.entry_date,
                    "exit_date": t.exit_date,
                    "direction": t.direction,
                    "holding_days": t.holding_days,
                    "trade_return": t.trade_return,
                    "signal_date": t.signal_date,
                    "signal_value": t.signal_value,
                    "signal_confidence": t.signal_confidence,
                    "signal_direction": t.signal_direction,
                    "contemp_corr": t.contemp_corr,
                    "leading_corr": t.leading_corr,
                    "correlation_regime": t.correlation_regime.value,
                    "signal_quality": t.signal_quality.value,
                    "actual_beat_consensus": t.actual_beat_consensus,
                    "actual_surprise": t.actual_surprise,
                    "actual_surprise_direction": t.actual_surprise_direction,
                    "prediction_error": t.prediction_error,
                    "signal_correct": t.signal_correct,
                    "trade_direction_correct": t.trade_direction_correct,
                    "outcome": t.outcome.value,
                    "benchmark_return": t.benchmark_return,
                    "alpha_contribution": t.alpha_contribution,
                }
            )
        return pl.DataFrame(rows)

    @property
    def n_trades(self) -> int:
        return len(self.trades)

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

    def quality_summary(self) -> pl.DataFrame:
        df = self.to_dataframe()
        if df.is_empty():
            return df
        return (
            df.group_by("signal_quality")
            .agg(
                pl.len().alias("count"),
                pl.col("signal_correct").mean().alias("signal_accuracy"),
                pl.col("trade_return").mean().alias("avg_return"),
                pl.col("alpha_contribution").mean().alias("avg_alpha"),
                (pl.col("trade_return") > 0).mean().alias("win_rate"),
            )
            .sort("signal_quality")
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
                pl.col("trade_return").mean().alias("avg_return"),
                pl.col("alpha_contribution").mean().alias("avg_alpha"),
                (pl.col("trade_return") > 0).mean().alias("win_rate"),
            )
            .sort("count", descending=True)
        )

    @property
    def signal_accuracy(self) -> float:
        """Fraction of trades where UCC signal predicted surprise correctly."""
        with_signal = [t for t in self.trades if t.actual_surprise_direction != 0]
        if not with_signal:
            return 0.0
        return sum(1 for t in with_signal if t.signal_correct) / len(with_signal)

    @property
    def direction_accuracy(self) -> float:
        """Fraction of trades where trade direction matched price move."""
        with_signal = [t for t in self.trades if t.actual_surprise_direction != 0]
        if not with_signal:
            return 0.0
        return sum(1 for t in with_signal if t.trade_direction_correct) / len(
            with_signal
        )

    @property
    def skill_ratio(self) -> float:
        """direction_right_profit / (direction_right_profit + direction_wrong_loss)"""
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

    def full_summary(self) -> dict[str, Any]:
        returns = np.array([t.trade_return for t in self.trades])
        alphas = np.array([t.alpha_contribution for t in self.trades])

        diversity = self.diversity_metrics()

        return {
            "n_trades": self.n_trades,
            "signal_accuracy": self.signal_accuracy,
            "direction_accuracy": self.direction_accuracy,
            "skill_ratio": self.skill_ratio,
            "headwind_ratio": self.headwind_ratio,
            "luck_ratio": self.luck_ratio,
            "avg_return": float(np.mean(returns)) if len(returns) > 0 else 0.0,
            "avg_alpha": float(np.mean(alphas)) if len(alphas) > 0 else 0.0,
            "total_return": float(np.prod(1 + returns) - 1)
            if len(returns) > 0
            else 0.0,
            "win_rate": float(np.mean(returns > 0)) if len(returns) > 0 else 0.0,
            "outcome_counts": self.outcome_counts(),
            **diversity,
        }

    # ── Diversity / concentration metrics ────────────────────────────

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

        # ── HHI on absolute return contributions ────────────────────
        abs_returns = np.abs(returns)
        total_abs = abs_returns.sum()
        if total_abs > 0:
            shares = abs_returns / total_abs
            hhi = float(np.sum(shares**2))
        else:
            hhi = 0.0

        # ── Top-N concentration (% of gross profit) ────────────────
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

        # ── Compounded return excluding top-K trades ────────────────
        sorted_idx = np.argsort(returns)[::-1]
        return_ex_top1 = (
            float(np.prod(1 + np.delete(returns, sorted_idx[:1])) - 1) if n > 1 else 0.0
        )
        return_ex_top3 = (
            float(np.prod(1 + np.delete(returns, sorted_idx[:3])) - 1) if n > 3 else 0.0
        )

        # ── Profit factor ───────────────────────────────────────────
        gross_loss = np.abs(returns[returns < 0]).sum()
        profit_factor = (
            float(total_gross_profit / gross_loss) if gross_loss > 0 else float("inf")
        )

        # ── Expectancy ──────────────────────────────────────────────
        winners = returns[returns > 0]
        losers = returns[returns < 0]
        win_rate = len(winners) / n if n > 0 else 0.0
        loss_rate = len(losers) / n if n > 0 else 0.0
        avg_win = float(winners.mean()) if len(winners) > 0 else 0.0
        avg_loss = float(np.abs(losers).mean()) if len(losers) > 0 else 0.0
        expectancy = avg_win * win_rate - avg_loss * loss_rate

        # ── Tail ratio ──────────────────────────────────────────────
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


def _classify_correlation_regime(
    contemp_corr: float | None,
    leading_corr: float | None,
    regime_shift: bool,
) -> CorrelationRegime:
    if regime_shift:
        return CorrelationRegime.REGIME_SHIFT
    corr = leading_corr if leading_corr is not None else contemp_corr
    if corr is None:
        return CorrelationRegime.UNKNOWN
    if corr > 0.5:
        return CorrelationRegime.STRONG_POSITIVE
    elif corr > 0:
        return CorrelationRegime.WEAK_POSITIVE
    elif corr > -0.5:
        return CorrelationRegime.WEAK_NEGATIVE
    else:
        return CorrelationRegime.STRONG_NEGATIVE


def _classify_signal_quality(
    confidence: float | None,
    contemp_corr: float | None,
    leading_corr: float | None,
) -> SignalQuality:
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
    """Classify trade outcome based on trade direction correctness."""
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
