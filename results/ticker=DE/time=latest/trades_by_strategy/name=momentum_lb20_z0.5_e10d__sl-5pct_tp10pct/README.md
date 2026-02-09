# Strategy Analysis: momentum_lb20_z0.5_e10d × sl-5%_tp10%

**Ticker:** DE
**Entry:** `momentum_lb20_z0.5_e10d`
**Exit:** `sl-5%_tp10%`
**Period:** 2016-08-05 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `10` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit targets a 2:1 reward/risk ratio

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 377.5% |
| **Annualized Return** | 5.5% |
| **Sharpe Ratio** | 0.281 |
| **Max Drawdown** | -35.9% |
| **Total Trades** | 110 |
| **Win Rate** | 50.9% |
| **Signal Accuracy** | 30.3% |
| **Direction Accuracy** | 50.9% |
| **Skill Ratio** | 51.1% |
| **Profit Factor** | 1.73 |
| **Expectancy** | 0.0168 |
| **Tail Ratio** | 1.49 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 701.3% | 377.5% | -323.8% |
| Annualized Return | 20.7% | 5.5% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0121 | Ideal for 110 trades: 0.0091 |
| Top-1 Trade | 4.1% of gross profit | Moderate concentration |
| Top-3 Trades | 10.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 304.9% | Positive without best trade |
| Return ex-Top-3 | 207.5% | Positive without top 3 |
| Max Single Trade | 17.9% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 45 | 7.89% | 355.2% | 8.85% | 13.36 |
| no_signal | 22 | 1.30% | 28.7% | 1.09% | 16.77 |
| direction_wrong_loss | 43 | -4.64% | -199.5% | -5.77% | 10.42 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 110 | 1.68% | 184.4% | 50.9% | 50.9% | 1.58% |

**Best-performing regime:** `unknown` — 110 trades, 184.4% total return, 50.9% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 33 | -4.76% | -157.1% |
| ❌ | ✅ | 32 | 7.98% | 255.2% |
| ✅ | ❌ | 10 | -4.23% | -42.3% |
| ✅ | ✅ | 13 | 7.69% | 99.9% |

### Flip Trades (Signal Wrong → Direction Right)

**43 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **7.9%**
- Total return: **338.6%**
- Average alpha: **8.6%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 43 | 7.87% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 110 | 1.68% | 184.4% | 50.9% | 50.9% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 47 | 2.51% | 117.8% | 61.7% | 61.7% |
| SHORT | 63 | 1.06% | 66.6% | 42.9% | 42.9% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 2 | -14.7% | -7.33% | 0.0% | 0.0% | -14.3% |
| 2017 | 11 | 26.4% | 2.40% | 54.5% | 54.5% | 7.0% |
| 2018 | 6 | 17.2% | 2.86% | 83.3% | 83.3% | 21.4% |
| 2019 | 2 | 0.5% | 0.27% | 50.0% | 50.0% | -9.0% |
| 2020 | 21 | 70.9% | 3.38% | 57.1% | 57.1% | 108.3% |
| 2021 | 10 | 17.8% | 1.78% | 50.0% | 50.0% | 7.2% |
| 2022 | 24 | 27.6% | 1.15% | 45.8% | 45.8% | 38.0% |
| 2023 | 8 | 14.0% | 1.75% | 50.0% | 50.0% | -1.6% |
| 2024 | 7 | 8.5% | 1.21% | 42.9% | 42.9% | 1.9% |
| 2025 | 17 | 3.0% | 0.18% | 41.2% | 41.2% | 2.8% |
| 2026 | 2 | 13.2% | 6.61% | 100.0% | 100.0% | 12.2% |

### Macro Context by Year

**2016** (Losing year: -14.7%, 2 trades)
- No major macro events flagged.

**2017** (Strong year: 26.4%, 11 trades)
- No major macro events flagged.

**2018** (Strong year: 17.2%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 0.5%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 70.9%, 21 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 17.8%, 10 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 27.6%, 24 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 14.0%, 8 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 8.5%, 7 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 3.0%, 17 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 13.2%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -27.9% cumulative (trade 91 to trade 98)
**Period:** 2024-11-26 to 2025-03-05 (8 trades)
**Peak cumulative return:** 168.1% → **Trough:** 140.2%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-11-26 | 2025-01-07 | -1.0000 | 10.02% | unknown | ✅ |
| 2025-01-08 | 2025-01-13 | -1.0000 | -4.86% | unknown | ❌ |
| 2025-01-14 | 2025-01-17 | -1.0000 | -5.35% | unknown | ❌ |
| 2025-01-21 | 2025-01-30 | -1.0000 | -3.64% | unknown | ❌ |
| 2025-01-30 | 2025-02-18 | 1.0000 | 4.49% | unknown | ✅ |
| 2025-02-19 | 2025-02-24 | 1.0000 | -4.85% | unknown | ❌ |
| 2025-02-25 | 2025-03-04 | 1.0000 | -5.99% | unknown | ❌ |
| 2025-03-05 | 2025-04-04 | 1.0000 | -7.73% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 35 | 0.74% | 25.9% | 42.9% |
| 16-30d | 20 | 3.09% | 61.9% | 60.0% |
| 31-50d | 6 | 3.44% | 20.6% | 83.3% |
| 50d+ | 4 | -1.24% | -5.0% | 25.0% |
| 6-15d | 45 | 1.80% | 80.9% | 51.1% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 4

## Observations & Caveats

**Sample size:** 110 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Well-distributed. HHI of 0.0121 is near the theoretical minimum of 0.0091 for 110 trades.
**Win/loss profile:** 50.9% win rate with 1.73× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (50.9%) exceeded signal accuracy (30.3%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2016 (-14.7%, 2 trades). Macro: No flagged events

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 13d, std 13d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.