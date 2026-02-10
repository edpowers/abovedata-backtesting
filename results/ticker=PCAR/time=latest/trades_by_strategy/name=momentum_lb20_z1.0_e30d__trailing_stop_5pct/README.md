# Strategy Analysis: momentum_lb20_z1.0_e30d × trailing_stop_5%

**Ticker:** PCAR
**Entry:** `momentum_lb20_z1.0_e30d`
**Exit:** `trailing_stop_5%`
**Period:** 2020-12-10 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `1.0`
- **zscore_window:** `60`
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 116.8% |
| **Annualized Return** | 7.7% |
| **Sharpe Ratio** | 0.912 |
| **Max Drawdown** | -13.2% |
| **Total Trades** | 28 |
| **Win Rate** | 64.3% |
| **Signal Accuracy** | 63.6% |
| **Direction Accuracy** | 64.3% |
| **Skill Ratio** | 61.5% |
| **Profit Factor** | 5.12 |
| **Expectancy** | 0.0299 |
| **Tail Ratio** | 5.14 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 170.5% | 116.8% | -53.7% |
| Annualized Return | 21.4% | 7.7% | — |

## Diversity & Concentration

Diversification: **Somewhat concentrated** — noticeable dependence on top trades (HHI ratio: 2.6×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0912 | Ideal for 28 trades: 0.0357 |
| Top-1 Trade | 27.8% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 50.1% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 68.2% | Positive without best trade |
| Return ex-Top-3 | 35.1% | Positive without top 3 |
| Max Single Trade | 28.9% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 28 | 2.99% | 83.6% | 64.3% | 64.3% | 2.99% |

**Best-performing regime:** `unknown` — 28 trades, 83.6% total return, 64.3% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 8 | -2.24% | -17.9% |
| ❌ | ✅ | 11 | 5.48% | 60.3% |
| ✅ | ❌ | 2 | -1.17% | -2.3% |
| ✅ | ✅ | 5 | 5.55% | 27.8% |

### Flip Trades (Signal Wrong → Direction Right)

**13 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.9%**
- Total return: **76.2%**
- Average alpha: **5.9%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 13 | 5.86% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 28 | 2.99% | 83.6% | 64.3% | 64.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 13 | 6.14% | 79.8% | 84.6% | 84.6% |
| SHORT | 15 | 0.25% | 3.8% | 46.7% | 46.7% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 1 | -4.4% | -4.41% | 0.0% | 0.0% | -4.4% |
| 2021 | 8 | 8.4% | 1.05% | 62.5% | 62.5% | 8.4% |
| 2022 | 6 | -3.4% | -0.56% | 33.3% | 33.3% | -3.4% |
| 2023 | 4 | 11.1% | 2.77% | 75.0% | 75.0% | 11.1% |
| 2024 | 6 | 56.7% | 9.45% | 100.0% | 100.0% | 56.7% |
| 2025 | 2 | 11.8% | 5.88% | 50.0% | 50.0% | 11.8% |
| 2026 | 1 | 3.5% | 3.49% | 100.0% | 100.0% | 3.5% |

### Macro Context by Year

**2020** (Roughly flat: -4.4%, 1 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 8.4%, 8 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Roughly flat: -3.4%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 11.1%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 56.7%, 6 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 11.8%, 2 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 3.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -5.3% cumulative (trade 11 to trade 15)
**Period:** 2022-03-17 to 2022-10-07 (5 trades)
**Peak cumulative return:** 6.0% → **Trough:** 0.6%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-03-17 | 2022-04-01 | -1.0000 | 5.59% | unknown | ✅ |
| 2022-04-04 | 2022-04-19 | -1.0000 | -1.64% | unknown | ❌ |
| 2022-09-13 | 2022-10-03 | -1.0000 | -0.49% | unknown | ❌ |
| 2022-10-04 | 2022-10-06 | -1.0000 | 0.23% | unknown | ✅ |
| 2022-10-07 | 2022-10-18 | -1.0000 | -3.44% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 7 | -0.54% | -3.8% | 42.9% |
| 16-30d | 7 | 3.29% | 23.0% | 71.4% |
| 31-50d | 3 | 15.07% | 45.2% | 100.0% |
| 6-15d | 11 | 1.74% | 19.1% | 63.6% |

## Win/Loss Streaks

- **Max consecutive wins:** 7
- **Max consecutive losses:** 3

## Observations & Caveats

**Sample size:** ⚠️ Only 28 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (35.1%).
**Win/loss profile:** 64.3% win rate with 5.12× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (63.6%) and direction accuracy (64.3%) are similar, suggesting the correlation flip had limited net impact in this sample.

### Known Vulnerabilities

- **Worst year:** 2020 (-4.4%, 1 trades). Macro: COVID-19 Crash & Recovery, Post-COVID Stimulus Rally

### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 170.5% buy-and-hold return (aligned to strategy period: None to None), yet 15 short trades returned 3.8% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 14d, std 12d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.