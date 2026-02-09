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
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 23.4% |
| **Annualized Return** | 26.9% |
| **Sharpe Ratio** | 1.493 |
| **Max Drawdown** | -17.3% |
| **Total Trades** | 189 |
| **Win Rate** | 43.4% |
| **Signal Accuracy** | 37.0% |
| **Direction Accuracy** | 43.4% |
| **Skill Ratio** | 43.5% |
| **Profit Factor** | 1.14 |
| **Expectancy** | 0.0026 |
| **Tail Ratio** | 1.58 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 701.3% | 23.4% | -677.9% |
| Annualized Return | 20.7% | 26.9% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.9×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0102 | Ideal for 189 trades: 0.0053 |
| Top-1 Trade | 9.2% of gross profit | Moderate concentration |
| Top-3 Trades | 17.2% of gross profit | Moderate concentration |
| Return ex-Top-1 | -10.3% | Negative without best trade |
| Return ex-Top-3 | -33.9% | Negative without top 3 |
| Max Single Trade | 37.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 73 | 4.83% | 352.3% | 4.85% | 7.55 |
| no_signal | 21 | 0.73% | 15.3% | -0.23% | 15.00 |
| direction_wrong_loss | 95 | -3.35% | -318.1% | -4.13% | 4.22 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 189 | 0.26% | 49.4% | 43.4% | 43.4% | -0.23% |

**Best-performing regime:** `unknown` — 189 trades, 49.4% total return, 43.4% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 64 | -3.45% | -220.7% |
| ❌ | ✅ | 47 | 4.57% | 214.8% |
| ✅ | ❌ | 31 | -3.14% | -97.5% |
| ✅ | ✅ | 26 | 5.29% | 137.4% |

### Flip Trades (Signal Wrong → Direction Right)

**56 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.9%**
- Total return: **272.1%**
- Average alpha: **5.2%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 56 | 4.86% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 189 | 0.26% | 49.4% | 43.4% | 43.4% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 73 | 1.24% | 90.7% | 47.9% | 47.9% |
| SHORT | 116 | -0.36% | -41.2% | 40.5% | 40.5% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 7 | -9.5% | -1.36% | 42.9% | 42.9% | -19.5% |
| 2017 | 6 | -12.9% | -2.15% | 16.7% | 16.7% | -21.0% |
| 2018 | 20 | 13.1% | 0.65% | 65.0% | 65.0% | 17.1% |
| 2019 | 21 | -22.0% | -1.05% | 28.6% | 28.6% | -36.7% |
| 2020 | 36 | 64.7% | 1.80% | 55.6% | 55.6% | 33.8% |
| 2021 | 26 | -5.4% | -0.21% | 42.3% | 42.3% | -17.7% |
| 2022 | 38 | 6.7% | 0.18% | 36.8% | 36.8% | 15.1% |
| 2023 | 16 | 2.4% | 0.15% | 37.5% | 37.5% | -12.7% |
| 2024 | 4 | -4.3% | -1.08% | 50.0% | 50.0% | -8.2% |
| 2025 | 14 | -2.8% | -0.20% | 35.7% | 35.7% | -13.6% |
| 2026 | 1 | 19.5% | 19.47% | 100.0% | 100.0% | 20.0% |

### Macro Context by Year

**2016** (Losing year: -9.5%, 7 trades)
- No major macro events flagged.

**2017** (Losing year: -12.9%, 6 trades)
- No major macro events flagged.

