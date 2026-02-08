# Strategy Analysis: corr_aware_leading_ma_noshift_e30d × fixed_holding_30d

**Ticker:** DE
**Entry:** `corr_aware_leading_ma_noshift_e30d`
**Exit:** `fixed_holding_30d`
**Period:** 2018-07-06 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `leading_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `True` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `fixed_holding_30d`
  - Fixed 30-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 398.5% |
| **Annualized Return** | 13.7% |
| **Sharpe Ratio** | 0.573 |
| **Max Drawdown** | -42.7% |
| **Total Trades** | 58 |
| **Win Rate** | 74.1% |
| **Signal Accuracy** | 55.1% |
| **Direction Accuracy** | 69.4% |
| **Skill Ratio** | 69.4% |
| **Profit Factor** | 2.54 |
| **Expectancy** | 0.0332 |
| **Tail Ratio** | 1.42 |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.0×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0351 | Ideal for 58 trades: 0.0172 |
| Top-1 Trade | 13.6% of gross profit | ✅ Low concentration |
| Top-3 Trades | 28.0% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 248.3% | Strategy survives without best trade |
| Return ex-Top-3 | 130.4% | Strategy survives without top 3 |
| Max Single Trade | 43.2% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 34 | 8.04% | 273.3% | 6.94% | 30.68 |
| no_signal | 9 | 4.93% | 44.4% | 2.49% | 23.22 |
| direction_wrong_loss | 15 | -8.33% | -125.0% | -8.85% | 20.33 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 9 | 13.62% | 122.6% | 77.8% | 77.8% | 10.67% |
| regime_shift | 20 | 2.88% | 57.7% | 75.0% | 75.0% | 1.85% |
| strong_positive | 9 | 2.57% | 23.2% | 77.8% | 77.8% | 0.54% |
| unknown | 4 | 1.33% | 5.3% | 75.0% | 75.0% | 3.70% |
| weak_positive | 9 | -0.56% | -5.1% | 66.7% | 66.7% | -0.77% |
| weak_negative | 7 | -1.57% | -11.0% | 71.4% | 71.4% | -2.91% |

**Best regime:** `strong_negative` — 9 trades, 122.6% total return, 77.8% win rate.
**Worst regime:** `weak_negative` — 7 trades, -11.0% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 7 | -7.81% | -54.7% |
| ❌ | ✅ | 15 | 10.10% | 151.5% |
| ✅ | ❌ | 8 | -8.79% | -70.3% |
| ✅ | ✅ | 19 | 6.41% | 121.9% |

### Flip Trades (Signal Wrong → Direction Right)

**24 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **8.2%**
- Total return: **195.8%**
- Average alpha: **6.3%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 9 | 3.73% |
| strong_positive | 5 | 8.07% |
| strong_negative | 4 | 24.16% |
| weak_positive | 4 | 5.87% |
| unknown | 2 | 0.90% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 38 | 5.23% | 198.8% | 78.9% | 78.9% |
| high | 7 | 0.71% | 5.0% | 57.1% | 57.1% |
| low | 13 | -0.85% | -11.1% | 69.2% | 69.2% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 29 | 5.97% | 173.0% | 82.8% | 82.8% |
| SHORT | 29 | 0.68% | 19.7% | 65.5% | 65.5% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 4 | 5.3% | 1.33% | 75.0% | 75.0% | 14.8% |
| 2019 | 10 | 9.5% | 0.95% | 70.0% | 70.0% | -21.1% |
| 2020 | 6 | 92.9% | 15.48% | 83.3% | 83.3% | 88.7% |
| 2021 | 7 | 31.5% | 4.50% | 85.7% | 85.7% | 17.4% |
| 2022 | 9 | -19.3% | -2.14% | 55.6% | 55.6% | -2.6% |
| 2023 | 6 | 18.8% | 3.13% | 66.7% | 66.7% | 3.5% |
| 2024 | 6 | -3.9% | -0.65% | 50.0% | 50.0% | -16.5% |
| 2025 | 9 | 41.1% | 4.57% | 100.0% | 100.0% | 24.2% |
| 2026 | 1 | 16.7% | 16.73% | 100.0% | 100.0% | 17.2% |

### Macro Context by Year

**2018** (Modestly positive: 5.3%, 4 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 9.5%, 10 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 92.9%, 6 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 31.5%, 7 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -19.3%, 9 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 18.8%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Flat: -3.9%, 6 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 41.1%, 9 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 16.7%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -51.9% cumulative (trade 28 to trade 32)
**Period:** 2022-01-06 to 2022-07-08 (5 trades)
**Peak cumulative return:** 150.5% → **Trough:** 98.6%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-01-06 | 2022-04-04 | 1.0000 | 11.20% | strong_positive | ✅ |
| 2022-04-05 | 2022-05-18 | 1.0000 | -10.89% | weak_positive | ❌ |
| 2022-05-19 | 2022-07-06 | 1.0000 | -20.41% | weak_positive | ❌ |
| 2022-07-07 | 2022-07-08 | 1.0000 | 0.22% | weak_negative | ✅ |
| 2022-07-08 | 2022-08-18 | -1.0000 | -20.80% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 11 | 1.34% | 14.8% | 72.7% |
| 16-30d | 20 | 2.73% | 54.5% | 75.0% |
| 31-50d | 13 | -1.35% | -17.5% | 69.2% |
| 50d+ | 9 | 15.92% | 143.2% | 100.0% |
| 6-15d | 5 | -0.46% | -2.3% | 40.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 10
- **Max consecutive losses:** 2

## Conclusions & Observations

**Statistical robustness:** 58 trades provides a reasonable sample, though some metrics may have wide confidence intervals.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (130.4% remaining).
**Edge:** Genuine structural edge: 74.1% win rate with 2.54× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (69.4%) exceeds signal accuracy (55.1%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Worst year:** 2022 (-19.3%, 9 trades). Macro: Fed Tightening Cycle, 2022 Bear Market
- **Losing regime:** `weak_positive` — 9 trades, -5.1% total return
- **Losing regime:** `weak_negative` — 7 trades, -11.0% total return