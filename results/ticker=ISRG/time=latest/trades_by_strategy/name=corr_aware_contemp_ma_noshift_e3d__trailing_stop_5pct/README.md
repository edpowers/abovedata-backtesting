# Strategy Analysis: corr_aware_contemp_ma_noshift_e3d × trailing_stop_5%

**Ticker:** ISRG
**Entry:** `corr_aware_contemp_ma_noshift_e3d`
**Exit:** `trailing_stop_5%`
**Period:** 2020-04-13 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `True` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `3` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 136.1% |
| **Annualized Return** | 29.8% |
| **Sharpe Ratio** | 1.755 |
| **Max Drawdown** | -23.5% |
| **Total Trades** | 150 |
| **Win Rate** | 36.0% |
| **Signal Accuracy** | 49.6% |
| **Direction Accuracy** | 36.0% |
| **Skill Ratio** | 36.0% |
| **Profit Factor** | 1.41 |
| **Expectancy** | 0.0077 |
| **Tail Ratio** | 2.48 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 730.6% | 136.1% | -594.5% |
| Annualized Return | 21.1% | 29.8% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.1×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0138 | Ideal for 150 trades: 0.0067 |
| Top-1 Trade | 6.6% of gross profit | ✅ Low concentration |
| Top-3 Trades | 18.2% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 87.3% | Strategy survives without best trade |
| Return ex-Top-3 | 24.4% | Strategy survives without top 3 |
| Max Single Trade | 26.1% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 45 | 7.45% | 335.2% | 7.29% | 13.04 |
| no_signal | 25 | 0.17% | 4.3% | 0.66% | 6.92 |
| direction_wrong_loss | 80 | -2.81% | -224.8% | -3.82% | 4.66 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 18 | 5.31% | 95.6% | 55.6% | 55.6% | 2.40% |
| strong_positive | 26 | 1.27% | 33.0% | 46.2% | 46.2% | 0.61% |
| weak_negative | 15 | 0.99% | 14.8% | 33.3% | 33.3% | 0.31% |
| regime_shift | 49 | 0.09% | 4.5% | 30.6% | 30.6% | 0.66% |
| unknown | 19 | -0.54% | -10.2% | 36.8% | 36.8% | -1.22% |
| weak_positive | 23 | -0.99% | -22.8% | 21.7% | 21.7% | -1.48% |

**Best regime:** `strong_negative` — 18 trades, 95.6% total return, 55.6% win rate.
**Worst regime:** `weak_positive` — 23 trades, -22.8% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 42 | -2.89% | -121.5% |
| ❌ | ✅ | 21 | 6.20% | 130.3% |
| ✅ | ❌ | 38 | -2.72% | -103.3% |
| ✅ | ✅ | 24 | 8.54% | 205.0% |

### Flip Trades (Signal Wrong → Direction Right)

**30 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **6.3%**
- Total return: **188.2%**
- Average alpha: **6.4%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 10 | 5.27% |
| strong_positive | 6 | 4.77% |
| weak_negative | 5 | 7.55% |
| strong_negative | 4 | 11.54% |
| weak_positive | 4 | 5.69% |
| unknown | 1 | 0.11% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 99 | 1.13% | 111.9% | 39.4% | 39.4% |
| high | 16 | 1.55% | 24.9% | 31.2% | 31.2% |
| no_data | 1 | -0.00% | -0.0% | 0.0% | 0.0% |
| low | 34 | -0.64% | -21.9% | 29.4% | 29.4% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 61 | 1.84% | 112.1% | 44.3% | 44.3% |
| SHORT | 89 | 0.03% | 2.7% | 30.3% | 30.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 32 | 13.3% | 0.42% | 37.5% | 37.5% | -25.9% |
| 2021 | 26 | 22.3% | 0.86% | 34.6% | 34.6% | 14.8% |
| 2022 | 32 | 12.6% | 0.39% | 34.4% | 34.4% | 26.0% |
| 2023 | 14 | 51.3% | 3.67% | 35.7% | 35.7% | 23.2% |
| 2024 | 17 | 23.9% | 1.40% | 41.2% | 41.2% | -0.1% |
| 2025 | 26 | -20.5% | -0.79% | 34.6% | 34.6% | -12.7% |
| 2026 | 3 | 11.9% | 3.97% | 33.3% | 33.3% | 13.4% |

