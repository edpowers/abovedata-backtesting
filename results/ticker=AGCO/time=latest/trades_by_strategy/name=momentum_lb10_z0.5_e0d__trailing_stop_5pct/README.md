# Strategy Analysis: momentum_lb10_z0.5_e0d × trailing_stop_5%

**Ticker:** AGCO
**Entry:** `momentum_lb10_z0.5_e0d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-10-26 to 2025-11-12
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `10`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `0` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 13.8% |
| **Annualized Return** | 15.7% |
| **Sharpe Ratio** | 1.287 |
| **Max Drawdown** | -14.1% |
| **Total Trades** | 83 |
| **Win Rate** | 41.0% |
| **Signal Accuracy** | 52.6% |
| **Direction Accuracy** | 41.0% |
| **Skill Ratio** | 41.9% |
| **Profit Factor** | 1.18 |
| **Expectancy** | 0.0025 |
| **Tail Ratio** | 2.23 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 163.1% | 13.8% | -149.4% |
| Annualized Return | 11.3% | 15.7% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.1×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0256 | Ideal for 83 trades: 0.0120 |
| Top-1 Trade | 17.5% of gross profit | Moderate concentration |
| Top-3 Trades | 34.1% of gross profit | Moderate concentration |
| Return ex-Top-1 | -8.8% | Negative without best trade |
| Return ex-Top-3 | -26.9% | Negative without top 3 |
| Max Single Trade | 24.7% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 26 | 3.91% | 101.7% | 3.91% | 7.42 |
| no_signal | 21 | 0.51% | 10.8% | 0.51% | 9.57 |
| direction_wrong_loss | 36 | -2.54% | -91.4% | -2.54% | 2.83 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 83 | 0.25% | 21.1% | 41.0% | 41.0% | 0.25% |

**Best-performing regime:** `unknown` — 83 trades, 21.1% total return, 41.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 15 | -2.76% | -41.4% |
| ❌ | ✅ | 17 | 2.42% | 41.1% |
| ✅ | ❌ | 21 | -2.38% | -50.0% |
| ✅ | ✅ | 9 | 6.73% | 60.6% |

### Flip Trades (Signal Wrong → Direction Right)

**25 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **3.2%**
- Total return: **80.4%**
- Average alpha: **3.2%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 25 | 3.22% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 83 | 0.25% | 21.1% | 41.0% | 41.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 29 | 1.43% | 41.5% | 58.6% | 58.6% |
| SHORT | 54 | -0.38% | -20.4% | 31.5% | 31.5% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 3 | -7.7% | -2.56% | 0.0% | 0.0% | -7.7% |
| 2017 | 8 | 1.8% | 0.22% | 25.0% | 25.0% | 1.8% |
| 2018 | 12 | -23.4% | -1.95% | 8.3% | 8.3% | -23.4% |
| 2020 | 12 | 37.2% | 3.10% | 75.0% | 75.0% | 37.2% |
| 2021 | 9 | -3.2% | -0.36% | 44.4% | 44.4% | -3.2% |
| 2022 | 9 | -1.0% | -0.11% | 44.4% | 44.4% | -1.0% |
| 2023 | 9 | 6.1% | 0.68% | 55.6% | 55.6% | 6.1% |
| 2024 | 9 | 2.6% | 0.29% | 33.3% | 33.3% | 2.6% |
| 2025 | 12 | 8.6% | 0.72% | 50.0% | 50.0% | 8.6% |

### Macro Context by Year

**2016** (Losing year: -7.7%, 3 trades)
- No major macro events flagged.

**2017** (Modestly positive: 1.8%, 8 trades)
- No major macro events flagged.

**2018** (Losing year: -23.4%, 12 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2020** (Strong year: 37.2%, 12 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Roughly flat: -3.2%, 9 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Roughly flat: -1.0%, 9 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 6.1%, 9 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 2.6%, 9 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 8.6%, 12 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -32.2% cumulative (trade 8 to trade 23)
**Period:** 2017-05-19 to 2018-11-09 (16 trades)
**Peak cumulative return:** 2.9% → **Trough:** -29.3%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2017-05-19 | 2017-07-27 | 1.0000 | 12.59% | unknown | ✅ |
| 2017-10-31 | 2017-11-20 | -1.0000 | -0.78% | unknown | ❌ |
| 2017-11-21 | 2017-12-01 | -1.0000 | -5.05% | unknown | ❌ |
| 2017-12-04 | 2017-12-15 | -1.0000 | -3.00% | unknown | ❌ |
| 2018-02-06 | 2018-02-07 | -1.0000 | -2.82% | unknown | ❌ |
| 2018-02-08 | 2018-02-09 | -1.0000 | -0.43% | unknown | ❌ |
| 2018-02-12 | 2018-02-16 | -1.0000 | 1.44% | unknown | ✅ |
| 2018-05-02 | 2018-05-07 | -1.0000 | -4.14% | unknown | ❌ |
| 2018-05-08 | 2018-05-10 | -1.0000 | -2.36% | unknown | ❌ |
| 2018-05-11 | 2018-05-18 | -1.0000 | -4.69% | unknown | ❌ |
| 2018-08-01 | 2018-08-02 | 1.0000 | -0.24% | unknown | ❌ |
| 2018-08-03 | 2018-08-09 | 1.0000 | -2.16% | unknown | ❌ |
| 2018-08-10 | 2018-08-13 | 1.0000 | -1.17% | unknown | ❌ |
| 2018-10-31 | 2018-11-01 | -1.0000 | -2.41% | unknown | ❌ |
| 2018-11-02 | 2018-11-08 | -1.0000 | -1.38% | unknown | ❌ |
| 2018-11-09 | 2018-11-13 | -1.0000 | -3.03% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 52 | -1.20% | -62.6% | 25.0% |
| 16-30d | 2 | 5.43% | 10.9% | 100.0% |
| 31-50d | 2 | 9.08% | 18.2% | 100.0% |
| 6-15d | 27 | 2.02% | 54.7% | 63.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 9

## Observations & Caveats

**Sample size:** 83 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-26.9%).
**Win/loss profile:** Profit factor of 1.18 with 41.0% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (52.6%) exceeded direction accuracy (41.0%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2018 (-23.4%, 12 trades). Macro: US-China Trade War Escalation

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 6d, std 7d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.