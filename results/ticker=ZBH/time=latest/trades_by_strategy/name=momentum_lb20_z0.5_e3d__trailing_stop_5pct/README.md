# Strategy Analysis: momentum_lb20_z0.5_e3d × trailing_stop_5%

**Ticker:** ZBH
**Entry:** `momentum_lb20_z0.5_e3d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-04-23 to 2025-08-04
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `3` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 89.2% |
| **Annualized Return** | 25.1% |
| **Sharpe Ratio** | 1.456 |
| **Max Drawdown** | -22.1% |
| **Total Trades** | 155 |
| **Win Rate** | 49.0% |
| **Signal Accuracy** | 29.5% |
| **Direction Accuracy** | 50.4% |
| **Skill Ratio** | 50.4% |
| **Profit Factor** | 1.33 |
| **Expectancy** | 0.0053 |
| **Tail Ratio** | 1.72 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -10.7% | 89.2% | 99.9% |
| Annualized Return | -1.0% | 25.1% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.8×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0116 | Ideal for 155 trades: 0.0065 |
| Top-1 Trade | 6.0% of gross profit | Moderate concentration |
| Top-3 Trades | 15.9% of gross profit | Moderate concentration |
| Return ex-Top-1 | 58.0% | Positive without best trade |
| Return ex-Top-3 | 16.4% | Positive without top 3 |
| Max Single Trade | 19.8% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 70 | 4.29% | 300.1% | 3.32% | 11.44 |
| no_signal | 16 | 0.63% | 10.0% | 0.91% | 6.69 |
| direction_wrong_loss | 69 | -3.30% | -227.4% | -3.86% | 6.06 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_positive | 15 | 3.06% | 45.9% | 73.3% | 73.3% | 1.54% |
| unknown | 34 | 1.00% | 33.8% | 55.9% | 55.9% | 0.63% |
| regime_shift | 42 | 0.51% | 21.6% | 45.2% | 45.2% | 0.01% |
| strong_negative | 27 | 0.12% | 3.1% | 48.1% | 48.1% | -0.79% |
| weak_positive | 14 | -0.11% | -1.5% | 35.7% | 35.7% | -0.25% |
| weak_negative | 23 | -0.88% | -20.3% | 39.1% | 39.1% | -1.72% |

**Best-performing regime:** `strong_positive` — 15 trades, 45.9% total return, 73.3% win rate.
**Worst-performing regime:** `weak_negative` — 23 trades, -20.3% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 49 | -3.41% | -167.0% |
| ❌ | ✅ | 49 | 4.34% | 212.7% |
| ✅ | ❌ | 20 | -3.02% | -60.5% |
| ✅ | ✅ | 21 | 4.16% | 87.4% |

### Flip Trades (Signal Wrong → Direction Right)

**55 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.5%**
- Total return: **244.8%**
- Average alpha: **4.0%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 17 | 3.60% |
| strong_negative | 13 | 5.21% |
| regime_shift | 9 | 5.66% |
| strong_positive | 7 | 4.55% |
| weak_negative | 6 | 2.35% |
| weak_positive | 3 | 6.31% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| high | 20 | 2.01% | 40.2% | 55.0% | 55.0% |
| low | 35 | 1.04% | 36.5% | 57.1% | 57.1% |
| medium | 100 | 0.06% | 5.9% | 45.0% | 45.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 81 | 0.83% | 67.0% | 53.1% | 53.1% |
| SHORT | 74 | 0.21% | 15.7% | 44.6% | 44.6% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 16 | 19.2% | 1.20% | 62.5% | 62.5% | 22.2% |
| 2019 | 17 | 18.3% | 1.08% | 52.9% | 52.9% | 3.2% |
| 2020 | 46 | 7.8% | 0.17% | 50.0% | 50.0% | -25.3% |
| 2021 | 14 | -11.7% | -0.84% | 35.7% | 35.7% | -21.1% |
| 2022 | 11 | 24.5% | 2.23% | 72.7% | 72.7% | 20.9% |
| 2023 | 22 | 22.8% | 1.04% | 40.9% | 40.9% | -9.9% |
| 2024 | 10 | -0.5% | -0.05% | 50.0% | 50.0% | -13.3% |
| 2025 | 19 | 2.2% | 0.12% | 36.8% | 36.8% | 3.7% |

### Macro Context by Year

**2018** (Strong year: 19.2%, 16 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 18.3%, 17 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Modestly positive: 7.8%, 46 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -11.7%, 14 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 24.5%, 11 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 22.8%, 22 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Roughly flat: -0.5%, 10 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 2.2%, 19 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -43.0% cumulative (trade 40 to trade 89)
**Period:** 2020-03-16 to 2021-08-11 (50 trades)
**Peak cumulative return:** 72.8% → **Trough:** 29.8%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-03-16 | 2020-03-17 | -1.0000 | 6.35% | strong_negative | ✅ |
| 2020-03-18 | 2020-03-19 | -1.0000 | -10.55% | strong_negative | ❌ |
| 2020-03-20 | 2020-03-23 | -1.0000 | 6.01% | strong_negative | ✅ |
| 2020-03-24 | 2020-03-25 | -1.0000 | -3.67% | strong_negative | ❌ |
| 2020-03-26 | 2020-03-27 | -1.0000 | 5.86% | strong_negative | ✅ |
| 2020-03-30 | 2020-03-31 | -1.0000 | -2.85% | strong_negative | ❌ |
| 2020-04-01 | 2020-04-02 | -1.0000 | -3.44% | strong_negative | ❌ |
| 2020-04-03 | 2020-04-06 | -1.0000 | -6.44% | strong_negative | ❌ |
| 2020-04-07 | 2020-04-08 | -1.0000 | -9.19% | strong_negative | ❌ |
| 2020-04-09 | 2020-04-14 | -1.0000 | -2.93% | strong_negative | ❌ |
| 2020-04-15 | 2020-04-17 | -1.0000 | -7.68% | strong_negative | ❌ |
| 2020-04-20 | 2020-04-24 | -1.0000 | 0.47% | strong_negative | ✅ |
| 2020-04-27 | 2020-04-29 | -1.0000 | -2.87% | strong_negative | ❌ |
| 2020-04-30 | 2020-05-05 | -1.0000 | 1.40% | strong_negative | ✅ |
| 2020-05-06 | 2020-05-11 | 1.0000 | 1.82% | strong_negative | ✅ |
| 2020-05-12 | 2020-05-13 | 1.0000 | -2.22% | regime_shift | ❌ |
| 2020-05-14 | 2020-05-18 | 1.0000 | 9.43% | regime_shift | ✅ |
| 2020-05-19 | 2020-05-21 | 1.0000 | -1.57% | regime_shift | ❌ |
| 2020-05-22 | 2020-05-29 | 1.0000 | 2.38% | regime_shift | ✅ |
| 2020-06-01 | 2020-06-09 | 1.0000 | 4.90% | regime_shift | ✅ |
| 2020-06-10 | 2020-06-11 | 1.0000 | -9.79% | regime_shift | ❌ |
| 2020-06-12 | 2020-06-15 | 1.0000 | 1.55% | regime_shift | ✅ |
| 2020-06-16 | 2020-06-19 | 1.0000 | -3.69% | regime_shift | ❌ |
| 2020-06-22 | 2020-06-24 | 1.0000 | -5.12% | regime_shift | ❌ |
| 2020-06-25 | 2020-07-07 | 1.0000 | 1.69% | regime_shift | ✅ |
| 2020-07-08 | 2020-07-15 | 1.0000 | 10.76% | regime_shift | ✅ |
| 2020-07-16 | 2020-08-04 | 1.0000 | 0.06% | regime_shift | ✅ |
| 2020-08-05 | 2020-09-18 | 1.0000 | 3.92% | weak_negative | ✅ |
| 2020-09-21 | 2020-09-24 | 1.0000 | -1.40% | weak_negative | ❌ |
| 2020-09-25 | 2020-10-15 | 1.0000 | 9.45% | weak_negative | ✅ |
| 2020-10-16 | 2020-10-19 | 1.0000 | -3.36% | weak_negative | ❌ |
| 2020-10-20 | 2020-10-28 | 1.0000 | -6.01% | weak_negative | ❌ |
| 2020-10-29 | 2020-11-03 | 1.0000 | 1.92% | weak_negative | ✅ |
| 2020-11-03 | 2020-11-06 | -1.0000 | -1.55% | weak_negative | ❌ |
| 2020-11-09 | 2020-11-16 | -1.0000 | 3.67% | weak_negative | ✅ |
| 2020-11-17 | 2020-11-18 | -1.0000 | 1.31% | weak_negative | ✅ |
| 2020-11-19 | 2020-11-24 | -1.0000 | -3.11% | weak_negative | ❌ |
| 2020-11-25 | 2020-12-15 | -1.0000 | 1.25% | weak_negative | ✅ |
| 2020-12-16 | 2020-12-29 | -1.0000 | -2.58% | weak_negative | ❌ |
| 2020-12-30 | 2021-01-06 | -1.0000 | -5.28% | weak_negative | ❌ |
| 2021-01-07 | 2021-01-13 | -1.0000 | -2.29% | weak_negative | ❌ |
| 2021-01-14 | 2021-02-02 | -1.0000 | 2.53% | weak_negative | ✅ |
| 2021-04-29 | 2021-05-04 | 1.0000 | -3.18% | regime_shift | ❌ |
| 2021-05-05 | 2021-05-12 | 1.0000 | -5.64% | regime_shift | ❌ |
| 2021-05-13 | 2021-06-02 | 1.0000 | -2.76% | regime_shift | ❌ |
| 2021-06-03 | 2021-07-08 | 1.0000 | -0.28% | regime_shift | ❌ |
| 2021-07-09 | 2021-07-16 | 1.0000 | -3.71% | regime_shift | ❌ |
| 2021-07-19 | 2021-08-03 | 1.0000 | 2.36% | regime_shift | ✅ |
| 2021-08-04 | 2021-08-10 | 1.0000 | -1.66% | regime_shift | ❌ |
| 2021-08-11 | 2021-09-09 | 1.0000 | -0.93% | regime_shift | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 85 | -0.57% | -48.8% | 35.3% |
| 16-30d | 22 | 3.44% | 75.8% | 68.2% |
| 31-50d | 3 | 5.71% | 17.1% | 100.0% |
| 50d+ | 2 | 10.67% | 21.3% | 100.0% |
| 6-15d | 43 | 0.40% | 17.3% | 60.5% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 155 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (16.4%).
**Win/loss profile:** Profit factor of 1.33 with 49.0% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (50.4%) exceeded signal accuracy (29.5%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.
**Regime dependence:** `strong_positive` (15 trades, 10% of total) contributed 45.9% — a disproportionate share. Performance may degrade if this regime becomes less common.

### Known Vulnerabilities

- **Worst year:** 2021 (-11.7%, 14 trades). Macro: Post-COVID Stimulus Rally
- **Losing regime:** `weak_positive` — 14 trades, -1.5% total return
- **Losing regime:** `weak_negative` — 23 trades, -20.3% total return

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.