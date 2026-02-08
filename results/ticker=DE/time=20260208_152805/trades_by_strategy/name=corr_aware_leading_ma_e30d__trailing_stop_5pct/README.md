# Strategy Analysis: corr_aware_leading_ma_e30d × trailing_stop_5%

**Ticker:** DE
**Entry:** `corr_aware_leading_ma_e30d`
**Exit:** `trailing_stop_5%`
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
| **Total Return** | 195.0% |
| **Annualized Return** | 37.9% |
| **Sharpe Ratio** | 1.644 |
| **Max Drawdown** | -29.9% |
| **Total Trades** | 113 |
| **Win Rate** | 51.3% |
| **Signal Accuracy** | 52.4% |
| **Direction Accuracy** | 48.5% |
| **Skill Ratio** | 48.5% |
| **Profit Factor** | 1.56 |
| **Expectancy** | 0.0123 |
| **Tail Ratio** | 1.91 |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.9×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0165 | Ideal for 113 trades: 0.0088 |
| Top-1 Trade | 7.8% of gross profit | ✅ Low concentration |
| Top-3 Trades | 20.6% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 126.9% | Strategy survives without best trade |
| Return ex-Top-3 | 45.9% | Strategy survives without top 3 |
| Max Single Trade | 30.0% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 50 | 6.46% | 322.8% | 4.91% | 20.34 |
| no_signal | 10 | 5.77% | 57.7% | 3.44% | 23.00 |
| direction_wrong_loss | 53 | -4.55% | -241.1% | -5.24% | 10.60 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 15 | 6.19% | 92.8% | 80.0% | 80.0% | 5.05% |
| weak_positive | 15 | 4.29% | 64.4% | 66.7% | 66.7% | 3.18% |
| strong_positive | 25 | 0.49% | 12.2% | 52.0% | 52.0% | -0.66% |
| unknown | 5 | 0.75% | 3.8% | 40.0% | 40.0% | 0.68% |
| regime_shift | 34 | 0.04% | 1.3% | 38.2% | 38.2% | -1.43% |
| weak_negative | 19 | -1.85% | -35.1% | 42.1% | 42.1% | -3.13% |

**Best regime:** `strong_negative` — 15 trades, 92.8% total return, 80.0% win rate.
**Worst regime:** `weak_negative` — 19 trades, -35.1% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 31 | -4.39% | -136.1% |
| ❌ | ✅ | 18 | 7.83% | 140.9% |
| ✅ | ❌ | 22 | -4.78% | -105.1% |
| ✅ | ✅ | 32 | 5.68% | 181.8% |

### Flip Trades (Signal Wrong → Direction Right)

**26 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **7.9%**
- Total return: **204.4%**
- Average alpha: **6.5%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 6 | 3.92% |
| strong_positive | 6 | 6.14% |
| strong_negative | 6 | 11.16% |
| weak_positive | 4 | 11.18% |
| weak_negative | 3 | 9.48% |
| unknown | 1 | 3.97% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 76 | 1.76% | 133.9% | 56.6% | 56.6% |
| low | 19 | 1.05% | 19.9% | 47.4% | 47.4% |
| high | 18 | -0.81% | -14.5% | 33.3% | 33.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 50 | 3.59% | 179.6% | 64.0% | 64.0% |
| SHORT | 63 | -0.64% | -40.3% | 41.3% | 41.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 8 | -1.9% | -0.24% | 50.0% | 50.0% | 2.7% |
| 2019 | 16 | 4.9% | 0.31% | 50.0% | 50.0% | -28.3% |
| 2020 | 19 | 39.7% | 2.09% | 42.1% | 42.1% | 2.1% |
| 2021 | 16 | 7.2% | 0.45% | 50.0% | 50.0% | -17.2% |
| 2022 | 18 | -6.0% | -0.33% | 44.4% | 44.4% | 12.2% |
| 2023 | 13 | 30.2% | 2.33% | 46.2% | 46.2% | 10.3% |
| 2024 | 12 | -3.2% | -0.26% | 58.3% | 58.3% | -22.8% |
| 2025 | 11 | 68.4% | 6.22% | 81.8% | 81.8% | 43.0% |

### Macro Context by Year

