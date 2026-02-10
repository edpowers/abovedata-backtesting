# Strategy Analysis: momentum_lb20_z1.0_e30d × sl-5%_tp10%

**Ticker:** PCAR
**Entry:** `momentum_lb20_z1.0_e30d`
**Exit:** `sl-5%_tp10%`
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

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit targets a 2:1 reward/risk ratio

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 96.0% |
| **Annualized Return** | 4.5% |
| **Sharpe Ratio** | 0.428 |
| **Max Drawdown** | -16.8% |
| **Total Trades** | 26 |
| **Win Rate** | 53.8% |
| **Signal Accuracy** | 58.3% |
| **Direction Accuracy** | 53.8% |
| **Skill Ratio** | 52.2% |
| **Profit Factor** | 3.04 |
| **Expectancy** | 0.0280 |
| **Tail Ratio** | 2.43 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 170.5% | 96.0% | -74.5% |
| Annualized Return | 21.4% | 4.5% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.4×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0555 | Ideal for 26 trades: 0.0385 |
| Top-1 Trade | 11.9% of gross profit | Moderate concentration |
| Top-3 Trades | 32.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 73.5% | Positive without best trade |
| Return ex-Top-3 | 40.0% | Positive without top 3 |
| Max Single Trade | 12.9% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 26 | 2.80% | 72.8% | 53.8% | 53.8% | 2.80% |

**Best-performing regime:** `unknown` — 26 trades, 72.8% total return, 53.8% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 7 | -2.96% | -20.7% |
| ❌ | ✅ | 9 | 6.31% | 56.8% |
| ✅ | ❌ | 4 | -3.47% | -13.9% |
| ✅ | ✅ | 3 | 10.63% | 31.9% |

### Flip Trades (Signal Wrong → Direction Right)

**11 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **7.0%**
- Total return: **76.6%**
- Average alpha: **7.0%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 11 | 6.96% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 26 | 2.80% | 72.8% | 53.8% | 53.8% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 13 | 6.53% | 84.9% | 84.6% | 84.6% |
| SHORT | 13 | -0.93% | -12.2% | 23.1% | 23.1% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 1 | -4.4% | -4.41% | 0.0% | 0.0% | -4.4% |
| 2021 | 7 | 7.8% | 1.11% | 42.9% | 42.9% | 7.8% |
| 2022 | 4 | -10.4% | -2.60% | 25.0% | 25.0% | -10.4% |
| 2023 | 3 | 20.2% | 6.74% | 100.0% | 100.0% | 20.2% |
| 2024 | 7 | 43.1% | 6.16% | 71.4% | 71.4% | 43.1% |
| 2025 | 2 | 6.7% | 3.33% | 50.0% | 50.0% | 6.7% |
| 2026 | 2 | 9.8% | 4.91% | 50.0% | 50.0% | 9.8% |

### Macro Context by Year

**2020** (Roughly flat: -4.4%, 1 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 7.8%, 7 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -10.4%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 20.2%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 43.1%, 7 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 6.7%, 2 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 9.8%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -12.4% cumulative (trade 9 to trade 12)
**Period:** 2022-03-14 to 2022-10-26 (4 trades)
**Peak cumulative return:** 5.3% → **Trough:** -7.0%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-03-14 | 2022-06-10 | -1.0000 | 1.97% | unknown | ✅ |
| 2022-09-13 | 2022-10-05 | -1.0000 | -5.64% | unknown | ❌ |
| 2022-10-06 | 2022-10-25 | -1.0000 | -2.27% | unknown | ❌ |
| 2022-10-26 | 2022-11-01 | -1.0000 | -4.47% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 3 | -2.43% | -7.3% | 0.0% |
| 16-30d | 8 | 3.94% | 31.6% | 62.5% |
| 31-50d | 6 | 3.53% | 21.2% | 66.7% |
| 50d+ | 1 | 1.97% | 2.0% | 100.0% |
| 6-15d | 8 | 3.17% | 25.3% | 50.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 3

## Observations & Caveats

**Sample size:** ⚠️ Only 26 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Well-distributed. HHI of 0.0555 is near the theoretical minimum of 0.0385 for 26 trades.
**Win/loss profile:** 53.8% win rate with 3.04× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (58.3%) exceeded direction accuracy (53.8%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2022 (-10.4%, 4 trades). Macro: Fed Tightening Cycle, 2022 Bear Market

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.