### Macro Context by Year

**2020** (Strong year: 13.3%, 32 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 22.3%, 26 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 12.6%, 32 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 51.3%, 14 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 23.9%, 17 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -20.5%, 26 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 11.9%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -65.4% cumulative (trade 117 to trade 137)
**Period:** 2024-10-08 to 2025-04-17 (21 trades)
**Peak cumulative return:** 137.0% → **Trough:** 71.6%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-10-08 | 2024-10-14 | 1.0000 | 1.42% | strong_positive | ✅ |
| 2024-10-14 | 2024-10-18 | -1.0000 | -6.88% | strong_positive | ❌ |
| 2024-10-21 | 2024-11-08 | -1.0000 | -3.39% | weak_positive | ❌ |
| 2024-11-11 | 2024-12-06 | -1.0000 | -2.74% | weak_positive | ❌ |
| 2024-12-09 | 2025-01-06 | -1.0000 | -0.65% | weak_positive | ❌ |
| 2025-01-07 | 2025-01-15 | -1.0000 | -9.07% | weak_positive | ❌ |
| 2025-01-16 | 2025-01-17 | -1.0000 | -1.47% | weak_positive | ❌ |
| 2025-01-17 | 2025-01-21 | 1.0000 | 1.94% | weak_positive | ✅ |
| 2025-01-22 | 2025-01-24 | 1.0000 | -4.32% | weak_positive | ❌ |
| 2025-01-27 | 2025-02-25 | 1.0000 | 0.05% | regime_shift | ✅ |
| 2025-02-26 | 2025-02-28 | 1.0000 | -1.34% | regime_shift | ❌ |
| 2025-03-03 | 2025-03-04 | 1.0000 | -1.59% | regime_shift | ❌ |
| 2025-03-05 | 2025-03-06 | 1.0000 | -5.18% | regime_shift | ❌ |
| 2025-03-07 | 2025-03-10 | 1.0000 | -6.88% | regime_shift | ❌ |
| 2025-03-11 | 2025-03-13 | 1.0000 | -3.43% | regime_shift | ❌ |
| 2025-03-14 | 2025-03-28 | 1.0000 | 1.53% | regime_shift | ✅ |
| 2025-03-31 | 2025-04-04 | 1.0000 | -8.82% | regime_shift | ❌ |
| 2025-04-07 | 2025-04-08 | 1.0000 | -1.29% | regime_shift | ❌ |
| 2025-04-09 | 2025-04-10 | 1.0000 | -6.39% | regime_shift | ❌ |
| 2025-04-11 | 2025-04-16 | 1.0000 | -2.48% | regime_shift | ❌ |
| 2025-04-17 | 2025-04-21 | 1.0000 | -2.99% | regime_shift | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 94 | -1.41% | -132.1% | 22.3% |
| 16-30d | 19 | 7.09% | 134.7% | 73.7% |
| 31-50d | 4 | 14.96% | 59.9% | 100.0% |
| 50d+ | 1 | 15.53% | 15.5% | 100.0% |
| 6-15d | 32 | 1.15% | 36.9% | 43.8% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 9

## Conclusions & Observations

**Statistical robustness:** With 150 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (24.4% remaining).
**Signal vs Direction:** Signal accuracy (49.6%) exceeds direction accuracy (36.0%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.
**Regime dependence:** `strong_negative` (18 trades, 12% of total) generates 95.6% — a disproportionate share of returns.

### Known Vulnerabilities

- **Worst year:** 2025 (-20.5%, 26 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery
- **Losing regime:** `unknown` — 19 trades, -10.2% total return
- **Losing regime:** `weak_positive` — 23 trades, -22.8% total return