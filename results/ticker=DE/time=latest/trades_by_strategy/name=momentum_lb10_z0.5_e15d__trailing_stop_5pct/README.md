# Strategy Analysis: momentum_lb10_z0.5_e15d × trailing_stop_5%

**Ticker:** DE
**Entry:** `momentum_lb10_z0.5_e15d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-07-29 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `10`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 21.0% |
| **Annualized Return** | 13.6% |
| **Sharpe Ratio** | 1.333 |
| **Max Drawdown** | -18.0% |
| **Total Trades** | 64 |
| **Win Rate** | 43.8% |
| **Signal Accuracy** | 34.1% |
| **Direction Accuracy** | 43.8% |
| **Skill Ratio** | 37.3% |
| **Profit Factor** | 1.23 |
| **Expectancy** | 0.0050 |
| **Tail Ratio** | 1.91 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.8×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0289 | Ideal for 64 trades: 0.0156 |
| Top-1 Trade | 16.6% of gross profit | Moderate concentration |
| Top-3 Trades | 35.3% of gross profit | Moderate concentration |
| Return ex-Top-1 | -5.6% | Negative without best trade |
| Return ex-Top-3 | -29.6% | Negative without top 3 |
| Max Single Trade | 28.2% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 19 | 6.54% | 124.4% | 6.54% | 10.26 |
| no_signal | 13 | 1.93% | 25.1% | 1.93% | 16.38 |
| direction_wrong_loss | 32 | -3.68% | -117.6% | -3.68% | 4.56 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 64 | 0.50% | 31.9% | 43.8% | 43.8% | 0.50% |

**Best-performing regime:** `unknown` — 64 trades, 31.9% total return, 43.8% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 22 | -3.98% | -87.6% |
| ❌ | ✅ | 14 | 7.26% | 101.7% |
| ✅ | ❌ | 10 | -3.00% | -30.0% |
| ✅ | ✅ | 5 | 4.54% | 22.7% |

### Flip Trades (Signal Wrong → Direction Right)

**23 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **6.4%**
- Total return: **146.9%**
- Average alpha: **6.4%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 23 | 6.39% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 64 | 0.50% | 31.9% | 43.8% | 43.8% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 22 | 1.95% | 42.9% | 50.0% | 50.0% |
| SHORT | 42 | -0.26% | -11.0% | 40.5% | 40.5% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 3 | -13.0% | -4.33% | 33.3% | 33.3% | -13.0% |
| 2017 | 3 | 41.9% | 13.97% | 100.0% | 100.0% | 41.9% |
| 2018 | 9 | -10.9% | -1.21% | 33.3% | 33.3% | -10.9% |
| 2019 | 3 | -18.6% | -6.19% | 0.0% | 0.0% | -18.6% |
| 2020 | 9 | -24.6% | -2.74% | 11.1% | 11.1% | -24.6% |
| 2021 | 9 | -6.6% | -0.73% | 44.4% | 44.4% | -6.6% |
| 2022 | 9 | 33.9% | 3.77% | 55.6% | 55.6% | 33.9% |
| 2023 | 3 | 3.4% | 1.13% | 66.7% | 66.7% | 3.4% |
| 2024 | 6 | 4.9% | 0.81% | 50.0% | 50.0% | 4.9% |
| 2025 | 9 | 8.3% | 0.92% | 55.6% | 55.6% | 8.3% |
| 2026 | 1 | 13.2% | 13.22% | 100.0% | 100.0% | 13.2% |

### Macro Context by Year

**2016** (Losing year: -13.0%, 3 trades)
- No major macro events flagged.

**2017** (Strong year: 41.9%, 3 trades)
- No major macro events flagged.

**2018** (Losing year: -10.9%, 9 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -18.6%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Losing year: -24.6%, 9 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -6.6%, 9 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 33.9%, 9 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 3.4%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 4.9%, 6 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 8.3%, 9 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 13.2%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -82.7% cumulative (trade 8 to trade 31)
**Period:** 2018-02-06 to 2021-04-30 (24 trades)
**Peak cumulative return:** 37.6% → **Trough:** -45.0%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2018-02-06 | 2018-02-07 | -1.0000 | 0.27% | unknown | ✅ |
| 2018-02-08 | 2018-02-09 | -1.0000 | -0.83% | unknown | ❌ |
| 2018-04-27 | 2018-05-04 | -1.0000 | 0.19% | unknown | ✅ |
| 2018-05-07 | 2018-05-10 | -1.0000 | -4.56% | unknown | ❌ |
| 2018-05-11 | 2018-05-18 | -1.0000 | -5.38% | unknown | ❌ |
| 2018-10-31 | 2018-11-02 | -1.0000 | -4.64% | unknown | ❌ |
| 2018-11-05 | 2018-11-07 | -1.0000 | -4.05% | unknown | ❌ |
| 2018-11-08 | 2018-11-14 | -1.0000 | -0.37% | unknown | ❌ |
| 2019-04-26 | 2019-05-06 | 1.0000 | -2.93% | unknown | ❌ |
| 2019-05-07 | 2019-05-13 | 1.0000 | -7.28% | unknown | ❌ |
| 2019-05-14 | 2019-05-17 | 1.0000 | -8.35% | unknown | ❌ |
| 2020-01-30 | 2020-02-05 | -1.0000 | -4.49% | unknown | ❌ |
| 2020-02-06 | 2020-02-21 | -1.0000 | -5.08% | unknown | ❌ |
| 2020-02-24 | 2020-03-02 | -1.0000 | 4.62% | unknown | ✅ |
| 2020-07-31 | 2020-08-05 | -1.0000 | -3.69% | unknown | ❌ |
| 2020-08-06 | 2020-08-10 | -1.0000 | -4.77% | unknown | ❌ |
| 2020-08-11 | 2020-08-21 | -1.0000 | -3.25% | unknown | ❌ |
| 2020-11-04 | 2020-11-05 | -1.0000 | -5.45% | unknown | ❌ |
| 2020-11-06 | 2020-11-09 | -1.0000 | -0.50% | unknown | ❌ |
| 2020-11-10 | 2020-11-16 | -1.0000 | -2.02% | unknown | ❌ |
| 2021-01-29 | 2021-02-02 | -1.0000 | -4.76% | unknown | ❌ |
| 2021-02-03 | 2021-02-08 | -1.0000 | -5.28% | unknown | ❌ |
| 2021-02-09 | 2021-02-19 | -1.0000 | -4.65% | unknown | ❌ |
| 2021-04-30 | 2021-05-06 | -1.0000 | -5.14% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 33 | -1.15% | -38.1% | 36.4% |
| 16-30d | 5 | 4.74% | 23.7% | 100.0% |
| 31-50d | 2 | 8.10% | 16.2% | 100.0% |
| 50d+ | 1 | 28.21% | 28.2% | 100.0% |
| 6-15d | 23 | 0.08% | 1.9% | 34.8% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 10

## Observations & Caveats

**Sample size:** 64 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-29.6%).
**Win/loss profile:** Profit factor of 1.23 with 43.8% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (43.8%) exceeded signal accuracy (34.1%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2020 (-24.6%, 9 trades). Macro: COVID-19 Crash & Recovery, Post-COVID Stimulus Rally

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 9d, std 10d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.