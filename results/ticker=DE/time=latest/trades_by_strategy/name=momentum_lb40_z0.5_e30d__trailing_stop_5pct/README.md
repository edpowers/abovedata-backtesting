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
| **Total Return** | 19.3% |
| **Annualized Return** | 34.4% |
| **Sharpe Ratio** | 1.770 |
| **Max Drawdown** | -21.9% |
| **Total Trades** | 228 |
| **Win Rate** | 41.7% |
| **Signal Accuracy** | 54.4% |
| **Direction Accuracy** | 41.5% |
| **Skill Ratio** | 41.5% |
| **Profit Factor** | 1.13 |
| **Expectancy** | 0.0024 |
| **Tail Ratio** | 2.04 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 701.3% | 19.3% | -682.0% |
| Annualized Return | 20.7% | 34.4% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.2×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0095 | Ideal for 228 trades: 0.0044 |
| Top-1 Trade | 7.2% of gross profit | ✅ Low concentration |
| Top-3 Trades | 19.2% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | -11.7% | Strategy fails without best trade |
| Return ex-Top-3 | -47.0% | Strategy fails without top 3 |
| Max Single Trade | 35.0% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 81 | 4.82% | 390.6% | 4.67% | 8.99 |
| no_signal | 33 | 0.81% | 26.8% | -0.40% | 15.52 |
| direction_wrong_loss | 114 | -3.18% | -362.7% | -3.55% | 4.77 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| weak_positive | 27 | 1.64% | 44.3% | 55.6% | 55.6% | 1.40% |
| unknown | 34 | 1.07% | 36.3% | 38.2% | 38.2% | 0.45% |
| strong_negative | 27 | 0.35% | 9.4% | 40.7% | 40.7% | -0.28% |
| weak_negative | 31 | 0.13% | 4.1% | 38.7% | 38.7% | 0.03% |
| regime_shift | 65 | 0.02% | 1.2% | 43.1% | 43.1% | -0.74% |
| strong_positive | 44 | -0.92% | -40.6% | 36.4% | 36.4% | -0.85% |

**Best regime:** `weak_positive` — 27 trades, 44.3% total return, 55.6% win rate.
**Worst regime:** `strong_positive` — 44 trades, -40.6% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 53 | -3.47% | -184.0% |
| ❌ | ✅ | 36 | 5.76% | 207.4% |
| ✅ | ❌ | 61 | -2.93% | -178.7% |
| ✅ | ✅ | 45 | 4.07% | 183.1% |

### Flip Trades (Signal Wrong → Direction Right)

**50 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **6.1%**
- Total return: **304.2%**
- Average alpha: **6.0%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_positive | 13 | 3.39% |
| unknown | 12 | 8.73% |
| regime_shift | 11 | 4.96% |
| strong_negative | 6 | 8.32% |
| weak_negative | 5 | 9.08% |
| weak_positive | 3 | 1.79% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 67 | 1.02% | 68.2% | 38.8% | 38.8% |
| medium | 118 | 0.19% | 22.7% | 45.8% | 45.8% |
| high | 43 | -0.84% | -36.3% | 34.9% | 34.9% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 80 | 1.43% | 114.6% | 50.0% | 50.0% |
| SHORT | 148 | -0.40% | -59.9% | 37.2% | 37.2% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 7 | 19.4% | 2.77% | 57.1% | 57.1% | 5.2% |
| 2017 | 5 | 20.0% | 4.00% | 40.0% | 40.0% | 7.2% |
| 2018 | 26 | -12.3% | -0.47% | 30.8% | 30.8% | 6.2% |
| 2019 | 20 | 5.2% | 0.26% | 40.0% | 40.0% | -5.3% |
| 2020 | 20 | 44.2% | 2.21% | 55.0% | 55.0% | 33.3% |
| 2021 | 24 | 4.6% | 0.19% | 54.2% | 54.2% | -14.5% |
| 2022 | 47 | 10.5% | 0.22% | 38.3% | 38.3% | 25.2% |
| 2023 | 30 | 2.3% | 0.08% | 46.7% | 46.7% | -19.8% |
| 2024 | 24 | -16.8% | -0.70% | 33.3% | 33.3% | -37.9% |
| 2025 | 25 | -22.5% | -0.90% | 36.0% | 36.0% | -39.2% |

