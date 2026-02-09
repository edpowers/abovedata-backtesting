# Strategy Analysis: momentum_lb20_z0.5_e20d × signal_change

**Ticker:** TTC
**Entry:** `momentum_lb20_z0.5_e20d`
**Exit:** `signal_change`
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

- **Exit type:** `signal_change`
  - Exit when the UCC signal reverses direction. Fundamentally-driven exit that stays in the trade as long as the thesis holds

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 352.8% |
| **Annualized Return** | 14.7% |
| **Sharpe Ratio** | 0.701 |
| **Max Drawdown** | -33.9% |
| **Total Trades** | 21 |
| **Win Rate** | 81.0% |
| **Signal Accuracy** | 42.9% |
| **Direction Accuracy** | 81.0% |
| **Skill Ratio** | 80.0% |
| **Profit Factor** | 3.90 |
| **Expectancy** | 0.0851 |
| **Tail Ratio** | 1.46 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 259.6% | 352.8% | 93.2% |
| Annualized Return | 12.2% | 14.7% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.4×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0661 | Ideal for 21 trades: 0.0476 |
| Top-1 Trade | 14.1% of gross profit | Moderate concentration |
| Top-3 Trades | 36.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 238.4% | Positive without best trade |
| Return ex-Top-3 | 112.0% | Positive without top 3 |
| Max Single Trade | 33.8% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 12 | 14.12% | 169.4% | 11.28% | 77.33 |
| no_signal | 6 | 8.32% | 49.9% | 1.62% | 75.83 |
| direction_wrong_loss | 3 | -13.52% | -40.6% | -23.09% | 104.67 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 21 | 8.51% | 178.8% | 81.0% | 81.0% | 3.61% |

**Best-performing regime:** `unknown` — 21 trades, 178.8% total return, 81.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 2 | -12.50% | -25.0% |
| ❌ | ✅ | 7 | 14.50% | 101.5% |
| ✅ | ❌ | 1 | -15.56% | -15.6% |
| ✅ | ✅ | 5 | 13.58% | 67.9% |

### Flip Trades (Signal Wrong → Direction Right)

**12 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **14.4%**
- Total return: **172.4%**
- Average alpha: **10.3%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 12 | 14.37% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 21 | 8.51% | 178.8% | 81.0% | 81.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 14 | 10.85% | 152.0% | 85.7% | 85.7% |
| SHORT | 7 | 3.83% | 26.8% | 71.4% | 71.4% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 1 | 33.8% | 33.82% | 100.0% | 100.0% | 26.5% |
| 2017 | 3 | 26.3% | 8.75% | 100.0% | 100.0% | 7.0% |
| 2018 | 1 | 21.9% | 21.91% | 100.0% | 100.0% | 14.7% |
| 2019 | 1 | 15.4% | 15.44% | 100.0% | 100.0% | 3.4% |
| 2020 | 2 | 49.4% | 24.69% | 100.0% | 100.0% | 55.2% |
| 2021 | 2 | -36.5% | -18.24% | 0.0% | 0.0% | -56.8% |
| 2022 | 2 | 41.0% | 20.50% | 100.0% | 100.0% | 46.9% |
| 2023 | 4 | 28.5% | 7.12% | 75.0% | 75.0% | 6.8% |
| 2024 | 2 | 2.1% | 1.06% | 100.0% | 100.0% | -1.2% |
| 2025 | 2 | -13.3% | -6.66% | 50.0% | 50.0% | -36.7% |
| 2026 | 1 | 10.1% | 10.12% | 100.0% | 100.0% | 10.1% |

### Macro Context by Year

**2016** (Strong year: 33.8%, 1 trades)
- No major macro events flagged.

**2017** (Strong year: 26.3%, 3 trades)
- No major macro events flagged.

**2018** (Strong year: 21.9%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 15.4%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 49.4%, 2 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -36.5%, 2 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 41.0%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 28.5%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 2.1%, 2 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -13.3%, 2 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 10.1%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -36.5% cumulative (trade 8 to trade 10)
**Period:** 2020-08-06 to 2021-05-05 (3 trades)
**Peak cumulative return:** 146.8% → **Trough:** 110.3%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-08-06 | 2020-11-17 | 1.0000 | 25.11% | unknown | ✅ |
| 2021-02-03 | 2021-05-05 | -1.0000 | -20.92% | unknown | ❌ |
| 2021-05-05 | 2022-02-02 | 1.0000 | -15.56% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 16-30d | 1 | 10.12% | 10.1% | 100.0% |
| 50d+ | 20 | 8.43% | 168.6% | 80.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 8
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 21 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Well-distributed. HHI of 0.0661 is near the theoretical minimum of 0.0476 for 21 trades.
**Win/loss profile:** 81.0% win rate with 3.90× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (81.0%) exceeded signal accuracy (42.9%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2021 (-36.5%, 2 trades). Macro: Post-COVID Stimulus Rally

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.