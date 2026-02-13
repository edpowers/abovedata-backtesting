# Strategy Analysis: momentum_lb20_z0.5_e30d × trailing_stop_10%

**Ticker:** ALGN
**Entry:** `momentum_lb20_z0.5_e30d`
**Exit:** `trailing_stop_10%`
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

- **Exit type:** `trailing_stop_10%`
  - 10% trailing stop. More room for normal volatility, targets larger trends

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 1061.5% |
| **Annualized Return** | 31.3% |
| **Sharpe Ratio** | 1.248 |
| **Max Drawdown** | -38.0% |
| **Total Trades** | 63 |
| **Win Rate** | 54.0% |
| **Signal Accuracy** | 48.9% |
| **Direction Accuracy** | 54.0% |
| **Skill Ratio** | 55.2% |
| **Profit Factor** | 2.92 |
| **Expectancy** | 0.0482 |
| **Tail Ratio** | 4.03 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -19.8% | 1061.5% | 1081.2% |
| Annualized Return | -2.7% | 31.3% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0370 | Ideal for 63 trades: 0.0159 |
| Top-1 Trade | 13.4% of gross profit | Moderate concentration |
| Top-3 Trades | 31.3% of gross profit | Moderate concentration |
| Return ex-Top-1 | 616.3% | Positive without best trade |
| Return ex-Top-3 | 259.5% | Positive without top 3 |
| Max Single Trade | 62.1% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 63 | 4.82% | 303.7% | 54.0% | 54.0% | 4.82% |

**Best-performing regime:** `unknown` — 63 trades, 303.7% total return, 54.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 17 | -4.97% | -84.5% |
| ❌ | ✅ | 19 | 12.83% | 243.8% |
| ✅ | ❌ | 9 | -5.33% | -47.9% |
| ✅ | ✅ | 13 | 15.02% | 195.2% |

### Flip Trades (Signal Wrong → Direction Right)

**21 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **12.7%**
- Total return: **266.9%**
- Average alpha: **12.7%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 21 | 12.71% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 63 | 4.82% | 303.7% | 54.0% | 54.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 27 | 7.82% | 211.2% | 63.0% | 63.0% |
| SHORT | 36 | 2.57% | 92.5% | 47.2% | 47.2% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2017 | 1 | 0.2% | 0.21% | 100.0% | 100.0% | 0.2% |
| 2018 | 9 | 13.5% | 1.50% | 33.3% | 33.3% | 13.5% |
| 2019 | 7 | 102.7% | 14.68% | 71.4% | 71.4% | 102.7% |
| 2020 | 8 | 21.1% | 2.64% | 62.5% | 62.5% | 21.1% |
| 2021 | 5 | 7.1% | 1.42% | 20.0% | 20.0% | 7.1% |
| 2022 | 8 | 69.1% | 8.64% | 50.0% | 50.0% | 69.1% |
| 2023 | 12 | 62.6% | 5.22% | 75.0% | 75.0% | 62.6% |
| 2024 | 8 | 30.3% | 3.78% | 50.0% | 50.0% | 30.3% |
| 2025 | 4 | -19.2% | -4.79% | 25.0% | 25.0% | -19.2% |
| 2026 | 1 | 16.3% | 16.31% | 100.0% | 100.0% | 16.3% |

### Macro Context by Year

**2017** (Modestly positive: 0.2%, 1 trades)
- No major macro events flagged.

**2018** (Strong year: 13.5%, 9 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 102.7%, 7 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 21.1%, 8 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 7.1%, 5 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 69.1%, 8 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 62.6%, 12 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 30.3%, 8 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -19.2%, 4 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 16.3%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -29.3% cumulative (trade 56 to trade 62)
**Period:** 2024-09-11 to 2025-12-10 (7 trades)
**Peak cumulative return:** 316.8% → **Trough:** 287.4%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-09-11 | 2024-10-02 | 1.0000 | 5.73% | unknown | ✅ |
| 2024-10-03 | 2024-10-11 | 1.0000 | -6.30% | unknown | ❌ |
| 2024-10-14 | 2024-12-18 | 1.0000 | -3.88% | unknown | ❌ |
| 2025-03-18 | 2025-04-07 | -1.0000 | 6.80% | unknown | ✅ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -14.35% | unknown | ❌ |
| 2025-04-10 | 2025-04-17 | -1.0000 | -7.04% | unknown | ❌ |
| 2025-12-10 | 2026-02-03 | 1.0000 | -4.58% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 19 | -4.13% | -78.4% | 21.1% |
| 16-30d | 17 | 10.35% | 175.9% | 82.4% |
| 31-50d | 5 | 18.47% | 92.4% | 60.0% |
| 50d+ | 1 | 44.68% | 44.7% | 100.0% |
| 6-15d | 21 | 3.30% | 69.2% | 57.1% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 5

## Observations & Caveats

**Sample size:** 63 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (259.5%).
**Win/loss profile:** 54.0% win rate with 2.92× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (54.0%) exceeded signal accuracy (48.9%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2025 (-19.2%, 4 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 14d, std 12d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.