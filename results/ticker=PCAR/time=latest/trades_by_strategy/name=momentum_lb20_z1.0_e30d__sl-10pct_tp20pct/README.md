# Strategy Analysis: momentum_lb20_z1.0_e30d × sl-10%_tp20%

**Ticker:** PCAR
**Entry:** `momentum_lb20_z1.0_e30d`
**Exit:** `sl-10%_tp20%`
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

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 94.9% |
| **Annualized Return** | 5.5% |
| **Sharpe Ratio** | 0.510 |
| **Max Drawdown** | -23.6% |
| **Total Trades** | 17 |
| **Win Rate** | 58.8% |
| **Signal Accuracy** | 62.5% |
| **Direction Accuracy** | 58.8% |
| **Skill Ratio** | 64.3% |
| **Profit Factor** | 3.09 |
| **Expectancy** | 0.0452 |
| **Tail Ratio** | 1.41 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 170.5% | 94.9% | -75.6% |
| Annualized Return | 21.4% | 5.5% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.6×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0960 | Ideal for 17 trades: 0.0588 |
| Top-1 Trade | 19.9% of gross profit | Moderate concentration |
| Top-3 Trades | 54.8% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 58.9% | Positive without best trade |
| Return ex-Top-3 | 10.6% | Positive without top 3 |
| Max Single Trade | 22.7% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 17 | 4.52% | 76.9% | 58.8% | 58.8% | 4.52% |

**Best-performing regime:** `unknown` — 17 trades, 76.9% total return, 58.8% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 3 | -7.87% | -23.6% |
| ❌ | ✅ | 6 | 9.31% | 55.9% |
| ✅ | ❌ | 2 | -5.57% | -11.1% |
| ✅ | ✅ | 3 | 12.68% | 38.0% |

### Flip Trades (Signal Wrong → Direction Right)

**7 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **10.8%**
- Total return: **75.6%**
- Average alpha: **10.8%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 7 | 10.80% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 17 | 4.52% | 76.9% | 58.8% | 58.8% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 8 | 11.48% | 91.8% | 87.5% | 87.5% |
| SHORT | 9 | -1.66% | -15.0% | 33.3% | 33.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 1 | -16.1% | -16.08% | 0.0% | 0.0% | -16.1% |
| 2021 | 3 | 13.1% | 4.38% | 66.7% | 66.7% | 13.1% |
| 2022 | 4 | -15.8% | -3.94% | 25.0% | 25.0% | -15.8% |
| 2023 | 2 | 31.2% | 15.59% | 100.0% | 100.0% | 31.2% |
| 2024 | 4 | 46.7% | 11.67% | 100.0% | 100.0% | 46.7% |
| 2025 | 2 | 17.8% | 8.89% | 50.0% | 50.0% | 17.8% |
| 2026 | 1 | -0.1% | -0.05% | 0.0% | 0.0% | -0.1% |

### Macro Context by Year

**2020** (Losing year: -16.1%, 1 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 13.1%, 3 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -15.8%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 31.2%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 46.7%, 4 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 17.8%, 2 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Roughly flat: -0.1%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -17.7% cumulative (trade 5 to trade 8)
**Period:** 2022-03-14 to 2022-11-11 (4 trades)
**Peak cumulative return:** -1.0% → **Trough:** -18.7%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-03-14 | 2022-06-10 | -1.0000 | 1.97% | unknown | ✅ |
| 2022-09-13 | 2022-10-25 | -1.0000 | -6.60% | unknown | ❌ |
| 2022-10-26 | 2022-11-10 | -1.0000 | -9.82% | unknown | ❌ |
| 2022-11-11 | 2022-12-08 | -1.0000 | -1.33% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 2 | -1.02% | -2.0% | 0.0% |
| 16-30d | 5 | -2.47% | -12.3% | 40.0% |
| 31-50d | 3 | 13.83% | 41.5% | 66.7% |
| 50d+ | 6 | 9.93% | 59.6% | 100.0% |
| 6-15d | 1 | -9.82% | -9.8% | 0.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 3

## Observations & Caveats

**Sample size:** ⚠️ Only 17 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (10.6%).
**Win/loss profile:** 58.8% win rate with 3.09× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (62.5%) exceeded direction accuracy (58.8%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2020 (-16.1%, 1 trades). Macro: COVID-19 Crash & Recovery, Post-COVID Stimulus Rally

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.