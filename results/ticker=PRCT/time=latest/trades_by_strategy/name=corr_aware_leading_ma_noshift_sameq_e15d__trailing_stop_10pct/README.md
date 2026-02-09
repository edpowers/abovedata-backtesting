# Strategy Analysis: corr_aware_leading_ma_noshift_sameq_e15d × trailing_stop_10%

**Ticker:** PRCT
**Entry:** `corr_aware_leading_ma_noshift_sameq_e15d`
**Exit:** `trailing_stop_10%`
**Period:** 2023-04-05 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `leading_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `True` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_10%`
  - 10% trailing stop. More room for normal volatility, captures larger trends

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 91.5% |
| **Annualized Return** | 81.0% |
| **Sharpe Ratio** | 2.308 |
| **Max Drawdown** | -24.3% |
| **Total Trades** | 72 |
| **Win Rate** | 45.8% |
| **Signal Accuracy** | 46.7% |
| **Direction Accuracy** | 44.4% |
| **Skill Ratio** | 44.4% |
| **Profit Factor** | 1.45 |
| **Expectancy** | 0.0145 |
| **Tail Ratio** | 1.77 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | -31.5% | 91.5% | 122.9% |
| Annualized Return | -8.3% | 81.0% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.8×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0257 | Ideal for 72 trades: 0.0139 |
| Top-1 Trade | 11.6% of gross profit | ✅ Low concentration |
| Top-3 Trades | 27.6% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 37.8% | Strategy survives without best trade |
| Return ex-Top-3 | -14.6% | Strategy fails without top 3 |
| Max Single Trade | 38.9% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 20 | 11.56% | 231.2% | 9.81% | 13.45 |
| no_signal | 27 | 0.98% | 26.3% | 0.06% | 7.85 |
| direction_wrong_loss | 25 | -6.14% | -153.5% | -6.19% | 6.44 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 18 | 2.91% | 52.4% | 38.9% | 38.9% | 0.60% |
| weak_negative | 30 | 1.60% | 48.1% | 50.0% | 50.0% | 1.19% |
| strong_negative | 17 | 0.69% | 11.8% | 41.2% | 41.2% | 0.78% |
| unknown | 7 | -1.17% | -8.2% | 57.1% | 57.1% | -2.36% |

**Best regime:** `regime_shift` — 18 trades, 52.4% total return, 38.9% win rate.
**Worst regime:** `unknown` — 7 trades, -8.2% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 15 | -6.07% | -91.1% |
| ❌ | ✅ | 9 | 12.70% | 114.3% |
| ✅ | ❌ | 10 | -6.24% | -62.4% |
| ✅ | ✅ | 11 | 10.62% | 116.9% |

### Flip Trades (Signal Wrong → Direction Right)

**22 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **10.0%**
- Total return: **219.8%**
- Average alpha: **9.6%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 11 | 8.72% |
| strong_negative | 7 | 9.69% |
| regime_shift | 4 | 14.02% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 65 | 1.73% | 112.3% | 44.6% | 44.6% |
| low | 7 | -1.17% | -8.2% | 57.1% | 57.1% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 45 | 1.38% | 62.0% | 42.2% | 42.2% |
| SHORT | 27 | 1.56% | 42.1% | 51.9% | 51.9% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 19 | -1.6% | -0.08% | 36.8% | 36.8% | -13.0% |
| 2024 | 23 | 61.7% | 2.68% | 47.8% | 47.8% | 36.4% |
| 2025 | 29 | 35.7% | 1.23% | 48.3% | 48.3% | 10.8% |
| 2026 | 1 | 8.3% | 8.27% | 100.0% | 100.0% | 8.9% |

### Macro Context by Year

**2023** (Flat: -1.6%, 19 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 61.7%, 23 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 35.7%, 29 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 8.3%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -52.5% cumulative (trade 1 to trade 15)
**Period:** 2023-04-05 to 2023-10-24 (15 trades)
**Peak cumulative return:** 6.6% → **Trough:** -45.9%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-04-05 | 2023-04-19 | 1.0000 | 6.59% | unknown | ✅ |
| 2023-04-20 | 2023-04-27 | 1.0000 | -25.06% | unknown | ❌ |
| 2023-04-28 | 2023-05-02 | 1.0000 | -6.05% | unknown | ❌ |
| 2023-05-03 | 2023-05-09 | 1.0000 | -4.05% | unknown | ❌ |
| 2023-05-10 | 2023-06-01 | 1.0000 | 9.95% | unknown | ✅ |
| 2023-06-02 | 2023-06-26 | 1.0000 | 4.65% | unknown | ✅ |
| 2023-06-27 | 2023-07-27 | 1.0000 | 5.76% | unknown | ✅ |
| 2023-07-28 | 2023-08-08 | 1.0000 | -6.74% | strong_negative | ❌ |
| 2023-08-09 | 2023-08-24 | 1.0000 | -4.75% | strong_negative | ❌ |
| 2023-08-25 | 2023-09-15 | 1.0000 | 6.28% | strong_negative | ✅ |
| 2023-09-18 | 2023-10-02 | 1.0000 | -4.27% | strong_negative | ❌ |
| 2023-10-03 | 2023-10-11 | 1.0000 | -5.82% | strong_negative | ❌ |
| 2023-10-12 | 2023-10-13 | 1.0000 | -4.50% | strong_negative | ❌ |
| 2023-10-16 | 2023-10-23 | 1.0000 | -8.30% | strong_negative | ❌ |
| 2023-10-24 | 2023-10-30 | 1.0000 | -9.62% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 31 | -2.64% | -81.9% | 25.8% |
| 16-30d | 11 | 4.37% | 48.0% | 72.7% |
| 31-50d | 1 | 27.23% | 27.2% | 100.0% |
| 6-15d | 29 | 3.82% | 110.7% | 55.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 3
- **Max consecutive losses:** 7

## Conclusions & Observations

**Statistical robustness:** 72 trades provides a reasonable sample, though some metrics may have wide confidence intervals.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (-14.6% remaining).
**Signal vs Direction:** Signal accuracy (46.7%) exceeds direction accuracy (44.4%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.
**Regime dependence:** `regime_shift` (18 trades, 25% of total) generates 52.4% — a disproportionate share of returns.

### Known Vulnerabilities

- **Losing regime:** `unknown` — 7 trades, -8.2% total return