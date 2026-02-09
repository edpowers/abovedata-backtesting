# Strategy Analysis: momentum_lb20_z0.5_e30d × signal_change

**Ticker:** ALGN
**Entry:** `momentum_lb20_z0.5_e30d`
**Exit:** `signal_change`
**Period:** 2018-03-13 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `signal_change`
  - Exit when the UCC signal reverses direction. Fundamentally-driven exit that stays in the trade as long as the thesis holds

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 1462.7% |
| **Annualized Return** | 24.6% |
| **Sharpe Ratio** | 0.682 |
| **Max Drawdown** | -67.0% |
| **Total Trades** | 14 |
| **Win Rate** | 100.0% |
| **Signal Accuracy** | 15.4% |
| **Direction Accuracy** | 100.0% |
| **Skill Ratio** | 100.0% |
| **Profit Factor** | inf |
| **Expectancy** | 0.2743 |
| **Tail Ratio** | 20.94 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 235.5% | 1462.7% | 1227.1% |
| Annualized Return | 11.5% | 24.6% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.1044 | Ideal for 14 trades: 0.0714 |
| Top-1 Trade | 16.1% of gross profit | Moderate concentration |
| Top-3 Trades | 43.9% of gross profit | Moderate concentration |
| Return ex-Top-1 | 1492.1% | Positive without best trade |
| Return ex-Top-3 | 576.9% | Positive without top 3 |
| Max Single Trade | 61.8% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 13 | 28.46% | 370.0% | 24.95% | 72.00 |
| no_signal | 1 | 13.99% | 14.0% | 13.25% | 39.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 4 | 36.71% | 146.8% | 100.0% | 100.0% | 31.23% |
| strong_positive | 3 | 31.83% | 95.5% | 100.0% | 100.0% | 31.52% |
| weak_negative | 1 | 58.92% | 58.9% | 100.0% | 100.0% | 76.24% |
| strong_negative | 4 | 14.49% | 58.0% | 100.0% | 100.0% | 9.60% |
| regime_shift | 2 | 12.39% | 24.8% | 100.0% | 100.0% | 1.76% |

**Best-performing regime:** `unknown` — 4 trades, 146.8% total return, 100.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ✅ | 11 | 29.95% | 329.4% |
| ✅ | ✅ | 2 | 20.29% | 40.6% |

### Flip Trades (Signal Wrong → Direction Right)

**12 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **28.6%**
- Total return: **343.4%**
- Average alpha: **25.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 4 | 36.71% |
| strong_negative | 3 | 12.36% |
| regime_shift | 2 | 12.39% |
| strong_positive | 2 | 37.91% |
| weak_negative | 1 | 58.92% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 4 | 39.60% | 158.4% | 100.0% | 100.0% |
| low | 5 | 29.96% | 149.8% | 100.0% | 100.0% |
| high | 5 | 15.17% | 75.8% | 100.0% | 100.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 8 | 27.76% | 222.1% | 100.0% | 100.0% |
| SHORT | 6 | 26.99% | 161.9% | 100.0% | 100.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 2 | 57.0% | 28.52% | 100.0% | 100.0% | 45.7% |
| 2019 | 2 | 89.8% | 44.90% | 100.0% | 100.0% | 79.2% |
| 2020 | 1 | 15.8% | 15.81% | 100.0% | 100.0% | 9.4% |
| 2021 | 1 | 58.9% | 58.92% | 100.0% | 100.0% | 76.2% |
| 2022 | 2 | 81.5% | 40.75% | 100.0% | 100.0% | 81.3% |
| 2023 | 4 | 49.3% | 12.32% | 100.0% | 100.0% | 18.8% |
| 2024 | 1 | 17.7% | 17.70% | 100.0% | 100.0% | 13.7% |
| 2025 | 1 | 14.0% | 13.99% | 100.0% | 100.0% | 13.2% |

### Macro Context by Year

**2018** (Strong year: 57.0%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 89.8%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 15.8%, 1 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 58.9%, 1 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 81.5%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 49.3%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 17.7%, 1 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 14.0%, 1 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** 0.0% cumulative (trade 1 to trade 1)
**Period:** 2018-03-13 to 2018-03-13 (1 trades)
**Peak cumulative return:** 41.6% → **Trough:** 41.6%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2018-03-13 | 2018-09-12 | 1.0000 | 41.57% | unknown | ✅ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 31-50d | 1 | 13.99% | 14.0% | 100.0% |
| 50d+ | 13 | 28.46% | 370.0% | 100.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 14
- **Max consecutive losses:** 0

## Observations & Caveats

**Sample size:** ⚠️ Only 14 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Well-distributed. HHI of 0.1044 is near the theoretical minimum of 0.0714 for 14 trades.
**Win/loss profile:** 100.0% win rate with inf× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (100.0%) exceeded signal accuracy (15.4%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **EXIT_EDGE:** 100% or near-100% win rate with `signal_change` exit suggests the exit is doing the heavy lifting. The strategy holds until profitable and never exits at a loss. Test with `fixed_holding_30d` or `fixed_holding_60d` to see if win rate drops significantly.
- **FLIP_OVERFITTING:** Signal accuracy is only 15.4% but win rate is 100.0%. The correlation flip mechanism is compensating for poor signal quality. This suggests the flip is overfitting to historical correlation regimes, which may not persist.
- **SUSPICIOUSLY_PERFECT:** Profit factor of inf with only 14 trades suggests the strategy may be avoiding losses through exit timing rather than signal skill. These results almost always degrade catastrophically out of sample.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.