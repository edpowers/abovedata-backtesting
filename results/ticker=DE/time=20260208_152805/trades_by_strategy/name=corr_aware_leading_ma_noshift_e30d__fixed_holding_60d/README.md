# Strategy Analysis: corr_aware_leading_ma_noshift_e30d × fixed_holding_60d

**Ticker:** DE
**Entry:** `corr_aware_leading_ma_noshift_e30d`
**Exit:** `fixed_holding_60d`
**Period:** 2018-07-06 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `leading_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `True` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `fixed_holding_60d`
  - Fixed 60-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 461.5% |
| **Annualized Return** | 12.8% |
| **Sharpe Ratio** | 0.534 |
| **Max Drawdown** | -48.2% |
| **Total Trades** | 33 |
| **Win Rate** | 72.7% |
| **Signal Accuracy** | 57.1% |
| **Direction Accuracy** | 67.9% |
| **Skill Ratio** | 67.9% |
| **Profit Factor** | 3.59 |
| **Expectancy** | 0.0647 |
| **Tail Ratio** | 2.35 |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.3×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0691 | Ideal for 33 trades: 0.0303 |
| Top-1 Trade | 21.4% of gross profit | ⚠️ High concentration |
| Top-3 Trades | 45.1% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 243.6% | Strategy survives without best trade |
| Return ex-Top-3 | 89.8% | Strategy survives without top 3 |
| Max Single Trade | 63.4% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 19 | 13.09% | 248.7% | 11.62% | 53.74 |
| no_signal | 5 | 9.50% | 47.5% | 6.38% | 36.60 |
| direction_wrong_loss | 9 | -9.18% | -82.6% | -13.22% | 42.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 5 | 28.53% | 142.6% | 100.0% | 100.0% | 21.44% |
| regime_shift | 11 | 7.20% | 79.2% | 81.8% | 81.8% | 5.73% |
| unknown | 3 | 3.14% | 9.4% | 100.0% | 100.0% | 6.57% |
| strong_positive | 5 | 1.05% | 5.3% | 60.0% | 60.0% | -1.56% |
| weak_positive | 5 | -0.19% | -0.9% | 60.0% | 60.0% | -4.78% |
| weak_negative | 4 | -5.50% | -22.0% | 25.0% | 25.0% | -6.14% |

**Best regime:** `strong_negative` — 5 trades, 142.6% total return, 100.0% win rate.
**Worst regime:** `weak_negative` — 4 trades, -22.0% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 3 | -9.19% | -27.6% |
| ❌ | ✅ | 9 | 15.90% | 143.1% |
| ✅ | ❌ | 6 | -9.17% | -55.0% |
| ✅ | ✅ | 10 | 10.56% | 105.6% |

### Flip Trades (Signal Wrong → Direction Right)

**14 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **13.6%**
- Total return: **190.6%**
- Average alpha: **11.6%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 6 | 8.14% |
| strong_negative | 2 | 55.10% |
| weak_positive | 2 | 7.57% |
| unknown | 2 | 1.81% |
| strong_positive | 2 | 6.39% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 22 | 9.98% | 219.6% | 77.3% | 77.3% |
| low | 8 | 0.23% | 1.8% | 75.0% | 75.0% |
| high | 3 | -2.64% | -7.9% | 33.3% | 33.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 16 | 12.16% | 194.5% | 87.5% | 87.5% |
| SHORT | 17 | 1.12% | 19.1% | 58.8% | 58.8% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 3 | 9.4% | 3.14% | 100.0% | 100.0% | 19.7% |
| 2019 | 6 | 8.2% | 1.36% | 66.7% | 66.7% | -26.2% |
| 2020 | 3 | 126.9% | 42.29% | 100.0% | 100.0% | 111.0% |
| 2021 | 3 | 7.4% | 2.47% | 33.3% | 33.3% | -1.1% |
| 2022 | 6 | -18.0% | -3.01% | 66.7% | 66.7% | -5.1% |
| 2023 | 3 | 19.2% | 6.39% | 66.7% | 66.7% | 4.6% |
| 2024 | 4 | 13.1% | 3.27% | 50.0% | 50.0% | -1.2% |
| 2025 | 5 | 47.5% | 9.50% | 100.0% | 100.0% | 31.9% |

### Macro Context by Year

**2018** (Modestly positive: 9.4%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 8.2%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 126.9%, 3 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 7.4%, 3 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -18.0%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 19.2%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 13.1%, 4 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 47.5%, 5 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -36.8% cumulative (trade 16 to trade 18)
**Period:** 2022-01-06 to 2022-07-08 (3 trades)
**Peak cumulative return:** 154.2% → **Trough:** 117.5%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-01-06 | 2022-05-17 | 1.0000 | 2.36% | strong_positive | ✅ |
| 2022-05-18 | 2022-07-08 | 1.0000 | -17.06% | weak_positive | ❌ |
| 2022-07-08 | 2022-08-17 | -1.0000 | -19.71% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 16-30d | 9 | 1.55% | 13.9% | 66.7% |
| 31-50d | 11 | 0.15% | 1.7% | 72.7% |
| 50d+ | 13 | 15.23% | 198.0% | 76.9% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 2

## Conclusions & Observations

**Statistical robustness:** 33 trades provides a reasonable sample, though some metrics may have wide confidence intervals.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (89.8% remaining).
**Edge:** Genuine structural edge: 72.7% win rate with 3.59× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (67.9%) exceeds signal accuracy (57.1%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Worst year:** 2022 (-18.0%, 6 trades). Macro: Fed Tightening Cycle, 2022 Bear Market
- **Losing regime:** `weak_positive` — 5 trades, -0.9% total return
- **Losing regime:** `weak_negative` — 4 trades, -22.0% total return