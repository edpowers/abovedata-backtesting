# Strategy Analysis: momentum_lb20_z1.0_e0d × trailing_stop_5%

**Ticker:** ZBH
**Entry:** `momentum_lb20_z1.0_e0d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-04-26 to 2026-02-02
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `1.0`
- **zscore_window:** `60`
- **entry_days_before:** `0` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | -35.2% |
| **Annualized Return** | 22.3% |
| **Sharpe Ratio** | 1.357 |
| **Max Drawdown** | -23.7% |
| **Total Trades** | 132 |
| **Win Rate** | 41.7% |
| **Signal Accuracy** | 16.2% |
| **Direction Accuracy** | 41.4% |
| **Skill Ratio** | 41.4% |
| **Profit Factor** | 0.90 |
| **Expectancy** | -0.0021 |
| **Tail Ratio** | 1.23 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | -10.7% | -35.2% | -24.5% |
| Annualized Return | -1.0% | 22.3% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.6×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0119 | Ideal for 132 trades: 0.0076 |
| Top-1 Trade | 6.6% of gross profit | ✅ Low concentration |
| Top-3 Trades | 15.1% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | -44.3% | Strategy fails without best trade |
| Return ex-Top-3 | -54.4% | Strategy fails without top 3 |
| Max Single Trade | 16.3% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 46 | 4.77% | 219.3% | 4.24% | 13.15 |
| no_signal | 21 | -0.86% | -18.1% | -1.52% | 7.95 |
| direction_wrong_loss | 65 | -3.51% | -228.4% | -3.74% | 5.69 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 22 | 0.62% | 13.7% | 40.9% | 40.9% | 0.31% |
| weak_positive | 11 | 1.23% | 13.5% | 45.5% | 45.5% | 1.44% |
| strong_positive | 10 | 0.19% | 1.9% | 60.0% | 60.0% | 0.42% |
| unknown | 31 | 0.02% | 0.5% | 41.9% | 41.9% | -0.64% |
| strong_negative | 28 | -0.50% | -14.1% | 39.3% | 39.3% | -0.93% |
| weak_negative | 30 | -1.42% | -42.7% | 36.7% | 36.7% | -2.03% |

**Best regime:** `regime_shift` — 22 trades, 13.7% total return, 40.9% win rate.
**Worst regime:** `weak_negative` — 30 trades, -42.7% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 52 | -3.53% | -183.5% |
| ❌ | ✅ | 41 | 4.44% | 182.1% |
| ✅ | ❌ | 13 | -3.46% | -45.0% |
| ✅ | ✅ | 5 | 7.43% | 37.1% |

### Flip Trades (Signal Wrong → Direction Right)

**50 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **4.2%**
- Total return: **210.3%**
- Average alpha: **3.6%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 11 | 2.85% |
| unknown | 11 | 3.37% |
| strong_negative | 11 | 5.29% |
| regime_shift | 7 | 7.21% |
| strong_positive | 6 | 1.96% |
| weak_positive | 4 | 5.38% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| high | 9 | 0.68% | 6.1% | 44.4% | 44.4% |
| low | 40 | -0.22% | -8.6% | 40.0% | 40.0% |
| medium | 83 | -0.30% | -24.7% | 42.2% | 42.2% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 62 | -0.30% | -18.4% | 43.5% | 43.5% |
| SHORT | 70 | -0.13% | -8.9% | 40.0% | 40.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 16 | 7.4% | 0.46% | 50.0% | 50.0% | 9.7% |
| 2019 | 15 | -6.9% | -0.46% | 33.3% | 33.3% | -29.4% |
| 2020 | 29 | -30.2% | -1.04% | 37.9% | 37.9% | -39.0% |
| 2021 | 8 | 5.4% | 0.68% | 37.5% | 37.5% | 5.6% |
| 2022 | 19 | 3.4% | 0.18% | 47.4% | 47.4% | 11.7% |
| 2023 | 11 | 6.5% | 0.59% | 45.5% | 45.5% | -5.1% |
| 2024 | 11 | 6.5% | 0.59% | 36.4% | 36.4% | 3.6% |
| 2025 | 20 | -27.9% | -1.40% | 35.0% | 35.0% | -44.5% |
| 2026 | 3 | 8.6% | 2.85% | 100.0% | 100.0% | 7.5% |

### Macro Context by Year

**2018** (Modestly positive: 7.4%, 16 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -6.9%, 15 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Losing year: -30.2%, 29 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 5.4%, 8 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Modestly positive: 3.4%, 19 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 6.5%, 11 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 6.5%, 11 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -27.9%, 20 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 8.6%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -50.0% cumulative (trade 14 to trade 39)
**Period:** 2018-12-12 to 2020-03-16 (26 trades)
**Peak cumulative return:** 8.5% → **Trough:** -41.5%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2018-12-12 | 2018-12-26 | -1.0000 | 9.68% | unknown | ✅ |
| 2018-12-27 | 2018-12-28 | -1.0000 | -0.92% | unknown | ❌ |
| 2018-12-31 | 2019-01-07 | -1.0000 | -0.17% | unknown | ❌ |
| 2019-01-08 | 2019-01-09 | -1.0000 | -0.82% | unknown | ❌ |
| 2019-01-10 | 2019-01-17 | -1.0000 | -2.41% | unknown | ❌ |
| 2019-01-18 | 2019-01-25 | -1.0000 | -1.97% | unknown | ❌ |
| 2019-01-28 | 2019-02-01 | -1.0000 | -10.17% | unknown | ❌ |
| 2019-02-04 | 2019-04-17 | 1.0000 | 1.56% | unknown | ✅ |
| 2019-04-18 | 2019-04-26 | 1.0000 | 3.22% | unknown | ✅ |
| 2019-04-29 | 2019-06-04 | -1.0000 | 2.83% | unknown | ✅ |
| 2019-06-05 | 2019-06-11 | -1.0000 | -1.64% | unknown | ❌ |
| 2019-06-12 | 2019-07-08 | -1.0000 | -0.22% | unknown | ❌ |
| 2019-07-09 | 2019-07-24 | -1.0000 | -4.26% | unknown | ❌ |
| 2019-07-25 | 2019-07-26 | -1.0000 | -8.55% | unknown | ❌ |
| 2019-07-29 | 2019-08-23 | 1.0000 | -0.66% | unknown | ❌ |
| 2019-08-26 | 2019-09-26 | 1.0000 | 1.49% | unknown | ✅ |
| 2019-09-27 | 2019-10-02 | 1.0000 | -1.63% | unknown | ❌ |
| 2019-10-03 | 2020-02-24 | 1.0000 | 16.27% | unknown | ✅ |
| 2020-02-25 | 2020-02-26 | 1.0000 | -2.12% | strong_negative | ❌ |
| 2020-02-27 | 2020-02-28 | 1.0000 | -2.72% | strong_negative | ❌ |
| 2020-03-02 | 2020-03-03 | 1.0000 | -3.87% | strong_negative | ❌ |
| 2020-03-04 | 2020-03-05 | 1.0000 | -6.43% | strong_negative | ❌ |
| 2020-03-06 | 2020-03-09 | 1.0000 | -10.35% | strong_negative | ❌ |
| 2020-03-10 | 2020-03-11 | 1.0000 | -6.02% | strong_negative | ❌ |
| 2020-03-12 | 2020-03-13 | 1.0000 | -4.15% | strong_negative | ❌ |
| 2020-03-16 | 2020-03-17 | 1.0000 | -6.35% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 72 | -1.43% | -103.2% | 30.6% |
| 16-30d | 20 | 2.71% | 54.2% | 70.0% |
| 31-50d | 1 | 9.13% | 9.1% | 100.0% |
| 50d+ | 2 | 8.92% | 17.8% | 100.0% |
| 6-15d | 37 | -0.14% | -5.2% | 43.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 8

## Conclusions & Observations

**Statistical robustness:** With 132 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (-54.4% remaining).
**Signal vs Direction:** Direction accuracy (41.4%) exceeds signal accuracy (16.2%), confirming the correlation flip adds value beyond raw signal prediction.
**Regime dependence:** `regime_shift` (22 trades, 17% of total) generates 13.7% — a disproportionate share of returns.

### Known Vulnerabilities

- **Worst year:** 2020 (-30.2%, 29 trades). Macro: COVID-19 Crash & Recovery, Post-COVID Stimulus Rally
- **Losing regime:** `strong_negative` — 28 trades, -14.1% total return
- **Losing regime:** `weak_negative` — 30 trades, -42.7% total return