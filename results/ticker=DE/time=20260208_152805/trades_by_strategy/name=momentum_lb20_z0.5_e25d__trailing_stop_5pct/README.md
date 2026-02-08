# Strategy Analysis: momentum_lb20_z0.5_e25d × trailing_stop_5%

**Ticker:** DE
**Entry:** `momentum_lb20_z0.5_e25d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-07-15 to 2025-12-31
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `25` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 74.9% |
| **Annualized Return** | 31.6% |
| **Sharpe Ratio** | 1.731 |
| **Max Drawdown** | -16.0% |
| **Total Trades** | 95 |
| **Win Rate** | 48.4% |
| **Signal Accuracy** | 48.7% |
| **Direction Accuracy** | 51.3% |
| **Skill Ratio** | 51.3% |
| **Profit Factor** | 1.40 |
| **Expectancy** | 0.0088 |
| **Tail Ratio** | 2.40 |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.4×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0257 | Ideal for 95 trades: 0.0105 |
| Top-1 Trade | 18.7% of gross profit | ✅ Low concentration |
| Top-3 Trades | 32.6% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 13.3% | Strategy survives without best trade |
| Return ex-Top-3 | -21.5% | Strategy fails without top 3 |
| Max Single Trade | 54.3% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 39 | 6.74% | 262.7% | 4.48% | 20.54 |
| no_signal | 19 | -1.27% | -24.1% | -2.26% | 19.42 |
| direction_wrong_loss | 37 | -4.20% | -155.5% | -4.26% | 10.46 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| weak_positive | 11 | 3.69% | 40.5% | 72.7% | 72.7% | 1.06% |
| strong_negative | 9 | 4.18% | 37.6% | 44.4% | 44.4% | 2.86% |
| regime_shift | 23 | 1.60% | 36.8% | 65.2% | 65.2% | 0.04% |
| weak_negative | 7 | 5.26% | 36.8% | 71.4% | 71.4% | 2.89% |
| unknown | 29 | -1.10% | -32.0% | 31.0% | 31.0% | -1.44% |
| strong_positive | 16 | -2.29% | -36.6% | 31.2% | 31.2% | -2.67% |

**Best regime:** `weak_positive` — 11 trades, 40.5% total return, 72.7% win rate.
**Worst regime:** `strong_positive` — 16 trades, -36.6% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 21 | -4.22% | -88.7% |
| ❌ | ✅ | 18 | 7.75% | 139.5% |
| ✅ | ❌ | 16 | -4.18% | -66.8% |
| ✅ | ✅ | 21 | 5.87% | 123.2% |

### Flip Trades (Signal Wrong → Direction Right)

**25 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **6.7%**
- Total return: **166.7%**
- Average alpha: **5.0%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 9 | 4.71% |
| unknown | 7 | 5.50% |
| strong_positive | 3 | 1.41% |
| strong_negative | 3 | 19.74% |
| weak_positive | 2 | 1.14% |
| weak_negative | 1 | 20.08% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 49 | 2.52% | 123.4% | 59.2% | 59.2% |
| low | 34 | -0.21% | -7.2% | 41.2% | 41.2% |
| high | 12 | -2.75% | -33.0% | 25.0% | 25.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 50 | 2.38% | 118.9% | 56.0% | 56.0% |
| SHORT | 45 | -0.79% | -35.7% | 40.0% | 40.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 3 | -4.2% | -1.40% | 33.3% | 33.3% | -4.9% |
| 2017 | 8 | -21.8% | -2.73% | 12.5% | 12.5% | -33.6% |
| 2018 | 21 | -16.9% | -0.80% | 38.1% | 38.1% | -12.5% |
| 2019 | 9 | 6.7% | 0.74% | 44.4% | 44.4% | -16.8% |
| 2020 | 5 | 68.2% | 13.64% | 40.0% | 40.0% | 49.6% |
| 2021 | 14 | 22.2% | 1.58% | 78.6% | 78.6% | 8.1% |
| 2022 | 5 | 19.7% | 3.94% | 80.0% | 80.0% | 22.4% |
| 2023 | 8 | 20.3% | 2.54% | 62.5% | 62.5% | 8.8% |
| 2024 | 10 | 5.8% | 0.58% | 50.0% | 50.0% | -18.3% |
| 2025 | 12 | -16.8% | -1.40% | 41.7% | 41.7% | -28.7% |

### Macro Context by Year

**2016** (Flat: -4.2%, 3 trades)
- No major macro events flagged.

**2017** (Losing year: -21.8%, 8 trades)
- No major macro events flagged.

**2018** (Losing year: -16.9%, 21 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 6.7%, 9 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 68.2%, 5 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 22.2%, 14 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 19.7%, 5 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 20.3%, 8 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 5.8%, 10 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -16.8%, 12 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -51.2% cumulative (trade 2 to trade 39)
**Period:** 2016-08-22 to 2019-08-13 (38 trades)
**Peak cumulative return:** -1.0% → **Trough:** -52.2%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2016-08-22 | 2016-09-28 | -1.0000 | 3.70% | unknown | ✅ |
| 2016-09-29 | 2016-10-19 | -1.0000 | -3.22% | unknown | ❌ |
| 2017-01-12 | 2017-02-10 | -1.0000 | -4.82% | unknown | ❌ |
| 2017-02-13 | 2017-04-25 | -1.0000 | -2.74% | unknown | ❌ |
| 2017-04-26 | 2017-05-19 | -1.0000 | -7.42% | unknown | ❌ |
| 2017-05-22 | 2017-06-16 | -1.0000 | -5.09% | unknown | ❌ |
| 2017-06-19 | 2017-07-10 | -1.0000 | -1.40% | unknown | ❌ |
| 2017-07-11 | 2017-08-04 | -1.0000 | -1.32% | unknown | ❌ |
| 2017-08-07 | 2017-09-19 | -1.0000 | 5.29% | unknown | ✅ |
| 2017-09-20 | 2017-10-18 | -1.0000 | -4.36% | unknown | ❌ |
| 2018-01-11 | 2018-02-05 | 1.0000 | -6.23% | unknown | ❌ |
| 2018-02-06 | 2018-02-08 | 1.0000 | -5.08% | unknown | ❌ |
| 2018-02-09 | 2018-02-28 | 1.0000 | 3.83% | unknown | ✅ |
| 2018-03-01 | 2018-03-19 | 1.0000 | 1.73% | unknown | ✅ |
| 2018-03-20 | 2018-03-22 | 1.0000 | -5.26% | unknown | ❌ |
| 2018-03-23 | 2018-04-06 | 1.0000 | -1.37% | unknown | ❌ |
| 2018-04-09 | 2018-04-13 | 1.0000 | 4.91% | unknown | ✅ |
| 2018-04-13 | 2018-04-24 | -1.0000 | 7.91% | unknown | ✅ |
| 2018-04-25 | 2018-05-08 | -1.0000 | -2.95% | unknown | ❌ |
| 2018-05-09 | 2018-05-18 | -1.0000 | -6.95% | unknown | ❌ |
| 2018-05-21 | 2018-06-06 | -1.0000 | -0.14% | unknown | ❌ |
| 2018-06-07 | 2018-07-26 | -1.0000 | 9.59% | unknown | ✅ |
| 2018-07-27 | 2018-08-07 | -1.0000 | -3.78% | unknown | ❌ |
| 2018-08-08 | 2018-08-21 | -1.0000 | 0.68% | unknown | ✅ |
| 2018-08-22 | 2018-09-10 | -1.0000 | -4.21% | unknown | ❌ |
| 2018-09-11 | 2018-10-02 | -1.0000 | -4.66% | unknown | ❌ |
| 2018-10-03 | 2018-11-01 | -1.0000 | 11.10% | unknown | ✅ |
| 2018-11-02 | 2018-11-26 | -1.0000 | -5.08% | unknown | ❌ |
| 2018-11-27 | 2018-12-03 | -1.0000 | -9.74% | strong_positive | ❌ |
| 2018-12-04 | 2018-12-27 | -1.0000 | 3.21% | strong_positive | ✅ |
| 2018-12-28 | 2019-01-04 | -1.0000 | -4.41% | strong_positive | ❌ |
| 2019-01-07 | 2019-01-10 | -1.0000 | -3.22% | strong_positive | ❌ |
| 2019-01-10 | 2019-01-18 | 1.0000 | 3.45% | strong_positive | ✅ |
| 2019-01-22 | 2019-03-22 | 1.0000 | -1.83% | strong_positive | ❌ |
| 2019-03-25 | 2019-04-11 | 1.0000 | 2.29% | strong_positive | ✅ |
| 2019-07-12 | 2019-08-01 | 1.0000 | -2.52% | strong_positive | ❌ |
| 2019-08-02 | 2019-08-12 | 1.0000 | -7.34% | strong_positive | ❌ |
| 2019-08-13 | 2019-08-23 | 1.0000 | -0.10% | strong_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 14 | -3.69% | -51.7% | 21.4% |
| 16-30d | 26 | 2.15% | 55.9% | 61.5% |
| 31-50d | 7 | 3.20% | 22.4% | 71.4% |
| 50d+ | 3 | 27.29% | 81.9% | 100.0% |
| 6-15d | 45 | -0.56% | -25.3% | 42.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 10
- **Max consecutive losses:** 7

## Conclusions & Observations

**Statistical robustness:** With 95 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (-21.5% remaining).
**Signal vs Direction:** Direction accuracy (51.3%) exceeds signal accuracy (48.7%), confirming the correlation flip adds value beyond raw signal prediction.
**Regime dependence:** `weak_positive` (11 trades, 12% of total) generates 40.5% — a disproportionate share of returns.

### Known Vulnerabilities

- **Worst year:** 2017 (-21.8%, 8 trades). Macro: No flagged events
- **Losing regime:** `unknown` — 29 trades, -32.0% total return
- **Losing regime:** `strong_positive` — 16 trades, -36.6% total return