# Strategy Analysis: momentum_lb40_z0.5_e10d × trailing_stop_5%

**Ticker:** DE
**Entry:** `momentum_lb40_z0.5_e10d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-08-05 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `40`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `10` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 122.7% |
| **Annualized Return** | 33.3% |
| **Sharpe Ratio** | 1.889 |
| **Max Drawdown** | -18.1% |
| **Total Trades** | 176 |
| **Win Rate** | 44.9% |
| **Signal Accuracy** | 35.2% |
| **Direction Accuracy** | 44.9% |
| **Skill Ratio** | 44.6% |
| **Profit Factor** | 1.35 |
| **Expectancy** | 0.0062 |
| **Tail Ratio** | 1.99 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 701.3% | 122.7% | -578.6% |
| Annualized Return | 20.7% | 33.3% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.0×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0114 | Ideal for 176 trades: 0.0057 |
| Top-1 Trade | 8.9% of gross profit | Moderate concentration |
| Top-3 Trades | 18.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 61.9% | Positive without best trade |
| Return ex-Top-3 | 14.0% | Positive without top 3 |
| Max Single Trade | 37.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 66 | 5.17% | 340.9% | 4.57% | 9.64 |
| no_signal | 28 | 0.91% | 25.6% | 0.21% | 13.36 |
| direction_wrong_loss | 82 | -3.14% | -257.8% | -3.55% | 5.24 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 176 | 0.62% | 108.7% | 44.9% | 44.9% | 0.09% |

**Best-performing regime:** `unknown` — 176 trades, 108.7% total return, 44.9% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 62 | -3.34% | -207.2% |
| ❌ | ✅ | 41 | 4.74% | 194.4% |
| ✅ | ❌ | 20 | -2.53% | -50.6% |
| ✅ | ✅ | 25 | 5.86% | 146.5% |

### Flip Trades (Signal Wrong → Direction Right)

**54 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.1%**
- Total return: **275.6%**
- Average alpha: **5.4%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 54 | 5.10% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 176 | 0.62% | 108.7% | 44.9% | 44.9% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 74 | 1.84% | 136.0% | 55.4% | 55.4% |
| SHORT | 102 | -0.27% | -27.3% | 37.3% | 37.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 7 | -7.2% | -1.02% | 42.9% | 42.9% | -15.1% |
| 2017 | 8 | 10.0% | 1.25% | 37.5% | 37.5% | -6.2% |
| 2018 | 30 | 7.5% | 0.25% | 40.0% | 40.0% | 6.3% |
| 2019 | 7 | 5.7% | 0.81% | 57.1% | 57.1% | 5.7% |
| 2020 | 19 | 54.0% | 2.84% | 57.9% | 57.9% | 20.5% |
| 2021 | 28 | 13.2% | 0.47% | 46.4% | 46.4% | -6.5% |
| 2022 | 23 | 33.2% | 1.44% | 52.2% | 52.2% | 45.0% |
| 2023 | 23 | -31.4% | -1.37% | 26.1% | 26.1% | -41.3% |
| 2024 | 11 | -8.0% | -0.73% | 45.5% | 45.5% | -16.9% |
| 2025 | 19 | 12.3% | 0.65% | 47.4% | 47.4% | 5.1% |
| 2026 | 1 | 19.5% | 19.47% | 100.0% | 100.0% | 20.0% |

### Macro Context by Year

**2016** (Losing year: -7.2%, 7 trades)
- No major macro events flagged.

**2017** (Modestly positive: 10.0%, 8 trades)
- No major macro events flagged.

**2018** (Modestly positive: 7.5%, 30 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 5.7%, 7 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 54.0%, 19 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 13.2%, 28 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 33.2%, 23 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Losing year: -31.4%, 23 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -8.0%, 11 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 12.3%, 19 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 19.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -46.2% cumulative (trade 132 to trade 153)
**Period:** 2023-05-02 to 2024-07-02 (22 trades)
**Peak cumulative return:** 120.5% → **Trough:** 74.3%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-05-02 | 2023-05-19 | -1.0000 | 5.28% | unknown | ✅ |
| 2023-05-22 | 2023-06-02 | -1.0000 | -2.93% | unknown | ❌ |
| 2023-06-05 | 2023-06-07 | -1.0000 | -5.00% | unknown | ❌ |
| 2023-06-08 | 2023-06-13 | -1.0000 | -4.59% | unknown | ❌ |
| 2023-06-14 | 2023-06-22 | -1.0000 | -4.17% | unknown | ❌ |
| 2023-06-23 | 2023-07-12 | -1.0000 | -1.11% | unknown | ❌ |
| 2023-07-13 | 2023-07-18 | -1.0000 | -5.37% | unknown | ❌ |
| 2023-07-19 | 2023-08-04 | -1.0000 | 2.78% | unknown | ✅ |
| 2023-08-04 | 2023-08-29 | 1.0000 | -4.70% | unknown | ❌ |
| 2023-08-30 | 2023-09-08 | 1.0000 | -3.29% | unknown | ❌ |
| 2023-09-11 | 2023-09-21 | 1.0000 | -3.18% | unknown | ❌ |
| 2023-09-22 | 2023-10-20 | 1.0000 | -1.15% | unknown | ❌ |
| 2023-10-23 | 2023-10-27 | 1.0000 | -3.25% | unknown | ❌ |
| 2023-10-30 | 2023-11-07 | 1.0000 | 0.39% | unknown | ✅ |
| 2024-02-01 | 2024-02-13 | 1.0000 | -3.66% | unknown | ❌ |
| 2024-02-14 | 2024-02-15 | 1.0000 | -5.23% | unknown | ❌ |
| 2024-02-16 | 2024-04-15 | 1.0000 | 9.59% | unknown | ✅ |
| 2024-04-16 | 2024-04-25 | 1.0000 | 0.27% | unknown | ✅ |
| 2024-04-26 | 2024-05-16 | 1.0000 | 0.28% | unknown | ✅ |
| 2024-05-17 | 2024-05-24 | 1.0000 | -5.56% | unknown | ❌ |
| 2024-05-28 | 2024-07-01 | 1.0000 | -1.86% | unknown | ❌ |
| 2024-07-02 | 2024-07-09 | 1.0000 | -4.41% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 84 | -1.37% | -115.2% | 28.6% |
| 16-30d | 15 | 3.22% | 48.3% | 60.0% |
| 31-50d | 5 | 15.85% | 79.3% | 100.0% |
| 50d+ | 1 | -5.32% | -5.3% | 0.0% |
| 6-15d | 71 | 1.43% | 101.6% | 57.7% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 176 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (14.0%).
**Win/loss profile:** Profit factor of 1.35 with 44.9% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (44.9%) exceeded signal accuracy (35.2%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2023 (-31.4%, 23 trades). Macro: Fed Tightening Cycle, 2023 Soft Landing Rally

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 8d, std 9d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.