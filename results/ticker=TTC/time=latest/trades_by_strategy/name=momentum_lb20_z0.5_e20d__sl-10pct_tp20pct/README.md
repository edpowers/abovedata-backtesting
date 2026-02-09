# Strategy Analysis: momentum_lb20_z0.5_e20d × sl-10%_tp20%

**Ticker:** TTC
**Entry:** `momentum_lb20_z0.5_e20d`
**Exit:** `sl-10%_tp20%`
**Period:** 2016-07-21 to 2026-02-09
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `20` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 359.9% |
| **Annualized Return** | 9.4% |
| **Sharpe Ratio** | 0.473 |
| **Max Drawdown** | -34.5% |
| **Total Trades** | 43 |
| **Win Rate** | 65.1% |
| **Signal Accuracy** | 66.7% |
| **Direction Accuracy** | 65.1% |
| **Skill Ratio** | 61.8% |
| **Profit Factor** | 2.47 |
| **Expectancy** | 0.0421 |
| **Tail Ratio** | 1.67 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 259.6% | 359.9% | 100.3% |
| Annualized Return | 12.2% | 9.4% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.4×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0331 | Ideal for 43 trades: 0.0233 |
| Top-1 Trade | 8.0% of gross profit | Moderate concentration |
| Top-3 Trades | 22.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 270.1% | Positive without best trade |
| Return ex-Top-3 | 151.3% | Positive without top 3 |
| Max Single Trade | 24.3% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 21 | 10.73% | 225.3% | 9.57% | 34.67 |
| no_signal | 9 | 6.35% | 57.1% | 1.74% | 50.00 |
| direction_wrong_loss | 13 | -7.82% | -101.6% | -9.37% | 38.15 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 43 | 4.21% | 180.9% | 65.1% | 65.1% | 2.21% |

**Best-performing regime:** `unknown` — 43 trades, 180.9% total return, 65.1% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 4 | -8.61% | -34.4% |
| ❌ | ✅ | 10 | 13.49% | 134.9% |
| ✅ | ❌ | 9 | -7.46% | -67.2% |
| ✅ | ✅ | 11 | 8.22% | 90.4% |

### Flip Trades (Signal Wrong → Direction Right)

**17 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **12.6%**
- Total return: **213.7%**
- Average alpha: **10.0%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 17 | 12.57% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 43 | 4.21% | 180.9% | 65.1% | 65.1% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 27 | 5.37% | 145.0% | 74.1% | 74.1% |
| SHORT | 16 | 2.24% | 35.9% | 50.0% | 50.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 2 | 30.9% | 15.43% | 100.0% | 100.0% | 24.0% |
| 2017 | 5 | 24.7% | 4.93% | 80.0% | 80.0% | 5.3% |
| 2018 | 2 | 13.0% | 6.48% | 50.0% | 50.0% | 14.6% |
| 2019 | 2 | 22.3% | 11.13% | 100.0% | 100.0% | 5.2% |
| 2020 | 6 | 62.9% | 10.49% | 83.3% | 83.3% | 75.5% |
| 2021 | 4 | -36.7% | -9.18% | 25.0% | 25.0% | -51.2% |
| 2022 | 5 | 40.7% | 8.14% | 80.0% | 80.0% | 43.4% |
| 2023 | 7 | 16.7% | 2.38% | 57.1% | 57.1% | 2.0% |
| 2024 | 6 | 10.5% | 1.75% | 50.0% | 50.0% | 2.8% |
| 2025 | 3 | -14.0% | -4.66% | 33.3% | 33.3% | -36.8% |
| 2026 | 1 | 10.0% | 9.97% | 100.0% | 100.0% | 10.0% |

### Macro Context by Year

**2016** (Strong year: 30.9%, 2 trades)
- No major macro events flagged.

**2017** (Strong year: 24.7%, 5 trades)
- No major macro events flagged.

**2018** (Strong year: 13.0%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 22.3%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 62.9%, 6 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -36.7%, 4 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 40.7%, 5 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 16.7%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 10.5%, 6 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -14.0%, 3 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 10.0%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -36.7% cumulative (trade 17 to trade 21)
**Period:** 2020-09-17 to 2021-05-05 (5 trades)
**Peak cumulative return:** 153.7% → **Trough:** 117.0%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-09-17 | 2020-11-17 | 1.0000 | 5.97% | unknown | ✅ |
| 2021-02-03 | 2021-04-05 | -1.0000 | -9.74% | unknown | ❌ |
| 2021-04-06 | 2021-04-22 | -1.0000 | -8.31% | unknown | ❌ |
| 2021-04-23 | 2021-05-05 | -1.0000 | 0.23% | unknown | ✅ |
| 2021-05-05 | 2022-01-21 | 1.0000 | -18.90% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 2 | 8.55% | 17.1% | 50.0% |
| 16-30d | 10 | 11.19% | 111.9% | 90.0% |
| 31-50d | 11 | 2.06% | 22.7% | 54.5% |
| 50d+ | 11 | 4.07% | 44.7% | 72.7% |
| 6-15d | 9 | -1.73% | -15.6% | 44.4% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** 43 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Well-distributed. HHI of 0.0331 is near the theoretical minimum of 0.0233 for 43 trades.
**Win/loss profile:** 65.1% win rate with 2.47× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (66.7%) and direction accuracy (65.1%) are similar, suggesting the correlation flip had limited net impact in this sample.

### Known Vulnerabilities

- **Worst year:** 2021 (-36.7%, 4 trades). Macro: Post-COVID Stimulus Rally

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 39d, std 35d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.