**2018** (Strong year: 13.1%, 20 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -22.0%, 21 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 64.7%, 36 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -5.4%, 26 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Modestly positive: 6.7%, 38 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 2.4%, 16 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Roughly flat: -4.3%, 4 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Roughly flat: -2.8%, 14 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 19.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -39.2% cumulative (trade 9 to trade 52)
**Period:** 2017-08-15 to 2019-07-16 (44 trades)
**Peak cumulative return:** -7.2% → **Trough:** -46.4%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2017-08-15 | 2017-09-11 | -1.0000 | 7.27% | unknown | ✅ |
| 2017-09-12 | 2017-09-19 | -1.0000 | -4.96% | unknown | ❌ |
| 2017-09-20 | 2017-10-03 | -1.0000 | -3.85% | unknown | ❌ |
| 2017-10-04 | 2017-10-27 | -1.0000 | -3.83% | unknown | ❌ |
| 2017-10-30 | 2017-11-17 | -1.0000 | -2.62% | unknown | ❌ |
| 2018-02-13 | 2018-02-15 | -1.0000 | -3.42% | unknown | ❌ |
| 2018-02-16 | 2018-03-06 | -1.0000 | 6.45% | unknown | ✅ |
| 2018-03-07 | 2018-03-09 | -1.0000 | -6.35% | unknown | ❌ |
| 2018-03-12 | 2018-03-27 | -1.0000 | 7.24% | unknown | ✅ |
| 2018-03-28 | 2018-04-05 | -1.0000 | 0.09% | unknown | ✅ |
| 2018-04-06 | 2018-04-12 | -1.0000 | -3.35% | unknown | ❌ |
| 2018-04-13 | 2018-04-24 | -1.0000 | 7.91% | unknown | ✅ |
| 2018-04-25 | 2018-05-04 | -1.0000 | 0.51% | unknown | ✅ |
| 2018-05-07 | 2018-05-10 | -1.0000 | -4.56% | unknown | ❌ |
| 2018-05-11 | 2018-05-15 | -1.0000 | 1.22% | unknown | ✅ |
| 2018-11-16 | 2018-11-21 | -1.0000 | 4.05% | unknown | ✅ |
| 2018-11-23 | 2018-11-26 | -1.0000 | -4.26% | unknown | ❌ |
| 2018-11-27 | 2018-11-30 | -1.0000 | -4.78% | unknown | ❌ |
| 2018-12-03 | 2018-12-04 | -1.0000 | 6.55% | unknown | ✅ |
| 2018-12-06 | 2018-12-07 | -1.0000 | 4.62% | unknown | ✅ |
| 2018-12-10 | 2018-12-11 | -1.0000 | 0.02% | unknown | ✅ |
| 2018-12-12 | 2018-12-19 | -1.0000 | 1.39% | unknown | ✅ |
| 2018-12-20 | 2018-12-26 | -1.0000 | 0.95% | unknown | ✅ |
| 2018-12-27 | 2018-12-28 | -1.0000 | 0.47% | unknown | ✅ |
| 2018-12-31 | 2019-01-04 | -1.0000 | -1.68% | unknown | ❌ |
| 2019-01-07 | 2019-01-10 | -1.0000 | -3.22% | unknown | ❌ |
| 2019-01-11 | 2019-01-18 | -1.0000 | -4.00% | unknown | ❌ |
| 2019-01-22 | 2019-01-30 | -1.0000 | -2.56% | unknown | ❌ |
| 2019-01-31 | 2019-02-12 | -1.0000 | -0.73% | unknown | ❌ |
| 2019-02-12 | 2019-02-21 | 1.0000 | -1.42% | unknown | ❌ |
| 2019-02-22 | 2019-03-06 | 1.0000 | -4.66% | unknown | ❌ |
| 2019-03-07 | 2019-04-10 | 1.0000 | 0.87% | unknown | ✅ |
| 2019-04-11 | 2019-04-25 | 1.0000 | 1.03% | unknown | ✅ |
| 2019-04-26 | 2019-05-06 | 1.0000 | -2.93% | unknown | ❌ |
| 2019-05-07 | 2019-05-13 | 1.0000 | -7.28% | unknown | ❌ |
| 2019-05-14 | 2019-05-17 | -1.0000 | 8.35% | unknown | ✅ |
| 2019-05-20 | 2019-05-21 | -1.0000 | -2.60% | unknown | ❌ |
| 2019-05-22 | 2019-05-30 | -1.0000 | -2.09% | unknown | ❌ |
| 2019-05-31 | 2019-06-04 | -1.0000 | -3.89% | unknown | ❌ |
| 2019-06-05 | 2019-06-11 | -1.0000 | -2.59% | unknown | ❌ |
| 2019-06-12 | 2019-06-17 | -1.0000 | -3.75% | unknown | ❌ |
| 2019-06-18 | 2019-06-21 | -1.0000 | -3.07% | unknown | ❌ |
| 2019-06-24 | 2019-07-15 | -1.0000 | 0.07% | unknown | ✅ |
| 2019-07-16 | 2019-07-26 | -1.0000 | -2.55% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 114 | -1.01% | -114.9% | 33.3% |
| 16-30d | 14 | 3.48% | 48.7% | 71.4% |
| 31-50d | 2 | 22.21% | 44.4% | 100.0% |
| 50d+ | 2 | 1.72% | 3.4% | 50.0% |
| 6-15d | 57 | 1.19% | 67.7% | 54.4% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 10

## Observations & Caveats

**Sample size:** 189 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-33.9%).
**Win/loss profile:** Profit factor of 1.14 with 43.4% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (43.4%) exceeded signal accuracy (37.0%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2019 (-22.0%, 21 trades). Macro: US-China Trade War Escalation, Fed Rate Cuts (2019)

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 7d, std 9d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.