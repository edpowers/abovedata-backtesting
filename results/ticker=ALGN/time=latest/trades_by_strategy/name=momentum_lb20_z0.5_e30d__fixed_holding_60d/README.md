# Strategy Analysis: momentum_lb20_z0.5_e30d × fixed_holding_60d

**Ticker:** ALGN
**Entry:** `momentum_lb20_z0.5_e30d`
**Exit:** `fixed_holding_60d`
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

- **Exit type:** `fixed_holding_60d`
  - Fixed 60-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 1192.0% |
| **Annualized Return** | 24.3% |
| **Sharpe Ratio** | 0.675 |
| **Max Drawdown** | -66.3% |
| **Total Trades** | 20 |
| **Win Rate** | 100.0% |
| **Signal Accuracy** | 15.8% |
| **Direction Accuracy** | 100.0% |
| **Skill Ratio** | 100.0% |
| **Profit Factor** | inf |
| **Expectancy** | 0.2056 |
| **Tail Ratio** | 24.57 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 235.5% | 1192.0% | 956.4% |
| Annualized Return | 11.5% | 24.3% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0733 | Ideal for 20 trades: 0.0500 |
| Top-1 Trade | 14.3% of gross profit | Moderate concentration |
| Top-3 Trades | 34.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 2229.7% | Positive without best trade |
| Return ex-Top-3 | 1080.4% | Positive without top 3 |
| Max Single Trade | 58.9% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 19 | 20.91% | 397.3% | 19.06% | 50.53 |
| no_signal | 1 | 13.99% | 14.0% | 13.25% | 39.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 7 | 24.61% | 172.3% | 100.0% | 100.0% | 23.46% |
| strong_positive | 4 | 22.09% | 88.4% | 100.0% | 100.0% | 21.84% |
| strong_negative | 5 | 12.69% | 63.4% | 100.0% | 100.0% | 8.05% |
| weak_negative | 1 | 58.92% | 58.9% | 100.0% | 100.0% | 76.24% |
| regime_shift | 3 | 9.43% | 28.3% | 100.0% | 100.0% | 2.45% |

**Best-performing regime:** `unknown` — 7 trades, 172.3% total return, 100.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ✅ | 16 | 22.25% | 355.9% |
| ✅ | ✅ | 3 | 13.78% | 41.3% |

### Flip Trades (Signal Wrong → Direction Right)

**17 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **21.8%**
- Total return: **369.9%**
- Average alpha: **20.0%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 7 | 24.61% |
| strong_positive | 3 | 22.90% |
| strong_negative | 3 | 13.92% |
| regime_shift | 3 | 9.43% |
| weak_negative | 1 | 58.92% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 8 | 21.90% | 175.2% | 100.0% | 100.0% |
| medium | 6 | 25.79% | 154.8% | 100.0% | 100.0% |
| high | 6 | 13.55% | 81.3% | 100.0% | 100.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 12 | 18.11% | 217.3% | 100.0% | 100.0% |
| SHORT | 8 | 24.25% | 194.0% | 100.0% | 100.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 3 | 55.8% | 18.60% | 100.0% | 100.0% | 44.7% |
| 2019 | 3 | 85.2% | 28.40% | 100.0% | 100.0% | 74.1% |
| 2020 | 2 | 47.1% | 23.54% | 100.0% | 100.0% | 54.8% |
| 2021 | 1 | 58.9% | 58.92% | 100.0% | 100.0% | 76.2% |
| 2022 | 2 | 47.1% | 23.56% | 100.0% | 100.0% | 44.7% |
| 2023 | 6 | 64.6% | 10.77% | 100.0% | 100.0% | 39.5% |
| 2024 | 2 | 38.6% | 19.28% | 100.0% | 100.0% | 28.1% |
| 2025 | 1 | 14.0% | 13.99% | 100.0% | 100.0% | 13.2% |

### Macro Context by Year

**2018** (Strong year: 55.8%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 85.2%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 47.1%, 2 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 58.9%, 1 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 47.1%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 64.6%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 38.6%, 2 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 14.0%, 1 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** 0.0% cumulative (trade 1 to trade 1)
**Period:** 2018-03-13 to 2018-03-13 (1 trades)
**Peak cumulative return:** 39.2% → **Trough:** 39.2%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2018-03-13 | 2018-07-20 | 1.0000 | 39.18% | unknown | ✅ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 16-30d | 5 | 15.07% | 75.4% | 100.0% |
| 31-50d | 6 | 15.52% | 93.1% | 100.0% |
| 50d+ | 9 | 26.97% | 242.8% | 100.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 20
- **Max consecutive losses:** 0

## Observations & Caveats

**Sample size:** ⚠️ Only 20 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Well-distributed. HHI of 0.0733 is near the theoretical minimum of 0.0500 for 20 trades.
**Win/loss profile:** 100.0% win rate with inf× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (100.0%) exceeded signal accuracy (15.8%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **FLIP_OVERFITTING:** Signal accuracy is only 15.8% but win rate is 100.0%. The correlation flip mechanism is compensating for poor signal quality. This suggests the flip is overfitting to historical correlation regimes, which may not persist.
- **SUSPICIOUSLY_PERFECT:** Profit factor of inf with only 20 trades suggests the strategy may be avoiding losses through exit timing rather than signal skill. These results almost always degrade catastrophically out of sample.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.