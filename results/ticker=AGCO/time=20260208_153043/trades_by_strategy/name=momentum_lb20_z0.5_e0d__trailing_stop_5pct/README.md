# Strategy Analysis: momentum_lb20_z0.5_e0d × trailing_stop_5%

**Ticker:** AGCO
**Entry:** `momentum_lb20_z0.5_e0d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-10-26 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `0` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 712.9% |
| **Annualized Return** | 56.9% |
| **Sharpe Ratio** | 2.263 |
| **Max Drawdown** | -26.5% |
| **Total Trades** | 113 |
| **Win Rate** | 52.2% |
| **Signal Accuracy** | 53.8% |
| **Direction Accuracy** | 52.7% |
| **Skill Ratio** | 52.7% |
| **Profit Factor** | 2.15 |
| **Expectancy** | 0.0216 |
| **Tail Ratio** | 2.90 |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.9×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0169 | Ideal for 113 trades: 0.0088 |
| Top-1 Trade | 6.7% of gross profit | ✅ Low concentration |
| Top-3 Trades | 18.8% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 523.0% | Strategy survives without best trade |
| Return ex-Top-3 | 282.4% | Strategy survives without top 3 |
| Max Single Trade | 30.5% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 48 | 7.64% | 366.6% | 6.07% | 18.69 |
| no_signal | 22 | 1.83% | 40.2% | 0.45% | 16.32 |
| direction_wrong_loss | 43 | -3.79% | -162.9% | -4.84% | 8.07 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 37 | 3.75% | 138.8% | 48.6% | 48.6% | 2.05% |
| unknown | 21 | 1.83% | 38.5% | 52.4% | 52.4% | 0.70% |
| strong_negative | 11 | 3.29% | 36.2% | 63.6% | 63.6% | 1.65% |
| weak_negative | 5 | 3.92% | 19.6% | 80.0% | 80.0% | 4.03% |
| weak_positive | 14 | 0.45% | 6.3% | 57.1% | 57.1% | -0.02% |
| strong_positive | 25 | 0.18% | 4.5% | 44.0% | 44.0% | -1.40% |

**Best regime:** `regime_shift` — 37 trades, 138.8% total return, 48.6% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 19 | -3.39% | -64.3% |
| ❌ | ✅ | 23 | 6.04% | 139.0% |
| ✅ | ❌ | 24 | -4.11% | -98.6% |
| ✅ | ✅ | 25 | 9.10% | 227.6% |

### Flip Trades (Signal Wrong → Direction Right)

**34 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **6.7%**
- Total return: **228.4%**
- Average alpha: **5.1%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_positive | 8 | 5.75% |
| unknown | 8 | 7.93% |
| strong_negative | 6 | 5.76% |
| regime_shift | 5 | 10.70% |
| weak_negative | 4 | 5.14% |
| strong_positive | 3 | 3.42% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 59 | 2.88% | 169.7% | 50.8% | 50.8% |
| low | 24 | 1.77% | 42.4% | 54.2% | 54.2% |
| high | 29 | 0.79% | 22.9% | 51.7% | 51.7% |
| no_data | 1 | 8.95% | 8.9% | 100.0% | 100.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 53 | 4.12% | 218.6% | 62.3% | 62.3% |
| SHORT | 60 | 0.42% | 25.3% | 43.3% | 43.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 2 | 23.5% | 11.74% | 100.0% | 100.0% | 15.6% |
| 2017 | 7 | 6.4% | 0.91% | 42.9% | 42.9% | -8.9% |
| 2018 | 12 | -0.5% | -0.04% | 41.7% | 41.7% | 4.4% |
| 2019 | 7 | 3.8% | 0.54% | 28.6% | 28.6% | -6.0% |
| 2020 | 19 | 104.8% | 5.52% | 57.9% | 57.9% | 56.4% |
| 2021 | 6 | 14.8% | 2.46% | 66.7% | 66.7% | 8.7% |
| 2022 | 19 | 55.6% | 2.93% | 52.6% | 52.6% | 41.5% |
| 2023 | 8 | 3.2% | 0.40% | 50.0% | 50.0% | -11.0% |
| 2024 | 14 | 17.9% | 1.28% | 64.3% | 64.3% | -2.2% |
| 2025 | 15 | 9.4% | 0.63% | 46.7% | 46.7% | -10.0% |
| 2026 | 4 | 5.0% | 1.24% | 50.0% | 50.0% | 5.0% |

### Macro Context by Year

**2016** (Strong year: 23.5%, 2 trades)
- No major macro events flagged.

**2017** (Modestly positive: 6.4%, 7 trades)
- No major macro events flagged.

**2018** (Flat: -0.5%, 12 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 3.8%, 7 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 104.8%, 19 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 14.8%, 6 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 55.6%, 19 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 3.2%, 8 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 17.9%, 14 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 9.4%, 15 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 5.0%, 4 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -26.2% cumulative (trade 13 to trade 27)
**Period:** 2018-05-21 to 2019-05-14 (15 trades)
**Peak cumulative return:** 38.1% → **Trough:** 11.8%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2018-05-21 | 2018-07-09 | -1.0000 | 7.22% | unknown | ✅ |
| 2018-07-10 | 2018-07-31 | -1.0000 | -0.57% | unknown | ❌ |
| 2018-08-01 | 2018-08-10 | 1.0000 | -3.86% | unknown | ❌ |
| 2018-08-13 | 2018-09-13 | 1.0000 | 0.72% | unknown | ✅ |
| 2018-09-14 | 2018-10-09 | 1.0000 | -0.26% | unknown | ❌ |
| 2018-10-10 | 2018-10-23 | 1.0000 | -7.59% | unknown | ❌ |
| 2018-10-24 | 2018-10-30 | 1.0000 | 8.13% | unknown | ✅ |
| 2018-10-30 | 2018-12-07 | -1.0000 | -5.11% | unknown | ❌ |
| 2018-12-10 | 2018-12-31 | -1.0000 | -0.13% | strong_positive | ❌ |
| 2019-01-02 | 2019-01-04 | -1.0000 | -3.62% | strong_positive | ❌ |
| 2019-01-07 | 2019-01-17 | -1.0000 | -5.58% | strong_positive | ❌ |
| 2019-01-18 | 2019-02-01 | -1.0000 | -0.40% | strong_positive | ❌ |
| 2019-02-04 | 2019-02-05 | -1.0000 | 3.39% | strong_positive | ✅ |
| 2019-05-02 | 2019-05-13 | 1.0000 | -5.74% | strong_negative | ❌ |
| 2019-05-14 | 2019-05-17 | 1.0000 | -5.59% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 32 | -1.02% | -32.5% | 40.6% |
| 16-30d | 22 | 7.68% | 169.0% | 81.8% |
| 31-50d | 12 | 10.33% | 123.9% | 100.0% |
| 50d+ | 3 | 6.22% | 18.6% | 100.0% |
| 6-15d | 44 | -0.80% | -35.2% | 29.5% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 6

## Conclusions & Observations

**Statistical robustness:** With 113 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (282.4% remaining).
**Edge:** Genuine structural edge: 52.2% win rate with 2.15× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Signal accuracy (53.8%) exceeds direction accuracy (52.7%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities
