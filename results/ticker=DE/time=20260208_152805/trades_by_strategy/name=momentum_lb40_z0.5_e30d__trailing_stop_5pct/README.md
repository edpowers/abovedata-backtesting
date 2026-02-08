# Strategy Analysis: momentum_lb40_z0.5_e30d × trailing_stop_5%

**Ticker:** DE
**Entry:** `momentum_lb40_z0.5_e30d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-07-08 to 2025-12-23
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `40`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | -11.7% |
| **Annualized Return** | 38.3% |
| **Sharpe Ratio** | 1.755 |
| **Max Drawdown** | -21.8% |
| **Total Trades** | 127 |
| **Win Rate** | 40.2% |
| **Signal Accuracy** | 54.6% |
| **Direction Accuracy** | 39.8% |
| **Skill Ratio** | 39.8% |
| **Profit Factor** | 1.08 |
| **Expectancy** | 0.0020 |
| **Tail Ratio** | 2.20 |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.3×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0183 | Ideal for 127 trades: 0.0079 |
| Top-1 Trade | 14.2% of gross profit | ✅ Low concentration |
| Top-3 Trades | 31.7% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | -41.3% | Strategy fails without best trade |
| Return ex-Top-3 | -65.7% | Strategy fails without top 3 |
| Max Single Trade | 50.4% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 43 | 6.23% | 267.7% | 5.88% | 18.77 |
| no_signal | 19 | 1.57% | 29.9% | -0.27% | 27.58 |
| direction_wrong_loss | 65 | -4.19% | -272.3% | -5.13% | 8.52 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 21 | 1.98% | 41.5% | 47.6% | 47.6% | 0.50% |
| weak_positive | 15 | 2.01% | 30.2% | 66.7% | 66.7% | 0.84% |
| strong_negative | 15 | 1.17% | 17.6% | 33.3% | 33.3% | 0.83% |
| regime_shift | 36 | -0.00% | -0.1% | 44.4% | 44.4% | -1.16% |
| weak_negative | 16 | -1.15% | -18.4% | 31.2% | 31.2% | -2.53% |
| strong_positive | 24 | -1.89% | -45.3% | 20.8% | 20.8% | -1.63% |

**Best regime:** `unknown` — 21 trades, 41.5% total return, 47.6% win rate.
**Worst regime:** `strong_positive` — 24 trades, -45.3% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 32 | -4.16% | -133.1% |
| ❌ | ✅ | 17 | 8.61% | 146.4% |
| ✅ | ❌ | 33 | -4.22% | -139.1% |
| ✅ | ✅ | 26 | 4.67% | 121.3% |

### Flip Trades (Signal Wrong → Direction Right)

**25 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **9.3%**
- Total return: **233.2%**
- Average alpha: **8.4%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 9 | 9.80% |
| regime_shift | 6 | 5.90% |
| strong_positive | 4 | 7.42% |
| strong_negative | 3 | 18.44% |
| weak_positive | 2 | 2.72% |
| weak_negative | 1 | 19.14% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 38 | 1.46% | 55.4% | 47.4% | 47.4% |
| medium | 61 | 0.30% | 18.6% | 42.6% | 42.6% |
| high | 28 | -1.74% | -48.6% | 25.0% | 25.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 46 | 2.70% | 124.3% | 52.2% | 52.2% |
| SHORT | 81 | -1.22% | -99.0% | 33.3% | 33.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 5 | 20.6% | 4.11% | 60.0% | 60.0% | 6.4% |
| 2017 | 3 | 17.7% | 5.89% | 33.3% | 33.3% | 4.1% |
| 2018 | 16 | -9.0% | -0.56% | 43.8% | 43.8% | 1.5% |
| 2019 | 11 | 7.9% | 0.72% | 36.4% | 36.4% | -5.1% |
| 2020 | 11 | 33.2% | 3.02% | 27.3% | 27.3% | 14.2% |
| 2021 | 15 | -5.1% | -0.34% | 40.0% | 40.0% | -25.5% |
| 2022 | 21 | -0.3% | -0.02% | 47.6% | 47.6% | 11.5% |
| 2023 | 15 | -1.9% | -0.12% | 46.7% | 46.7% | -21.8% |
| 2024 | 15 | -13.2% | -0.88% | 40.0% | 40.0% | -37.8% |
| 2025 | 15 | -24.5% | -1.63% | 26.7% | 26.7% | -33.3% |

### Macro Context by Year

**2016** (Strong year: 20.6%, 5 trades)
- No major macro events flagged.

**2017** (Strong year: 17.7%, 3 trades)
- No major macro events flagged.

**2018** (Losing year: -9.0%, 16 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 7.9%, 11 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 33.2%, 11 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -5.1%, 15 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Flat: -0.3%, 21 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Flat: -1.9%, 15 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -13.2%, 15 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -24.5%, 15 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -72.6% cumulative (trade 73 to trade 126)
**Period:** 2022-06-28 to 2025-11-24 (54 trades)
**Peak cumulative return:** 94.0% → **Trough:** 21.4%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-06-28 | 2022-07-07 | -1.0000 | 1.32% | weak_negative | ✅ |
| 2022-07-08 | 2022-07-19 | -1.0000 | -2.28% | weak_negative | ❌ |
| 2022-07-20 | 2022-07-28 | -1.0000 | -5.16% | weak_negative | ❌ |
| 2022-07-29 | 2022-08-10 | -1.0000 | -2.67% | weak_negative | ❌ |
| 2022-08-11 | 2022-08-24 | -1.0000 | -5.38% | weak_negative | ❌ |
| 2022-08-25 | 2022-10-04 | -1.0000 | 6.87% | strong_negative | ✅ |
| 2022-10-05 | 2022-10-21 | -1.0000 | -7.67% | strong_negative | ❌ |
| 2022-10-24 | 2022-11-10 | -1.0000 | -5.63% | strong_negative | ❌ |
| 2022-11-11 | 2022-11-23 | -1.0000 | -7.76% | strong_negative | ❌ |
| 2022-11-25 | 2023-01-10 | -1.0000 | 0.64% | regime_shift | ✅ |
| 2023-01-11 | 2023-02-17 | -1.0000 | 0.04% | regime_shift | ✅ |
| 2023-02-21 | 2023-03-30 | -1.0000 | 5.20% | regime_shift | ✅ |
| 2023-03-31 | 2023-04-17 | -1.0000 | 5.20% | regime_shift | ✅ |
| 2023-04-18 | 2023-06-02 | -1.0000 | 6.46% | regime_shift | ✅ |
| 2023-06-05 | 2023-06-12 | -1.0000 | -6.46% | regime_shift | ❌ |
| 2023-06-13 | 2023-07-07 | -1.0000 | -2.08% | regime_shift | ❌ |
| 2023-07-07 | 2023-07-17 | 1.0000 | 3.78% | regime_shift | ✅ |
| 2023-07-18 | 2023-08-03 | 1.0000 | -1.77% | regime_shift | ❌ |
| 2023-08-04 | 2023-08-18 | 1.0000 | -6.37% | regime_shift | ❌ |
| 2023-08-21 | 2023-09-21 | 1.0000 | -0.81% | regime_shift | ❌ |
| 2023-09-22 | 2023-10-11 | 1.0000 | 2.59% | regime_shift | ✅ |
| 2023-10-11 | 2023-10-26 | -1.0000 | 5.09% | regime_shift | ✅ |
| 2023-10-27 | 2023-11-03 | -1.0000 | -5.83% | regime_shift | ❌ |
| 2023-11-06 | 2023-12-14 | -1.0000 | -2.69% | regime_shift | ❌ |
| 2023-12-15 | 2024-01-02 | -1.0000 | -4.23% | strong_positive | ❌ |
| 2024-01-03 | 2024-02-15 | 1.0000 | -7.29% | strong_positive | ❌ |
| 2024-02-16 | 2024-04-30 | 1.0000 | 8.92% | weak_positive | ✅ |
| 2024-05-01 | 2024-05-20 | 1.0000 | 1.03% | weak_positive | ✅ |
| 2024-05-21 | 2024-05-29 | 1.0000 | -5.63% | weak_positive | ❌ |
| 2024-05-30 | 2024-07-01 | 1.0000 | -1.61% | weak_positive | ❌ |
| 2024-07-02 | 2024-07-03 | 1.0000 | -0.59% | weak_positive | ❌ |
| 2024-07-03 | 2024-08-01 | -1.0000 | 1.35% | weak_positive | ✅ |
| 2024-08-02 | 2024-08-15 | -1.0000 | -5.52% | weak_positive | ❌ |
| 2024-08-16 | 2024-09-04 | -1.0000 | -3.71% | regime_shift | ❌ |
| 2024-09-05 | 2024-09-18 | -1.0000 | -4.53% | regime_shift | ❌ |
| 2024-09-19 | 2024-10-10 | -1.0000 | 0.62% | regime_shift | ✅ |
| 2024-10-10 | 2024-11-21 | 1.0000 | 7.83% | regime_shift | ✅ |
| 2024-11-22 | 2024-12-12 | 1.0000 | -1.61% | strong_negative | ❌ |
| 2024-12-13 | 2024-12-30 | 1.0000 | -3.59% | strong_negative | ❌ |
| 2024-12-30 | 2025-01-02 | -1.0000 | 1.14% | strong_negative | ✅ |
| 2025-01-03 | 2025-01-13 | -1.0000 | -1.82% | strong_negative | ❌ |
| 2025-01-14 | 2025-01-17 | -1.0000 | -5.35% | strong_negative | ❌ |
| 2025-01-21 | 2025-01-27 | -1.0000 | -4.53% | strong_negative | ❌ |
| 2025-01-28 | 2025-02-18 | -1.0000 | -4.49% | strong_negative | ❌ |
| 2025-02-19 | 2025-03-06 | -1.0000 | 5.19% | regime_shift | ✅ |
| 2025-03-07 | 2025-04-09 | -1.0000 | 9.10% | regime_shift | ✅ |
| 2025-04-10 | 2025-04-14 | -1.0000 | -5.29% | regime_shift | ❌ |
| 2025-04-15 | 2025-04-24 | -1.0000 | -0.70% | regime_shift | ❌ |
| 2025-04-25 | 2025-05-08 | -1.0000 | -6.68% | regime_shift | ❌ |
| 2025-05-09 | 2025-05-16 | -1.0000 | -7.89% | regime_shift | ❌ |
| 2025-05-19 | 2025-07-02 | -1.0000 | 1.49% | weak_positive | ✅ |
| 2025-10-15 | 2025-10-24 | -1.0000 | -5.42% | regime_shift | ❌ |
| 2025-10-27 | 2025-11-21 | -1.0000 | -1.91% | regime_shift | ❌ |
| 2025-11-24 | 2025-12-15 | -1.0000 | -0.16% | regime_shift | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 28 | -3.85% | -107.7% | 14.3% |
| 16-30d | 28 | 2.51% | 70.2% | 64.3% |
| 31-50d | 2 | 7.69% | 15.4% | 100.0% |
| 50d+ | 5 | 21.92% | 109.6% | 80.0% |
| 6-15d | 64 | -0.97% | -62.1% | 35.9% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 7

## Conclusions & Observations

**Statistical robustness:** With 127 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (-65.7% remaining).
**Signal vs Direction:** Signal accuracy (54.6%) exceeds direction accuracy (39.8%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.
**Regime dependence:** `unknown` (21 trades, 17% of total) generates 41.5% — a disproportionate share of returns.

### Known Vulnerabilities

- **Worst year:** 2025 (-24.5%, 15 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery
- **Losing regime:** `regime_shift` — 36 trades, -0.1% total return
- **Losing regime:** `weak_negative` — 16 trades, -18.4% total return
- **Losing regime:** `strong_positive` — 24 trades, -45.3% total return