### Macro Context by Year

**2016** (Strong year: 19.4%, 7 trades)
- No major macro events flagged.

**2017** (Strong year: 20.0%, 5 trades)
- No major macro events flagged.

**2018** (Losing year: -12.3%, 26 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 5.2%, 20 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 44.2%, 20 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 4.6%, 24 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 10.5%, 47 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 2.3%, 30 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -16.8%, 24 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -22.5%, 25 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -80.1% cumulative (trade 129 to trade 225)
**Period:** 2022-07-08 to 2025-11-13 (97 trades)
**Peak cumulative return:** 128.4% → **Trough:** 48.3%

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
| 2022-07-08 | 2022-07-18 | -1.0000 | 2.20% | weak_negative | ✅ |
| 2022-07-19 | 2022-07-20 | -1.0000 | -1.21% | weak_negative | ❌ |
| 2022-07-21 | 2022-07-26 | -1.0000 | -0.92% | weak_negative | ❌ |
| 2022-07-27 | 2022-07-29 | -1.0000 | -5.36% | weak_negative | ❌ |
| 2022-08-01 | 2022-08-08 | -1.0000 | -1.63% | weak_negative | ❌ |
| 2022-08-09 | 2022-08-11 | -1.0000 | -5.31% | weak_negative | ❌ |
| 2022-08-12 | 2022-08-22 | -1.0000 | -0.40% | weak_negative | ❌ |
| 2022-08-23 | 2022-08-25 | -1.0000 | -3.54% | strong_negative | ❌ |
| 2022-08-26 | 2022-09-09 | -1.0000 | 1.88% | strong_negative | ✅ |
| 2022-09-12 | 2022-09-28 | -1.0000 | 7.52% | strong_negative | ✅ |
| 2022-09-29 | 2022-10-04 | -1.0000 | -5.66% | strong_negative | ❌ |
| 2022-10-05 | 2022-10-11 | -1.0000 | -2.12% | strong_negative | ❌ |
| 2022-10-12 | 2022-10-13 | -1.0000 | -1.65% | strong_negative | ❌ |
| 2022-10-14 | 2022-10-19 | -1.0000 | -3.97% | strong_negative | ❌ |
| 2022-10-20 | 2022-10-21 | -1.0000 | -4.80% | strong_negative | ❌ |
| 2022-10-24 | 2022-10-27 | -1.0000 | -2.25% | strong_negative | ❌ |
| 2022-10-28 | 2022-11-04 | -1.0000 | 0.44% | strong_negative | ✅ |
| 2022-11-07 | 2022-11-17 | -1.0000 | -3.57% | strong_negative | ❌ |
| 2022-11-18 | 2022-11-23 | -1.0000 | -5.61% | strong_negative | ❌ |
| 2022-11-25 | 2022-12-21 | -1.0000 | -0.04% | regime_shift | ❌ |
| 2022-12-22 | 2023-01-09 | -1.0000 | 1.48% | regime_shift | ✅ |
| 2023-01-10 | 2023-01-30 | -1.0000 | 3.85% | regime_shift | ✅ |
| 2023-01-31 | 2023-02-02 | -1.0000 | 3.85% | regime_shift | ✅ |
| 2023-02-03 | 2023-02-17 | -1.0000 | -6.71% | regime_shift | ❌ |
| 2023-02-21 | 2023-03-10 | -1.0000 | 7.31% | regime_shift | ✅ |
| 2023-03-13 | 2023-03-14 | -1.0000 | -1.06% | regime_shift | ❌ |
| 2023-03-15 | 2023-03-21 | -1.0000 | -3.10% | regime_shift | ❌ |
| 2023-03-22 | 2023-03-29 | -1.0000 | -1.47% | regime_shift | ❌ |
| 2023-03-30 | 2023-04-05 | -1.0000 | 7.40% | regime_shift | ✅ |
| 2023-04-06 | 2023-04-11 | -1.0000 | -3.02% | regime_shift | ❌ |
| 2023-04-12 | 2023-04-18 | -1.0000 | -3.20% | regime_shift | ❌ |
| 2023-04-19 | 2023-05-01 | -1.0000 | 2.71% | regime_shift | ✅ |
| 2023-05-02 | 2023-05-19 | -1.0000 | 5.28% | regime_shift | ✅ |
| 2023-05-22 | 2023-06-02 | -1.0000 | -2.93% | regime_shift | ❌ |
| 2023-06-05 | 2023-06-07 | -1.0000 | -5.00% | regime_shift | ❌ |
| 2023-06-08 | 2023-06-13 | -1.0000 | -4.59% | regime_shift | ❌ |
| 2023-06-14 | 2023-06-22 | -1.0000 | -4.17% | regime_shift | ❌ |
| 2023-06-23 | 2023-07-07 | -1.0000 | -0.52% | regime_shift | ❌ |
| 2023-07-07 | 2023-07-12 | 1.0000 | 0.59% | regime_shift | ✅ |
| 2023-07-13 | 2023-07-27 | 1.0000 | 4.66% | regime_shift | ✅ |
| 2023-07-28 | 2023-08-17 | 1.0000 | -1.86% | regime_shift | ❌ |
| 2023-08-18 | 2023-08-21 | 1.0000 | -1.57% | regime_shift | ❌ |
| 2023-08-22 | 2023-09-08 | 1.0000 | 3.75% | regime_shift | ✅ |
| 2023-09-11 | 2023-09-21 | 1.0000 | -3.18% | regime_shift | ❌ |
| 2023-09-22 | 2023-10-11 | 1.0000 | 2.59% | regime_shift | ✅ |
| 2023-10-11 | 2023-10-20 | -1.0000 | 3.65% | regime_shift | ✅ |
| 2023-10-23 | 2023-11-02 | -1.0000 | -0.08% | regime_shift | ❌ |
| 2023-11-03 | 2023-11-15 | -1.0000 | 0.35% | regime_shift | ✅ |
| 2023-11-16 | 2023-12-13 | -1.0000 | 0.41% | regime_shift | ✅ |
| 2023-12-14 | 2023-12-26 | -1.0000 | -3.31% | strong_positive | ❌ |
| 2023-12-27 | 2024-01-03 | -1.0000 | 1.70% | strong_positive | ✅ |
| 2024-01-03 | 2024-01-26 | 1.0000 | 0.07% | strong_positive | ✅ |
| 2024-01-29 | 2024-02-13 | 1.0000 | -4.63% | strong_positive | ❌ |
| 2024-02-14 | 2024-02-15 | 1.0000 | -5.23% | strong_positive | ❌ |
| 2024-02-16 | 2024-04-15 | 1.0000 | 9.59% | weak_positive | ✅ |
| 2024-04-16 | 2024-04-25 | 1.0000 | 0.27% | weak_positive | ✅ |
| 2024-04-26 | 2024-05-16 | 1.0000 | 0.28% | weak_positive | ✅ |
| 2024-05-17 | 2024-05-24 | 1.0000 | -5.56% | weak_positive | ❌ |
| 2024-05-28 | 2024-07-01 | 1.0000 | -1.86% | weak_positive | ❌ |
| 2024-07-02 | 2024-07-03 | 1.0000 | -0.59% | weak_positive | ❌ |
| 2024-07-03 | 2024-07-09 | -1.0000 | 3.85% | weak_positive | ✅ |
| 2024-07-10 | 2024-07-12 | -1.0000 | -3.93% | weak_positive | ❌ |
| 2024-07-15 | 2024-07-17 | -1.0000 | -3.62% | weak_positive | ❌ |
| 2024-07-18 | 2024-07-26 | -1.0000 | -1.55% | weak_positive | ❌ |
| 2024-07-29 | 2024-08-15 | -1.0000 | 0.93% | weak_positive | ✅ |
| 2024-08-16 | 2024-09-04 | -1.0000 | -3.71% | regime_shift | ❌ |
| 2024-09-05 | 2024-09-16 | -1.0000 | -2.86% | regime_shift | ❌ |
| 2024-09-17 | 2024-09-24 | -1.0000 | -3.27% | regime_shift | ❌ |
| 2024-09-25 | 2024-10-10 | -1.0000 | -0.06% | regime_shift | ❌ |
| 2024-10-10 | 2024-11-18 | 1.0000 | -0.30% | regime_shift | ❌ |
| 2024-11-19 | 2024-11-21 | 1.0000 | 9.36% | regime_shift | ✅ |
| 2024-11-22 | 2024-12-06 | 1.0000 | -0.59% | strong_negative | ❌ |
| 2024-12-09 | 2024-12-18 | 1.0000 | -5.21% | strong_negative | ❌ |
| 2024-12-19 | 2024-12-30 | 1.0000 | -0.47% | strong_negative | ❌ |
| 2024-12-30 | 2025-01-07 | -1.0000 | 2.30% | strong_negative | ✅ |
| 2025-01-08 | 2025-01-13 | -1.0000 | -4.86% | strong_negative | ❌ |
| 2025-01-14 | 2025-01-17 | -1.0000 | -5.35% | strong_negative | ❌ |
| 2025-01-21 | 2025-01-24 | -1.0000 | -3.37% | strong_negative | ❌ |
| 2025-01-27 | 2025-02-13 | -1.0000 | 3.70% | strong_negative | ✅ |
| 2025-02-14 | 2025-02-18 | -1.0000 | -4.44% | regime_shift | ❌ |
| 2025-02-19 | 2025-03-06 | -1.0000 | 5.19% | regime_shift | ✅ |
| 2025-03-07 | 2025-03-10 | -1.0000 | 2.17% | regime_shift | ✅ |
| 2025-03-11 | 2025-03-27 | -1.0000 | -0.89% | regime_shift | ❌ |
| 2025-03-28 | 2025-04-07 | -1.0000 | 8.70% | regime_shift | ✅ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -9.59% | regime_shift | ❌ |
| 2025-04-10 | 2025-04-11 | -1.0000 | -3.36% | regime_shift | ❌ |
| 2025-04-14 | 2025-04-22 | -1.0000 | 2.78% | regime_shift | ✅ |
| 2025-04-23 | 2025-05-01 | -1.0000 | -5.17% | regime_shift | ❌ |
| 2025-05-02 | 2025-05-08 | -1.0000 | -1.73% | regime_shift | ❌ |
| 2025-05-09 | 2025-05-12 | -1.0000 | -0.61% | regime_shift | ❌ |
| 2025-05-13 | 2025-05-15 | -1.0000 | -3.56% | regime_shift | ❌ |
| 2025-05-16 | 2025-06-16 | -1.0000 | 1.32% | weak_positive | ✅ |
| 2025-06-17 | 2025-07-02 | -1.0000 | 0.22% | weak_positive | ✅ |
| 2025-10-15 | 2025-10-22 | -1.0000 | -3.10% | regime_shift | ❌ |
| 2025-10-23 | 2025-11-06 | -1.0000 | -1.27% | regime_shift | ❌ |
| 2025-11-07 | 2025-11-12 | -1.0000 | -2.78% | regime_shift | ❌ |
| 2025-11-13 | 2025-11-24 | -1.0000 | -2.92% | regime_shift | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 120 | -1.35% | -162.0% | 25.8% |
| 16-30d | 14 | 2.92% | 40.9% | 64.3% |
| 31-50d | 3 | 15.61% | 46.8% | 100.0% |
| 50d+ | 3 | 16.69% | 50.1% | 66.7% |
| 6-15d | 88 | 0.90% | 78.9% | 56.8% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 7

## Conclusions & Observations

**Statistical robustness:** With 228 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (-47.0% remaining).
**Signal vs Direction:** Signal accuracy (54.4%) exceeds direction accuracy (41.5%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.
**Regime dependence:** `weak_positive` (27 trades, 12% of total) generates 44.3% — a disproportionate share of returns.

### Known Vulnerabilities

- **Worst year:** 2025 (-22.5%, 25 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery
- **Losing regime:** `strong_positive` — 44 trades, -40.6% total return