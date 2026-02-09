# Strategy Analysis: momentum_lb20_z0.5_e20d × trailing_stop_5%

**Ticker:** TTC
**Entry:** `momentum_lb20_z0.5_e20d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-07-21 to 2026-02-09
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
| **Total Return** | 279.1% |
| **Annualized Return** | 25.9% |
| **Sharpe Ratio** | 1.511 |
| **Max Drawdown** | -23.4% |
| **Total Trades** | 149 |
| **Win Rate** | 47.7% |
| **Signal Accuracy** | 62.7% |
| **Direction Accuracy** | 47.7% |
| **Skill Ratio** | 46.2% |
| **Profit Factor** | 1.73 |
| **Expectancy** | 0.0105 |
| **Tail Ratio** | 2.56 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 259.6% | 279.1% | 19.5% |
| Annualized Return | 12.2% | 25.9% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.2×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0151 | Ideal for 149 trades: 0.0067 |
| Top-1 Trade | 7.8% of gross profit | Moderate concentration |
| Top-3 Trades | 19.5% of gross profit | Moderate concentration |
| Return ex-Top-1 | 194.3% | Positive without best trade |
| Return ex-Top-3 | 98.7% | Positive without top 3 |
| Max Single Trade | 28.8% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 54 | 4.94% | 266.7% | 4.27% | 13.48 |
| no_signal | 32 | 1.68% | 53.7% | 0.62% | 13.00 |
| direction_wrong_loss | 63 | -2.59% | -163.3% | -3.39% | 6.71 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 149 | 1.05% | 157.1% | 47.7% | 47.7% | 0.24% |

**Best-performing regime:** `unknown` — 149 trades, 157.1% total return, 47.7% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 27 | -2.57% | -69.5% |
| ❌ | ✅ | 21 | 5.21% | 109.4% |
| ✅ | ❌ | 36 | -2.61% | -93.8% |
| ✅ | ✅ | 33 | 4.77% | 157.3% |

### Flip Trades (Signal Wrong → Direction Right)

**38 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.6%**
- Total return: **214.2%**
- Average alpha: **3.6%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 38 | 5.64% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 149 | 1.05% | 157.1% | 47.7% | 47.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 81 | 1.87% | 151.9% | 53.1% | 53.1% |
| SHORT | 68 | 0.08% | 5.2% | 41.2% | 41.2% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 5 | 31.8% | 6.36% | 60.0% | 60.0% | 23.4% |
| 2017 | 10 | 20.6% | 2.06% | 80.0% | 80.0% | 2.5% |
| 2018 | 4 | 20.6% | 5.14% | 25.0% | 25.0% | 14.4% |
| 2019 | 7 | 13.7% | 1.96% | 57.1% | 57.1% | 3.5% |
| 2020 | 25 | 33.4% | 1.33% | 60.0% | 60.0% | 21.0% |
| 2021 | 20 | -32.5% | -1.63% | 25.0% | 25.0% | -54.6% |
| 2022 | 18 | 41.3% | 2.29% | 50.0% | 50.0% | 45.8% |
| 2023 | 26 | 22.9% | 0.88% | 46.2% | 46.2% | -1.6% |
| 2024 | 14 | 2.1% | 0.15% | 42.9% | 42.9% | -5.2% |
| 2025 | 18 | -1.8% | -0.10% | 38.9% | 38.9% | -18.0% |
| 2026 | 2 | 4.9% | 2.46% | 50.0% | 50.0% | 5.2% |

### Macro Context by Year

**2016** (Strong year: 31.8%, 5 trades)
- No major macro events flagged.

**2017** (Strong year: 20.6%, 10 trades)
- No major macro events flagged.

**2018** (Strong year: 20.6%, 4 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 13.7%, 7 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 33.4%, 25 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -32.5%, 20 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 41.3%, 18 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 22.9%, 26 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 2.1%, 14 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Roughly flat: -1.8%, 18 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 4.9%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -37.9% cumulative (trade 51 to trade 67)
**Period:** 2020-11-10 to 2021-10-13 (17 trades)
**Peak cumulative return:** 120.1% → **Trough:** 82.2%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-11-10 | 2020-11-17 | 1.0000 | 3.59% | unknown | ✅ |
| 2021-02-03 | 2021-02-08 | -1.0000 | -3.90% | unknown | ❌ |
| 2021-02-09 | 2021-03-01 | -1.0000 | -2.71% | unknown | ❌ |
| 2021-03-02 | 2021-03-04 | -1.0000 | 4.75% | unknown | ✅ |
| 2021-03-05 | 2021-03-10 | -1.0000 | -3.06% | unknown | ❌ |
| 2021-03-11 | 2021-03-18 | -1.0000 | -4.56% | unknown | ❌ |
| 2021-03-19 | 2021-03-29 | -1.0000 | -0.55% | unknown | ❌ |
| 2021-03-30 | 2021-04-15 | -1.0000 | -4.28% | unknown | ❌ |
| 2021-04-16 | 2021-04-22 | -1.0000 | -1.88% | unknown | ❌ |
| 2021-04-23 | 2021-05-05 | -1.0000 | 0.23% | unknown | ✅ |
| 2021-05-05 | 2021-06-23 | 1.0000 | -7.30% | unknown | ❌ |
| 2021-06-24 | 2021-08-19 | 1.0000 | 1.00% | unknown | ✅ |
| 2021-08-20 | 2021-09-07 | 1.0000 | -2.18% | unknown | ❌ |
| 2021-09-08 | 2021-09-17 | 1.0000 | -4.76% | unknown | ❌ |
| 2021-09-20 | 2021-10-01 | 1.0000 | -3.19% | unknown | ❌ |
| 2021-10-04 | 2021-10-12 | 1.0000 | -5.13% | unknown | ❌ |
| 2021-10-13 | 2021-10-27 | 1.0000 | -0.42% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 57 | -0.17% | -9.6% | 36.8% |
| 16-30d | 18 | 3.02% | 54.3% | 77.8% |
| 31-50d | 10 | 7.31% | 73.1% | 90.0% |
| 50d+ | 1 | 23.93% | 23.9% | 100.0% |
| 6-15d | 63 | 0.24% | 15.2% | 41.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 9
- **Max consecutive losses:** 5

## Observations & Caveats

**Sample size:** 149 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (98.7%).
**Win/loss profile:** Profit factor of 1.73 with 47.7% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (62.7%) exceeded direction accuracy (47.7%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2021 (-32.5%, 20 trades). Macro: Post-COVID Stimulus Rally

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 11d, std 11d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.