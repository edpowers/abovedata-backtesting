# Strategy Analysis: momentum_lb20_z0.5_e10d × sl-10%_tp20%

**Ticker:** DE
**Entry:** `momentum_lb20_z0.5_e10d`
**Exit:** `sl-10%_tp20%`
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

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 246.5% |
| **Annualized Return** | 7.2% |
| **Sharpe Ratio** | 0.331 |
| **Max Drawdown** | -29.6% |
| **Total Trades** | 42 |
| **Win Rate** | 57.1% |
| **Signal Accuracy** | 33.3% |
| **Direction Accuracy** | 58.5% |
| **Skill Ratio** | 61.3% |
| **Profit Factor** | 2.22 |
| **Expectancy** | 0.0362 |
| **Tail Ratio** | 1.47 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 701.3% | 246.5% | -454.8% |
| Annualized Return | 20.7% | 7.2% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0365 | Ideal for 42 trades: 0.0238 |
| Top-1 Trade | 9.8% of gross profit | Moderate concentration |
| Top-3 Trades | 26.1% of gross profit | Moderate concentration |
| Return ex-Top-1 | 172.4% | Positive without best trade |
| Return ex-Top-3 | 81.4% | Positive without top 3 |
| Max Single Trade | 27.2% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 19 | 11.76% | 223.4% | 10.45% | 41.58 |
| no_signal | 11 | 1.48% | 16.2% | 0.14% | 39.73 |
| direction_wrong_loss | 12 | -7.30% | -87.6% | -7.57% | 21.58 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 42 | 3.62% | 152.0% | 57.1% | 57.1% | 2.60% |

**Best-performing regime:** `unknown` — 42 trades, 152.0% total return, 57.1% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 10 | -6.73% | -67.3% |
| ❌ | ✅ | 12 | 13.97% | 167.6% |
| ✅ | ❌ | 2 | -10.11% | -20.2% |
| ✅ | ✅ | 7 | 7.97% | 55.8% |

### Flip Trades (Signal Wrong → Direction Right)

**17 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **13.0%**
- Total return: **221.1%**
- Average alpha: **12.0%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 17 | 13.00% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 42 | 3.62% | 152.0% | 57.1% | 57.1% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 21 | 6.19% | 130.0% | 71.4% | 71.4% |
| SHORT | 21 | 1.05% | 22.0% | 42.9% | 42.9% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 2 | -14.7% | -7.33% | 0.0% | 0.0% | -14.3% |
| 2017 | 6 | 26.1% | 4.35% | 66.7% | 66.7% | 6.1% |
| 2018 | 2 | 13.9% | 6.94% | 50.0% | 50.0% | 17.6% |
| 2019 | 1 | 2.3% | 2.34% | 100.0% | 100.0% | -7.0% |
| 2020 | 8 | 44.7% | 5.59% | 62.5% | 62.5% | 51.7% |
| 2021 | 3 | 5.9% | 1.96% | 66.7% | 66.7% | -3.4% |
| 2022 | 7 | 29.1% | 4.15% | 57.1% | 57.1% | 35.9% |
| 2023 | 4 | 19.9% | 4.98% | 50.0% | 50.0% | 10.1% |
| 2024 | 3 | -7.8% | -2.60% | 33.3% | 33.3% | -17.0% |
| 2025 | 5 | 32.6% | 6.51% | 80.0% | 80.0% | 29.6% |
| 2026 | 1 | 0.0% | 0.00% | 0.0% | 0.0% | 0.0% |

### Macro Context by Year

**2016** (Losing year: -14.7%, 2 trades)
- No major macro events flagged.

**2017** (Strong year: 26.1%, 6 trades)
- No major macro events flagged.

**2018** (Strong year: 13.9%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 2.3%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 44.7%, 8 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 5.9%, 3 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 29.1%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 19.9%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -7.8%, 3 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 32.6%, 5 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Roughly flat: 0.0%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -32.8% cumulative (trade 17 to trade 23)
**Period:** 2020-09-16 to 2022-02-04 (7 trades)
**Peak cumulative return:** 95.4% → **Trough:** 62.6%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-09-16 | 2020-11-09 | 1.0000 | 15.94% | unknown | ✅ |
| 2020-11-10 | 2020-11-11 | 1.0000 | -1.82% | unknown | ❌ |
| 2020-11-11 | 2021-01-13 | -1.0000 | -21.15% | unknown | ❌ |
| 2021-01-14 | 2021-02-04 | -1.0000 | -2.12% | unknown | ❌ |
| 2021-05-07 | 2021-08-06 | -1.0000 | 6.70% | unknown | ✅ |
| 2021-08-06 | 2022-02-04 | 1.0000 | 1.32% | unknown | ✅ |
| 2022-02-04 | 2022-03-22 | -1.0000 | -15.71% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 5 | 3.17% | 15.9% | 40.0% |
| 16-30d | 6 | 10.86% | 65.2% | 83.3% |
| 31-50d | 8 | 3.11% | 24.8% | 50.0% |
| 50d+ | 14 | 4.45% | 62.3% | 71.4% |
| 6-15d | 9 | -1.79% | -16.2% | 33.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 3

## Observations & Caveats

**Sample size:** 42 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (81.4%).
**Win/loss profile:** 57.1% win rate with 2.22× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (58.5%) exceeded signal accuracy (33.3%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2016 (-14.7%, 2 trades). Macro: No flagged events

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.