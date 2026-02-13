# Strategy Analysis: momentum_lb20_z0.5_e30d × signal_change

**Ticker:** ALGN
**Entry:** `momentum_lb20_z0.5_e30d`
**Exit:** `signal_change`
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

- **Exit type:** `signal_change`
  - Exit when the UCC signal reverses direction. Fundamentally-driven exit that stays in the trade as long as the thesis holds

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 1462.7% |
| **Annualized Return** | 24.6% |
| **Sharpe Ratio** | 0.682 |
| **Max Drawdown** | -67.0% |
| **Total Trades** | 19 |
| **Win Rate** | 73.7% |
| **Signal Accuracy** | 46.2% |
| **Direction Accuracy** | 73.7% |
| **Skill Ratio** | 76.5% |
| **Profit Factor** | 8.14 |
| **Expectancy** | 0.1773 |
| **Tail Ratio** | 4.03 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -19.8% | 1462.7% | 1482.4% |
| Annualized Return | -2.7% | 24.6% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.6×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0856 | Ideal for 19 trades: 0.0526 |
| Top-1 Trade | 16.1% of gross profit | Moderate concentration |
| Top-3 Trades | 43.9% of gross profit | Moderate concentration |
| Return ex-Top-1 | 865.6% | Positive without best trade |
| Return ex-Top-3 | 310.6% | Positive without top 3 |
| Max Single Trade | 61.8% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 19 | 17.73% | 336.8% | 73.7% | 73.7% | 17.73% |

**Best-performing regime:** `unknown` — 19 trades, 336.8% total return, 73.7% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 4 | -9.06% | -36.2% |
| ❌ | ✅ | 7 | 30.33% | 212.3% |
| ✅ | ✅ | 6 | 26.29% | 157.7% |

### Flip Trades (Signal Wrong → Direction Right)

**8 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **28.3%**
- Total return: **226.3%**
- Average alpha: **28.3%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 8 | 28.28% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 19 | 17.73% | 336.8% | 73.7% | 73.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 9 | 24.10% | 216.9% | 88.9% | 88.9% |
| SHORT | 10 | 11.99% | 119.9% | 60.0% | 60.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2017 | 1 | -15.4% | -15.36% | 0.0% | 0.0% | -15.4% |
| 2018 | 2 | 57.0% | 28.52% | 100.0% | 100.0% | 57.0% |
| 2019 | 3 | 84.7% | 28.22% | 66.7% | 66.7% | 84.7% |
| 2020 | 1 | 15.8% | 15.81% | 100.0% | 100.0% | 15.8% |
| 2021 | 2 | 48.3% | 24.16% | 50.0% | 50.0% | 48.3% |
| 2022 | 2 | 81.5% | 40.75% | 100.0% | 100.0% | 81.5% |
| 2023 | 4 | 49.3% | 12.32% | 100.0% | 100.0% | 49.3% |
| 2024 | 2 | 12.6% | 6.28% | 50.0% | 50.0% | 12.6% |
| 2025 | 2 | 3.1% | 1.53% | 50.0% | 50.0% | 3.1% |

### Macro Context by Year

**2017** (Losing year: -15.4%, 1 trades)
- No major macro events flagged.

**2018** (Strong year: 57.0%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 84.7%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 15.8%, 1 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 48.3%, 2 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 81.5%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 49.3%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 12.6%, 2 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 3.1%, 2 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -16.1% cumulative (trade 16 to trade 18)
**Period:** 2024-03-12 to 2025-03-18 (3 trades)
**Peak cumulative return:** 338.9% → **Trough:** 322.9%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-03-12 | 2024-06-10 | -1.0000 | 17.70% | unknown | ✅ |
| 2024-09-11 | 2024-12-19 | 1.0000 | -5.14% | unknown | ❌ |
| 2025-03-18 | 2025-06-16 | -1.0000 | -10.93% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 31-50d | 1 | 13.99% | 14.0% | 100.0% |
| 50d+ | 18 | 17.94% | 322.9% | 72.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 8
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 19 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (310.6%).
**Win/loss profile:** 73.7% win rate with 8.14× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (73.7%) exceeded signal accuracy (46.2%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2017 (-15.4%, 1 trades). Macro: No flagged events

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.