# Strategy Analysis: momentum_lb40_z1.0_e15d × sl-10%_tp20%

**Ticker:** TTC
**Entry:** `momentum_lb40_z1.0_e15d`
**Exit:** `sl-10%_tp20%`
**Period:** 2016-11-16 to 2026-02-09
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `40`
- **zscore_threshold:** `1.0`
- **zscore_window:** `60`
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 322.3% |
| **Annualized Return** | 8.5% |
| **Sharpe Ratio** | 0.449 |
| **Max Drawdown** | -34.9% |
| **Total Trades** | 36 |
| **Win Rate** | 61.1% |
| **Signal Accuracy** | 50.0% |
| **Direction Accuracy** | 61.1% |
| **Skill Ratio** | 57.7% |
| **Profit Factor** | 2.50 |
| **Expectancy** | 0.0472 |
| **Tail Ratio** | 1.77 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 259.6% | 322.3% | 62.8% |
| Annualized Return | 12.2% | 8.5% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0352 | Ideal for 36 trades: 0.0278 |
| Top-1 Trade | 7.6% of gross profit | Moderate concentration |
| Top-3 Trades | 21.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 247.5% | Positive without best trade |
| Return ex-Top-3 | 140.8% | Positive without top 3 |
| Max Single Trade | 21.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 15 | 14.10% | 211.6% | 13.32% | 45.33 |
| no_signal | 10 | 4.61% | 46.1% | -0.34% | 36.40 |
| direction_wrong_loss | 11 | -7.99% | -87.9% | -9.14% | 22.36 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 36 | 4.72% | 169.8% | 61.1% | 61.1% | 2.66% |

**Best-performing regime:** `unknown` — 36 trades, 169.8% total return, 61.1% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 6 | -7.99% | -47.9% |
| ❌ | ✅ | 8 | 15.54% | 124.3% |
| ✅ | ❌ | 5 | -8.00% | -40.0% |
| ✅ | ✅ | 7 | 12.47% | 87.3% |

### Flip Trades (Signal Wrong → Direction Right)

**15 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **13.1%**
- Total return: **195.8%**
- Average alpha: **12.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 15 | 13.05% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 36 | 4.72% | 169.8% | 61.1% | 61.1% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 24 | 4.25% | 101.9% | 62.5% | 62.5% |
| SHORT | 12 | 5.65% | 67.8% | 58.3% | 58.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 1 | 12.8% | 12.84% | 100.0% | 100.0% | 7.7% |
| 2017 | 3 | 22.3% | 7.43% | 66.7% | 66.7% | 14.3% |
| 2018 | 1 | 11.1% | 11.10% | 100.0% | 100.0% | 17.6% |
| 2019 | 1 | 15.0% | 15.00% | 100.0% | 100.0% | -0.5% |
| 2020 | 8 | 87.1% | 10.89% | 75.0% | 75.0% | 81.9% |
| 2021 | 2 | -9.0% | -4.52% | 50.0% | 50.0% | -12.7% |
| 2022 | 2 | 25.6% | 12.80% | 100.0% | 100.0% | 27.0% |
| 2023 | 3 | -4.9% | -1.62% | 33.3% | 33.3% | -12.8% |
| 2024 | 8 | 1.1% | 0.13% | 37.5% | 37.5% | -19.8% |
| 2025 | 6 | -0.8% | -0.14% | 50.0% | 50.0% | -16.3% |
| 2026 | 1 | 9.5% | 9.50% | 100.0% | 100.0% | 9.5% |

### Macro Context by Year

**2016** (Strong year: 12.8%, 1 trades)
- No major macro events flagged.

**2017** (Strong year: 22.3%, 3 trades)
- No major macro events flagged.

**2018** (Strong year: 11.1%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 15.0%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 87.1%, 8 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -9.0%, 2 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 25.6%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Roughly flat: -4.9%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 1.1%, 8 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Roughly flat: -0.8%, 6 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 9.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -21.3% cumulative (trade 30 to trade 34)
**Period:** 2025-02-12 to 2025-08-15 (5 trades)
**Peak cumulative return:** 177.7% → **Trough:** 156.4%

**Macro context during drawdown:**
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-02-12 | 2025-04-04 | -1.0000 | 16.59% | unknown | ✅ |
| 2025-04-07 | 2025-05-02 | -1.0000 | -9.86% | unknown | ❌ |
| 2025-05-05 | 2025-05-14 | -1.0000 | -6.23% | unknown | ❌ |
| 2025-05-14 | 2025-08-14 | 1.0000 | 4.05% | unknown | ✅ |
| 2025-08-15 | 2025-11-18 | 1.0000 | -9.28% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 3 | 4.29% | 12.9% | 66.7% |
| 16-30d | 7 | 6.93% | 48.5% | 71.4% |
| 31-50d | 4 | 10.56% | 42.3% | 75.0% |
| 50d+ | 13 | 8.09% | 105.2% | 76.9% |
| 6-15d | 9 | -4.34% | -39.1% | 22.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** 36 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Well-distributed. HHI of 0.0352 is near the theoretical minimum of 0.0278 for 36 trades.
**Win/loss profile:** 61.1% win rate with 2.50× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (61.1%) exceeded signal accuracy (50.0%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2021 (-9.0%, 2 trades). Macro: Post-COVID Stimulus Rally

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 36d, std 30d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.