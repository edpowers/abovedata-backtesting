# Strategy Analysis: momentum_lb20_z0.5_e20d × trailing_stop_5%

**Ticker:** PCAR
**Entry:** `momentum_lb20_z0.5_e20d`
**Exit:** `trailing_stop_5%`
**Period:** 2020-12-24 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `20` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 69.7% |
| **Annualized Return** | 6.5% |
| **Sharpe Ratio** | 0.680 |
| **Max Drawdown** | -16.7% |
| **Total Trades** | 43 |
| **Win Rate** | 58.1% |
| **Signal Accuracy** | 70.0% |
| **Direction Accuracy** | 58.1% |
| **Skill Ratio** | 55.9% |
| **Profit Factor** | 2.54 |
| **Expectancy** | 0.0134 |
| **Tail Ratio** | 2.28 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 167.2% | 69.7% | -97.5% |
| Annualized Return | 21.3% | 6.5% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.4×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0551 | Ideal for 43 trades: 0.0233 |
| Top-1 Trade | 21.8% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 40.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 40.6% | Positive without best trade |
| Return ex-Top-3 | 19.3% | Positive without top 3 |
| Max Single Trade | 20.7% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 43 | 1.34% | 57.4% | 58.1% | 58.1% | 1.34% |

**Best-performing regime:** `unknown` — 43 trades, 57.4% total return, 58.1% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 10 | -1.58% | -15.8% |
| ❌ | ✅ | 10 | 4.96% | 49.6% |
| ✅ | ❌ | 5 | -1.62% | -8.1% |
| ✅ | ✅ | 9 | 2.25% | 20.2% |

### Flip Trades (Signal Wrong → Direction Right)

**16 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.7%**
- Total return: **74.6%**
- Average alpha: **4.7%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 16 | 4.66% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 43 | 1.34% | 57.4% | 58.1% | 58.1% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 11 | 4.96% | 54.5% | 90.9% | 90.9% |
| SHORT | 32 | 0.09% | 2.9% | 46.9% | 46.9% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 1 | -3.1% | -3.14% | 0.0% | 0.0% | -3.1% |
| 2021 | 7 | 11.1% | 1.58% | 42.9% | 42.9% | 11.1% |
| 2022 | 7 | -1.8% | -0.26% | 42.9% | 42.9% | -1.8% |
| 2023 | 12 | 5.0% | 0.42% | 66.7% | 66.7% | 5.0% |
| 2024 | 5 | 34.4% | 6.89% | 80.0% | 80.0% | 34.4% |
| 2025 | 9 | 3.5% | 0.39% | 55.6% | 55.6% | 3.5% |
| 2026 | 2 | 8.3% | 4.13% | 100.0% | 100.0% | 8.3% |

### Macro Context by Year

**2020** (Roughly flat: -3.1%, 1 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 11.1%, 7 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Roughly flat: -1.8%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 5.0%, 12 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 34.4%, 5 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 3.5%, 9 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 8.3%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -13.4% cumulative (trade 35 to trade 38)
**Period:** 2025-03-31 to 2025-09-23 (4 trades)
**Peak cumulative return:** 55.4% → **Trough:** 41.9%

**Macro context during drawdown:**
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-03-31 | 2025-04-07 | -1.0000 | 9.48% | unknown | ✅ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -8.72% | unknown | ❌ |
| 2025-04-10 | 2025-04-11 | -1.0000 | -1.92% | unknown | ❌ |
| 2025-09-23 | 2025-09-26 | -1.0000 | -2.81% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 17 | -0.08% | -1.3% | 47.1% |
| 16-30d | 6 | 3.50% | 21.0% | 83.3% |
| 31-50d | 2 | 12.33% | 24.7% | 100.0% |
| 6-15d | 18 | 0.73% | 13.1% | 55.6% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 4

## Observations & Caveats

**Sample size:** 43 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (19.3%).
**Win/loss profile:** 58.1% win rate with 2.54× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (70.0%) exceeded direction accuracy (58.1%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2020 (-3.1%, 1 trades). Macro: COVID-19 Crash & Recovery, Post-COVID Stimulus Rally

### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 167.2% buy-and-hold return (aligned to strategy period: None to None), yet 32 short trades returned 2.9% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 10d, std 10d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.