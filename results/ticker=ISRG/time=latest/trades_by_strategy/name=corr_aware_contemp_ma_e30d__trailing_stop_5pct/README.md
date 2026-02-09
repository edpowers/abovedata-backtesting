# Strategy Analysis: corr_aware_contemp_ma_e30d × trailing_stop_5%

**Ticker:** ISRG
**Entry:** `corr_aware_contemp_ma_e30d`
**Exit:** `trailing_stop_5%`
**Period:** 2020-03-04 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 238.5% |
| **Annualized Return** | 37.3% |
| **Sharpe Ratio** | 1.975 |
| **Max Drawdown** | -23.5% |
| **Total Trades** | 181 |
| **Win Rate** | 38.7% |
| **Signal Accuracy** | 37.8% |
| **Direction Accuracy** | 41.2% |
| **Skill Ratio** | 41.2% |
| **Profit Factor** | 1.45 |
| **Expectancy** | 0.0092 |
| **Tail Ratio** | 2.22 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 730.6% | 238.5% | -492.1% |
| Annualized Return | 21.1% | 37.3% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.1×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0116 | Ideal for 181 trades: 0.0055 |
| Top-1 Trade | 6.0% of gross profit | ✅ Low concentration |
| Top-3 Trades | 15.7% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 155.8% | Strategy survives without best trade |
| Return ex-Top-3 | 61.0% | Strategy survives without top 3 |
| Max Single Trade | 32.3% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 61 | 7.86% | 479.2% | 8.42% | 10.80 |
| no_signal | 33 | -0.58% | -19.2% | -0.23% | 6.94 |
| direction_wrong_loss | 87 | -3.37% | -293.5% | -4.41% | 4.92 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 57 | 1.36% | 77.3% | 36.8% | 36.8% | 1.88% |
| strong_negative | 35 | 1.04% | 36.4% | 40.0% | 40.0% | -0.40% |
| weak_positive | 20 | 0.92% | 18.3% | 35.0% | 35.0% | 0.38% |
| weak_negative | 16 | 0.80% | 12.9% | 31.2% | 31.2% | 0.24% |
| strong_positive | 26 | 0.48% | 12.6% | 46.2% | 46.2% | -0.16% |
| unknown | 27 | 0.33% | 9.0% | 40.7% | 40.7% | 0.79% |

**Best regime:** `regime_shift` — 57 trades, 77.3% total return, 36.8% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 52 | -3.65% | -189.9% |
| ❌ | ✅ | 40 | 6.70% | 268.0% |
| ✅ | ❌ | 35 | -2.96% | -103.6% |
| ✅ | ✅ | 21 | 10.05% | 211.1% |

### Flip Trades (Signal Wrong → Direction Right)

**49 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **6.7%**
- Total return: **326.6%**
- Average alpha: **7.8%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 16 | 6.98% |
| strong_negative | 8 | 5.83% |
| strong_positive | 7 | 4.01% |
| unknown | 7 | 8.12% |
| weak_positive | 6 | 7.43% |
| weak_negative | 5 | 7.75% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 113 | 1.19% | 134.0% | 41.6% | 41.6% |
| high | 25 | 1.41% | 35.2% | 36.0% | 36.0% |
| no_data | 1 | -0.00% | -0.0% | 0.0% | 0.0% |
| low | 42 | -0.06% | -2.7% | 33.3% | 33.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 79 | 1.37% | 108.6% | 41.8% | 41.8% |
| SHORT | 102 | 0.57% | 57.9% | 36.3% | 36.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 42 | 12.6% | 0.30% | 38.1% | 38.1% | -1.1% |
| 2021 | 24 | 80.0% | 3.33% | 45.8% | 45.8% | 68.9% |
| 2022 | 47 | 0.7% | 0.02% | 38.3% | 38.3% | 19.4% |
| 2023 | 17 | 64.0% | 3.76% | 52.9% | 52.9% | 39.0% |
| 2024 | 17 | 28.4% | 1.67% | 41.2% | 41.2% | 5.9% |
| 2025 | 32 | -38.8% | -1.21% | 25.0% | 25.0% | -31.6% |
| 2026 | 2 | 19.6% | 9.79% | 50.0% | 50.0% | 21.3% |

### Macro Context by Year

**2020** (Strong year: 12.6%, 42 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 80.0%, 24 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Modestly positive: 0.7%, 47 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 64.0%, 17 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 28.4%, 17 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -38.8%, 32 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 19.6%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -67.7% cumulative (trade 141 to trade 173)
**Period:** 2024-08-06 to 2025-09-16 (33 trades)
**Peak cumulative return:** 193.5% → **Trough:** 125.9%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-08-06 | 2024-09-05 | 1.0000 | 6.48% | strong_positive | ✅ |
| 2024-09-06 | 2024-09-11 | -1.0000 | -4.05% | strong_positive | ❌ |
| 2024-09-12 | 2024-10-18 | -1.0000 | -5.49% | strong_positive | ❌ |
| 2024-10-21 | 2024-11-08 | -1.0000 | -3.39% | weak_positive | ❌ |
| 2024-11-11 | 2024-12-06 | -1.0000 | -2.74% | weak_positive | ❌ |
| 2024-12-09 | 2024-12-19 | 1.0000 | -2.77% | weak_positive | ❌ |
| 2024-12-20 | 2025-01-15 | 1.0000 | 10.62% | weak_positive | ✅ |
| 2025-01-16 | 2025-01-24 | 1.0000 | -0.01% | weak_positive | ❌ |
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
| 2025-04-22 | 2025-04-23 | 1.0000 | 1.92% | regime_shift | ✅ |
| 2025-04-24 | 2025-05-23 | 1.0000 | 6.18% | strong_negative | ✅ |
| 2025-05-27 | 2025-06-09 | 1.0000 | -4.37% | strong_negative | ❌ |
| 2025-06-10 | 2025-06-13 | 1.0000 | -3.29% | strong_negative | ❌ |
| 2025-06-16 | 2025-07-09 | 1.0000 | 1.75% | strong_negative | ✅ |
| 2025-07-10 | 2025-07-23 | 1.0000 | -4.58% | strong_negative | ❌ |
| 2025-07-24 | 2025-07-31 | 1.0000 | -1.54% | strong_negative | ❌ |
| 2025-08-01 | 2025-08-07 | 1.0000 | -2.76% | strong_negative | ❌ |
| 2025-08-08 | 2025-08-21 | 1.0000 | -0.04% | strong_negative | ❌ |
| 2025-08-22 | 2025-09-03 | 1.0000 | -7.35% | strong_negative | ❌ |
| 2025-09-04 | 2025-09-10 | 1.0000 | -1.00% | strong_negative | ❌ |
| 2025-09-11 | 2025-09-15 | 1.0000 | -4.80% | strong_negative | ❌ |
| 2025-09-16 | 2025-10-10 | 1.0000 | -1.13% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 109 | -1.32% | -144.1% | 27.5% |
| 16-30d | 19 | 7.50% | 142.6% | 68.4% |
| 31-50d | 5 | 14.84% | 74.2% | 80.0% |
| 50d+ | 1 | 15.53% | 15.5% | 100.0% |
| 6-15d | 47 | 1.67% | 78.4% | 46.8% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 9

## Conclusions & Observations

**Statistical robustness:** With 181 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (61.0% remaining).
**Signal vs Direction:** Direction accuracy (41.2%) exceeds signal accuracy (37.8%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Worst year:** 2025 (-38.8%, 32 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery