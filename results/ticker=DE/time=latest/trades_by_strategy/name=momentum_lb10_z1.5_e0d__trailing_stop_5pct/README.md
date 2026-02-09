# Strategy Analysis: momentum_lb10_z1.5_e0d × trailing_stop_5%

**Ticker:** DE
**Entry:** `momentum_lb10_z1.5_e0d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-08-19 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `10`
- **zscore_threshold:** `1.5`
- **zscore_window:** `60`
- **entry_days_before:** `0` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | -22.0% |
| **Annualized Return** | 15.6% |
| **Sharpe Ratio** | 1.274 |
| **Max Drawdown** | -7.2% |
| **Total Trades** | 45 |
| **Win Rate** | 28.9% |
| **Signal Accuracy** | 31.0% |
| **Direction Accuracy** | 29.5% |
| **Skill Ratio** | 25.7% |
| **Profit Factor** | 0.84 |
| **Expectancy** | -0.0035 |
| **Tail Ratio** | 2.58 |

## Diversity & Concentration

Diversification: **Somewhat concentrated** — noticeable dependence on top trades (HHI ratio: 2.7×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0602 | Ideal for 45 trades: 0.0222 |
| Top-1 Trade | 43.5% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 64.4% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | -43.0% | Negative without best trade |
| Return ex-Top-3 | -51.9% | Negative without top 3 |
| Max Single Trade | 36.9% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 9 | 4.41% | 39.7% | 4.41% | 18.67 |
| no_signal | 10 | 3.25% | 32.5% | 3.25% | 24.80 |
| direction_wrong_loss | 26 | -3.39% | -88.0% | -3.39% | 6.38 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 45 | -0.35% | -15.8% | 28.9% | 28.9% | -0.35% |

**Best-performing regime:** `unknown` — 45 trades, -15.8% total return, 28.9% win rate.
**Worst-performing regime:** `unknown` — 45 trades, -15.8% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 19 | -3.59% | -68.1% |
| ❌ | ✅ | 7 | 4.75% | 33.3% |
| ✅ | ❌ | 7 | -2.84% | -19.9% |
| ✅ | ✅ | 2 | 3.19% | 6.4% |

### Flip Trades (Signal Wrong → Direction Right)

**11 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **7.1%**
- Total return: **78.4%**
- Average alpha: **7.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 11 | 7.13% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 45 | -0.35% | -15.8% | 28.9% | 28.9% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 21 | 0.60% | 12.5% | 33.3% | 33.3% |
| SHORT | 24 | -1.18% | -28.4% | 25.0% | 25.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 3 | 30.2% | 10.05% | 33.3% | 33.3% | 30.2% |
| 2017 | 6 | 0.3% | 0.05% | 50.0% | 50.0% | 0.3% |
| 2018 | 5 | -2.4% | -0.49% | 40.0% | 40.0% | -2.4% |
| 2019 | 5 | -11.6% | -2.31% | 0.0% | 0.0% | -11.6% |
| 2020 | 1 | 4.1% | 4.10% | 100.0% | 100.0% | 4.1% |
| 2021 | 3 | 3.9% | 1.30% | 66.7% | 66.7% | 3.9% |
| 2022 | 5 | -15.7% | -3.15% | 0.0% | 0.0% | -15.7% |
| 2023 | 7 | -7.9% | -1.12% | 28.6% | 28.6% | -7.9% |
| 2024 | 6 | -18.3% | -3.05% | 16.7% | 16.7% | -18.3% |
| 2025 | 3 | 1.6% | 0.52% | 33.3% | 33.3% | 1.6% |
| 2026 | 1 | 0.0% | 0.00% | 0.0% | 0.0% | 0.0% |

### Macro Context by Year

**2016** (Strong year: 30.2%, 3 trades)
- No major macro events flagged.

**2017** (Modestly positive: 0.3%, 6 trades)
- No major macro events flagged.

**2018** (Roughly flat: -2.4%, 5 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -11.6%, 5 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Modestly positive: 4.1%, 1 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 3.9%, 3 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -15.7%, 5 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Losing year: -7.9%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -18.3%, 6 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 1.6%, 3 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Roughly flat: 0.0%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -55.2% cumulative (trade 12 to trade 42)
**Period:** 2018-05-18 to 2025-08-14 (31 trades)
**Peak cumulative return:** 35.6% → **Trough:** -19.6%

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
| 2018-05-18 | 2018-05-23 | 1.0000 | 0.86% | unknown | ✅ |
| 2018-05-24 | 2018-05-31 | 1.0000 | -5.48% | unknown | ❌ |
| 2018-06-01 | 2018-06-14 | 1.0000 | -2.09% | unknown | ❌ |
| 2019-05-17 | 2019-05-21 | -1.0000 | -3.02% | unknown | ❌ |
| 2019-05-22 | 2019-05-30 | -1.0000 | -2.09% | unknown | ❌ |
| 2019-05-31 | 2019-06-04 | -1.0000 | -3.89% | unknown | ❌ |
| 2019-11-27 | 2019-12-11 | -1.0000 | -0.38% | unknown | ❌ |
| 2019-12-12 | 2020-01-02 | -1.0000 | -2.19% | unknown | ❌ |
| 2020-01-03 | 2020-02-05 | -1.0000 | 4.10% | unknown | ✅ |
| 2021-05-21 | 2021-06-21 | -1.0000 | 6.08% | unknown | ✅ |
| 2021-06-22 | 2021-06-24 | -1.0000 | -2.49% | unknown | ❌ |
| 2021-06-25 | 2021-07-20 | -1.0000 | 0.30% | unknown | ✅ |
| 2022-05-20 | 2022-05-23 | -1.0000 | -7.04% | unknown | ❌ |
| 2022-05-24 | 2022-05-25 | -1.0000 | -1.76% | unknown | ❌ |
| 2022-05-26 | 2022-05-27 | -1.0000 | -3.80% | unknown | ❌ |
| 2022-11-23 | 2022-12-16 | 1.0000 | -1.47% | unknown | ❌ |
| 2022-12-19 | 2023-01-03 | 1.0000 | -1.66% | unknown | ❌ |
| 2023-01-04 | 2023-01-19 | 1.0000 | -3.51% | unknown | ❌ |
| 2023-02-17 | 2023-02-24 | 1.0000 | -3.67% | unknown | ❌ |
| 2023-02-27 | 2023-03-10 | 1.0000 | -6.10% | unknown | ❌ |
| 2023-03-13 | 2023-03-15 | 1.0000 | -1.94% | unknown | ❌ |
| 2023-08-18 | 2023-08-29 | -1.0000 | -1.78% | unknown | ❌ |
| 2023-08-30 | 2023-10-10 | -1.0000 | 5.09% | unknown | ✅ |
| 2023-10-11 | 2023-11-02 | -1.0000 | 4.06% | unknown | ✅ |
| 2024-02-15 | 2024-03-07 | -1.0000 | -2.92% | unknown | ❌ |
| 2024-03-08 | 2024-03-19 | -1.0000 | -4.65% | unknown | ❌ |
| 2024-03-20 | 2024-03-27 | -1.0000 | -4.21% | unknown | ❌ |
| 2024-11-21 | 2024-12-06 | 1.0000 | 1.48% | unknown | ✅ |
| 2024-12-09 | 2024-12-18 | 1.0000 | -5.21% | unknown | ❌ |
| 2024-12-19 | 2025-01-07 | 1.0000 | -2.76% | unknown | ❌ |
| 2025-08-14 | 2025-08-19 | -1.0000 | -2.21% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 18 | -2.47% | -44.5% | 11.1% |
| 16-30d | 7 | 2.73% | 19.1% | 85.7% |
| 31-50d | 3 | 5.21% | 15.6% | 100.0% |
| 50d+ | 1 | 36.89% | 36.9% | 100.0% |
| 6-15d | 16 | -2.68% | -42.9% | 6.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 3
- **Max consecutive losses:** 10

## Observations & Caveats

**Sample size:** 45 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-51.9%).
**Signal vs Direction:** Signal accuracy (31.0%) and direction accuracy (29.5%) are similar, suggesting the correlation flip had limited net impact in this sample.

### Known Vulnerabilities

- **Worst year:** 2024 (-18.3%, 6 trades). Macro: 2024 Election Year Uncertainty
- **Losing regime:** `unknown` — 45 trades, -15.8% total return

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 13d, std 18d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.