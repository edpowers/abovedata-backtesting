# Strategy Analysis: momentum_lb40_z0.5_e3d × trailing_stop_5%

**Ticker:** CAT
**Entry:** `momentum_lb40_z0.5_e3d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-07-25 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `40`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `3` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 146.5% |
| **Annualized Return** | 30.6% |
| **Sharpe Ratio** | 1.716 |
| **Max Drawdown** | -20.4% |
| **Total Trades** | 184 |
| **Win Rate** | 43.5% |
| **Signal Accuracy** | 39.4% |
| **Direction Accuracy** | 43.5% |
| **Skill Ratio** | 42.9% |
| **Profit Factor** | 1.37 |
| **Expectancy** | 0.0064 |
| **Tail Ratio** | 2.20 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 954.1% | 146.5% | -807.5% |
| Annualized Return | 23.7% | 30.6% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.9×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0102 | Ideal for 184 trades: 0.0054 |
| Top-1 Trade | 5.4% of gross profit | Moderate concentration |
| Top-3 Trades | 13.4% of gross profit | Moderate concentration |
| Return ex-Top-1 | 99.5% | Positive without best trade |
| Return ex-Top-3 | 44.2% | Positive without top 3 |
| Max Single Trade | 23.6% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 67 | 5.50% | 368.8% | 5.35% | 10.42 |
| no_signal | 28 | 0.43% | 12.0% | -0.16% | 5.07 |
| direction_wrong_loss | 89 | -2.95% | -262.8% | -3.56% | 4.19 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 184 | 0.64% | 118.0% | 43.5% | 43.5% | 0.20% |

**Best-performing regime:** `unknown` — 184 trades, 118.0% total return, 43.5% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 72 | -3.03% | -218.4% |
| ❌ | ✅ | 47 | 5.03% | 236.4% |
| ✅ | ❌ | 17 | -2.61% | -44.4% |
| ✅ | ✅ | 20 | 6.62% | 132.4% |

### Flip Trades (Signal Wrong → Direction Right)

**60 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.1%**
- Total return: **306.4%**
- Average alpha: **5.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 60 | 5.11% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| high | 44 | 1.52% | 67.1% | 50.0% | 50.0% |
| medium | 72 | 0.49% | 35.0% | 43.1% | 43.1% |
| low | 65 | 0.41% | 26.5% | 40.0% | 40.0% |
| no_data | 3 | -3.53% | -10.6% | 33.3% | 33.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 71 | 1.49% | 106.0% | 46.5% | 46.5% |
| SHORT | 113 | 0.11% | 12.0% | 41.6% | 41.6% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 23 | 12.4% | 0.54% | 43.5% | 43.5% | 25.2% |
| 2019 | 19 | 25.7% | 1.35% | 42.1% | 42.1% | 0.5% |
| 2020 | 25 | 12.1% | 0.48% | 44.0% | 44.0% | 2.3% |
| 2021 | 22 | -7.0% | -0.32% | 36.4% | 36.4% | -24.7% |
| 2022 | 25 | 11.6% | 0.46% | 48.0% | 48.0% | 17.4% |
| 2023 | 23 | -2.5% | -0.11% | 34.8% | 34.8% | -13.0% |
| 2024 | 18 | 37.7% | 2.10% | 50.0% | 50.0% | 15.5% |
| 2025 | 24 | 39.5% | 1.65% | 50.0% | 50.0% | 27.0% |
| 2026 | 5 | -11.5% | -2.30% | 40.0% | 40.0% | -13.0% |

### Macro Context by Year

**2018** (Strong year: 12.4%, 23 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 25.7%, 19 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 12.1%, 25 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -7.0%, 22 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 11.6%, 25 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Roughly flat: -2.5%, 23 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 37.7%, 18 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 39.5%, 24 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -11.5%, 5 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -37.0% cumulative (trade 49 to trade 82)
**Period:** 2020-03-10 to 2021-05-11 (34 trades)
**Peak cumulative return:** 60.6% → **Trough:** 23.7%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-03-10 | 2020-03-11 | -1.0000 | 5.45% | unknown | ✅ |
| 2020-03-12 | 2020-03-13 | -1.0000 | -8.00% | unknown | ❌ |
| 2020-03-16 | 2020-03-17 | -1.0000 | -7.27% | unknown | ❌ |
| 2020-03-18 | 2020-03-19 | -1.0000 | -2.89% | unknown | ❌ |
| 2020-03-20 | 2020-03-23 | -1.0000 | 3.82% | unknown | ✅ |
| 2020-03-24 | 2020-03-25 | -1.0000 | -3.29% | unknown | ❌ |
| 2020-03-26 | 2020-03-27 | -1.0000 | 4.58% | unknown | ✅ |
| 2020-03-30 | 2020-03-31 | -1.0000 | -3.88% | unknown | ❌ |
| 2020-04-01 | 2020-04-02 | -1.0000 | -4.84% | unknown | ❌ |
| 2020-04-03 | 2020-04-06 | -1.0000 | -5.02% | unknown | ❌ |
| 2020-04-07 | 2020-04-08 | -1.0000 | -4.49% | unknown | ❌ |
| 2020-04-09 | 2020-04-13 | -1.0000 | 8.71% | unknown | ✅ |
| 2020-04-14 | 2020-04-17 | -1.0000 | -0.76% | unknown | ❌ |
| 2020-04-20 | 2020-04-23 | -1.0000 | 1.47% | unknown | ✅ |
| 2020-10-22 | 2020-10-26 | 1.0000 | -3.22% | unknown | ❌ |
| 2020-10-27 | 2020-10-28 | 1.0000 | -4.27% | unknown | ❌ |
| 2020-10-29 | 2020-11-04 | 1.0000 | 0.36% | unknown | ✅ |
| 2020-11-05 | 2020-11-11 | 1.0000 | 3.91% | unknown | ✅ |
| 2020-11-12 | 2021-01-06 | 1.0000 | 14.62% | unknown | ✅ |
| 2021-01-07 | 2021-01-25 | 1.0000 | -3.03% | unknown | ❌ |
| 2021-01-26 | 2021-01-29 | -1.0000 | 2.33% | unknown | ✅ |
| 2021-02-01 | 2021-02-02 | -1.0000 | -4.21% | unknown | ❌ |
| 2021-02-03 | 2021-02-09 | -1.0000 | -3.05% | unknown | ❌ |
| 2021-02-10 | 2021-02-16 | -1.0000 | -2.36% | unknown | ❌ |
| 2021-02-17 | 2021-02-19 | -1.0000 | -3.76% | unknown | ❌ |
| 2021-02-22 | 2021-02-23 | -1.0000 | -0.97% | unknown | ❌ |
| 2021-02-24 | 2021-03-05 | -1.0000 | 1.04% | unknown | ✅ |
| 2021-03-08 | 2021-03-12 | -1.0000 | -3.35% | unknown | ❌ |
| 2021-03-15 | 2021-03-18 | -1.0000 | 0.03% | unknown | ✅ |
| 2021-03-19 | 2021-03-26 | -1.0000 | -1.87% | unknown | ❌ |
| 2021-03-29 | 2021-04-29 | -1.0000 | 0.75% | unknown | ✅ |
| 2021-04-30 | 2021-05-05 | -1.0000 | -4.28% | unknown | ❌ |
| 2021-05-06 | 2021-05-10 | -1.0000 | -2.34% | unknown | ❌ |
| 2021-05-11 | 2021-06-01 | -1.0000 | -1.45% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 116 | -1.12% | -129.7% | 31.9% |
| 16-30d | 13 | 6.45% | 83.8% | 100.0% |
| 31-50d | 5 | 12.96% | 64.8% | 100.0% |
| 6-15d | 50 | 1.98% | 99.1% | 50.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 184 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (44.2%).
**Win/loss profile:** Profit factor of 1.37 with 43.5% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (43.5%) exceeded signal accuracy (39.4%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2026 (-11.5%, 5 trades). Macro: No flagged events

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 7d, std 8d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.