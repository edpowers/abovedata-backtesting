# Strategy Analysis: corr_aware_contemp_sameq_e1d × trailing_stop_5%

**Ticker:** ZBH
**Entry:** `corr_aware_contemp_sameq_e1d`
**Exit:** `trailing_stop_5%`
**Period:** 2019-11-04 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `1` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 15.1% |
| **Annualized Return** | 24.7% |
| **Sharpe Ratio** | 1.368 |
| **Max Drawdown** | -23.7% |
| **Total Trades** | 165 |
| **Win Rate** | 43.6% |
| **Signal Accuracy** | 31.4% |
| **Direction Accuracy** | 44.5% |
| **Skill Ratio** | 44.5% |
| **Profit Factor** | 1.11 |
| **Expectancy** | 0.0021 |
| **Tail Ratio** | 1.35 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | -10.7% | 15.1% | 25.8% |
| Annualized Return | -1.0% | 24.7% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.5×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0092 | Ideal for 165 trades: 0.0061 |
| Top-1 Trade | 3.8% of gross profit | ✅ Low concentration |
| Top-3 Trades | 10.9% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 1.6% | Strategy survives without best trade |
| Return ex-Top-3 | -19.7% | Strategy fails without top 3 |
| Max Single Trade | 13.2% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 61 | 5.12% | 312.1% | 3.74% | 13.43 |
| no_signal | 28 | -0.87% | -24.3% | -2.00% | 8.04 |
| direction_wrong_loss | 76 | -3.33% | -253.5% | -3.38% | 4.88 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 57 | 0.67% | 38.0% | 49.1% | 49.1% | -0.12% |
| weak_positive | 12 | 2.17% | 26.1% | 50.0% | 50.0% | 2.21% |
| unknown | 1 | 13.22% | 13.2% | 100.0% | 100.0% | 7.81% |
| strong_negative | 28 | 0.07% | 1.8% | 46.4% | 46.4% | -0.55% |
| weak_negative | 34 | -0.32% | -10.9% | 44.1% | 44.1% | -1.21% |
| strong_positive | 33 | -1.03% | -33.9% | 27.3% | 27.3% | -1.71% |

**Best regime:** `regime_shift` — 57 trades, 38.0% total return, 49.1% win rate.
**Worst regime:** `strong_positive` — 33 trades, -33.9% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 53 | -3.39% | -179.9% |
| ❌ | ✅ | 41 | 4.95% | 202.8% |
| ✅ | ❌ | 23 | -3.20% | -73.6% |
| ✅ | ✅ | 20 | 5.47% | 109.3% |

### Flip Trades (Signal Wrong → Direction Right)

**52 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **4.7%**
- Total return: **242.5%**
- Average alpha: **3.1%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 15 | 5.16% |
| strong_negative | 13 | 5.27% |
| weak_negative | 12 | 3.79% |
| strong_positive | 8 | 3.69% |
| weak_positive | 4 | 5.41% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 115 | 0.61% | 70.5% | 49.6% | 49.6% |
| low | 11 | 0.21% | 2.4% | 36.4% | 36.4% |
| high | 39 | -0.99% | -38.5% | 28.2% | 28.2% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 95 | 0.15% | 14.6% | 45.3% | 45.3% |
| SHORT | 70 | 0.28% | 19.7% | 41.4% | 41.4% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2019 | 1 | 13.2% | 13.22% | 100.0% | 100.0% | 7.8% |
| 2020 | 45 | 9.8% | 0.22% | 48.9% | 48.9% | -16.6% |
| 2021 | 21 | 48.0% | 2.28% | 61.9% | 61.9% | 30.6% |
| 2022 | 31 | -20.1% | -0.65% | 35.5% | 35.5% | -17.0% |
| 2023 | 19 | 13.1% | 0.69% | 36.8% | 36.8% | -10.7% |
| 2024 | 18 | -7.7% | -0.43% | 33.3% | 33.3% | -22.4% |
| 2025 | 27 | -16.8% | -0.62% | 40.7% | 40.7% | -51.5% |
| 2026 | 3 | -5.3% | -1.77% | 33.3% | 33.3% | -5.4% |

### Macro Context by Year

