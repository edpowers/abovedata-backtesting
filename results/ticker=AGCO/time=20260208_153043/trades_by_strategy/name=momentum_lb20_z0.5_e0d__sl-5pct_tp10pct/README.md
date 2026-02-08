# Strategy Analysis: momentum_lb20_z0.5_e0d × sl-5%_tp10%

**Ticker:** AGCO
**Entry:** `momentum_lb20_z0.5_e0d`
**Exit:** `sl-5%_tp10%`
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

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit creates a 2:1 reward/risk ratio — when direction is correct, gains are 2× what losses are when wrong

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 1232.5% |
| **Annualized Return** | 17.0% |
| **Sharpe Ratio** | 0.679 |
| **Max Drawdown** | -37.4% |
| **Total Trades** | 111 |
| **Win Rate** | 55.0% |
| **Signal Accuracy** | 56.7% |
| **Direction Accuracy** | 54.4% |
| **Skill Ratio** | 54.4% |
| **Profit Factor** | 2.00 |
| **Expectancy** | 0.0271 |
| **Tail Ratio** | 1.71 |

## Diversity & Concentration

Diversification: **Excellent** — nearly perfectly diversified (HHI ratio: 1.2×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0107 | Ideal for 111 trades: 0.0090 |
| Top-1 Trade | 3.1% of gross profit | ✅ Low concentration |
| Top-3 Trades | 9.0% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 1021.8% | Strategy survives without best trade |
| Return ex-Top-3 | 710.4% | Strategy survives without top 3 |
| Max Single Trade | 18.8% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 49 | 9.90% | 485.0% | 9.58% | 15.00 |
| no_signal | 21 | 3.08% | 64.7% | 1.33% | 21.29 |
| direction_wrong_loss | 41 | -6.07% | -248.9% | -6.55% | 10.44 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 47 | 4.06% | 190.9% | 61.7% | 61.7% | 3.21% |
| strong_positive | 25 | 2.65% | 66.3% | 52.0% | 52.0% | 3.21% |
| unknown | 13 | 2.75% | 35.8% | 61.5% | 61.5% | 0.71% |
| strong_negative | 10 | 0.93% | 9.3% | 50.0% | 50.0% | 0.00% |
| weak_negative | 6 | 1.25% | 7.5% | 50.0% | 50.0% | 0.53% |
| weak_positive | 10 | -0.89% | -8.9% | 30.0% | 30.0% | -1.52% |

**Best regime:** `regime_shift` — 47 trades, 190.9% total return, 61.7% win rate.
**Worst regime:** `weak_positive` — 10 trades, -8.9% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 19 | -5.91% | -112.3% |
| ❌ | ✅ | 20 | 8.55% | 170.9% |
| ✅ | ❌ | 22 | -6.21% | -136.6% |
| ✅ | ✅ | 29 | 10.83% | 314.1% |

### Flip Trades (Signal Wrong → Direction Right)

**32 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **9.0%**
- Total return: **288.6%**
- Average alpha: **7.5%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 10 | 9.86% |
| unknown | 7 | 7.09% |
| strong_positive | 6 | 8.63% |
| weak_positive | 3 | 13.30% |
| strong_negative | 3 | 6.88% |
| weak_negative | 3 | 9.35% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 67 | 3.55% | 237.9% | 58.2% | 58.2% |
| low | 17 | 2.39% | 40.7% | 58.8% | 58.8% |
| high | 26 | 0.60% | 15.7% | 42.3% | 42.3% |
| no_data | 1 | 6.62% | 6.6% | 100.0% | 100.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 57 | 3.67% | 209.3% | 61.4% | 61.4% |
| SHORT | 54 | 1.69% | 91.5% | 48.1% | 48.1% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 2 | 21.0% | 10.52% | 100.0% | 100.0% | 14.8% |
| 2017 | 4 | 18.3% | 4.58% | 75.0% | 75.0% | 3.8% |
| 2018 | 9 | -11.4% | -1.27% | 33.3% | 33.3% | -7.1% |
| 2019 | 6 | 2.5% | 0.42% | 50.0% | 50.0% | -5.9% |
| 2020 | 24 | 154.2% | 6.42% | 70.8% | 70.8% | 162.5% |
| 2021 | 8 | 5.1% | 0.64% | 50.0% | 50.0% | 0.2% |
| 2022 | 20 | 68.6% | 3.43% | 60.0% | 60.0% | 68.7% |
| 2023 | 7 | 9.0% | 1.29% | 42.9% | 42.9% | -6.9% |
| 2024 | 14 | 5.6% | 0.40% | 42.9% | 42.9% | -13.1% |
| 2025 | 14 | 15.3% | 1.09% | 42.9% | 42.9% | -0.1% |
| 2026 | 3 | 12.6% | 4.19% | 66.7% | 66.7% | 11.8% |

### Macro Context by Year

**2016** (Strong year: 21.0%, 2 trades)
- No major macro events flagged.

**2017** (Strong year: 18.3%, 4 trades)
- No major macro events flagged.

**2018** (Losing year: -11.4%, 9 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 2.5%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 154.2%, 24 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 5.1%, 8 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 68.6%, 20 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 9.0%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 5.6%, 14 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 15.3%, 14 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 12.6%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -29.6% cumulative (trade 7 to trade 19)
**Period:** 2018-03-05 to 2019-05-14 (13 trades)
**Peak cumulative return:** 42.5% → **Trough:** 12.9%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2018-03-05 | 2018-07-31 | -1.0000 | 3.19% | unknown | ✅ |
| 2018-07-31 | 2018-08-13 | 1.0000 | -7.14% | unknown | ❌ |
| 2018-08-14 | 2018-10-12 | 1.0000 | -5.25% | unknown | ❌ |
| 2018-10-15 | 2018-10-23 | 1.0000 | -5.62% | unknown | ❌ |
| 2018-10-24 | 2018-10-30 | 1.0000 | 8.13% | unknown | ✅ |
| 2018-10-30 | 2018-10-31 | -1.0000 | -3.51% | unknown | ❌ |
| 2018-11-01 | 2018-12-03 | -1.0000 | -6.71% | strong_positive | ❌ |
| 2018-12-04 | 2018-12-24 | -1.0000 | 12.01% | strong_positive | ✅ |
| 2018-12-26 | 2019-01-04 | -1.0000 | -6.51% | strong_positive | ❌ |
| 2019-01-07 | 2019-01-17 | -1.0000 | -5.58% | strong_positive | ❌ |
| 2019-01-18 | 2019-02-05 | -1.0000 | 1.89% | strong_positive | ✅ |
| 2019-05-02 | 2019-05-13 | 1.0000 | -5.74% | strong_negative | ❌ |
| 2019-05-14 | 2019-05-17 | 1.0000 | -5.59% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 33 | 2.91% | 96.0% | 54.5% |
| 16-30d | 16 | 5.93% | 94.9% | 75.0% |
| 31-50d | 9 | 2.08% | 18.7% | 55.6% |
| 50d+ | 4 | 3.81% | 15.3% | 75.0% |
| 6-15d | 49 | 1.55% | 76.0% | 46.9% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 4

## Conclusions & Observations

**Statistical robustness:** With 111 trades, this sample is large enough for reliable inference.
**Diversification:** Excellent. HHI of 0.0107 is near the theoretical minimum of 0.0090. No single trade dominates returns.
**Edge:** Genuine structural edge: 55.0% win rate with 2.00× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Signal accuracy (56.7%) exceeds direction accuracy (54.4%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities

- **Worst year:** 2018 (-11.4%, 9 trades). Macro: US-China Trade War Escalation
- **Losing regime:** `weak_positive` — 10 trades, -8.9% total return