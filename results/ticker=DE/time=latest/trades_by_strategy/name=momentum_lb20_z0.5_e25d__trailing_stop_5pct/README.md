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
| **Total Return** | 80.6% |
| **Annualized Return** | 33.9% |
| **Sharpe Ratio** | 2.054 |
| **Max Drawdown** | -16.5% |
| **Total Trades** | 183 |
| **Win Rate** | 47.5% |
| **Signal Accuracy** | 47.4% |
| **Direction Accuracy** | 50.0% |
| **Skill Ratio** | 50.0% |
| **Profit Factor** | 1.28 |
| **Expectancy** | 0.0045 |
| **Tail Ratio** | 1.81 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 701.3% | 80.6% | -620.7% |
| Annualized Return | 20.7% | 33.9% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.0×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0111 | Ideal for 183 trades: 0.0055 |
| Top-1 Trade | 10.1% of gross profit | ✅ Low concentration |
| Top-3 Trades | 18.6% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 31.3% | Strategy survives without best trade |
| Return ex-Top-3 | -2.3% | Strategy fails without top 3 |
| Max Single Trade | 37.5% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 76 | 4.44% | 337.1% | 3.37% | 9.99 |
| no_signal | 31 | -0.80% | -24.7% | -1.45% | 11.39 |
| direction_wrong_loss | 76 | -3.03% | -230.6% | -2.93% | 4.67 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 17 | 3.16% | 53.7% | 64.7% | 64.7% | 1.97% |
| regime_shift | 47 | 0.71% | 33.5% | 51.1% | 51.1% | -0.20% |
| weak_positive | 25 | 1.00% | 25.0% | 56.0% | 56.0% | 0.26% |
| weak_negative | 16 | 1.56% | 25.0% | 62.5% | 62.5% | 1.05% |
| unknown | 47 | -0.57% | -26.9% | 29.8% | 29.8% | -0.62% |
| strong_positive | 31 | -0.92% | -28.6% | 45.2% | 45.2% | -0.97% |

**Best regime:** `strong_negative` — 17 trades, 53.7% total return, 64.7% win rate.
**Worst regime:** `strong_positive` — 31 trades, -28.6% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 43 | -3.08% | -132.5% |
| ❌ | ✅ | 37 | 4.85% | 179.4% |
| ✅ | ❌ | 33 | -2.97% | -98.2% |
| ✅ | ✅ | 39 | 4.04% | 157.7% |

### Flip Trades (Signal Wrong → Direction Right)

**48 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **4.5%**
- Total return: **214.7%**
- Average alpha: **3.7%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 15 | 3.94% |
| unknown | 11 | 5.50% |
| strong_negative | 9 | 7.48% |
| strong_positive | 6 | 1.83% |
| weak_negative | 4 | 3.75% |
| weak_positive | 3 | 0.63% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 103 | 1.07% | 110.6% | 59.2% | 59.2% |
| low | 60 | -0.14% | -8.4% | 33.3% | 33.3% |
| high | 20 | -1.02% | -20.4% | 30.0% | 30.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 96 | 1.02% | 97.9% | 53.1% | 53.1% |
| SHORT | 87 | -0.19% | -16.1% | 41.4% | 41.4% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 4 | -4.7% | -1.19% | 50.0% | 50.0% | -6.7% |
| 2017 | 10 | -21.0% | -2.10% | 10.0% | 10.0% | -33.5% |
| 2018 | 42 | 2.2% | 0.05% | 40.5% | 40.5% | 20.0% |
| 2019 | 15 | -0.1% | -0.01% | 60.0% | 60.0% | -19.0% |
| 2020 | 16 | 63.1% | 3.95% | 68.8% | 68.8% | 43.5% |
| 2021 | 23 | 26.4% | 1.15% | 60.9% | 60.9% | 14.8% |
| 2022 | 13 | 12.7% | 0.98% | 53.8% | 53.8% | 12.6% |
| 2023 | 17 | 17.0% | 1.00% | 47.1% | 47.1% | 2.5% |
| 2024 | 20 | -0.8% | -0.04% | 45.0% | 45.0% | -19.0% |
| 2025 | 23 | -13.1% | -0.57% | 39.1% | 39.1% | -26.7% |

### Macro Context by Year

**2016** (Flat: -4.7%, 4 trades)
- No major macro events flagged.

**2017** (Losing year: -21.0%, 10 trades)
- No major macro events flagged.

**2018** (Modestly positive: 2.2%, 42 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Flat: -0.1%, 15 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 63.1%, 16 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 26.4%, 23 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 12.7%, 13 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 17.0%, 17 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Flat: -0.8%, 20 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -13.1%, 23 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -41.9% cumulative (trade 2 to trade 40)
**Period:** 2016-08-22 to 2018-09-21 (39 trades)
**Peak cumulative return:** -1.0% → **Trough:** -42.9%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2016-08-22 | 2016-09-28 | -1.0000 | 3.70% | unknown | ✅ |
| 2016-09-29 | 2016-10-10 | -1.0000 | -4.33% | unknown | ❌ |
| 2016-10-11 | 2016-10-19 | -1.0000 | 0.56% | unknown | ✅ |
| 2017-01-12 | 2017-02-09 | -1.0000 | -3.76% | unknown | ❌ |
| 2017-02-10 | 2017-04-25 | -1.0000 | -3.21% | unknown | ❌ |
| 2017-04-26 | 2017-05-19 | -1.0000 | -7.42% | unknown | ❌ |
| 2017-05-22 | 2017-06-05 | -1.0000 | -2.97% | unknown | ❌ |
| 2017-06-06 | 2017-07-10 | -1.0000 | -2.98% | unknown | ❌ |
| 2017-07-11 | 2017-07-31 | -1.0000 | -0.17% | unknown | ❌ |
| 2017-08-01 | 2017-09-11 | -1.0000 | 8.60% | unknown | ✅ |
| 2017-09-12 | 2017-09-19 | -1.0000 | -4.96% | unknown | ❌ |
| 2017-09-20 | 2017-10-03 | -1.0000 | -3.85% | unknown | ❌ |
| 2017-10-04 | 2017-10-18 | -1.0000 | -0.30% | unknown | ❌ |
| 2018-01-11 | 2018-02-05 | 1.0000 | -6.23% | unknown | ❌ |
| 2018-02-06 | 2018-02-08 | 1.0000 | -5.08% | unknown | ❌ |
| 2018-02-09 | 2018-02-16 | 1.0000 | 9.37% | unknown | ✅ |
| 2018-02-20 | 2018-02-28 | 1.0000 | -2.37% | unknown | ❌ |
| 2018-03-01 | 2018-03-02 | 1.0000 | -2.23% | unknown | ❌ |
| 2018-03-05 | 2018-03-14 | 1.0000 | 1.69% | unknown | ✅ |
| 2018-03-15 | 2018-03-21 | 1.0000 | -0.97% | unknown | ❌ |
| 2018-03-22 | 2018-03-23 | 1.0000 | -2.36% | unknown | ❌ |
| 2018-03-26 | 2018-04-04 | 1.0000 | -2.73% | unknown | ❌ |
| 2018-04-05 | 2018-04-06 | 1.0000 | -3.93% | unknown | ❌ |
| 2018-04-09 | 2018-04-13 | 1.0000 | 4.91% | unknown | ✅ |
| 2018-04-13 | 2018-04-24 | -1.0000 | 7.91% | unknown | ✅ |
| 2018-04-25 | 2018-05-04 | -1.0000 | 0.51% | unknown | ✅ |
| 2018-05-07 | 2018-05-10 | -1.0000 | -4.56% | unknown | ❌ |
| 2018-05-11 | 2018-05-18 | -1.0000 | -5.38% | unknown | ❌ |
| 2018-05-21 | 2018-06-06 | -1.0000 | -0.14% | unknown | ❌ |
| 2018-06-07 | 2018-07-09 | -1.0000 | 8.52% | unknown | ✅ |
| 2018-07-10 | 2018-07-19 | -1.0000 | 2.94% | unknown | ✅ |
| 2018-07-20 | 2018-07-25 | -1.0000 | -3.03% | unknown | ❌ |
| 2018-07-26 | 2018-07-31 | -1.0000 | -1.44% | unknown | ❌ |
| 2018-08-01 | 2018-08-07 | -1.0000 | -2.97% | unknown | ❌ |
| 2018-08-08 | 2018-08-17 | -1.0000 | 2.91% | unknown | ✅ |
| 2018-08-20 | 2018-08-27 | -1.0000 | -4.03% | unknown | ❌ |
| 2018-08-28 | 2018-09-07 | -1.0000 | -0.77% | unknown | ❌ |
| 2018-09-10 | 2018-09-20 | -1.0000 | -3.67% | unknown | ❌ |
| 2018-09-21 | 2018-10-03 | -1.0000 | -4.01% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 97 | -0.82% | -79.6% | 35.1% |
| 16-30d | 20 | 1.82% | 36.3% | 65.0% |
| 31-50d | 6 | 9.66% | 57.9% | 83.3% |
| 6-15d | 60 | 1.12% | 67.1% | 58.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 6

## Conclusions & Observations

**Statistical robustness:** With 183 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (-2.3% remaining).
**Signal vs Direction:** Direction accuracy (50.0%) exceeds signal accuracy (47.4%), confirming the correlation flip adds value beyond raw signal prediction.
**Regime dependence:** `strong_negative` (17 trades, 9% of total) generates 53.7% — a disproportionate share of returns.

### Known Vulnerabilities

- **Worst year:** 2017 (-21.0%, 10 trades). Macro: No flagged events
- **Losing regime:** `unknown` — 47 trades, -26.9% total return
- **Losing regime:** `strong_positive` — 31 trades, -28.6% total return