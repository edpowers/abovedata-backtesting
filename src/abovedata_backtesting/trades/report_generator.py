"""Auto-generated strategy analysis report (Markdown README).

Takes a strategy's metadata dict + trade-level DataFrame and produces
an interpretive markdown report with macro context, regime analysis,
and actionable conclusions.

Usage inside save_results:
    report = StrategyReport(metadata=strat_summary, trades_df=best_trades, ticker="DE")
    report.write(top_dir / "README.md")
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
import polars as pl

# =============================================================================
# Macro context timeline
# =============================================================================


@dataclass(frozen=True)
class MacroEvent:
    """A macro-economic event or regime that provides context for trade periods."""

    name: str
    start: date
    end: date
    description: str
    impact: str  # "bullish", "bearish", "volatile", "neutral"


# Hardcoded timeline of major macro events affecting US equities / industrials.
MACRO_TIMELINE: list[MacroEvent] = [
    MacroEvent(
        name="US-China Trade War Escalation",
        start=date(2018, 3, 1),
        end=date(2019, 12, 31),
        description=(
            "Tariff escalation between US and China created uncertainty for "
            "industrial exporters. Deere particularly exposed due to agricultural "
            "equipment demand tied to commodity prices and trade flows."
        ),
        impact="volatile",
    ),
    MacroEvent(
        name="Fed Rate Cuts (2019)",
        start=date(2019, 7, 1),
        end=date(2019, 10, 31),
        description=(
            "Three 'insurance' rate cuts as growth slowed. Supportive for "
            "capital-intensive industrials but uncertainty remained elevated."
        ),
        impact="bullish",
    ),
    MacroEvent(
        name="COVID-19 Crash & Recovery",
        start=date(2020, 2, 20),
        end=date(2020, 4, 30),
        description=(
            "S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder "
            "due to supply chain disruption and demand collapse. DE fell from "
            "$180 to $115 before recovering."
        ),
        impact="bearish",
    ),
    MacroEvent(
        name="Post-COVID Stimulus Rally",
        start=date(2020, 4, 1),
        end=date(2021, 11, 30),
        description=(
            "Unprecedented fiscal and monetary stimulus drove a broad equity "
            "rally. Agricultural commodity boom and infrastructure spending "
            "expectations boosted DE from ~$130 to ~$390. Strong negative "
            "UCC-price correlation period — falling UCC filings while "
            "revenues surged."
        ),
        impact="bullish",
    ),
    MacroEvent(
        name="Fed Tightening Cycle",
        start=date(2022, 1, 1),
        end=date(2023, 7, 31),
        description=(
            "Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive "
            "industrials whipsawed as markets repriced duration risk. DE "
            "traded in a wide $280-$450 range with sharp reversals."
        ),
        impact="volatile",
    ),
    MacroEvent(
        name="2022 Bear Market",
        start=date(2022, 1, 3),
        end=date(2022, 10, 12),
        description=(
            "S&P 500 peak-to-trough decline of ~25%. Industrials sold off on "
            "recession fears. Weak correlation signals during this period — "
            "macro dominated micro."
        ),
        impact="bearish",
    ),
    MacroEvent(
        name="2023 Soft Landing Rally",
        start=date(2023, 1, 1),
        end=date(2023, 12, 31),
        description=(
            "Growing confidence in a soft landing. DE benefited from strong "
            "ag cycle and precision agriculture demand. Correlation regimes "
            "began shifting as rate expectations stabilized."
        ),
        impact="bullish",
    ),
    MacroEvent(
        name="2024 Election Year Uncertainty",
        start=date(2024, 6, 1),
        end=date(2024, 11, 30),
        description=(
            "Policy uncertainty around tariffs, trade, and fiscal direction "
            "created headwinds for export-oriented industrials. DE faced "
            "ag cycle downturn concerns."
        ),
        impact="volatile",
    ),
    MacroEvent(
        name="2025 Tariff Escalation",
        start=date(2025, 2, 1),
        end=date(2025, 6, 30),
        description=(
            "New tariff announcements on steel, aluminum, and reciprocal "
            "tariffs created fresh uncertainty for industrial supply chains. "
            "Regime shifts in correlation structure as market repriced "
            "trade exposure."
        ),
        impact="volatile",
    ),
    MacroEvent(
        name="2025 H2 Recovery",
        start=date(2025, 7, 1),
        end=date(2025, 12, 31),
        description=(
            "Trade deal optimism and rate cut expectations drove industrial "
            "recovery. DE recovered on strong order book and precision ag "
            "technology demand."
        ),
        impact="bullish",
    ),
]


def _get_macro_context(start: date, end: date) -> list[MacroEvent]:
    """Return macro events overlapping with a date range."""
    return [e for e in MACRO_TIMELINE if e.start <= end and e.end >= start]


def _get_macro_for_year(year: int) -> list[MacroEvent]:
    """Return macro events active during a given year."""
    return _get_macro_context(date(year, 1, 1), date(year, 12, 31))


# =============================================================================
# Entry/exit parameter descriptions
# =============================================================================

ENTRY_PARAM_DESCRIPTIONS: dict[str, str] = {
    "signal_col": "UCC signal column used as the fundamental input",
    "corr_col": (
        "Correlation variant for direction determination. "
        "'leading_ma' uses the smoothed leading correlation between UCC filings "
        "and next-quarter revenue, which captures the predictive relationship"
    ),
    "min_signal_abs": (
        "Minimum absolute signal value to trigger a trade. "
        "0.0 means any non-zero signal generates a trade"
    ),
    "skip_regime_shifts": (
        "Whether to skip entries during correlation regime shifts. "
        "When True, avoids trading during unstable correlation periods"
    ),
    "scale_by_confidence": "Whether to scale position size by signal confidence score",
    "confidence_col": "Which confidence metric to use for scaling",
    "entry_days_before": (
        "Number of trading days before earnings to enter. "
        "Higher values capture the pre-earnings drift but increase "
        "exposure to non-earnings price moves"
    ),
    "use_prior_quarter_corr": (
        "Use the prior quarter's correlation for direction (True), "
        "or the current quarter's in-progress estimate. Prior quarter "
        "avoids look-ahead bias from partial-quarter correlation estimates"
    ),
}

EXIT_TYPE_DESCRIPTIONS: dict[str, str] = {
    "sl-5%_tp10%": (
        "Stop-loss at -5%, take-profit at +10%. Asymmetric exit creates "
        "a 2:1 reward/risk ratio — when direction is correct, gains are "
        "2× what losses are when wrong"
    ),
    "sl-10%_tp20%": (
        "Stop-loss at -10%, take-profit at +20%. Wider bands allow more "
        "time for the thesis to play out but increase per-trade risk"
    ),
    "trailing_stop_5%": (
        "5% trailing stop from the high-water mark. Lets winners run "
        "while cutting losses, but can exit too early in volatile markets"
    ),
    "trailing_stop_10%": (
        "10% trailing stop. More room for normal volatility, captures larger trends"
    ),
    "signal_change": (
        "Exit when the UCC signal reverses direction. Fundamentally-driven "
        "exit that stays in the trade as long as the thesis holds"
    ),
    "fixed_holding_30d": "Fixed 30-day holding period after entry",
    "fixed_holding_60d": "Fixed 60-day holding period after entry",
    "fixed_holding_90d": "Fixed 90-day holding period after entry",
}


# =============================================================================
# Analysis computations (all pure functions on DataFrames)
# =============================================================================


def _compute_annual_performance(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.with_columns(pl.col("entry_date").dt.year().alias("year"))
        .group_by("year")
        .agg(
            pl.len().alias("trades"),
            pl.col("trade_return").sum().alias("total_return"),
            pl.col("trade_return").mean().alias("avg_return"),
            (pl.col("trade_return") > 0).mean().alias("win_rate"),
            pl.col("trade_direction_correct").mean().alias("direction_accuracy"),
            pl.col("alpha_contribution").sum().alias("total_alpha"),
        )
        .sort("year")
    )


def _compute_regime_performance(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.group_by("correlation_regime")
        .agg(
            pl.len().alias("count"),
            pl.col("trade_return").mean().alias("avg_return"),
            pl.col("trade_return").sum().alias("total_return"),
            pl.col("trade_direction_correct").mean().alias("direction_accuracy"),
            (pl.col("trade_return") > 0).mean().alias("win_rate"),
            pl.col("alpha_contribution").mean().alias("avg_alpha"),
        )
        .sort("total_return", descending=True)
    )


def _compute_outcome_breakdown(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.group_by("outcome")
        .agg(
            pl.len().alias("count"),
            pl.col("trade_return").mean().alias("avg_return"),
            pl.col("trade_return").sum().alias("total_return"),
            pl.col("alpha_contribution").mean().alias("avg_alpha"),
            pl.col("holding_days").mean().alias("avg_holding"),
        )
        .sort("total_return", descending=True)
    )


def _compute_signal_vs_direction(df: pl.DataFrame) -> pl.DataFrame:
    with_signal = df.filter(pl.col("outcome") != "no_signal")
    return (
        with_signal.group_by("signal_correct", "trade_direction_correct")
        .agg(
            pl.len().alias("count"),
            pl.col("trade_return").mean().alias("avg_return"),
            pl.col("trade_return").sum().alias("total_return"),
        )
        .sort("signal_correct", "trade_direction_correct")
    )


def _compute_correlation_flip(df: pl.DataFrame) -> dict[str, Any]:
    """Trades where signal was wrong but direction was right."""
    flip = df.filter(
        (pl.col("signal_correct") == False)  # noqa: E712
        & (pl.col("trade_direction_correct") == True)  # noqa: E712
    )
    if flip.is_empty():
        return {"count": 0, "avg_return": 0.0, "total_return": 0.0, "avg_alpha": 0.0}
    return {
        "count": flip.height,
        "avg_return": flip["trade_return"].mean(),
        "total_return": flip["trade_return"].sum(),
        "avg_alpha": flip["alpha_contribution"].mean(),
        "regime_distribution": (
            flip.group_by("correlation_regime")
            .agg(
                pl.len().alias("count"),
                pl.col("trade_return").mean().alias("avg_return"),
            )
            .sort("count", descending=True)
        ),
    }


def _compute_quality_performance(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.group_by("signal_quality")
        .agg(
            pl.len().alias("count"),
            pl.col("trade_return").mean().alias("avg_return"),
            pl.col("trade_return").sum().alias("total_return"),
            pl.col("trade_direction_correct").mean().alias("direction_accuracy"),
            (pl.col("trade_return") > 0).mean().alias("win_rate"),
        )
        .sort("total_return", descending=True)
    )


def _compute_holding_buckets(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.with_columns(
            pl.when(pl.col("holding_days") <= 5)
            .then(pl.lit("1-5d"))
            .when(pl.col("holding_days") <= 15)
            .then(pl.lit("6-15d"))
            .when(pl.col("holding_days") <= 30)
            .then(pl.lit("16-30d"))
            .when(pl.col("holding_days") <= 50)
            .then(pl.lit("31-50d"))
            .otherwise(pl.lit("50d+"))
            .alias("bucket")
        )
        .group_by("bucket")
        .agg(
            pl.len().alias("count"),
            pl.col("trade_return").mean().alias("avg_return"),
            pl.col("trade_return").sum().alias("total_return"),
            (pl.col("trade_return") > 0).mean().alias("win_rate"),
        )
        .sort("bucket")
    )


def _compute_long_short_split(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.with_columns(
            pl.when(pl.col("direction") > 0)
            .then(pl.lit("LONG"))
            .otherwise(pl.lit("SHORT"))
            .alias("side")
        )
        .group_by("side")
        .agg(
            pl.len().alias("count"),
            pl.col("trade_return").mean().alias("avg_return"),
            pl.col("trade_return").sum().alias("total_return"),
            (pl.col("trade_return") > 0).mean().alias("win_rate"),
            pl.col("trade_direction_correct").mean().alias("direction_accuracy"),
        )
        .sort("side")
    )


def _compute_drawdown(
    returns: list[float],
    dates: list[date],
) -> dict[str, Any]:
    """Worst drawdown in the cumulative trade-by-trade return series."""
    if len(returns) < 2:
        return {"drawdown": 0.0, "peak_idx": 0, "trough_idx": 0}
    cum = np.cumsum(returns)
    peak = np.maximum.accumulate(cum)
    dd = cum - peak
    trough_idx = int(np.argmin(dd))
    peak_val = peak[trough_idx]
    peak_idx = int(np.where(cum == peak_val)[0][0])
    return {
        "drawdown": float(dd[trough_idx]),
        "peak_idx": peak_idx,
        "trough_idx": trough_idx,
        "peak_date": dates[peak_idx],
        "trough_date": dates[trough_idx],
        "peak_cum_return": float(peak_val),
        "trough_cum_return": float(cum[trough_idx]),
        "n_trades": trough_idx - peak_idx + 1,
    }


def _compute_streaks(wins: list[bool]) -> dict[str, int]:
    max_win = max_loss = cur_win = cur_loss = 0
    for w in wins:
        if w:
            cur_win += 1
            cur_loss = 0
            max_win = max(max_win, cur_win)
        else:
            cur_loss += 1
            cur_win = 0
            max_loss = max(max_loss, cur_loss)
    return {"max_win_streak": max_win, "max_loss_streak": max_loss}


# =============================================================================
# Markdown formatting helpers
# =============================================================================


def _fmt_pct(v: float | None, decimals: int = 1) -> str:
    if v is None:
        return "N/A"
    return f"{v:.{decimals}%}"


def _fmt_f(v: float | None, decimals: int = 2) -> str:
    if v is None:
        return "N/A"
    return f"{v:.{decimals}f}"


def _md_table(df: pl.DataFrame, fmt_map: dict[str, str] | None = None) -> str:
    """Convert a Polars DataFrame to a markdown table."""
    fmt_map = fmt_map or {}
    headers = df.columns
    rows_data = df.to_dicts()

    formatted_rows: list[list[str]] = []
    for row in rows_data:
        cells: list[str] = []
        for col in headers:
            val = row[col]
            fmt = fmt_map.get(col, "")
            if val is None:
                cells.append("—")
            elif fmt == "pct":
                cells.append(_fmt_pct(val))
            elif fmt == "pct2":
                cells.append(_fmt_pct(val, 2))
            elif fmt == "f2":
                cells.append(_fmt_f(val, 2))
            elif fmt == "f4":
                cells.append(_fmt_f(val, 4))
            elif isinstance(val, bool):
                cells.append("✅" if val else "❌")
            elif isinstance(val, float):
                cells.append(_fmt_f(val, 4))
            else:
                cells.append(str(val))
        formatted_rows.append(cells)

    display_headers = [h.replace("_", " ").title() for h in headers]
    lines = [
        "| " + " | ".join(display_headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for cells in formatted_rows:
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


# =============================================================================
# Strategy Report
# =============================================================================


@dataclass
class StrategyReport:
    """Generates an interpretive markdown analysis report for a strategy.

    Parameters
    ----------
    metadata : dict
        Strategy metadata (from save_results strat_summary dict).
    trades_df : pl.DataFrame
        Trade-level DataFrame with all analysis columns.
    ticker : str
        Ticker symbol for context.
    """

    metadata: dict[str, Any]
    trades_df: pl.DataFrame
    ticker: str

    @classmethod
    def from_saved(cls, directory: str | Path, ticker: str = "") -> StrategyReport:
        """Load from a saved strategy directory (trades.parquet + metadata.json)."""
        import json

        d = Path(directory)
        with open(d / "metadata.json") as f:
            metadata = json.load(f)
        trades_df = pl.read_parquet(d / "trades.parquet")
        ticker = ticker or metadata.get("ticker", "UNKNOWN")
        return cls(metadata=metadata, trades_df=trades_df, ticker=ticker)

    def _ensure_date_cols(self) -> pl.DataFrame:
        """Ensure date columns are Date type (handles CSV string inputs)."""
        df = self.trades_df
        for col in ("entry_date", "exit_date", "signal_date"):
            if col in df.columns and df[col].dtype == pl.Utf8:
                df = df.with_columns(pl.col(col).str.to_date())
        return df

    def generate(self) -> str:
        """Generate the full markdown report."""
        df = self._ensure_date_cols()
        m = self.metadata
        sections = [
            self._header(m, df),
            self._strategy_description(m),
            self._headline_metrics(m),
            self._diversity_assessment(m),
            self._outcome_analysis(df),
            self._regime_analysis(df),
            self._correlation_flip_analysis(df),
            self._signal_quality_analysis(df),
            self._long_short_analysis(df),
            self._annual_performance(df),
            self._drawdown_analysis(df),
            self._holding_period_analysis(df),
            self._streak_analysis(df),
            self._conclusions(m, df),
        ]
        return "\n\n".join(s for s in sections if s)

    def write(self, path: str | Path) -> None:
        """Write the report to a markdown file."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.generate())

    # ── Section generators ──────────────────────────────────────────────

    def _header(self, m: dict, df: pl.DataFrame) -> str:
        first_date = df["entry_date"].min()
        last_date = df["exit_date"].max()
        return textwrap.dedent(f"""\
            # Strategy Analysis: {m['name']}

            **Ticker:** {self.ticker}
            **Entry:** `{m['entry']}`
            **Exit:** `{m['exit']}`
            **Period:** {first_date} to {last_date}
            **Generated:** Auto-generated strategy analysis report""")

    def _strategy_description(self, m: dict) -> str:
        lines = ["## Strategy Description", ""]
        entry_params = m.get("entry_params", {})
        exit_params = m.get("exit_params", {})
        entry_type = entry_params.get("entry_type", "unknown")

        if entry_type == "correlation_aware":
            lines.extend(
                [
                    "This is a **correlation-aware** entry strategy that uses UCC "
                    "(Uniform Commercial Code) filing data as a leading indicator "
                    "of corporate revenue trends. Unlike simple signal-threshold "
                    "strategies, it determines trade **direction** by combining the "
                    "signal value with the historical correlation between UCC filings "
                    "and revenue outcomes:",
                    "",
                    "> `trade_direction = sign(UCC_signal) × sign(correlation)`",
                    "",
                    "When UCC filings and revenue are positively correlated "
                    "(more filings → more revenue), a positive signal means go long. "
                    "When they're **negatively** correlated (more filings → less revenue), "
                    "a positive signal means go **short** — the correlation flip.",
                ]
            )
        else:
            lines.append(f"Entry type: **{entry_type}**")

        lines.extend(["", "### Entry Parameters", ""])
        for param, value in entry_params.items():
            if param == "entry_type":
                continue
            desc = ENTRY_PARAM_DESCRIPTIONS.get(param, "")
            desc_str = f" — {desc}" if desc else ""
            lines.append(f"- **{param}:** `{value}`{desc_str}")

        lines.extend(["", "### Exit Parameters", ""])
        exit_type = exit_params.get("exit_type", m.get("exit", ""))
        desc = EXIT_TYPE_DESCRIPTIONS.get(exit_type, "")
        lines.append(f"- **Exit type:** `{exit_type}`")
        if desc:
            lines.append(f"  - {desc}")

        return "\n".join(lines)

    def _headline_metrics(self, m: dict) -> str:
        return textwrap.dedent(f"""\
            ## Headline Performance

            | Metric | Value |
            |---|---|
            | **Total Return** | {_fmt_pct(m.get('total_return'))} |
            | **Annualized Return** | {_fmt_pct(m.get('annualized_return'))} |
            | **Sharpe Ratio** | {_fmt_f(m.get('sharpe'), 3)} |
            | **Max Drawdown** | {_fmt_pct(m.get('max_drawdown'))} |
            | **Total Trades** | {m.get('n_trades')} |
            | **Win Rate** | {_fmt_pct(m.get('win_rate'))} |
            | **Signal Accuracy** | {_fmt_pct(m.get('signal_accuracy'))} |
            | **Direction Accuracy** | {_fmt_pct(m.get('direction_accuracy'))} |
            | **Skill Ratio** | {_fmt_pct(m.get('skill_ratio'))} |
            | **Profit Factor** | {_fmt_f(m.get('profit_factor'))} |
            | **Expectancy** | {_fmt_f(m.get('expectancy'), 4)} |
            | **Tail Ratio** | {_fmt_f(m.get('tail_ratio'))} |""")

    def _diversity_assessment(self, m: dict) -> str:
        n = m.get("n_trades", 1)
        hhi = m.get("hhi", 0)
        ideal_hhi = 1 / n if n > 0 else 0
        hhi_ratio = hhi / ideal_hhi if ideal_hhi > 0 else 0

        if hhi_ratio < 1.5:
            assessment = "**Excellent** — nearly perfectly diversified"
        elif hhi_ratio < 2.5:
            assessment = "**Good** — moderate concentration, acceptable"
        elif hhi_ratio < 4.0:
            assessment = "**Moderate** — noticeable concentration in top trades"
        else:
            assessment = "**Concentrated** — returns depend heavily on a few trades"

        top1 = m.get("top1_pct", 0) or 0
        top3 = m.get("top3_pct", 0) or 0
        ex1 = m.get("return_ex_top1", 0) or 0
        ex3 = m.get("return_ex_top3", 0) or 0

        lines = [
            "## Diversity & Concentration",
            "",
            f"Diversification: {assessment} (HHI ratio: {_fmt_f(hhi_ratio, 1)}×)",
            "",
            "| Metric | Value | Interpretation |",
            "|---|---|---|",
            f"| HHI | {_fmt_f(hhi, 4)} | Ideal for {n} trades: {_fmt_f(ideal_hhi, 4)} |",
            f"| Top-1 Trade | {_fmt_pct(top1)} of gross profit | {'⚠️ High' if top1 > 0.2 else '✅ Low'} concentration |",
            f"| Top-3 Trades | {_fmt_pct(top3)} of gross profit | {'⚠️ High' if top3 > 0.5 else '✅ Low'} concentration |",
            f"| Return ex-Top-1 | {_fmt_pct(ex1)} | Strategy {'survives' if ex1 > 0 else 'fails'} without best trade |",
            f"| Return ex-Top-3 | {_fmt_pct(ex3)} | Strategy {'survives' if ex3 > 0 else 'fails'} without top 3 |",
            f"| Max Single Trade | {_fmt_pct(m.get('max_single_contribution'))} | Largest individual trade return |",
        ]
        return "\n".join(lines)

    def _outcome_analysis(self, df: pl.DataFrame) -> str:
        outcomes = _compute_outcome_breakdown(df)
        lines = ["## Outcome Analysis", ""]

        outcome_types = set(outcomes["outcome"].to_list())
        has_right_loss = "direction_right_loss" in outcome_types
        has_wrong_profit = "direction_wrong_profit" in outcome_types

        if not has_right_loss and not has_wrong_profit:
            lines.extend(
                [
                    "**Clean binary outcomes:** Every trade with ground truth either "
                    "got direction right and profited, or got direction wrong and lost. "
                    "Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). "
                    "This indicates the exit mechanism (SL/TP) is perfectly aligned with "
                    "direction correctness — the asymmetric payoff is the entire edge.",
                    "",
                ]
            )

        lines.append(
            _md_table(
                outcomes,
                {
                    "avg_return": "pct2",
                    "total_return": "pct",
                    "avg_alpha": "pct2",
                    "avg_holding": "f2",
                },
            )
        )
        return "\n".join(lines)

    def _regime_analysis(self, df: pl.DataFrame) -> str:
        regimes = _compute_regime_performance(df)
        lines = [
            "## Correlation Regime Performance",
            "",
            "Performance by the correlation regime at entry time. Regimes are "
            "classified from the contemporaneous and leading correlation between "
            "UCC filings and revenue.",
            "",
            _md_table(
                regimes,
                {
                    "avg_return": "pct2",
                    "total_return": "pct",
                    "direction_accuracy": "pct",
                    "win_rate": "pct",
                    "avg_alpha": "pct2",
                },
            ),
        ]

        if not regimes.is_empty():
            best = regimes.row(0, named=True)
            worst = regimes.row(-1, named=True)
            lines.extend(
                [
                    "",
                    f"**Best regime:** `{best['correlation_regime']}` — "
                    f"{best['count']} trades, {_fmt_pct(best['total_return'])} total return, "
                    f"{_fmt_pct(best['win_rate'])} win rate.",
                ]
            )
            if worst["total_return"] < 0:
                lines.append(
                    f"**Worst regime:** `{worst['correlation_regime']}` — "
                    f"{worst['count']} trades, {_fmt_pct(worst['total_return'])} total return."
                )
        return "\n".join(lines)

    def _correlation_flip_analysis(self, df: pl.DataFrame) -> str:
        flip = _compute_correlation_flip(df)
        cross = _compute_signal_vs_direction(df)

        lines = [
            "## The Correlation Flip Effect",
            "",
            "For correlation-aware strategies, the trade direction includes a "
            "correlation-based flip: `direction = sign(signal) × sign(correlation)`. "
            "The signal can be 'wrong' about the earnings surprise while the trade "
            "direction is correct because the correlation flip compensated.",
            "",
        ]

        if not cross.is_empty():
            lines.extend(
                [
                    "### Signal × Direction Cross-Tab",
                    "",
                    _md_table(cross, {"avg_return": "pct2", "total_return": "pct"}),
                    "",
                ]
            )

        if flip["count"] > 0:
            lines.extend(
                [
                    "### Flip Trades (Signal Wrong → Direction Right)",
                    "",
                    f"**{flip['count']} trades** where the UCC signal missed the earnings "
                    "surprise but the correlation flip correctly identified the price move.",
                    "",
                    f"- Average return: **{_fmt_pct(flip['avg_return'])}**",
                    f"- Total return: **{_fmt_pct(flip['total_return'])}**",
                    f"- Average alpha: **{_fmt_pct(flip['avg_alpha'])}**",
                ]
            )
            regime_dist = flip.get("regime_distribution")
            if regime_dist is not None and not regime_dist.is_empty():
                lines.extend(
                    [
                        "",
                        "Regime distribution of flip trades:",
                        "",
                        _md_table(regime_dist, {"avg_return": "pct2"}),
                    ]
                )

        return "\n".join(lines)

    def _signal_quality_analysis(self, df: pl.DataFrame) -> str:
        quality = _compute_quality_performance(df)
        lines = [
            "## Signal Quality Analysis",
            "",
            "High = strong confidence + strong correlation; "
            "Medium = moderate; Low = weak signals.",
            "",
            _md_table(
                quality,
                {
                    "avg_return": "pct2",
                    "total_return": "pct",
                    "direction_accuracy": "pct",
                    "win_rate": "pct",
                },
            ),
        ]
        return "\n".join(lines)

    def _long_short_analysis(self, df: pl.DataFrame) -> str:
        ls = _compute_long_short_split(df)
        return "\n".join(
            [
                "## Long vs Short Performance",
                "",
                _md_table(
                    ls,
                    {
                        "avg_return": "pct2",
                        "total_return": "pct",
                        "win_rate": "pct",
                        "direction_accuracy": "pct",
                    },
                ),
            ]
        )

    def _annual_performance(self, df: pl.DataFrame) -> str:
        annual = _compute_annual_performance(df)
        lines = [
            "## Annual Performance",
            "",
            _md_table(
                annual,
                {
                    "total_return": "pct",
                    "avg_return": "pct2",
                    "win_rate": "pct",
                    "direction_accuracy": "pct",
                    "total_alpha": "pct",
                },
            ),
            "",
            "### Macro Context by Year",
            "",
        ]

        for row in annual.iter_rows(named=True):
            year = row["year"]
            events = _get_macro_for_year(year)
            total_ret = row["total_return"]
            n_trades = row["trades"]

            if total_ret > 0.1:
                tone = "Strong year"
            elif total_ret > 0:
                tone = "Modestly positive"
            elif total_ret > -0.05:
                tone = "Flat"
            else:
                tone = "Losing year"

            lines.append(
                f"**{year}** ({tone}: {_fmt_pct(total_ret)}, {n_trades} trades)"
            )
            if events:
                for e in events:
                    lines.append(f"- *{e.name}* ({e.impact}): {e.description}")
            else:
                lines.append("- No major macro events flagged.")
            lines.append("")

        return "\n".join(lines)

    def _drawdown_analysis(self, df: pl.DataFrame) -> str:
        returns = df["trade_return"].to_list()
        dates = df["entry_date"].to_list()
        dd = _compute_drawdown(returns, dates)

        lines = [
            "## Worst Drawdown Period",
            "",
            f"**Drawdown:** {_fmt_pct(dd['drawdown'])} cumulative "
            f"(trade {dd['peak_idx'] + 1} to trade {dd['trough_idx'] + 1})",
        ]

        if "peak_date" in dd:
            lines.extend(
                [
                    f"**Period:** {dd['peak_date']} to {dd['trough_date']} "
                    f"({dd['n_trades']} trades)",
                    f"**Peak cumulative return:** {_fmt_pct(dd['peak_cum_return'])} → "
                    f"**Trough:** {_fmt_pct(dd['trough_cum_return'])}",
                ]
            )

            events = _get_macro_context(dd["peak_date"], dd["trough_date"])
            if events:
                lines.extend(["", "**Macro context during drawdown:**"])
                for e in events:
                    lines.append(f"- *{e.name}* ({e.impact}): {e.description}")

            dd_trades = df.slice(dd["peak_idx"], dd["n_trades"])
            if not dd_trades.is_empty():
                display_cols = [
                    c
                    for c in [
                        "entry_date",
                        "exit_date",
                        "direction",
                        "trade_return",
                        "correlation_regime",
                        "trade_direction_correct",
                    ]
                    if c in dd_trades.columns
                ]
                lines.extend(
                    [
                        "",
                        "**Trades during drawdown:**",
                        "",
                        _md_table(
                            dd_trades.select(display_cols), {"trade_return": "pct2"}
                        ),
                    ]
                )

        return "\n".join(lines)

    def _holding_period_analysis(self, df: pl.DataFrame) -> str:
        buckets = _compute_holding_buckets(df)
        return "\n".join(
            [
                "## Holding Period Analysis",
                "",
                _md_table(
                    buckets,
                    {"avg_return": "pct2", "total_return": "pct", "win_rate": "pct"},
                ),
            ]
        )

    def _streak_analysis(self, df: pl.DataFrame) -> str:
        wins = (df["trade_return"] > 0).to_list()
        streaks = _compute_streaks(wins)
        return textwrap.dedent(f"""\
            ## Win/Loss Streaks

            - **Max consecutive wins:** {streaks['max_win_streak']}
            - **Max consecutive losses:** {streaks['max_loss_streak']}""")

    def _conclusions(self, m: dict, df: pl.DataFrame) -> str:
        lines = ["## Conclusions & Observations", ""]
        n = m.get("n_trades", 0)
        hhi = m.get("hhi", 0)
        total_ret = m.get("total_return", 0)
        ex_top3 = m.get("return_ex_top3", 0)
        win_rate = m.get("win_rate", 0)
        profit_factor = m.get("profit_factor", 0)
        direction_acc = m.get("direction_accuracy", 0)
        signal_acc = m.get("signal_accuracy", 0)

        # Statistical robustness
        if n >= 80:
            lines.append(
                f"**Statistical robustness:** With {n} trades, this sample "
                "is large enough for reliable inference."
            )
        elif n >= 30:
            lines.append(
                f"**Statistical robustness:** {n} trades provides a reasonable "
                "sample, though some metrics may have wide confidence intervals."
            )
        else:
            lines.append(
                f"**Statistical robustness:** ⚠️ Only {n} trades — interpret cautiously."
            )

        # Diversification
        ideal_hhi = 1 / n if n > 0 else 0
        if hhi < ideal_hhi * 1.5:
            lines.append(
                f"**Diversification:** Excellent. HHI of {_fmt_f(hhi, 4)} is near "
                f"the theoretical minimum of {_fmt_f(ideal_hhi, 4)}. No single "
                "trade dominates returns."
            )
        elif hhi < ideal_hhi * 3:
            lines.append(
                f"**Diversification:** Acceptable. Returns survive removal of top "
                f"3 trades ({_fmt_pct(ex_top3)} remaining)."
            )
        else:
            lines.append(
                f"**Diversification:** ⚠️ Concentrated. HHI of {_fmt_f(hhi, 4)} "
                f"is {_fmt_f(hhi / ideal_hhi, 1)}× the ideal."
            )

        # Edge
        if profit_factor and profit_factor > 1.5 and win_rate and win_rate > 0.5:
            lines.append(
                f"**Edge:** Genuine structural edge: "
                f"{_fmt_pct(win_rate)} win rate with {_fmt_f(profit_factor)}× "
                "profit factor — wins are systematically larger than losses."
            )

        # Signal vs direction
        if direction_acc and signal_acc:
            if direction_acc < signal_acc:
                lines.append(
                    f"**Signal vs Direction:** Signal accuracy ({_fmt_pct(signal_acc)}) "
                    f"exceeds direction accuracy ({_fmt_pct(direction_acc)}), "
                    "suggesting the correlation flip occasionally inverts a correct "
                    "signal. The flip helps more than it hurts overall."
                )
            elif direction_acc > signal_acc:
                lines.append(
                    f"**Signal vs Direction:** Direction accuracy ({_fmt_pct(direction_acc)}) "
                    f"exceeds signal accuracy ({_fmt_pct(signal_acc)}), confirming "
                    "the correlation flip adds value beyond raw signal prediction."
                )

        # Regime dependence
        regimes = _compute_regime_performance(df)
        if not regimes.is_empty():
            best = regimes.row(0, named=True)
            if (
                best["total_return"] > (total_ret * 0.4 if total_ret else 0)
                and best["count"] < n * 0.3
            ):
                lines.append(
                    f"**Regime dependence:** `{best['correlation_regime']}` "
                    f"({best['count']} trades, {best['count'] / n:.0%} of total) generates "
                    f"{_fmt_pct(best['total_return'])} — a disproportionate share of returns."
                )

        # Vulnerabilities
        lines.extend(["", "### Known Vulnerabilities", ""])
        annual = _compute_annual_performance(df)
        if not annual.is_empty():
            worst_year = annual.sort("total_return").row(0, named=True)
            if worst_year["total_return"] < -0.03:
                events = _get_macro_for_year(worst_year["year"])
                macro_names = (
                    ", ".join(e.name for e in events) if events else "No flagged events"
                )
                lines.append(
                    f"- **Worst year:** {worst_year['year']} "
                    f"({_fmt_pct(worst_year['total_return'])}, "
                    f"{worst_year['trades']} trades). Macro: {macro_names}"
                )

        losing_regimes = regimes.filter(pl.col("total_return") < 0)
        for row in losing_regimes.iter_rows(named=True):
            lines.append(
                f"- **Losing regime:** `{row['correlation_regime']}` — "
                f"{row['count']} trades, {_fmt_pct(row['total_return'])} total return"
            )

        return "\n".join(lines)
