# Strategy Analysis: momentum_lb20_z0.5_e20d × trailing_stop_5%

**Ticker:** DE
**Entry:** `momentum_lb20_z0.5_e20d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-07-22 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `20` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 15.3% |
| **Annualized Return** | 38.9% |
| **Sharpe Ratio** | 1.894 |
| **Max Drawdown** | -22.5% |
| **Total Trades** | 107 |
| **Win Rate** | 43.0% |
| **Signal Accuracy** | 46.5% |
| **Direction Accuracy** | 44.2% |
| **Skill Ratio** | 44.2% |
| **Profit Factor** | 1.15 |
| **Expectancy** | 0.0040 |
| **Tail Ratio** | 2.15 |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.8×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0173 | Ideal for 107 trades: 0.0093 |
| Top-1 Trade | 8.7% of gross profit | ✅ Low concentration |
| Top-3 Trades | 24.8% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | -9.8% | Strategy fails without best trade |
| Return ex-Top-3 | -43.0% | Strategy fails without top 3 |
| Max Single Trade | 27.8% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 38 | 6.84% | 260.0% | 5.84% | 19.66 |
| no_signal | 21 | -0.07% | -1.5% | -1.37% | 21.90 |
| direction_wrong_loss | 48 | -4.49% | -215.7% | -5.51% | 8.50 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| weak_positive | 10 | 6.86% | 68.6% | 80.0% | 80.0% | 4.68% |
| weak_negative | 19 | 1.16% | 22.1% | 57.9% | 57.9% | -0.10% |
| strong_negative | 17 | 0.14% | 2.4% | 23.5% | 23.5% | -0.43% |
| strong_positive | 14 | -0.77% | -10.7% | 35.7% | 35.7% | -2.09% |
| regime_shift | 26 | -0.50% | -13.1% | 42.3% | 42.3% | -1.36% |
| unknown | 21 | -1.26% | -26.5% | 33.3% | 33.3% | -2.12% |

**Best regime:** `weak_positive` — 10 trades, 68.6% total return, 80.0% win rate.
**Worst regime:** `unknown` — 21 trades, -26.5% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 31 | -4.34% | -134.4% |
| ❌ | ✅ | 15 | 7.83% | 117.5% |
| ✅ | ❌ | 17 | -4.78% | -81.2% |
| ✅ | ✅ | 23 | 6.20% | 142.5% |

### Flip Trades (Signal Wrong → Direction Right)

**23 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **7.7%**
- Total return: **177.7%**
- Average alpha: **7.0%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 7 | 5.06% |
| regime_shift | 6 | 4.88% |
| weak_positive | 3 | 11.35% |
| strong_positive | 3 | 8.84% |
| strong_negative | 2 | 15.12% |
| weak_negative | 2 | 11.10% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 37 | 1.04% | 38.3% | 48.6% | 48.6% |
| medium | 60 | 0.08% | 5.1% | 41.7% | 41.7% |
| high | 10 | -0.05% | -0.5% | 30.0% | 30.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 43 | 3.08% | 132.6% | 55.8% | 55.8% |
| SHORT | 64 | -1.40% | -89.7% | 34.4% | 34.4% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 3 | -9.1% | -3.02% | 33.3% | 33.3% | -8.9% |
| 2017 | 10 | -3.9% | -0.39% | 30.0% | 30.0% | -19.6% |
| 2018 | 11 | -24.4% | -2.22% | 36.4% | 36.4% | -25.3% |
| 2019 | 9 | 6.8% | 0.76% | 44.4% | 44.4% | -22.9% |
| 2020 | 17 | -15.7% | -0.92% | 23.5% | 23.5% | -37.9% |
| 2021 | 16 | 8.2% | 0.51% | 43.8% | 43.8% | -7.1% |
| 2022 | 16 | 58.6% | 3.66% | 68.8% | 68.8% | 61.2% |
| 2023 | 5 | 3.2% | 0.64% | 60.0% | 60.0% | -2.0% |
| 2024 | 5 | 9.5% | 1.90% | 60.0% | 60.0% | 1.8% |
| 2025 | 15 | 9.8% | 0.65% | 40.0% | 40.0% | -10.9% |

### Macro Context by Year

**2016** (Losing year: -9.1%, 3 trades)
- No major macro events flagged.

**2017** (Flat: -3.9%, 10 trades)
- No major macro events flagged.

**2018** (Losing year: -24.4%, 11 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 6.8%, 9 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Losing year: -15.7%, 17 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 8.2%, 16 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 58.6%, 16 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 3.2%, 5 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 9.5%, 5 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 9.8%, 15 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -48.3% cumulative (trade 2 to trade 30)
**Period:** 2016-08-22 to 2019-05-14 (29 trades)
**Peak cumulative return:** -5.3% → **Trough:** -53.5%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2016-08-22 | 2016-09-28 | -1.0000 | 3.70% | unknown | ✅ |
| 2016-09-29 | 2016-10-26 | -1.0000 | -3.79% | unknown | ❌ |
| 2017-01-20 | 2017-04-25 | -1.0000 | -6.60% | unknown | ❌ |
| 2017-04-26 | 2017-05-19 | -1.0000 | -7.42% | unknown | ❌ |
| 2017-05-22 | 2017-06-16 | -1.0000 | -5.09% | unknown | ❌ |
| 2017-06-19 | 2017-07-10 | -1.0000 | -1.40% | unknown | ❌ |
| 2017-07-11 | 2017-08-04 | -1.0000 | -1.32% | unknown | ❌ |
| 2017-08-07 | 2017-09-19 | -1.0000 | 5.29% | unknown | ✅ |
| 2017-09-20 | 2017-10-20 | -1.0000 | -4.70% | unknown | ❌ |
| 2017-10-23 | 2017-10-25 | -1.0000 | -0.75% | unknown | ❌ |
| 2017-10-25 | 2017-11-20 | 1.0000 | 4.87% | unknown | ✅ |
| 2017-11-21 | 2018-02-05 | 1.0000 | 13.21% | unknown | ✅ |
| 2018-02-06 | 2018-02-08 | 1.0000 | -5.08% | unknown | ❌ |
| 2018-02-09 | 2018-02-28 | 1.0000 | 3.83% | unknown | ✅ |
| 2018-03-01 | 2018-03-19 | 1.0000 | 1.73% | unknown | ✅ |
| 2018-03-20 | 2018-03-22 | 1.0000 | -5.26% | unknown | ❌ |
| 2018-03-23 | 2018-04-06 | 1.0000 | -1.37% | unknown | ❌ |
| 2018-04-09 | 2018-04-20 | 1.0000 | 2.80% | unknown | ✅ |
| 2018-10-24 | 2018-11-01 | -1.0000 | -5.05% | unknown | ❌ |
| 2018-11-02 | 2018-11-26 | -1.0000 | -5.08% | unknown | ❌ |
| 2018-11-27 | 2018-12-03 | -1.0000 | -9.74% | strong_positive | ❌ |
| 2018-12-04 | 2018-12-27 | -1.0000 | 3.21% | strong_positive | ✅ |
| 2018-12-28 | 2019-01-04 | -1.0000 | -4.41% | strong_positive | ❌ |
| 2019-01-07 | 2019-01-17 | -1.0000 | -3.83% | strong_positive | ❌ |
| 2019-01-17 | 2019-01-18 | 1.0000 | 2.84% | strong_positive | ✅ |
| 2019-01-22 | 2019-03-22 | 1.0000 | -1.83% | strong_positive | ❌ |
| 2019-03-25 | 2019-05-06 | 1.0000 | 2.30% | strong_positive | ✅ |
| 2019-05-07 | 2019-05-13 | 1.0000 | -7.28% | strong_positive | ❌ |
| 2019-05-14 | 2019-05-17 | 1.0000 | -8.35% | strong_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 29 | -3.50% | -101.4% | 20.7% |
| 16-30d | 25 | 0.75% | 18.8% | 52.0% |
| 31-50d | 7 | 9.60% | 67.2% | 85.7% |
| 50d+ | 5 | 14.16% | 70.8% | 80.0% |
| 6-15d | 41 | -0.30% | -12.5% | 41.5% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 8

## Conclusions & Observations

**Statistical robustness:** With 107 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (-43.0% remaining).
**Signal vs Direction:** Signal accuracy (46.5%) exceeds direction accuracy (44.2%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.
**Regime dependence:** `weak_positive` (10 trades, 9% of total) generates 68.6% — a disproportionate share of returns.

### Known Vulnerabilities

- **Worst year:** 2018 (-24.4%, 11 trades). Macro: US-China Trade War Escalation
- **Losing regime:** `strong_positive` — 14 trades, -10.7% total return
- **Losing regime:** `regime_shift` — 26 trades, -13.1% total return
- **Losing regime:** `unknown` — 21 trades, -26.5% total return