# Strategy Analysis: momentum_lb10_z0.5_e10d × sl-5%_tp10%

**Ticker:** CAT
**Entry:** `momentum_lb10_z0.5_e10d`
**Exit:** `sl-5%_tp10%`
**Period:** 2018-10-09 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `10`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `10` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit targets a 2:1 reward/risk ratio

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 302.7% |
| **Annualized Return** | 14.3% |
| **Sharpe Ratio** | 0.762 |
| **Max Drawdown** | -38.7% |
| **Total Trades** | 105 |
| **Win Rate** | 46.7% |
| **Signal Accuracy** | 44.4% |
| **Direction Accuracy** | 47.1% |
| **Skill Ratio** | 50.6% |
| **Profit Factor** | 1.62 |
| **Expectancy** | 0.0160 |
| **Tail Ratio** | 1.88 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 954.1% | 302.7% | -651.3% |
| Annualized Return | 23.7% | 14.3% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.2×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0116 | Ideal for 105 trades: 0.0095 |
| Top-1 Trade | 3.7% of gross profit | Moderate concentration |
| Top-3 Trades | 9.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 246.5% | Positive without best trade |
| Return ex-Top-3 | 169.7% | Positive without top 3 |
| Max Single Trade | 16.2% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 42 | 9.00% | 377.9% | 7.79% | 15.57 |
| no_signal | 22 | -0.35% | -7.8% | -1.20% | 7.64 |
| direction_wrong_loss | 41 | -4.94% | -202.5% | -4.87% | 8.98 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 105 | 1.60% | 167.6% | 46.7% | 46.7% | 0.96% |

**Best-performing regime:** `unknown` — 105 trades, 167.6% total return, 46.7% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 33 | -4.98% | -164.5% |
| ❌ | ✅ | 26 | 9.25% | 240.5% |
| ✅ | ❌ | 8 | -4.76% | -38.0% |
| ✅ | ✅ | 16 | 8.59% | 137.4% |

### Flip Trades (Signal Wrong → Direction Right)

**33 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **9.2%**
- Total return: **302.4%**
- Average alpha: **8.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 33 | 9.16% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 43 | 2.17% | 93.3% | 53.5% | 53.5% |
| high | 17 | 3.65% | 62.1% | 58.8% | 58.8% |
| low | 43 | 0.36% | 15.7% | 37.2% | 37.2% |
| no_data | 2 | -1.75% | -3.5% | 0.0% | 0.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 66 | 2.42% | 159.6% | 51.5% | 51.5% |
| SHORT | 39 | 0.21% | 8.0% | 38.5% | 38.5% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 8 | -3.7% | -0.46% | 37.5% | 37.5% | 0.6% |
| 2019 | 8 | -4.2% | -0.52% | 37.5% | 37.5% | -26.0% |
| 2020 | 24 | 69.5% | 2.90% | 50.0% | 50.0% | 77.0% |
| 2021 | 13 | 44.5% | 3.42% | 61.5% | 61.5% | 14.5% |
| 2022 | 15 | 41.2% | 2.74% | 53.3% | 53.3% | 46.6% |
| 2023 | 4 | 3.2% | 0.80% | 50.0% | 50.0% | 6.8% |
| 2024 | 10 | 30.7% | 3.07% | 60.0% | 60.0% | 15.5% |
| 2025 | 19 | -29.2% | -1.54% | 26.3% | 26.3% | -50.6% |
| 2026 | 4 | 15.7% | 3.93% | 50.0% | 50.0% | 16.6% |

### Macro Context by Year

**2018** (Roughly flat: -3.7%, 8 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Roughly flat: -4.2%, 8 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 69.5%, 24 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 44.5%, 13 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 41.2%, 15 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 3.2%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 30.7%, 10 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -29.2%, 19 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 15.7%, 4 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -40.3% cumulative (trade 82 to trade 97)
**Period:** 2024-09-20 to 2025-11-05 (16 trades)
**Peak cumulative return:** 181.1% → **Trough:** 140.9%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-09-20 | 2024-10-16 | 1.0000 | 6.72% | unknown | ✅ |
| 2025-01-15 | 2025-02-12 | 1.0000 | -5.75% | unknown | ❌ |
| 2025-02-13 | 2025-03-03 | 1.0000 | -6.12% | unknown | ❌ |
| 2025-03-04 | 2025-04-03 | 1.0000 | -6.42% | unknown | ❌ |
| 2025-04-04 | 2025-04-07 | 1.0000 | -2.78% | unknown | ❌ |
| 2025-04-08 | 2025-04-09 | 1.0000 | 9.88% | unknown | ✅ |
| 2025-04-10 | 2025-04-15 | 1.0000 | 1.48% | unknown | ✅ |
| 2025-04-15 | 2025-05-01 | -1.0000 | -7.51% | unknown | ❌ |
| 2025-05-02 | 2025-05-12 | -1.0000 | -5.83% | unknown | ❌ |
| 2025-05-13 | 2025-06-24 | -1.0000 | -5.81% | unknown | ❌ |
| 2025-06-25 | 2025-07-01 | -1.0000 | -5.20% | unknown | ❌ |
| 2025-07-02 | 2025-07-17 | -1.0000 | -4.93% | unknown | ❌ |
| 2025-07-18 | 2025-07-22 | -1.0000 | -1.21% | unknown | ❌ |
| 2025-10-15 | 2025-10-29 | 1.0000 | 9.95% | unknown | ✅ |
| 2025-10-30 | 2025-11-04 | 1.0000 | -6.10% | unknown | ❌ |
| 2025-11-05 | 2025-11-18 | 1.0000 | -3.91% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 35 | -1.07% | -37.4% | 28.6% |
| 16-30d | 15 | 1.68% | 25.1% | 53.3% |
| 31-50d | 5 | 5.15% | 25.8% | 60.0% |
| 50d+ | 2 | 11.28% | 22.6% | 100.0% |
| 6-15d | 48 | 2.74% | 131.6% | 54.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 105 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Well-distributed. HHI of 0.0116 is near the theoretical minimum of 0.0095 for 105 trades.
**Win/loss profile:** Profit factor of 1.62 with 46.7% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (47.1%) exceeded signal accuracy (44.4%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2025 (-29.2%, 19 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 11d, std 12d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.