**2019** (Strong year: 13.2%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Modestly positive: 9.8%, 45 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 48.0%, 21 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -20.1%, 31 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 13.1%, 19 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -7.7%, 18 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -16.8%, 27 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -5.3%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -48.0% cumulative (trade 110 to trade 165)
**Period:** 2023-09-29 to 2026-01-30 (56 trades)
**Peak cumulative return:** 82.2% → **Trough:** 34.3%

**Macro context during drawdown:**
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-09-29 | 2023-10-11 | -1.0000 | 6.12% | weak_positive | ✅ |
| 2023-10-12 | 2023-10-17 | -1.0000 | -3.77% | weak_positive | ❌ |
| 2023-10-18 | 2023-11-02 | -1.0000 | -3.78% | weak_positive | ❌ |
| 2023-11-03 | 2023-11-13 | -1.0000 | 2.69% | weak_positive | ✅ |
| 2023-11-14 | 2023-11-17 | -1.0000 | -3.33% | strong_positive | ❌ |
| 2023-11-20 | 2023-12-01 | -1.0000 | -4.86% | strong_positive | ❌ |
| 2023-12-04 | 2023-12-20 | -1.0000 | -2.66% | strong_positive | ❌ |
| 2023-12-21 | 2024-01-11 | -1.0000 | -2.49% | strong_positive | ❌ |
| 2024-01-12 | 2024-01-31 | -1.0000 | -2.06% | strong_positive | ❌ |
| 2024-02-01 | 2024-02-09 | -1.0000 | 3.50% | strong_positive | ✅ |
| 2024-02-12 | 2024-02-21 | -1.0000 | -1.99% | weak_positive | ❌ |
| 2024-02-22 | 2024-03-27 | -1.0000 | -3.36% | weak_positive | ❌ |
| 2024-03-28 | 2024-05-01 | -1.0000 | 9.41% | weak_positive | ✅ |
| 2024-05-01 | 2024-05-02 | 1.0000 | -0.92% | weak_positive | ❌ |
| 2024-05-03 | 2024-05-23 | 1.0000 | -4.78% | regime_shift | ❌ |
| 2024-05-24 | 2024-06-10 | 1.0000 | -3.03% | regime_shift | ❌ |
| 2024-06-11 | 2024-06-12 | 1.0000 | -1.63% | regime_shift | ❌ |
| 2024-06-13 | 2024-08-05 | 1.0000 | 0.29% | regime_shift | ✅ |
| 2024-08-06 | 2024-08-16 | -1.0000 | -0.99% | regime_shift | ❌ |
| 2024-08-19 | 2024-08-26 | -1.0000 | -2.56% | weak_negative | ❌ |
| 2024-08-27 | 2024-09-27 | -1.0000 | 5.62% | weak_negative | ✅ |
| 2024-09-30 | 2024-10-18 | -1.0000 | 1.52% | weak_negative | ✅ |
| 2024-10-21 | 2024-10-30 | -1.0000 | -4.38% | weak_negative | ❌ |
| 2024-10-31 | 2024-11-06 | -1.0000 | -3.04% | weak_negative | ❌ |
| 2024-11-07 | 2024-11-18 | -1.0000 | -3.98% | weak_negative | ❌ |
| 2024-11-19 | 2025-01-13 | -1.0000 | 4.71% | weak_negative | ✅ |
| 2025-01-14 | 2025-01-16 | -1.0000 | -4.04% | weak_negative | ❌ |
| 2025-01-17 | 2025-02-06 | -1.0000 | 6.27% | weak_negative | ✅ |
| 2025-02-07 | 2025-02-19 | -1.0000 | -2.39% | regime_shift | ❌ |
| 2025-02-20 | 2025-03-07 | -1.0000 | -4.21% | regime_shift | ❌ |
| 2025-03-10 | 2025-03-14 | -1.0000 | 0.61% | regime_shift | ✅ |
| 2025-03-17 | 2025-04-03 | -1.0000 | -0.99% | regime_shift | ❌ |
| 2025-04-04 | 2025-04-07 | -1.0000 | 2.33% | regime_shift | ✅ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -0.63% | regime_shift | ❌ |
| 2025-04-10 | 2025-04-15 | -1.0000 | 4.88% | regime_shift | ✅ |
| 2025-04-16 | 2025-04-23 | -1.0000 | -2.59% | regime_shift | ❌ |
| 2025-04-24 | 2025-05-02 | -1.0000 | -0.87% | regime_shift | ❌ |
| 2025-05-02 | 2025-05-05 | 1.0000 | -11.62% | regime_shift | ❌ |
| 2025-05-06 | 2025-05-19 | 1.0000 | 3.79% | strong_negative | ✅ |
| 2025-05-20 | 2025-05-22 | 1.0000 | -3.86% | strong_negative | ❌ |
| 2025-05-23 | 2025-06-03 | 1.0000 | -0.85% | strong_negative | ❌ |
| 2025-06-04 | 2025-06-16 | 1.0000 | 0.77% | strong_negative | ✅ |
| 2025-06-17 | 2025-07-30 | 1.0000 | 3.72% | strong_negative | ✅ |
| 2025-07-31 | 2025-08-07 | 1.0000 | 7.40% | strong_negative | ✅ |
| 2025-08-08 | 2025-09-10 | 1.0000 | 3.06% | weak_negative | ✅ |
| 2025-09-11 | 2025-09-16 | 1.0000 | -4.93% | weak_negative | ❌ |
| 2025-09-17 | 2025-09-25 | 1.0000 | -2.95% | weak_negative | ❌ |
| 2025-09-26 | 2025-10-10 | 1.0000 | -3.36% | weak_negative | ❌ |
| 2025-10-13 | 2025-10-28 | 1.0000 | 6.36% | weak_negative | ✅ |
| 2025-10-29 | 2025-11-05 | 1.0000 | -12.20% | weak_negative | ❌ |
| 2025-11-06 | 2025-12-03 | 1.0000 | 5.19% | weak_negative | ✅ |
| 2025-12-04 | 2025-12-19 | 1.0000 | -4.33% | weak_negative | ❌ |
| 2025-12-22 | 2026-01-13 | 1.0000 | -1.36% | weak_negative | ❌ |
| 2026-01-14 | 2026-01-27 | 1.0000 | -3.64% | weak_negative | ❌ |
| 2026-01-28 | 2026-01-30 | 1.0000 | 1.59% | weak_negative | ✅ |
| 2026-01-30 | 2026-02-06 | -1.0000 | -3.26% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 79 | -1.31% | -103.4% | 30.4% |
| 16-30d | 15 | 5.97% | 89.6% | 93.3% |
| 31-50d | 5 | 4.53% | 22.7% | 100.0% |
| 50d+ | 2 | 12.51% | 25.0% | 100.0% |
| 6-15d | 64 | 0.01% | 0.4% | 42.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 8

## Conclusions & Observations

**Statistical robustness:** With 165 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (-19.7% remaining).
**Signal vs Direction:** Direction accuracy (44.5%) exceeds signal accuracy (31.4%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Worst year:** 2022 (-20.1%, 31 trades). Macro: Fed Tightening Cycle, 2022 Bear Market
- **Losing regime:** `weak_negative` — 34 trades, -10.9% total return
- **Losing regime:** `strong_positive` — 33 trades, -33.9% total return