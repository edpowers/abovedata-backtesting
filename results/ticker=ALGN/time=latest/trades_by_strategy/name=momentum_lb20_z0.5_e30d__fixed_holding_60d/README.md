# Strategy Analysis: momentum_lb20_z0.5_e30d × fixed_holding_60d

**Ticker:** ALGN
**Entry:** `momentum_lb20_z0.5_e30d`
**Exit:** `fixed_holding_60d`
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

- **Exit type:** `fixed_holding_60d`
  - Fixed 60-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 1192.0% |
| **Annualized Return** | 24.3% |
| **Sharpe Ratio** | 0.675 |
| **Max Drawdown** | -66.3% |
| **Total Trades** | 27 |
| **Win Rate** | 74.1% |
| **Signal Accuracy** | 50.0% |
| **Direction Accuracy** | 74.1% |
| **Skill Ratio** | 76.0% |
| **Profit Factor** | 4.58 |
| **Expectancy** | 0.1190 |
| **Tail Ratio** | 1.75 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -19.8% | 1192.0% | 1211.7% |
| Annualized Return | -2.7% | 24.3% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.6×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0585 | Ideal for 27 trades: 0.0370 |
| Top-1 Trade | 14.3% of gross profit | Moderate concentration |
| Top-3 Trades | 34.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 713.0% | Positive without best trade |
| Return ex-Top-3 | 311.9% | Positive without top 3 |
| Max Single Trade | 58.9% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 27 | 11.90% | 321.4% | 74.1% | 74.1% | 11.90% |

**Best-performing regime:** `unknown` — 27 trades, 321.4% total return, 74.1% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 5 | -7.34% | -36.7% |
| ❌ | ✅ | 10 | 24.24% | 242.4% |
| ✅ | ❌ | 1 | -42.22% | -42.2% |
| ✅ | ✅ | 9 | 17.21% | 154.9% |

### Flip Trades (Signal Wrong → Direction Right)

**11 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **23.3%**
- Total return: **256.4%**
- Average alpha: **23.3%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 11 | 23.31% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 27 | 11.90% | 321.4% | 74.1% | 74.1% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 14 | 14.94% | 209.2% | 85.7% | 85.7% |
| SHORT | 13 | 8.63% | 112.2% | 61.5% | 61.5% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2017 | 1 | -15.4% | -15.36% | 0.0% | 0.0% | -15.4% |
| 2018 | 3 | 55.8% | 18.60% | 100.0% | 100.0% | 55.8% |
| 2019 | 4 | 82.5% | 20.63% | 75.0% | 75.0% | 82.5% |
| 2020 | 3 | 4.9% | 1.62% | 66.7% | 66.7% | 4.9% |
| 2021 | 2 | 48.3% | 24.16% | 50.0% | 50.0% | 48.3% |
| 2022 | 2 | 47.1% | 23.56% | 100.0% | 100.0% | 47.1% |
| 2023 | 7 | 61.7% | 8.81% | 85.7% | 85.7% | 61.7% |
| 2024 | 3 | 33.4% | 11.14% | 66.7% | 66.7% | 33.4% |
| 2025 | 2 | 3.1% | 1.53% | 50.0% | 50.0% | 3.1% |

### Macro Context by Year

**2017** (Losing year: -15.4%, 1 trades)
- No major macro events flagged.

**2018** (Strong year: 55.8%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 82.5%, 4 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Modestly positive: 4.9%, 3 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 48.3%, 2 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 47.1%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 61.7%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 33.4%, 3 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 3.1%, 2 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -42.2% cumulative (trade 9 to trade 10)
**Period:** 2020-01-22 to 2020-04-27 (2 trades)
**Peak cumulative return:** 154.2% → **Trough:** 112.0%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-01-22 | 2020-04-24 | -1.0000 | 31.27% | unknown | ✅ |
| 2020-04-27 | 2020-06-09 | -1.0000 | -42.22% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 16-30d | 7 | 4.35% | 30.5% | 71.4% |
| 31-50d | 7 | 12.89% | 90.2% | 85.7% |
| 50d+ | 13 | 15.44% | 200.7% | 69.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 27 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (311.9%).
**Win/loss profile:** 74.1% win rate with 4.58× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (74.1%) exceeded signal accuracy (50.0%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2017 (-15.4%, 1 trades). Macro: No flagged events

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.