**2018** (Flat: -1.9%, 8 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 4.9%, 16 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 39.7%, 19 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 7.2%, 16 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -6.0%, 18 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 30.2%, 13 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Flat: -3.2%, 12 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 68.4%, 11 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -40.0% cumulative (trade 13 to trade 38)
**Period:** 2019-05-07 to 2020-05-27 (26 trades)
**Peak cumulative return:** 22.1% → **Trough:** -17.9%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2019-05-07 | 2019-05-30 | -1.0000 | 10.19% | strong_positive | ✅ |
| 2019-05-31 | 2019-06-07 | -1.0000 | -6.09% | strong_positive | ❌ |
| 2019-06-10 | 2019-06-18 | -1.0000 | -6.39% | strong_positive | ❌ |
| 2019-06-19 | 2019-07-23 | -1.0000 | -5.74% | strong_positive | ❌ |
| 2019-07-24 | 2019-08-19 | -1.0000 | 8.85% | strong_positive | ✅ |
| 2019-08-20 | 2019-08-29 | -1.0000 | -2.88% | regime_shift | ❌ |
| 2019-08-30 | 2019-09-10 | -1.0000 | -5.89% | regime_shift | ❌ |
| 2019-09-11 | 2019-10-11 | -1.0000 | -3.99% | regime_shift | ❌ |
| 2019-10-14 | 2019-10-16 | -1.0000 | -1.26% | regime_shift | ❌ |
| 2019-10-16 | 2019-11-04 | 1.0000 | 4.70% | regime_shift | ✅ |
| 2019-11-05 | 2019-11-27 | 1.0000 | -5.51% | regime_shift | ❌ |
| 2019-11-29 | 2020-01-08 | 1.0000 | 5.13% | regime_shift | ✅ |
| 2020-01-08 | 2020-01-27 | -1.0000 | 7.17% | regime_shift | ✅ |
| 2020-01-28 | 2020-02-05 | -1.0000 | -3.29% | regime_shift | ❌ |
| 2020-02-06 | 2020-02-21 | -1.0000 | -5.08% | regime_shift | ❌ |
| 2020-02-24 | 2020-03-13 | -1.0000 | 19.14% | weak_negative | ✅ |
| 2020-03-16 | 2020-03-17 | -1.0000 | -5.55% | weak_negative | ❌ |
| 2020-03-18 | 2020-03-24 | -1.0000 | -10.32% | weak_negative | ❌ |
| 2020-03-25 | 2020-03-26 | -1.0000 | -8.25% | weak_negative | ❌ |
| 2020-03-27 | 2020-03-30 | -1.0000 | -5.12% | weak_negative | ❌ |
| 2020-03-31 | 2020-04-06 | -1.0000 | -3.86% | weak_negative | ❌ |
| 2020-04-07 | 2020-04-17 | -1.0000 | 3.05% | weak_negative | ✅ |
| 2020-04-20 | 2020-04-28 | -1.0000 | -3.10% | weak_negative | ❌ |
| 2020-04-29 | 2020-05-18 | -1.0000 | 6.25% | weak_negative | ✅ |
| 2020-05-19 | 2020-05-26 | -1.0000 | -8.73% | weak_negative | ❌ |
| 2020-05-27 | 2020-06-03 | -1.0000 | -3.25% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 22 | -2.41% | -53.0% | 27.3% |
| 16-30d | 31 | 2.22% | 68.8% | 64.5% |
| 31-50d | 8 | 5.85% | 46.8% | 75.0% |
| 50d+ | 4 | 16.41% | 65.6% | 100.0% |
| 6-15d | 48 | 0.23% | 11.0% | 45.8% |

## Win/Loss Streaks

- **Max consecutive wins:** 9
- **Max consecutive losses:** 7

## Conclusions & Observations

**Statistical robustness:** With 113 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (45.9% remaining).
**Edge:** Genuine structural edge: 51.3% win rate with 1.56× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Signal accuracy (52.4%) exceeds direction accuracy (48.5%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.
**Regime dependence:** `strong_negative` (15 trades, 13% of total) generates 92.8% — a disproportionate share of returns.

### Known Vulnerabilities

- **Worst year:** 2022 (-6.0%, 18 trades). Macro: Fed Tightening Cycle, 2022 Bear Market
- **Losing regime:** `weak_negative` — 19 trades, -35.1% total return