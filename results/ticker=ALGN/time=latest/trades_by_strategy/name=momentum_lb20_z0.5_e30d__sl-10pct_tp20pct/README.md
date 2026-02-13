# Strategy Analysis: momentum_lb20_z0.5_e30d × sl-10%_tp20%

**Ticker:** ALGN
**Entry:** `momentum_lb20_z0.5_e30d`
**Exit:** `sl-10%_tp20%`
**Period:** 2017-12-14 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 1309.1% |
| **Annualized Return** | 22.4% |
| **Sharpe Ratio** | 0.753 |
| **Max Drawdown** | -37.7% |
| **Total Trades** | 50 |
| **Win Rate** | 58.0% |
| **Signal Accuracy** | 52.6% |
| **Direction Accuracy** | 58.0% |
| **Skill Ratio** | 57.4% |
| **Profit Factor** | 3.10 |
| **Expectancy** | 0.0629 |
| **Tail Ratio** | 2.82 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -19.8% | 1309.1% | 1328.8% |
| Annualized Return | -2.7% | 22.4% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0300 | Ideal for 50 trades: 0.0200 |
| Top-1 Trade | 8.3% of gross profit | Moderate concentration |
| Top-3 Trades | 23.7% of gross profit | Moderate concentration |
| Return ex-Top-1 | 915.4% | Positive without best trade |
| Return ex-Top-3 | 451.0% | Positive without top 3 |
| Max Single Trade | 38.8% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 50 | 6.29% | 314.6% | 58.0% | 58.0% | 6.29% |

**Best-performing regime:** `unknown` — 50 trades, 314.6% total return, 58.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 14 | -6.59% | -92.3% |
| ❌ | ✅ | 13 | 17.31% | 225.0% |
| ✅ | ❌ | 6 | -8.36% | -50.2% |
| ✅ | ✅ | 14 | 16.06% | 224.8% |

### Flip Trades (Signal Wrong → Direction Right)

**15 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **16.0%**
- Total return: **240.0%**
- Average alpha: **16.0%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 15 | 16.00% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 50 | 6.29% | 314.6% | 58.0% | 58.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 19 | 8.77% | 166.7% | 73.7% | 73.7% |
| SHORT | 31 | 4.77% | 147.9% | 48.4% | 48.4% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2017 | 1 | -10.5% | -10.53% | 0.0% | 0.0% | -10.5% |
| 2018 | 6 | 20.0% | 3.34% | 50.0% | 50.0% | 20.0% |
| 2019 | 6 | 100.8% | 16.80% | 83.3% | 83.3% | 100.8% |
| 2020 | 7 | 30.6% | 4.37% | 57.1% | 57.1% | 30.6% |
| 2021 | 4 | -4.7% | -1.17% | 25.0% | 25.0% | -4.7% |
| 2022 | 7 | 91.0% | 13.01% | 85.7% | 85.7% | 91.0% |
| 2023 | 11 | 56.3% | 5.12% | 54.5% | 54.5% | 56.3% |
| 2024 | 5 | 23.8% | 4.75% | 40.0% | 40.0% | 23.8% |
| 2025 | 3 | 7.2% | 2.41% | 66.7% | 66.7% | 7.2% |

### Macro Context by Year

**2017** (Losing year: -10.5%, 1 trades)
- No major macro events flagged.

**2018** (Strong year: 20.0%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 100.8%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 30.6%, 7 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Roughly flat: -4.7%, 4 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 91.0%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 56.3%, 11 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 23.8%, 5 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 7.2%, 3 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -33.6% cumulative (trade 15 to trade 23)
**Period:** 2020-02-26 to 2021-12-20 (9 trades)
**Peak cumulative return:** 152.9% → **Trough:** 119.3%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-02-26 | 2020-03-12 | -1.0000 | 20.84% | unknown | ✅ |
| 2020-03-18 | 2020-03-24 | -1.0000 | -13.39% | unknown | ❌ |
| 2020-03-25 | 2020-04-20 | -1.0000 | -7.09% | unknown | ❌ |
| 2020-04-21 | 2020-04-28 | -1.0000 | -8.68% | unknown | ❌ |
| 2020-06-09 | 2020-07-15 | 1.0000 | 12.37% | unknown | ✅ |
| 2020-07-16 | 2020-09-09 | 1.0000 | 4.83% | unknown | ✅ |
| 2021-03-16 | 2021-04-12 | -1.0000 | -10.80% | unknown | ❌ |
| 2021-04-13 | 2021-06-15 | -1.0000 | -0.74% | unknown | ❌ |
| 2021-12-20 | 2021-12-23 | -1.0000 | -10.11% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 8 | -7.12% | -57.0% | 12.5% |
| 16-30d | 12 | 8.04% | 96.5% | 58.3% |
| 31-50d | 14 | 11.60% | 162.4% | 85.7% |
| 50d+ | 3 | -0.46% | -1.4% | 33.3% |
| 6-15d | 13 | 8.77% | 114.0% | 61.5% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 3

## Observations & Caveats

**Sample size:** 50 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (451.0%).
**Win/loss profile:** 58.0% win rate with 3.10× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (58.0%) exceeded signal accuracy (52.6%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2017 (-10.5%, 1 trades). Macro: No flagged events

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.