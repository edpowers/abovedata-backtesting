# Strategy Analysis: momentum_lb20_z0.5_e10d × trailing_stop_5%

**Ticker:** DE
**Entry:** `momentum_lb20_z0.5_e10d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-08-05 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `10` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 204.9% |
| **Annualized Return** | 26.2% |
| **Sharpe Ratio** | 1.503 |
| **Max Drawdown** | -18.2% |
| **Total Trades** | 180 |
| **Win Rate** | 46.1% |
| **Signal Accuracy** | 29.8% |
| **Direction Accuracy** | 46.1% |
| **Skill Ratio** | 45.6% |
| **Profit Factor** | 1.45 |
| **Expectancy** | 0.0077 |
| **Tail Ratio** | 1.71 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 701.3% | 204.9% | -496.4% |
| Annualized Return | 20.7% | 26.2% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.8×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0100 | Ideal for 180 trades: 0.0056 |
| Top-1 Trade | 4.4% of gross profit | Moderate concentration |
| Top-3 Trades | 12.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 155.2% | Positive without best trade |
| Return ex-Top-3 | 81.1% | Positive without top 3 |
| Max Single Trade | 19.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 68 | 5.29% | 359.9% | 5.48% | 9.04 |
| no_signal | 31 | 1.30% | 40.3% | 0.59% | 12.13 |
| direction_wrong_loss | 81 | -3.23% | -261.7% | -4.16% | 4.36 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 180 | 0.77% | 138.4% | 46.1% | 46.1% | 0.30% |

**Best-performing regime:** `unknown` — 180 trades, 138.4% total return, 46.1% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 60 | -3.35% | -201.2% |
| ❌ | ✅ | 50 | 5.19% | 259.6% |
| ✅ | ❌ | 21 | -2.88% | -60.5% |
| ✅ | ✅ | 18 | 5.57% | 100.2% |

### Flip Trades (Signal Wrong → Direction Right)

**65 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.3%**
- Total return: **344.5%**
- Average alpha: **5.5%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 65 | 5.30% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 180 | 0.77% | 138.4% | 46.1% | 46.1% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 64 | 2.18% | 139.6% | 54.7% | 54.7% |
| SHORT | 116 | -0.01% | -1.2% | 41.4% | 41.4% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 5 | -15.6% | -3.12% | 20.0% | 20.0% | -17.0% |
| 2017 | 13 | 16.5% | 1.27% | 46.2% | 46.2% | -2.2% |
| 2018 | 12 | 10.0% | 0.83% | 58.3% | 58.3% | 10.1% |
| 2019 | 5 | 0.7% | 0.14% | 80.0% | 80.0% | -8.7% |
| 2020 | 31 | 17.6% | 0.57% | 45.2% | 45.2% | -0.4% |
| 2021 | 23 | 12.5% | 0.54% | 43.5% | 43.5% | 1.0% |
| 2022 | 41 | 48.5% | 1.18% | 46.3% | 46.3% | 64.8% |
| 2023 | 17 | 9.2% | 0.54% | 35.3% | 35.3% | -9.9% |
| 2024 | 10 | 4.1% | 0.41% | 50.0% | 50.0% | -0.6% |
| 2025 | 22 | 15.4% | 0.70% | 45.5% | 45.5% | -2.5% |
| 2026 | 1 | 19.5% | 19.47% | 100.0% | 100.0% | 20.0% |

### Macro Context by Year

**2016** (Losing year: -15.6%, 5 trades)
- No major macro events flagged.

**2017** (Strong year: 16.5%, 13 trades)
- No major macro events flagged.

**2018** (Modestly positive: 10.0%, 12 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 0.7%, 5 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 17.6%, 31 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 12.5%, 23 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 48.5%, 41 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 9.2%, 17 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 4.1%, 10 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 15.4%, 22 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 19.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -35.5% cumulative (trade 43 to trade 49)
**Period:** 2020-03-19 to 2020-04-07 (7 trades)
**Peak cumulative return:** 44.6% → **Trough:** 9.1%

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

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 95 | -0.52% | -49.5% | 33.7% |
| 16-30d | 17 | 5.54% | 94.2% | 88.2% |
| 31-50d | 2 | 12.91% | 25.8% | 100.0% |
| 50d+ | 1 | -5.36% | -5.4% | 0.0% |
| 6-15d | 65 | 1.13% | 73.2% | 52.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 180 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (81.1%).
**Win/loss profile:** Profit factor of 1.45 with 46.1% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (46.1%) exceeded signal accuracy (29.8%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2016 (-15.6%, 5 trades). Macro: No flagged events

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 7d, std 8d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.