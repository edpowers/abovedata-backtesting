# Strategy Analysis: momentum_lb20_z1.0_e30d × fixed_holding_30d

**Ticker:** PCAR
**Entry:** `momentum_lb20_z1.0_e30d`
**Exit:** `fixed_holding_30d`
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

- **Exit type:** `fixed_holding_30d`
  - Fixed 30-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 74.1% |
| **Annualized Return** | 5.1% |
| **Sharpe Ratio** | 0.449 |
| **Max Drawdown** | -24.7% |
| **Total Trades** | 21 |
| **Win Rate** | 66.7% |
| **Signal Accuracy** | 62.5% |
| **Direction Accuracy** | 66.7% |
| **Skill Ratio** | 66.7% |
| **Profit Factor** | 2.47 |
| **Expectancy** | 0.0320 |
| **Tail Ratio** | 1.42 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 170.5% | 74.1% | -96.5% |
| Annualized Return | 21.4% | 5.1% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.1×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0976 | Ideal for 21 trades: 0.0476 |
| Top-1 Trade | 22.6% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 57.0% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 38.7% | Positive without best trade |
| Return ex-Top-3 | -2.4% | Negative without top 3 |
| Max Single Trade | 25.5% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 21 | 3.20% | 67.1% | 66.7% | 66.7% | 3.20% |

**Best-performing regime:** `unknown` — 21 trades, 67.1% total return, 66.7% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 5 | -8.27% | -41.3% |
| ❌ | ✅ | 8 | 7.21% | 57.7% |
| ✅ | ❌ | 1 | -1.50% | -1.5% |
| ✅ | ✅ | 4 | 9.34% | 37.3% |

### Flip Trades (Signal Wrong → Direction Right)

**10 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **7.5%**
- Total return: **75.4%**
- Average alpha: **7.5%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 10 | 7.54% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 21 | 3.20% | 67.1% | 66.7% | 66.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 11 | 8.14% | 89.5% | 90.9% | 90.9% |
| SHORT | 10 | -2.24% | -22.4% | 40.0% | 40.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 1 | -13.9% | -13.93% | 0.0% | 0.0% | -13.9% |
| 2021 | 6 | 13.2% | 2.20% | 66.7% | 66.7% | 13.2% |
| 2022 | 3 | -21.5% | -7.16% | 33.3% | 33.3% | -21.5% |
| 2023 | 3 | 35.9% | 11.98% | 100.0% | 100.0% | 35.9% |
| 2024 | 4 | 31.7% | 7.94% | 75.0% | 75.0% | 31.7% |
| 2025 | 3 | 17.4% | 5.79% | 66.7% | 66.7% | 17.4% |
| 2026 | 1 | 4.3% | 4.29% | 100.0% | 100.0% | 4.3% |

### Macro Context by Year

**2020** (Losing year: -13.9%, 1 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 13.2%, 6 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -21.5%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 35.9%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 31.7%, 4 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 17.4%, 3 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 4.3%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -21.9% cumulative (trade 9 to trade 10)
**Period:** 2022-06-09 to 2022-09-13 (2 trades)
**Peak cumulative return:** -0.4% → **Trough:** -22.2%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-06-09 | 2022-06-10 | -1.0000 | 3.33% | unknown | ✅ |
| 2022-09-13 | 2022-12-07 | -1.0000 | -21.85% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 7 | -0.05% | -0.4% | 42.9% |
| 16-30d | 3 | 6.42% | 19.3% | 100.0% |
| 31-50d | 2 | 4.66% | 9.3% | 100.0% |
| 50d+ | 7 | 4.20% | 29.4% | 57.1% |
| 6-15d | 2 | 4.77% | 9.5% | 100.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 21 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-2.4%).
**Win/loss profile:** 66.7% win rate with 2.47× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (66.7%) exceeded signal accuracy (62.5%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2022 (-21.5%, 3 trades). Macro: Fed Tightening Cycle, 2022 Bear Market

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 29d, std 25d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.