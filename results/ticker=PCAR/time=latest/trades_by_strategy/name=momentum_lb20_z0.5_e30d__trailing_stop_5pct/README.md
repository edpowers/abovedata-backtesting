# Strategy Analysis: momentum_lb20_z0.5_e30d × trailing_stop_5%

**Ticker:** PCAR
**Entry:** `momentum_lb20_z0.5_e30d`
**Exit:** `trailing_stop_5%`
**Period:** 2020-12-10 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 132.3% |
| **Annualized Return** | 8.7% |
| **Sharpe Ratio** | 0.852 |
| **Max Drawdown** | -20.1% |
| **Total Trades** | 48 |
| **Win Rate** | 62.5% |
| **Signal Accuracy** | 57.9% |
| **Direction Accuracy** | 62.5% |
| **Skill Ratio** | 60.0% |
| **Profit Factor** | 3.16 |
| **Expectancy** | 0.0192 |
| **Tail Ratio** | 3.18 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 170.5% | 132.3% | -38.3% |
| Annualized Return | 21.4% | 8.7% | — |

## Diversity & Concentration

Diversification: **Somewhat concentrated** — noticeable dependence on top trades (HHI ratio: 2.6×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0543 | Ideal for 48 trades: 0.0208 |
| Top-1 Trade | 21.5% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 39.7% of gross profit | Moderate concentration |
| Return ex-Top-1 | 80.0% | Positive without best trade |
| Return ex-Top-3 | 43.0% | Positive without top 3 |
| Max Single Trade | 29.0% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 24 | 4.19% | 100.6% | 4.19% | 13.71 |
| no_signal | 8 | 2.92% | 23.4% | 2.92% | 10.38 |
| direction_wrong_loss | 16 | -2.00% | -32.0% | -2.00% | 5.56 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 48 | 1.92% | 92.0% | 62.5% | 62.5% | 1.92% |

**Best-performing regime:** `unknown` — 48 trades, 92.0% total return, 62.5% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 13 | -2.25% | -29.2% |
| ❌ | ✅ | 16 | 4.29% | 68.6% |
| ✅ | ❌ | 3 | -0.91% | -2.7% |
| ✅ | ✅ | 8 | 3.99% | 31.9% |

### Flip Trades (Signal Wrong → Direction Right)

**22 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.7%**
- Total return: **102.6%**
- Average alpha: **4.7%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 22 | 4.67% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 48 | 1.92% | 92.0% | 62.5% | 62.5% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 21 | 4.02% | 84.3% | 81.0% | 81.0% |
| SHORT | 27 | 0.28% | 7.6% | 48.1% | 48.1% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 1 | -4.4% | -4.41% | 0.0% | 0.0% | -4.4% |
| 2021 | 11 | 6.5% | 0.59% | 54.5% | 54.5% | 6.5% |
| 2022 | 9 | -1.8% | -0.20% | 55.6% | 55.6% | -1.8% |
| 2023 | 10 | 16.1% | 1.61% | 70.0% | 70.0% | 16.1% |
| 2024 | 8 | 52.8% | 6.59% | 75.0% | 75.0% | 52.8% |
| 2025 | 8 | 19.3% | 2.42% | 62.5% | 62.5% | 19.3% |
| 2026 | 1 | 3.5% | 3.49% | 100.0% | 100.0% | 3.5% |

### Macro Context by Year

**2020** (Roughly flat: -4.4%, 1 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 6.5%, 11 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Roughly flat: -1.8%, 9 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 16.1%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 52.8%, 8 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 19.3%, 8 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 3.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -10.6% cumulative (trade 41 to trade 43)
**Period:** 2025-03-18 to 2025-04-10 (3 trades)
**Peak cumulative return:** 80.6% → **Trough:** 70.0%

**Macro context during drawdown:**
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-03-18 | 2025-04-07 | -1.0000 | 12.04% | unknown | ✅ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -8.72% | unknown | ❌ |
| 2025-04-10 | 2025-04-11 | -1.0000 | -1.92% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 21 | -0.81% | -17.0% | 38.1% |
| 16-30d | 6 | 3.34% | 20.0% | 83.3% |
| 31-50d | 2 | 8.16% | 16.3% | 100.0% |
| 50d+ | 1 | 29.00% | 29.0% | 100.0% |
| 6-15d | 18 | 2.43% | 43.7% | 77.8% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 3

## Observations & Caveats

**Sample size:** 48 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (43.0%).
**Win/loss profile:** 62.5% win rate with 3.16× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (62.5%) exceeded signal accuracy (57.9%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2020 (-4.4%, 1 trades). Macro: COVID-19 Crash & Recovery, Post-COVID Stimulus Rally

### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 170.5% buy-and-hold return (aligned to strategy period: None to None), yet 27 short trades returned 7.6% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 10d, std 11d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.