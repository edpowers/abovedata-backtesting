# Strategy Analysis: momentum_lb40_z1.0_e3d × trailing_stop_5%

**Ticker:** DE
**Entry:** `momentum_lb40_z1.0_e3d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-08-16 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `40`
- **zscore_threshold:** `1.0`
- **zscore_window:** `60`
- **entry_days_before:** `3` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 22.5% |
| **Annualized Return** | 34.0% |
| **Sharpe Ratio** | 1.687 |
| **Max Drawdown** | -21.0% |
| **Total Trades** | 99 |
| **Win Rate** | 45.5% |
| **Signal Accuracy** | 51.7% |
| **Direction Accuracy** | 44.8% |
| **Skill Ratio** | 44.8% |
| **Profit Factor** | 1.19 |
| **Expectancy** | 0.0052 |
| **Tail Ratio** | 2.30 |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.0×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0207 | Ideal for 99 trades: 0.0101 |
| Top-1 Trade | 14.6% of gross profit | ✅ Low concentration |
| Top-3 Trades | 31.0% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | -16.0% | Strategy fails without best trade |
| Return ex-Top-3 | -46.9% | Strategy fails without top 3 |
| Max Single Trade | 45.8% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 39 | 6.55% | 255.5% | 5.80% | 17.56 |
| no_signal | 12 | 1.93% | 23.1% | 0.12% | 27.42 |
| direction_wrong_loss | 48 | -4.74% | -227.4% | -5.56% | 7.15 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 13 | 4.45% | 57.9% | 46.2% | 46.2% | 4.23% |
| weak_positive | 9 | 5.22% | 47.0% | 66.7% | 66.7% | 5.06% |
| weak_negative | 23 | 0.39% | 9.0% | 47.8% | 47.8% | -0.96% |
| unknown | 17 | -0.09% | -1.6% | 47.1% | 47.1% | -1.20% |
| regime_shift | 15 | -1.25% | -18.7% | 40.0% | 40.0% | -1.83% |
| strong_positive | 22 | -1.93% | -42.4% | 36.4% | 36.4% | -3.18% |

**Best regime:** `strong_negative` — 13 trades, 57.9% total return, 46.2% win rate.
**Worst regime:** `strong_positive` — 22 trades, -42.4% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 25 | -4.91% | -122.8% |
| ❌ | ✅ | 17 | 8.00% | 135.9% |
| ✅ | ❌ | 23 | -4.55% | -104.6% |
| ✅ | ✅ | 22 | 5.43% | 119.5% |

### Flip Trades (Signal Wrong → Direction Right)

**23 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **8.5%**
- Total return: **194.9%**
- Average alpha: **7.1%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 8 | 5.03% |
| weak_negative | 4 | 9.86% |
| strong_positive | 4 | 4.78% |
| strong_negative | 3 | 20.54% |
| weak_positive | 2 | 17.22% |
| regime_shift | 2 | 0.04% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 50 | 1.22% | 60.9% | 50.0% | 50.0% |
| low | 35 | 0.69% | 24.3% | 45.7% | 45.7% |
| high | 14 | -2.43% | -34.0% | 28.6% | 28.6% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 38 | 2.80% | 106.5% | 52.6% | 52.6% |
| SHORT | 61 | -0.91% | -55.2% | 41.0% | 41.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 6 | -0.1% | -0.02% | 50.0% | 50.0% | -9.7% |
| 2017 | 4 | -11.1% | -2.79% | 25.0% | 25.0% | -19.7% |
| 2018 | 10 | -1.3% | -0.13% | 50.0% | 50.0% | -0.2% |
| 2019 | 12 | -23.4% | -1.95% | 33.3% | 33.3% | -40.7% |
| 2020 | 14 | 51.9% | 3.71% | 42.9% | 42.9% | 22.6% |
| 2021 | 15 | -9.5% | -0.63% | 53.3% | 53.3% | -24.8% |
| 2022 | 20 | 13.1% | 0.65% | 40.0% | 40.0% | 22.8% |
| 2023 | 8 | 17.2% | 2.15% | 62.5% | 62.5% | 9.2% |
| 2024 | 3 | -2.7% | -0.89% | 66.7% | 66.7% | -6.7% |
| 2025 | 7 | 17.1% | 2.44% | 42.9% | 42.9% | 8.0% |

### Macro Context by Year

**2016** (Flat: -0.1%, 6 trades)
- No major macro events flagged.

**2017** (Losing year: -11.1%, 4 trades)
- No major macro events flagged.

**2018** (Flat: -1.3%, 10 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -23.4%, 12 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 51.9%, 14 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -9.5%, 15 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 13.1%, 20 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 17.2%, 8 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Flat: -2.7%, 3 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 17.1%, 7 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -56.5% cumulative (trade 6 to trade 41)
**Period:** 2016-11-25 to 2020-04-20 (36 trades)
**Peak cumulative return:** -0.1% → **Trough:** -56.6%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2016-11-25 | 2017-02-14 | 1.0000 | 6.51% | unknown | ✅ |
| 2017-02-14 | 2017-05-16 | -1.0000 | -4.90% | unknown | ❌ |
| 2017-08-15 | 2017-09-19 | -1.0000 | 3.22% | unknown | ✅ |
| 2017-09-20 | 2017-10-20 | -1.0000 | -4.70% | unknown | ❌ |
| 2017-10-23 | 2017-11-17 | -1.0000 | -4.77% | unknown | ❌ |
| 2018-02-13 | 2018-02-16 | -1.0000 | -5.05% | unknown | ❌ |
| 2018-02-20 | 2018-03-08 | -1.0000 | 2.25% | unknown | ✅ |
| 2018-03-09 | 2018-03-29 | -1.0000 | 7.14% | unknown | ✅ |
| 2018-04-02 | 2018-04-12 | -1.0000 | 1.03% | unknown | ✅ |
| 2018-04-13 | 2018-05-08 | -1.0000 | 5.27% | unknown | ✅ |
| 2018-05-09 | 2018-05-15 | -1.0000 | -0.25% | unknown | ❌ |
| 2018-11-16 | 2018-11-26 | -1.0000 | -0.71% | unknown | ❌ |
| 2018-11-27 | 2018-12-03 | -1.0000 | -9.74% | strong_positive | ❌ |
| 2018-12-04 | 2018-12-27 | -1.0000 | 3.21% | strong_positive | ✅ |
| 2018-12-28 | 2019-01-04 | -1.0000 | -4.41% | strong_positive | ❌ |
| 2019-01-07 | 2019-01-18 | -1.0000 | -6.78% | strong_positive | ❌ |
| 2019-01-22 | 2019-02-04 | -1.0000 | -3.57% | strong_positive | ❌ |
| 2019-02-05 | 2019-02-12 | -1.0000 | -0.60% | strong_positive | ❌ |
| 2019-02-12 | 2019-02-22 | 1.0000 | 0.47% | strong_positive | ✅ |
| 2019-02-25 | 2019-03-22 | 1.0000 | -5.41% | strong_positive | ❌ |
| 2019-03-25 | 2019-05-06 | 1.0000 | 2.30% | strong_positive | ✅ |
| 2019-05-07 | 2019-05-13 | 1.0000 | -7.28% | strong_positive | ❌ |
| 2019-05-14 | 2019-05-30 | -1.0000 | 3.69% | strong_positive | ✅ |
| 2019-05-31 | 2019-06-07 | -1.0000 | -6.09% | strong_positive | ❌ |
| 2019-06-10 | 2019-06-18 | -1.0000 | -6.39% | strong_positive | ❌ |
| 2019-06-19 | 2019-07-23 | -1.0000 | -5.74% | strong_positive | ❌ |
| 2019-07-24 | 2019-08-13 | -1.0000 | 11.97% | strong_positive | ✅ |
| 2020-02-18 | 2020-02-21 | -1.0000 | -6.69% | regime_shift | ❌ |
| 2020-02-24 | 2020-03-13 | -1.0000 | 19.14% | weak_negative | ✅ |
| 2020-03-16 | 2020-03-17 | -1.0000 | -5.55% | weak_negative | ❌ |
| 2020-03-18 | 2020-03-24 | -1.0000 | -10.32% | weak_negative | ❌ |
| 2020-03-25 | 2020-03-26 | -1.0000 | -8.25% | weak_negative | ❌ |
| 2020-03-27 | 2020-03-30 | -1.0000 | -5.12% | weak_negative | ❌ |
| 2020-03-31 | 2020-04-06 | -1.0000 | -3.86% | weak_negative | ❌ |
| 2020-04-07 | 2020-04-17 | -1.0000 | 3.05% | weak_negative | ✅ |
| 2020-04-20 | 2020-04-28 | -1.0000 | -3.10% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 34 | -3.81% | -129.6% | 17.6% |
| 16-30d | 20 | 1.70% | 34.0% | 55.0% |
| 31-50d | 6 | 8.05% | 48.3% | 100.0% |
| 50d+ | 4 | 18.26% | 73.0% | 75.0% |
| 6-15d | 35 | 0.73% | 25.5% | 54.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 5

## Conclusions & Observations

**Statistical robustness:** With 99 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (-46.9% remaining).
**Signal vs Direction:** Signal accuracy (51.7%) exceeds direction accuracy (44.8%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.
**Regime dependence:** `strong_negative` (13 trades, 13% of total) generates 57.9% — a disproportionate share of returns.

### Known Vulnerabilities

- **Worst year:** 2019 (-23.4%, 12 trades). Macro: US-China Trade War Escalation, Fed Rate Cuts (2019)
- **Losing regime:** `unknown` — 17 trades, -1.6% total return
- **Losing regime:** `regime_shift` — 15 trades, -18.7% total return
- **Losing regime:** `strong_positive` — 22 trades, -42.4% total return