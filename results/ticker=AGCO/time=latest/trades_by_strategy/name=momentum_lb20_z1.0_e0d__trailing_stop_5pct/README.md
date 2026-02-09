# Strategy Analysis: momentum_lb20_z1.0_e0d × trailing_stop_5%

**Ticker:** AGCO
**Entry:** `momentum_lb20_z1.0_e0d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-10-26 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `1.0`
- **zscore_window:** `60`
- **entry_days_before:** `0` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | -7.7% |
| **Annualized Return** | 11.7% |
| **Sharpe Ratio** | 1.199 |
| **Max Drawdown** | -15.1% |
| **Total Trades** | 52 |
| **Win Rate** | 38.5% |
| **Signal Accuracy** | 57.6% |
| **Direction Accuracy** | 39.2% |
| **Skill Ratio** | 38.5% |
| **Profit Factor** | 0.96 |
| **Expectancy** | -0.0006 |
| **Tail Ratio** | 1.73 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 222.5% | -7.7% | -230.2% |
| Annualized Return | 13.5% | 11.7% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.8×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0352 | Ideal for 52 trades: 0.0192 |
| Top-1 Trade | 20.6% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 42.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | -21.3% | Negative without best trade |
| Return ex-Top-3 | -33.6% | Negative without top 3 |
| Max Single Trade | 17.2% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 15 | 2.85% | 42.7% | 2.85% | 7.60 |
| no_signal | 13 | 1.87% | 24.3% | 1.87% | 12.00 |
| direction_wrong_loss | 24 | -2.92% | -70.1% | -2.92% | 2.79 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 52 | -0.06% | -3.1% | 38.5% | 38.5% | -0.06% |

**Best-performing regime:** `unknown` — 52 trades, -3.1% total return, 38.5% win rate.
**Worst-performing regime:** `unknown` — 52 trades, -3.1% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 12 | -2.87% | -34.4% |
| ❌ | ✅ | 8 | 1.70% | 13.6% |
| ✅ | ❌ | 12 | -2.98% | -35.7% |
| ✅ | ✅ | 7 | 4.16% | 29.1% |

### Flip Trades (Signal Wrong → Direction Right)

**13 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.2%**
- Total return: **54.3%**
- Average alpha: **4.2%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 13 | 4.18% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 52 | -0.06% | -3.1% | 38.5% | 38.5% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 25 | 0.79% | 19.7% | 48.0% | 48.0% |
| SHORT | 27 | -0.85% | -22.9% | 29.6% | 29.6% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 3 | 13.3% | 4.42% | 33.3% | 33.3% | 13.3% |
| 2017 | 7 | 1.6% | 0.23% | 42.9% | 42.9% | 1.6% |
| 2018 | 9 | -14.5% | -1.61% | 11.1% | 11.1% | -14.5% |
| 2020 | 6 | 6.3% | 1.05% | 66.7% | 66.7% | 6.3% |
| 2021 | 3 | -3.4% | -1.13% | 33.3% | 33.3% | -3.4% |
| 2022 | 9 | 2.8% | 0.31% | 55.6% | 55.6% | 2.8% |
| 2023 | 3 | -5.5% | -1.84% | 33.3% | 33.3% | -5.5% |
| 2024 | 6 | -5.5% | -0.92% | 33.3% | 33.3% | -5.5% |
| 2025 | 3 | -6.0% | -1.99% | 0.0% | 0.0% | -6.0% |
| 2026 | 3 | 7.8% | 2.60% | 66.7% | 66.7% | 7.8% |

### Macro Context by Year

**2016** (Strong year: 13.3%, 3 trades)
- No major macro events flagged.

**2017** (Modestly positive: 1.6%, 7 trades)
- No major macro events flagged.

**2018** (Losing year: -14.5%, 9 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2020** (Modestly positive: 6.3%, 6 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Roughly flat: -3.4%, 3 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Modestly positive: 2.8%, 9 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Losing year: -5.5%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -5.5%, 6 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -6.0%, 3 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 7.8%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -33.8% cumulative (trade 8 to trade 49)
**Period:** 2017-11-01 to 2025-11-10 (42 trades)
**Peak cumulative return:** 22.9% → **Trough:** -10.9%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2017-11-01 | 2017-11-20 | -1.0000 | 0.47% | unknown | ✅ |
| 2017-11-21 | 2017-12-01 | -1.0000 | -5.05% | unknown | ❌ |
| 2017-12-04 | 2017-12-15 | -1.0000 | -3.00% | unknown | ❌ |
| 2018-02-06 | 2018-02-07 | -1.0000 | -2.82% | unknown | ❌ |
| 2018-02-08 | 2018-02-09 | -1.0000 | -0.43% | unknown | ❌ |
| 2018-02-12 | 2018-02-16 | -1.0000 | 1.44% | unknown | ✅ |
| 2018-07-31 | 2018-08-02 | 1.0000 | -2.51% | unknown | ❌ |
| 2018-08-03 | 2018-08-09 | 1.0000 | -2.16% | unknown | ❌ |
| 2018-08-10 | 2018-08-13 | 1.0000 | -1.17% | unknown | ❌ |
| 2018-10-31 | 2018-11-01 | -1.0000 | -2.41% | unknown | ❌ |
| 2018-11-02 | 2018-11-08 | -1.0000 | -1.38% | unknown | ❌ |
| 2018-11-09 | 2018-11-13 | -1.0000 | -3.03% | unknown | ❌ |
| 2020-02-06 | 2020-02-25 | -1.0000 | 6.86% | unknown | ✅ |
| 2020-02-26 | 2020-02-27 | -1.0000 | 1.45% | unknown | ✅ |
| 2020-02-28 | 2020-03-02 | -1.0000 | -5.25% | unknown | ❌ |
| 2020-07-30 | 2020-07-31 | 1.0000 | -3.37% | unknown | ❌ |
| 2020-08-03 | 2020-08-20 | 1.0000 | 5.30% | unknown | ✅ |
| 2020-08-21 | 2020-09-08 | 1.0000 | 1.32% | unknown | ✅ |
| 2021-04-29 | 2021-05-04 | -1.0000 | -3.12% | unknown | ❌ |
| 2021-05-05 | 2021-05-06 | -1.0000 | -2.89% | unknown | ❌ |
| 2021-05-07 | 2021-05-17 | -1.0000 | 2.62% | unknown | ✅ |
| 2022-02-08 | 2022-02-11 | 1.0000 | 1.59% | unknown | ✅ |
| 2022-02-14 | 2022-02-17 | 1.0000 | -0.68% | unknown | ❌ |
| 2022-02-18 | 2022-02-22 | 1.0000 | -4.43% | unknown | ❌ |
| 2022-05-03 | 2022-05-04 | -1.0000 | -4.34% | unknown | ❌ |
| 2022-05-05 | 2022-05-06 | -1.0000 | 5.76% | unknown | ✅ |
| 2022-05-09 | 2022-05-13 | -1.0000 | -0.18% | unknown | ❌ |
| 2022-07-28 | 2022-08-04 | 1.0000 | 2.97% | unknown | ✅ |
| 2022-08-05 | 2022-08-22 | 1.0000 | 1.42% | unknown | ✅ |
| 2022-08-23 | 2022-08-29 | 1.0000 | 0.64% | unknown | ✅ |
| 2023-02-07 | 2023-02-08 | -1.0000 | 0.39% | unknown | ✅ |
| 2023-02-09 | 2023-02-13 | -1.0000 | -3.27% | unknown | ❌ |
| 2023-02-14 | 2023-02-17 | -1.0000 | -2.63% | unknown | ❌ |
| 2024-05-02 | 2024-05-06 | -1.0000 | -4.37% | unknown | ❌ |
| 2024-05-07 | 2024-05-14 | -1.0000 | -0.42% | unknown | ❌ |
| 2024-05-15 | 2024-06-03 | -1.0000 | 8.71% | unknown | ✅ |
| 2024-07-30 | 2024-08-05 | 1.0000 | -8.93% | unknown | ❌ |
| 2024-08-06 | 2024-08-12 | 1.0000 | -2.29% | unknown | ❌ |
| 2024-08-13 | 2024-09-06 | 1.0000 | 1.78% | unknown | ✅ |
| 2025-10-31 | 2025-11-03 | -1.0000 | -2.04% | unknown | ❌ |
| 2025-11-04 | 2025-11-07 | -1.0000 | -0.83% | unknown | ❌ |
| 2025-11-10 | 2025-11-12 | -1.0000 | -3.09% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 38 | -1.40% | -53.2% | 23.7% |
| 16-30d | 2 | 9.50% | 19.0% | 100.0% |
| 31-50d | 1 | 6.54% | 6.5% | 100.0% |
| 50d+ | 1 | 9.13% | 9.1% | 100.0% |
| 6-15d | 10 | 1.54% | 15.4% | 70.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 52 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-33.6%).
**Signal vs Direction:** Signal accuracy (57.6%) exceeded direction accuracy (39.2%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2018 (-14.5%, 9 trades). Macro: US-China Trade War Escalation
- **Losing regime:** `unknown` — 52 trades, -3.1% total return

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 6d, std 10d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.