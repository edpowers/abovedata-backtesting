# Strategy Analysis: momentum_lb10_z0.5_e15d × trailing_stop_5%

**Ticker:** ALGN
**Entry:** `momentum_lb10_z0.5_e15d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-01-08 to 2026-02-05
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `10`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 15.3% |
| **Annualized Return** | 13.9% |
| **Sharpe Ratio** | 1.127 |
| **Max Drawdown** | -11.8% |
| **Total Trades** | 75 |
| **Win Rate** | 44.0% |
| **Signal Accuracy** | 64.3% |
| **Direction Accuracy** | 44.0% |
| **Skill Ratio** | 47.6% |
| **Profit Factor** | 1.22 |
| **Expectancy** | 0.0052 |
| **Tail Ratio** | 1.40 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -29.4% | 15.3% | 44.7% |
| Annualized Return | -4.2% | 13.9% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0331 | Ideal for 75 trades: 0.0133 |
| Top-1 Trade | 16.6% of gross profit | Moderate concentration |
| Top-3 Trades | 37.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | -14.8% | Negative without best trade |
| Return ex-Top-3 | -43.2% | Negative without top 3 |
| Max Single Trade | 35.4% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 75 | 0.52% | 38.7% | 44.0% | 44.0% | 0.52% |

**Best-performing regime:** `unknown` — 75 trades, 38.7% total return, 44.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 17 | -3.20% | -54.4% |
| ❌ | ✅ | 19 | 7.82% | 148.6% |
| ✅ | ❌ | 16 | -2.62% | -42.0% |
| ✅ | ✅ | 11 | 4.82% | 53.1% |

### Flip Trades (Signal Wrong → Direction Right)

**22 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **7.3%**
- Total return: **160.1%**
- Average alpha: **7.3%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 22 | 7.28% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 75 | 0.52% | 38.7% | 44.0% | 44.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 33 | 1.17% | 38.7% | 51.5% | 51.5% |
| SHORT | 42 | -0.00% | -0.0% | 38.1% | 38.1% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 12 | -0.2% | -0.02% | 41.7% | 41.7% | -0.2% |
| 2019 | 12 | 68.2% | 5.68% | 58.3% | 58.3% | 68.2% |
| 2020 | 9 | -15.9% | -1.77% | 22.2% | 22.2% | -15.9% |
| 2021 | 6 | 9.9% | 1.66% | 33.3% | 33.3% | 9.9% |
| 2022 | 6 | 11.6% | 1.94% | 50.0% | 50.0% | 11.6% |
| 2023 | 9 | 15.0% | 1.67% | 55.6% | 55.6% | 15.0% |
| 2024 | 9 | 16.6% | 1.85% | 66.7% | 66.7% | 16.6% |
| 2025 | 9 | -59.3% | -6.59% | 22.2% | 22.2% | -59.3% |
| 2026 | 3 | -7.4% | -2.46% | 33.3% | 33.3% | -7.4% |

### Macro Context by Year

**2018** (Roughly flat: -0.2%, 12 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 68.2%, 12 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Losing year: -15.9%, 9 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 9.9%, 6 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 11.6%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 15.0%, 9 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 16.6%, 9 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -59.3%, 9 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -7.4%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -66.7% cumulative (trade 63 to trade 75)
**Period:** 2024-10-30 to 2026-02-04 (13 trades)
**Peak cumulative return:** 105.3% → **Trough:** 38.7%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-10-30 | 2024-11-04 | -1.0000 | 0.04% | unknown | ✅ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -14.35% | unknown | ❌ |
| 2025-04-10 | 2025-04-11 | -1.0000 | -2.50% | unknown | ❌ |
| 2025-04-14 | 2025-04-17 | -1.0000 | -3.50% | unknown | ❌ |
| 2025-07-09 | 2025-07-10 | 1.0000 | 2.00% | unknown | ✅ |
| 2025-07-11 | 2025-07-15 | 1.0000 | -4.68% | unknown | ❌ |
| 2025-07-16 | 2025-07-31 | 1.0000 | -32.19% | unknown | ❌ |
| 2025-10-08 | 2025-10-10 | 1.0000 | -5.49% | unknown | ❌ |
| 2025-10-13 | 2025-10-29 | 1.0000 | 1.83% | unknown | ✅ |
| 2025-10-30 | 2025-10-31 | 1.0000 | -0.40% | unknown | ❌ |
| 2026-01-02 | 2026-01-20 | -1.0000 | -6.10% | unknown | ❌ |
| 2026-01-21 | 2026-02-03 | -1.0000 | 7.59% | unknown | ✅ |
| 2026-02-04 | 2026-02-05 | -1.0000 | -8.88% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 64 | -0.63% | -40.5% | 37.5% |
| 16-30d | 2 | 9.23% | 18.5% | 100.0% |
| 6-15d | 9 | 6.75% | 60.7% | 77.8% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 7

## Observations & Caveats

**Sample size:** 75 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-43.2%).
**Win/loss profile:** Profit factor of 1.22 with 44.0% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (64.3%) exceeded direction accuracy (44.0%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2025 (-59.3%, 9 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 3d, std 4d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.