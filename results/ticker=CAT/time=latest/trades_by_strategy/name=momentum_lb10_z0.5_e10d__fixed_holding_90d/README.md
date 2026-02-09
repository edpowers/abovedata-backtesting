# Strategy Analysis: momentum_lb10_z0.5_e10d × fixed_holding_90d

**Ticker:** CAT
**Entry:** `momentum_lb10_z0.5_e10d`
**Exit:** `fixed_holding_90d`
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

- **Exit type:** `fixed_holding_90d`
  - Fixed 90-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 247.8% |
| **Annualized Return** | 14.3% |
| **Sharpe Ratio** | 0.623 |
| **Max Drawdown** | -49.3% |
| **Total Trades** | 13 |
| **Win Rate** | 84.6% |
| **Signal Accuracy** | 57.1% |
| **Direction Accuracy** | 84.6% |
| **Skill Ratio** | 90.9% |
| **Profit Factor** | 3.94 |
| **Expectancy** | 0.1469 |
| **Tail Ratio** | 2.43 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 954.1% | 247.8% | -706.3% |
| Annualized Return | 23.7% | 14.3% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.2×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.1705 | Ideal for 13 trades: 0.0769 |
| Top-1 Trade | 41.2% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 72.6% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 69.4% | Positive without best trade |
| Return ex-Top-3 | -13.8% | Negative without top 3 |
| Max Single Trade | 105.3% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 10 | 21.90% | 219.0% | 15.03% | 107.60 |
| no_signal | 2 | -3.35% | -6.7% | -14.07% | 72.00 |
| direction_wrong_loss | 1 | -21.44% | -21.4% | -12.41% | 62.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 13 | 14.69% | 190.9% | 84.6% | 84.6% | 8.44% |

**Best-performing regime:** `unknown` — 13 trades, 190.9% total return, 84.6% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ✅ | 7 | 27.85% | 194.9% |
| ✅ | ❌ | 1 | -21.44% | -21.4% |
| ✅ | ✅ | 3 | 8.04% | 24.1% |

### Flip Trades (Signal Wrong → Direction Right)

**8 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **29.0%**
- Total return: **231.6%**
- Average alpha: **20.4%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 8 | 28.95% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 4 | 30.31% | 121.2% | 100.0% | 100.0% |
| high | 3 | 29.06% | 87.2% | 100.0% | 100.0% |
| medium | 6 | -2.92% | -17.5% | 66.7% | 66.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 8 | 24.98% | 199.9% | 87.5% | 87.5% |
| SHORT | 5 | -1.79% | -9.0% | 80.0% | 80.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 1 | 11.1% | 11.05% | 100.0% | 100.0% | 20.4% |
| 2019 | 2 | 4.9% | 2.45% | 100.0% | 100.0% | -5.0% |
| 2020 | 1 | 105.3% | 105.29% | 100.0% | 100.0% | 56.4% |
| 2021 | 2 | 29.1% | 14.54% | 100.0% | 100.0% | 21.1% |
| 2022 | 1 | 43.7% | 43.73% | 100.0% | 100.0% | 41.4% |
| 2023 | 1 | 3.9% | 3.86% | 100.0% | 100.0% | 7.5% |
| 2024 | 2 | 21.1% | 10.56% | 100.0% | 100.0% | 8.4% |
| 2025 | 3 | -28.1% | -9.38% | 33.3% | 33.3% | -40.6% |

### Macro Context by Year

**2018** (Strong year: 11.1%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 4.9%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 105.3%, 1 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 29.1%, 2 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 43.7%, 1 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 3.9%, 1 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 21.1%, 2 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -28.1%, 3 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -64.8% cumulative (trade 10 to trade 12)
**Period:** 2024-07-23 to 2025-04-15 (3 trades)
**Peak cumulative return:** 219.0% → **Trough:** 154.2%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-07-23 | 2024-10-16 | 1.0000 | 14.37% | unknown | ✅ |
| 2025-01-15 | 2025-04-15 | 1.0000 | -21.44% | unknown | ❌ |
| 2025-04-15 | 2025-07-22 | -1.0000 | -43.38% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 50d+ | 13 | 14.69% | 190.9% | 84.6% |

## Win/Loss Streaks

- **Max consecutive wins:** 10
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 13 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-13.8%).
**Win/loss profile:** 84.6% win rate with 3.94× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (84.6%) exceeded signal accuracy (57.1%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2025 (-28.1%, 3 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.