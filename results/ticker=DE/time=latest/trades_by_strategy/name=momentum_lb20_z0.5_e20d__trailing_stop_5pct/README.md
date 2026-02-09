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
| **Total Return** | 105.0% |
| **Annualized Return** | 31.8% |
| **Sharpe Ratio** | 1.770 |
| **Max Drawdown** | -17.3% |
| **Total Trades** | 200 |
| **Win Rate** | 47.0% |
| **Signal Accuracy** | 35.1% |
| **Direction Accuracy** | 47.0% |
| **Skill Ratio** | 47.2% |
| **Profit Factor** | 1.29 |
| **Expectancy** | 0.0050 |
| **Tail Ratio** | 1.62 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 701.3% | 105.0% | -596.3% |
| Annualized Return | 20.7% | 31.8% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.9×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0097 | Ideal for 200 trades: 0.0050 |
| Top-1 Trade | 4.7% of gross profit | Moderate concentration |
| Top-3 Trades | 13.5% of gross profit | Moderate concentration |
| Return ex-Top-1 | 70.1% | Positive without best trade |
| Return ex-Top-3 | 18.9% | Positive without top 3 |
| Max Single Trade | 20.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 77 | 4.77% | 367.0% | 4.44% | 9.21 |
| no_signal | 37 | 0.20% | 7.4% | -0.48% | 11.89 |
| direction_wrong_loss | 86 | -3.19% | -274.2% | -3.78% | 4.31 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 200 | 0.50% | 100.2% | 47.0% | 47.0% | -0.00% |

**Best-performing regime:** `unknown` — 200 trades, 100.2% total return, 47.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 60 | -3.40% | -204.3% |
| ❌ | ✅ | 51 | 5.01% | 255.7% |
| ✅ | ❌ | 26 | -2.69% | -69.9% |
| ✅ | ✅ | 26 | 4.28% | 111.3% |

### Flip Trades (Signal Wrong → Direction Right)

**68 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.9%**
- Total return: **329.8%**
- Average alpha: **5.0%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 68 | 4.85% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 200 | 0.50% | 100.2% | 47.0% | 47.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 81 | 1.63% | 131.7% | 56.8% | 56.8% |
| SHORT | 119 | -0.27% | -31.6% | 40.3% | 40.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 4 | -9.6% | -2.40% | 50.0% | 50.0% | -10.7% |
| 2017 | 12 | -0.3% | -0.03% | 25.0% | 25.0% | -16.7% |
| 2018 | 25 | -4.0% | -0.16% | 44.0% | 44.0% | 7.6% |
| 2019 | 15 | 0.2% | 0.02% | 53.3% | 53.3% | -29.2% |
| 2020 | 30 | -0.0% | -0.00% | 43.3% | 43.3% | -21.1% |
| 2021 | 25 | 12.8% | 0.51% | 44.0% | 44.0% | -5.7% |
| 2022 | 36 | 77.9% | 2.16% | 58.3% | 58.3% | 86.5% |
| 2023 | 12 | -4.4% | -0.37% | 33.3% | 33.3% | -13.9% |
| 2024 | 12 | 4.6% | 0.38% | 50.0% | 50.0% | -1.0% |
| 2025 | 28 | 3.5% | 0.12% | 50.0% | 50.0% | -16.7% |
| 2026 | 1 | 19.5% | 19.47% | 100.0% | 100.0% | 20.0% |

### Macro Context by Year

**2016** (Losing year: -9.6%, 4 trades)
- No major macro events flagged.

**2017** (Roughly flat: -0.3%, 12 trades)
- No major macro events flagged.

**2018** (Roughly flat: -4.0%, 25 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 0.2%, 15 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Roughly flat: -0.0%, 30 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 12.8%, 25 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 77.9%, 36 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Roughly flat: -4.4%, 12 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 4.6%, 12 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 3.5%, 28 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 19.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -40.4% cumulative (trade 65 to trade 89)
**Period:** 2020-03-19 to 2021-01-21 (25 trades)
**Peak cumulative return:** 20.4% → **Trough:** -20.0%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-03-19 | 2020-03-20 | -1.0000 | 6.71% | unknown | ✅ |
| 2020-03-23 | 2020-03-24 | -1.0000 | -13.36% | unknown | ❌ |
| 2020-03-25 | 2020-03-26 | -1.0000 | -8.25% | unknown | ❌ |
| 2020-03-27 | 2020-03-30 | -1.0000 | -5.12% | unknown | ❌ |
| 2020-03-31 | 2020-04-02 | -1.0000 | -0.88% | unknown | ❌ |
| 2020-04-03 | 2020-04-06 | -1.0000 | -5.88% | unknown | ❌ |
| 2020-04-07 | 2020-04-09 | -1.0000 | -2.05% | unknown | ❌ |
| 2020-04-13 | 2020-04-14 | -1.0000 | 1.19% | unknown | ✅ |
| 2020-04-15 | 2020-04-16 | -1.0000 | 3.96% | unknown | ✅ |
| 2020-04-17 | 2020-04-20 | -1.0000 | 0.84% | unknown | ✅ |
| 2020-04-21 | 2020-04-23 | -1.0000 | -2.28% | unknown | ❌ |
| 2020-07-24 | 2020-09-04 | 1.0000 | 20.52% | unknown | ✅ |
| 2020-09-08 | 2020-09-21 | 1.0000 | 1.89% | unknown | ✅ |
| 2020-09-22 | 2020-10-02 | 1.0000 | 3.67% | unknown | ✅ |
| 2020-10-05 | 2020-10-27 | 1.0000 | 0.68% | unknown | ✅ |
| 2020-10-28 | 2020-11-03 | -1.0000 | -7.43% | unknown | ❌ |
| 2020-11-04 | 2020-11-05 | -1.0000 | -5.45% | unknown | ❌ |
| 2020-11-06 | 2020-11-09 | -1.0000 | -0.50% | unknown | ❌ |
| 2020-11-10 | 2020-11-16 | -1.0000 | -2.02% | unknown | ❌ |
| 2020-11-17 | 2020-12-15 | -1.0000 | -1.46% | unknown | ❌ |
| 2020-12-16 | 2020-12-28 | -1.0000 | -2.44% | unknown | ❌ |
| 2020-12-29 | 2021-01-06 | -1.0000 | -9.74% | unknown | ❌ |
| 2021-01-07 | 2021-01-12 | -1.0000 | -0.79% | unknown | ❌ |
| 2021-01-13 | 2021-01-21 | -1.0000 | -1.42% | unknown | ❌ |
| 2021-01-21 | 2021-01-28 | 1.0000 | -4.10% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 111 | -0.64% | -71.5% | 36.9% |
| 16-30d | 19 | 3.96% | 75.2% | 73.7% |
| 31-50d | 5 | 6.59% | 33.0% | 80.0% |
| 50d+ | 1 | 19.14% | 19.1% | 100.0% |
| 6-15d | 64 | 0.69% | 44.4% | 53.1% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 10

## Observations & Caveats

**Sample size:** 200 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (18.9%).
**Win/loss profile:** Profit factor of 1.29 with 47.0% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (47.0%) exceeded signal accuracy (35.1%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2016 (-9.6%, 4 trades). Macro: No flagged events

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 8d, std 9d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.