# Strategy Analysis: momentum_lb10_z0.5_e15d × trailing_stop_10%

**Ticker:** ALGN
**Entry:** `momentum_lb10_z0.5_e15d`
**Exit:** `trailing_stop_10%`
**Period:** 2018-01-08 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `10`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_10%`
  - 10% trailing stop. More room for normal volatility, targets larger trends

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 68.1% |
| **Annualized Return** | 27.5% |
| **Sharpe Ratio** | 1.171 |
| **Max Drawdown** | -30.4% |
| **Total Trades** | 73 |
| **Win Rate** | 49.3% |
| **Signal Accuracy** | 48.8% |
| **Direction Accuracy** | 50.0% |
| **Skill Ratio** | 52.5% |
| **Profit Factor** | 1.43 |
| **Expectancy** | 0.0155 |
| **Tail Ratio** | 1.67 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -24.6% | 68.1% | 92.7% |
| Annualized Return | -3.4% | 27.5% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0313 | Ideal for 73 trades: 0.0137 |
| Top-1 Trade | 11.1% of gross profit | Moderate concentration |
| Top-3 Trades | 31.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 18.9% | Positive without best trade |
| Return ex-Top-3 | -38.3% | Negative without top 3 |
| Max Single Trade | 41.4% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 73 | 1.55% | 113.3% | 49.3% | 49.3% | 1.55% |

**Best-performing regime:** `unknown` — 73 trades, 113.3% total return, 49.3% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 18 | -5.65% | -101.8% |
| ❌ | ✅ | 22 | 10.84% | 238.4% |
| ✅ | ❌ | 11 | -7.70% | -84.7% |
| ✅ | ✅ | 10 | 11.32% | 113.2% |

### Flip Trades (Signal Wrong → Direction Right)

**26 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **10.0%**
- Total return: **261.2%**
- Average alpha: **10.0%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 26 | 10.05% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 73 | 1.55% | 113.3% | 49.3% | 49.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 32 | 3.48% | 111.4% | 65.6% | 65.6% |
| SHORT | 41 | 0.05% | 1.8% | 36.6% | 36.6% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 11 | 10.6% | 0.97% | 27.3% | 27.3% | 10.6% |
| 2019 | 11 | 94.0% | 8.54% | 72.7% | 72.7% | 94.0% |
| 2020 | 9 | -47.6% | -5.29% | 44.4% | 44.4% | -47.6% |
| 2021 | 6 | 15.5% | 2.58% | 66.7% | 66.7% | 15.5% |
| 2022 | 6 | 12.9% | 2.14% | 66.7% | 66.7% | 12.9% |
| 2023 | 9 | 68.2% | 7.57% | 55.6% | 55.6% | 68.2% |
| 2024 | 9 | 11.5% | 1.28% | 44.4% | 44.4% | 11.5% |
| 2025 | 9 | -42.2% | -4.69% | 44.4% | 44.4% | -42.2% |
| 2026 | 3 | -9.5% | -3.18% | 0.0% | 0.0% | -9.5% |

### Macro Context by Year

**2018** (Strong year: 10.6%, 11 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 94.0%, 11 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Losing year: -47.6%, 9 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 15.5%, 6 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 12.9%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 68.2%, 9 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 11.5%, 9 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -42.2%, 9 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -9.5%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -72.8% cumulative (trade 56 to trade 69)
**Period:** 2024-07-02 to 2025-11-03 (14 trades)
**Peak cumulative return:** 178.9% → **Trough:** 106.1%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-07-02 | 2024-07-11 | 1.0000 | 6.91% | unknown | ✅ |
| 2024-07-12 | 2024-07-25 | 1.0000 | -6.84% | unknown | ❌ |
| 2024-07-26 | 2024-08-02 | 1.0000 | -3.16% | unknown | ❌ |
| 2024-10-03 | 2024-10-24 | -1.0000 | 8.67% | unknown | ✅ |
| 2024-10-25 | 2024-11-11 | -1.0000 | -2.71% | unknown | ❌ |
| 2024-11-12 | 2024-11-25 | -1.0000 | -9.78% | unknown | ❌ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -14.35% | unknown | ❌ |
| 2025-04-10 | 2025-04-17 | -1.0000 | -7.04% | unknown | ❌ |
| 2025-04-21 | 2025-04-23 | -1.0000 | -2.91% | unknown | ❌ |
| 2025-07-09 | 2025-07-10 | 1.0000 | 2.00% | unknown | ✅ |
| 2025-07-11 | 2025-07-31 | 1.0000 | -36.22% | unknown | ❌ |
| 2025-08-01 | 2025-09-02 | 1.0000 | 0.47% | unknown | ✅ |
| 2025-10-08 | 2025-10-31 | 1.0000 | 3.60% | unknown | ✅ |
| 2025-11-03 | 2025-11-18 | 1.0000 | -4.51% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 22 | -5.15% | -113.4% | 22.7% |
| 16-30d | 17 | 7.70% | 130.9% | 70.6% |
| 31-50d | 5 | 14.55% | 72.7% | 100.0% |
| 50d+ | 1 | 41.42% | 41.4% | 100.0% |
| 6-15d | 28 | -0.66% | -18.4% | 46.4% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 7

## Observations & Caveats

**Sample size:** 73 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-38.3%).
**Win/loss profile:** Profit factor of 1.43 with 49.3% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (48.8%) and direction accuracy (50.0%) are similar, suggesting the correlation flip had limited net impact in this sample.

### Known Vulnerabilities

- **Worst year:** 2020 (-47.6%, 9 trades). Macro: COVID-19 Crash & Recovery, Post-COVID Stimulus Rally

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 13d, std 11d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.