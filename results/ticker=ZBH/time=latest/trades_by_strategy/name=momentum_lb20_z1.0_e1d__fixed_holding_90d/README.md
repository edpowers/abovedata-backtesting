# Strategy Analysis: momentum_lb20_z1.0_e1d × fixed_holding_90d

**Ticker:** ZBH
**Entry:** `momentum_lb20_z1.0_e1d`
**Exit:** `fixed_holding_90d`
**Period:** 2018-04-25 to 2025-08-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `1.0`
- **zscore_window:** `60`
- **entry_days_before:** `1` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `fixed_holding_90d`
  - Fixed 90-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 161.7% |
| **Annualized Return** | 8.3% |
| **Sharpe Ratio** | 0.419 |
| **Max Drawdown** | -56.2% |
| **Total Trades** | 17 |
| **Win Rate** | 76.5% |
| **Signal Accuracy** | 37.5% |
| **Direction Accuracy** | 75.0% |
| **Skill Ratio** | 75.0% |
| **Profit Factor** | 4.66 |
| **Expectancy** | 0.0626 |
| **Tail Ratio** | 1.33 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -10.7% | 161.7% | 172.4% |
| Annualized Return | -1.0% | 8.3% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.4×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0809 | Ideal for 17 trades: 0.0588 |
| Top-1 Trade | 15.3% of gross profit | Moderate concentration |
| Top-3 Trades | 40.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 116.8% | Positive without best trade |
| Return ex-Top-3 | 57.5% | Positive without top 3 |
| Max Single Trade | 20.7% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 12 | 10.40% | 124.9% | 8.38% | 70.58 |
| no_signal | 1 | 10.74% | 10.7% | -1.24% | 65.00 |
| direction_wrong_loss | 4 | -7.27% | -29.1% | -16.79% | 61.25 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 6 | 10.60% | 63.6% | 100.0% | 100.0% | 9.02% |
| regime_shift | 6 | 5.26% | 31.5% | 66.7% | 66.7% | 0.25% |
| weak_positive | 3 | 8.25% | 24.8% | 66.7% | 66.7% | -1.77% |
| strong_positive | 1 | 2.12% | 2.1% | 100.0% | 100.0% | 8.13% |
| weak_negative | 1 | -15.53% | -15.5% | 0.0% | 0.0% | -26.26% |

**Best-performing regime:** `unknown` — 6 trades, 63.6% total return, 100.0% win rate.
**Worst-performing regime:** `weak_negative` — 1 trades, -15.5% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 2 | -6.62% | -13.2% |
| ❌ | ✅ | 8 | 10.70% | 85.6% |
| ✅ | ❌ | 2 | -7.93% | -15.9% |
| ✅ | ✅ | 4 | 9.81% | 39.2% |

### Flip Trades (Signal Wrong → Direction Right)

**9 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **10.7%**
- Total return: **96.4%**
- Average alpha: **6.8%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 5 | 9.17% |
| regime_shift | 2 | 15.72% |
| strong_positive | 1 | 2.12% |
| weak_positive | 1 | 16.93% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 7 | 10.25% | 71.8% | 100.0% | 100.0% |
| high | 3 | 5.95% | 17.9% | 66.7% | 66.7% |
| medium | 7 | 2.41% | 16.9% | 57.1% | 57.1% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 9 | 4.85% | 43.7% | 66.7% | 66.7% |
| SHORT | 8 | 7.85% | 62.8% | 87.5% | 87.5% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 2 | 21.0% | 10.50% | 100.0% | 100.0% | 17.1% |
| 2019 | 3 | 24.9% | 8.29% | 100.0% | 100.0% | 10.0% |
| 2020 | 3 | 5.1% | 1.69% | 66.7% | 66.7% | -3.4% |
| 2021 | 1 | -8.3% | -8.26% | 0.0% | 0.0% | -13.2% |
| 2022 | 2 | 12.6% | 6.30% | 100.0% | 100.0% | 19.7% |
| 2023 | 3 | 37.3% | 12.44% | 66.7% | 66.7% | 16.4% |
| 2024 | 2 | 3.2% | 1.58% | 50.0% | 50.0% | -13.3% |
| 2025 | 1 | 10.7% | 10.74% | 100.0% | 100.0% | -1.2% |

### Macro Context by Year

**2018** (Strong year: 21.0%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 24.9%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Modestly positive: 5.1%, 3 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -8.3%, 1 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 12.6%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 37.3%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 3.2%, 2 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 10.7%, 1 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -23.8% cumulative (trade 7 to trade 9)
**Period:** 2020-08-03 to 2021-05-03 (3 trades)
**Peak cumulative return:** 66.5% → **Trough:** 42.7%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-08-03 | 2020-11-05 | 1.0000 | 2.86% | regime_shift | ✅ |
| 2020-11-05 | 2021-02-04 | -1.0000 | -15.53% | weak_negative | ❌ |
| 2021-05-03 | 2021-08-02 | 1.0000 | -8.26% | regime_shift | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 50d+ | 17 | 6.26% | 106.5% | 76.5% |

## Win/Loss Streaks

- **Max consecutive wins:** 7
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 17 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Well-distributed. HHI of 0.0809 is near the theoretical minimum of 0.0588 for 17 trades.
**Win/loss profile:** 76.5% win rate with 4.66× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (75.0%) exceeded signal accuracy (37.5%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2021 (-8.3%, 1 trades). Macro: Post-COVID Stimulus Rally
- **Losing regime:** `weak_negative` — 1 trades, -15.5% total return

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.