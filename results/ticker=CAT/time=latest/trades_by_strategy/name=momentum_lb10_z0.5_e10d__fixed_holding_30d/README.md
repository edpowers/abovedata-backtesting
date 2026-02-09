# Strategy Analysis: momentum_lb10_z0.5_e10d × fixed_holding_30d

**Ticker:** CAT
**Entry:** `momentum_lb10_z0.5_e10d`
**Exit:** `fixed_holding_30d`
**Period:** 2018-10-09 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `10`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `10` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `fixed_holding_30d`
  - Fixed 30-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 258.5% |
| **Annualized Return** | 13.6% |
| **Sharpe Ratio** | 0.596 |
| **Max Drawdown** | -50.4% |
| **Total Trades** | 44 |
| **Win Rate** | 68.2% |
| **Signal Accuracy** | 51.9% |
| **Direction Accuracy** | 68.2% |
| **Skill Ratio** | 73.0% |
| **Profit Factor** | 2.35 |
| **Expectancy** | 0.0357 |
| **Tail Ratio** | 1.58 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 954.1% | 258.5% | -695.6% |
| Annualized Return | 23.7% | 13.6% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.8×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0413 | Ideal for 44 trades: 0.0227 |
| Top-1 Trade | 12.6% of gross profit | Moderate concentration |
| Top-3 Trades | 32.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 166.4% | Positive without best trade |
| Return ex-Top-3 | 66.3% | Positive without top 3 |
| Max Single Trade | 34.6% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 27 | 8.87% | 239.4% | 7.51% | 31.26 |
| no_signal | 7 | -2.73% | -19.1% | -5.32% | 23.00 |
| direction_wrong_loss | 10 | -6.32% | -63.2% | -8.77% | 24.60 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 44 | 3.57% | 157.1% | 68.2% | 68.2% | 1.77% |

**Best-performing regime:** `unknown` — 44 trades, 157.1% total return, 68.2% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 8 | -6.32% | -50.6% |
| ❌ | ✅ | 15 | 10.45% | 156.7% |
| ✅ | ❌ | 2 | -6.29% | -12.6% |
| ✅ | ✅ | 12 | 6.89% | 82.7% |

### Flip Trades (Signal Wrong → Direction Right)

**18 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **10.6%**
- Total return: **191.2%**
- Average alpha: **10.0%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 18 | 10.62% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| high | 6 | 12.33% | 74.0% | 100.0% | 100.0% |
| low | 14 | 3.63% | 50.8% | 57.1% | 57.1% |
| medium | 24 | 1.34% | 32.3% | 66.7% | 66.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 28 | 6.14% | 172.0% | 82.1% | 82.1% |
| SHORT | 16 | -0.93% | -14.8% | 43.8% | 43.8% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 2 | 6.6% | 3.32% | 50.0% | 50.0% | 13.9% |
| 2019 | 5 | -17.3% | -3.46% | 40.0% | 40.0% | -40.5% |
| 2020 | 7 | 84.0% | 12.00% | 85.7% | 85.7% | 61.1% |
| 2021 | 10 | 57.1% | 5.71% | 90.0% | 90.0% | 39.3% |
| 2022 | 5 | 40.6% | 8.12% | 100.0% | 100.0% | 37.6% |
| 2023 | 2 | 1.6% | 0.80% | 50.0% | 50.0% | 6.1% |
| 2024 | 5 | 12.6% | 2.53% | 60.0% | 60.0% | 1.5% |
| 2025 | 7 | -37.4% | -5.34% | 28.6% | 28.6% | -50.9% |
| 2026 | 1 | 9.2% | 9.16% | 100.0% | 100.0% | 9.7% |

### Macro Context by Year

**2018** (Modestly positive: 6.6%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -17.3%, 5 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 84.0%, 7 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 57.1%, 10 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 40.6%, 5 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 1.6%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 12.6%, 5 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -37.4%, 7 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 9.2%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -62.7% cumulative (trade 36 to trade 41)
**Period:** 2024-09-19 to 2025-06-13 (6 trades)
**Peak cumulative return:** 185.3% → **Trough:** 122.6%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-09-19 | 2024-10-16 | 1.0000 | 5.44% | unknown | ✅ |
| 2025-01-15 | 2025-03-14 | 1.0000 | -9.07% | unknown | ❌ |
| 2025-03-17 | 2025-04-15 | 1.0000 | -14.36% | unknown | ❌ |
| 2025-04-15 | 2025-04-29 | -1.0000 | -5.27% | unknown | ❌ |
| 2025-04-30 | 2025-06-12 | -1.0000 | -16.71% | unknown | ❌ |
| 2025-06-13 | 2025-07-22 | -1.0000 | -17.27% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 1 | -2.36% | -2.4% | 0.0% |
| 16-30d | 20 | -0.74% | -14.8% | 60.0% |
| 31-50d | 16 | 7.48% | 119.7% | 81.2% |
| 50d+ | 2 | 23.65% | 47.3% | 100.0% |
| 6-15d | 5 | 1.45% | 7.3% | 60.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 13
- **Max consecutive losses:** 5

## Observations & Caveats

**Sample size:** 44 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (66.3%).
**Win/loss profile:** 68.2% win rate with 2.35× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (68.2%) exceeded signal accuracy (51.9%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2025 (-37.4%, 7 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.