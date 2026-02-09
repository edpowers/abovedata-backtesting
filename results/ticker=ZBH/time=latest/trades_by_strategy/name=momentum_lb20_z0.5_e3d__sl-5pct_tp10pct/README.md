# Strategy Analysis: momentum_lb20_z0.5_e3d × sl-5%_tp10%

**Ticker:** ZBH
**Entry:** `momentum_lb20_z0.5_e3d`
**Exit:** `sl-5%_tp10%`
**Period:** 2018-04-23 to 2025-08-04
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `3` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit targets a 2:1 reward/risk ratio

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 155.7% |
| **Annualized Return** | 6.0% |
| **Sharpe Ratio** | 0.339 |
| **Max Drawdown** | -36.3% |
| **Total Trades** | 86 |
| **Win Rate** | 52.3% |
| **Signal Accuracy** | 25.3% |
| **Direction Accuracy** | 51.9% |
| **Skill Ratio** | 51.9% |
| **Profit Factor** | 1.53 |
| **Expectancy** | 0.0136 |
| **Tail Ratio** | 1.34 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -10.7% | 155.7% | 166.4% |
| Annualized Return | -1.0% | 6.0% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0152 | Ideal for 86 trades: 0.0116 |
| Top-1 Trade | 4.3% of gross profit | Moderate concentration |
| Top-3 Trades | 12.2% of gross profit | Moderate concentration |
| Return ex-Top-1 | 123.3% | Positive without best trade |
| Return ex-Top-3 | 73.9% | Positive without top 3 |
| Max Single Trade | 14.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 41 | 7.37% | 302.3% | 6.61% | 17.44 |
| no_signal | 7 | 2.69% | 18.8% | 2.72% | 16.14 |
| direction_wrong_loss | 38 | -5.37% | -204.1% | -6.89% | 15.03 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 17 | 2.45% | 41.6% | 58.8% | 58.8% | 1.34% |
| strong_negative | 17 | 2.15% | 36.5% | 58.8% | 58.8% | 2.82% |
| regime_shift | 21 | 1.57% | 33.0% | 52.4% | 52.4% | 0.21% |
| strong_positive | 10 | 2.92% | 29.2% | 60.0% | 60.0% | 0.64% |
| weak_positive | 9 | 2.65% | 23.8% | 55.6% | 55.6% | 1.92% |
| weak_negative | 12 | -3.94% | -47.2% | 25.0% | 25.0% | -5.92% |

**Best-performing regime:** `unknown` — 17 trades, 41.6% total return, 58.8% win rate.
**Worst-performing regime:** `weak_negative` — 12 trades, -47.2% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 29 | -5.05% | -146.6% |
| ❌ | ✅ | 30 | 7.38% | 221.3% |
| ✅ | ❌ | 9 | -6.39% | -57.5% |
| ✅ | ✅ | 11 | 7.36% | 80.9% |

### Flip Trades (Signal Wrong → Direction Right)

**34 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **7.5%**
- Total return: **256.6%**
- Average alpha: **7.6%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_negative | 10 | 7.86% |
| unknown | 9 | 7.73% |
| regime_shift | 7 | 7.16% |
| strong_positive | 4 | 8.86% |
| weak_positive | 3 | 7.48% |
| weak_negative | 1 | 0.50% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 52 | 1.17% | 60.8% | 50.0% | 50.0% |
| low | 18 | 2.88% | 51.9% | 61.1% | 61.1% |
| high | 16 | 0.27% | 4.2% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 45 | 1.95% | 87.6% | 55.6% | 55.6% |
| SHORT | 41 | 0.72% | 29.3% | 48.8% | 48.8% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 5 | 26.3% | 5.25% | 60.0% | 60.0% | 27.6% |
| 2019 | 11 | 19.0% | 1.73% | 63.6% | 63.6% | -0.7% |
| 2020 | 28 | 32.8% | 1.17% | 50.0% | 50.0% | 30.6% |
| 2021 | 5 | -15.1% | -3.02% | 40.0% | 40.0% | -28.1% |
| 2022 | 7 | 25.6% | 3.66% | 57.1% | 57.1% | 14.6% |
| 2023 | 14 | 21.8% | 1.55% | 50.0% | 50.0% | 1.1% |
| 2024 | 8 | -3.7% | -0.47% | 50.0% | 50.0% | -26.6% |
| 2025 | 8 | 10.3% | 1.29% | 50.0% | 50.0% | 9.3% |

### Macro Context by Year

**2018** (Strong year: 26.3%, 5 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 19.0%, 11 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 32.8%, 28 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -15.1%, 5 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 25.6%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 21.8%, 14 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Roughly flat: -3.7%, 8 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 10.3%, 8 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -45.8% cumulative (trade 39 to trade 50)
**Period:** 2020-09-21 to 2022-07-28 (12 trades)
**Peak cumulative return:** 105.2% → **Trough:** 59.4%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-09-21 | 2020-10-08 | 1.0000 | 9.64% | weak_negative | ✅ |
| 2020-10-09 | 2020-10-26 | 1.0000 | -5.73% | weak_negative | ❌ |
| 2020-10-27 | 2020-10-29 | 1.0000 | -3.43% | weak_negative | ❌ |
| 2020-10-30 | 2020-11-03 | 1.0000 | 3.26% | weak_negative | ✅ |
| 2020-11-03 | 2020-11-09 | -1.0000 | -14.32% | weak_negative | ❌ |
| 2020-11-10 | 2021-01-06 | -1.0000 | -6.89% | weak_negative | ❌ |
| 2021-01-07 | 2021-02-02 | -1.0000 | 0.50% | weak_negative | ✅ |
| 2021-04-29 | 2021-05-11 | 1.0000 | -6.19% | regime_shift | ❌ |
| 2021-05-12 | 2021-07-14 | 1.0000 | -4.86% | regime_shift | ❌ |
| 2021-07-15 | 2021-08-10 | 1.0000 | -4.79% | regime_shift | ❌ |
| 2021-08-11 | 2021-11-01 | 1.0000 | 0.22% | regime_shift | ✅ |
| 2022-07-28 | 2022-09-01 | 1.0000 | -3.59% | strong_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 36 | 0.23% | 8.1% | 47.2% |
| 16-30d | 14 | 2.56% | 35.8% | 57.1% |
| 31-50d | 10 | 3.61% | 36.1% | 60.0% |
| 50d+ | 7 | 0.78% | 5.5% | 57.1% |
| 6-15d | 19 | 1.66% | 31.5% | 52.6% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 4

## Observations & Caveats

**Sample size:** 86 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Well-distributed. HHI of 0.0152 is near the theoretical minimum of 0.0116 for 86 trades.
**Win/loss profile:** 52.3% win rate with 1.53× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (51.9%) exceeded signal accuracy (25.3%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2021 (-15.1%, 5 trades). Macro: Post-COVID Stimulus Rally
- **Losing regime:** `weak_negative` — 12 trades, -47.2% total return

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.