# Strategy Analysis: momentum_lb20_z0.5_e0d × trailing_stop_5%

**Ticker:** AGCO
**Entry:** `momentum_lb20_z0.5_e0d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-10-26 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `0` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | -5.8% |
| **Annualized Return** | 17.9% |
| **Sharpe Ratio** | 1.386 |
| **Max Drawdown** | -15.2% |
| **Total Trades** | 82 |
| **Win Rate** | 41.5% |
| **Signal Accuracy** | 56.1% |
| **Direction Accuracy** | 42.0% |
| **Skill Ratio** | 41.3% |
| **Profit Factor** | 1.03 |
| **Expectancy** | 0.0005 |
| **Tail Ratio** | 1.93 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 222.5% | -5.8% | -228.2% |
| Annualized Return | 13.5% | 17.9% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.0×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0239 | Ideal for 82 trades: 0.0122 |
| Top-1 Trade | 16.4% of gross profit | Moderate concentration |
| Top-3 Trades | 34.5% of gross profit | Moderate concentration |
| Return ex-Top-1 | -24.5% | Negative without best trade |
| Return ex-Top-3 | -41.5% | Negative without top 3 |
| Max Single Trade | 24.7% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 26 | 3.93% | 102.2% | 3.93% | 6.85 |
| no_signal | 19 | 0.96% | 18.2% | 0.96% | 9.84 |
| direction_wrong_loss | 37 | -3.14% | -116.3% | -3.14% | 3.22 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 82 | 0.05% | 4.0% | 41.5% | 41.5% | 0.05% |

**Best-performing regime:** `unknown` — 82 trades, 4.0% total return, 41.5% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 15 | -2.83% | -42.4% |
| ❌ | ✅ | 16 | 2.97% | 47.6% |
| ✅ | ❌ | 22 | -3.36% | -73.9% |
| ✅ | ✅ | 10 | 5.46% | 54.6% |

### Flip Trades (Signal Wrong → Direction Right)

**24 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.0%**
- Total return: **96.5%**
- Average alpha: **4.0%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 24 | 4.02% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 82 | 0.05% | 4.0% | 41.5% | 41.5% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 46 | 1.07% | 49.1% | 52.2% | 52.2% |
| SHORT | 36 | -1.25% | -45.1% | 27.8% | 27.8% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 3 | 13.3% | 4.42% | 33.3% | 33.3% | 13.3% |
| 2017 | 7 | 1.6% | 0.23% | 42.9% | 42.9% | 1.6% |
| 2018 | 12 | -23.4% | -1.95% | 8.3% | 8.3% | -23.4% |
| 2019 | 3 | -12.0% | -4.00% | 0.0% | 0.0% | -12.0% |
| 2020 | 12 | 37.2% | 3.10% | 75.0% | 75.0% | 37.2% |
| 2021 | 3 | -3.4% | -1.13% | 33.3% | 33.3% | -3.4% |
| 2022 | 12 | 18.0% | 1.50% | 66.7% | 66.7% | 18.0% |
| 2023 | 6 | -10.6% | -1.77% | 16.7% | 16.7% | -10.6% |
| 2024 | 12 | -12.5% | -1.04% | 41.7% | 41.7% | -12.5% |
| 2025 | 9 | -12.1% | -1.34% | 33.3% | 33.3% | -12.1% |
| 2026 | 3 | 7.8% | 2.60% | 66.7% | 66.7% | 7.8% |

### Macro Context by Year

**2016** (Strong year: 13.3%, 3 trades)
- No major macro events flagged.

**2017** (Modestly positive: 1.6%, 7 trades)
- No major macro events flagged.

**2018** (Losing year: -23.4%, 12 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -12.0%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 37.2%, 12 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Roughly flat: -3.4%, 3 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 18.0%, 12 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Losing year: -10.6%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -12.5%, 12 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -12.1%, 9 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 7.8%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -43.4% cumulative (trade 8 to trade 25)
**Period:** 2017-11-01 to 2019-05-14 (18 trades)
**Peak cumulative return:** 22.9% → **Trough:** -20.5%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2017-11-01 | 2017-11-20 | -1.0000 | 0.47% | unknown | ✅ |
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
| 2019-05-02 | 2019-05-09 | 1.0000 | -2.74% | unknown | ❌ |
| 2019-05-10 | 2019-05-13 | 1.0000 | -3.67% | unknown | ❌ |
| 2019-05-14 | 2019-05-17 | 1.0000 | -5.59% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 57 | -1.69% | -96.5% | 24.6% |
| 16-30d | 2 | 9.50% | 19.0% | 100.0% |
| 31-50d | 1 | 6.54% | 6.5% | 100.0% |
| 50d+ | 1 | 9.13% | 9.1% | 100.0% |
| 6-15d | 21 | 3.14% | 65.8% | 76.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 12

## Observations & Caveats

**Sample size:** 82 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-41.5%).
**Win/loss profile:** Profit factor of 1.03 with 41.5% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (56.1%) exceeded direction accuracy (42.0%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2018 (-23.4%, 12 trades). Macro: US-China Trade War Escalation

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 6d, std 8d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.