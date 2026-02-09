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
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 37.6% |
| **Annualized Return** | 18.5% |
| **Sharpe Ratio** | 1.512 |
| **Max Drawdown** | -17.6% |
| **Total Trades** | 78 |
| **Win Rate** | 46.2% |
| **Signal Accuracy** | 37.0% |
| **Direction Accuracy** | 46.2% |
| **Skill Ratio** | 49.2% |
| **Profit Factor** | 1.31 |
| **Expectancy** | 0.0057 |
| **Tail Ratio** | 1.88 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.9×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0243 | Ideal for 78 trades: 0.0128 |
| Top-1 Trade | 10.8% of gross profit | Moderate concentration |
| Top-3 Trades | 31.2% of gross profit | Moderate concentration |
| Return ex-Top-1 | 14.1% | Positive without best trade |
| Return ex-Top-3 | -19.8% | Negative without top 3 |
| Max Single Trade | 20.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 29 | 4.99% | 144.8% | 4.99% | 12.14 |
| no_signal | 19 | 0.12% | 2.3% | 0.12% | 15.63 |
| direction_wrong_loss | 30 | -3.41% | -102.3% | -3.41% | 4.77 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 78 | 0.57% | 44.8% | 46.2% | 46.2% | 0.57% |

**Best-performing regime:** `unknown` — 78 trades, 44.8% total return, 46.2% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 20 | -3.93% | -78.7% |
| ❌ | ✅ | 19 | 4.74% | 90.1% |
| ✅ | ❌ | 10 | -2.36% | -23.6% |
| ✅ | ✅ | 10 | 5.47% | 54.7% |

### Flip Trades (Signal Wrong → Direction Right)

**26 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.2%**
- Total return: **135.0%**
- Average alpha: **5.2%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 26 | 5.19% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 78 | 0.57% | 44.8% | 46.2% | 46.2% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 38 | 2.31% | 87.7% | 60.5% | 60.5% |
| SHORT | 40 | -1.07% | -43.0% | 32.5% | 32.5% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 3 | -9.6% | -3.20% | 33.3% | 33.3% | -9.6% |
| 2017 | 9 | 6.4% | 0.71% | 33.3% | 33.3% | 6.4% |
| 2018 | 5 | 4.0% | 0.80% | 40.0% | 40.0% | 4.0% |
| 2019 | 9 | -13.1% | -1.45% | 44.4% | 44.4% | -13.1% |
| 2020 | 9 | 13.3% | 1.48% | 55.6% | 55.6% | 13.3% |
| 2021 | 9 | 11.8% | 1.31% | 55.6% | 55.6% | 11.8% |
| 2022 | 12 | 32.6% | 2.71% | 58.3% | 58.3% | 32.6% |
| 2023 | 3 | -5.3% | -1.76% | 33.3% | 33.3% | -5.3% |
| 2024 | 6 | -11.2% | -1.87% | 33.3% | 33.3% | -11.2% |
| 2025 | 12 | -3.6% | -0.30% | 41.7% | 41.7% | -3.6% |
| 2026 | 1 | 19.5% | 19.47% | 100.0% | 100.0% | 19.5% |

### Macro Context by Year

**2016** (Losing year: -9.6%, 3 trades)
- No major macro events flagged.

**2017** (Modestly positive: 6.4%, 9 trades)
- No major macro events flagged.

**2018** (Modestly positive: 4.0%, 5 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -13.1%, 9 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 13.3%, 9 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 11.8%, 9 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 32.6%, 12 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Losing year: -5.3%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -11.2%, 6 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Roughly flat: -3.6%, 12 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 19.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -34.5% cumulative (trade 55 to trade 72)
**Period:** 2022-11-03 to 2025-07-17 (18 trades)
**Peak cumulative return:** 47.1% → **Trough:** 12.5%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-11-03 | 2022-12-16 | 1.0000 | 9.52% | unknown | ✅ |
| 2022-12-19 | 2023-01-03 | 1.0000 | -1.66% | unknown | ❌ |
| 2023-01-20 | 2023-01-30 | -1.0000 | -2.44% | unknown | ❌ |
| 2023-01-31 | 2023-02-02 | -1.0000 | 3.85% | unknown | ✅ |
| 2023-02-03 | 2023-02-17 | -1.0000 | -6.71% | unknown | ❌ |
| 2024-07-18 | 2024-07-23 | 1.0000 | -2.40% | unknown | ❌ |
| 2024-07-24 | 2024-07-30 | 1.0000 | 0.64% | unknown | ✅ |
| 2024-07-31 | 2024-08-01 | 1.0000 | -3.78% | unknown | ❌ |
| 2024-10-24 | 2024-11-08 | -1.0000 | 4.14% | unknown | ✅ |
| 2024-11-11 | 2024-11-18 | -1.0000 | -0.47% | unknown | ❌ |
| 2024-11-19 | 2024-11-21 | -1.0000 | -9.36% | unknown | ❌ |
| 2025-01-15 | 2025-01-17 | -1.0000 | -6.19% | unknown | ❌ |
| 2025-01-21 | 2025-01-24 | -1.0000 | -3.37% | unknown | ❌ |
| 2025-01-27 | 2025-02-13 | -1.0000 | 3.70% | unknown | ✅ |
| 2025-04-16 | 2025-04-22 | -1.0000 | -0.50% | unknown | ❌ |
| 2025-04-23 | 2025-05-01 | -1.0000 | -5.17% | unknown | ❌ |
| 2025-05-02 | 2025-05-08 | -1.0000 | -1.73% | unknown | ❌ |
| 2025-07-17 | 2025-07-24 | -1.0000 | -3.11% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 34 | -1.30% | -44.1% | 29.4% |
| 16-30d | 10 | 6.44% | 64.4% | 80.0% |
| 31-50d | 3 | 2.33% | 7.0% | 66.7% |
| 50d+ | 1 | 19.14% | 19.1% | 100.0% |
| 6-15d | 30 | -0.06% | -1.7% | 50.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 78 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-19.8%).
**Win/loss profile:** Profit factor of 1.31 with 46.2% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (46.2%) exceeded signal accuracy (37.0%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2019 (-13.1%, 9 trades). Macro: US-China Trade War Escalation, Fed Rate Cuts (2019)

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 10d, std 11d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.