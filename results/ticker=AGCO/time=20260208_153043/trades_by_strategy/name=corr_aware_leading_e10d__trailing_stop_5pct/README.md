# Strategy Analysis: corr_aware_leading_e10d × trailing_stop_5%

**Ticker:** AGCO
**Entry:** `corr_aware_leading_e10d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-07-17 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `leading` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `10` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 345.0% |
| **Annualized Return** | 59.4% |
| **Sharpe Ratio** | 2.238 |
| **Max Drawdown** | -20.3% |
| **Total Trades** | 130 |
| **Win Rate** | 50.8% |
| **Signal Accuracy** | 57.3% |
| **Direction Accuracy** | 51.8% |
| **Skill Ratio** | 51.8% |
| **Profit Factor** | 1.61 |
| **Expectancy** | 0.0147 |
| **Tail Ratio** | 1.94 |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.7×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0133 | Ideal for 130 trades: 0.0077 |
| Top-1 Trade | 6.0% of gross profit | ✅ Low concentration |
| Top-3 Trades | 15.9% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 241.1% | Strategy survives without best trade |
| Return ex-Top-3 | 118.9% | Strategy survives without top 3 |
| Max Single Trade | 30.5% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 57 | 8.08% | 460.4% | 5.53% | 19.19 |
| no_signal | 20 | -0.92% | -18.4% | -1.55% | 11.30 |
| direction_wrong_loss | 53 | -4.73% | -250.8% | -3.97% | 8.72 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 57 | 2.83% | 161.2% | 56.1% | 56.1% | 1.39% |
| weak_positive | 14 | 3.12% | 43.6% | 71.4% | 71.4% | 2.65% |
| weak_negative | 13 | 2.77% | 36.0% | 61.5% | 61.5% | 2.45% |
| unknown | 5 | 1.24% | 6.2% | 40.0% | 40.0% | 1.05% |
| strong_negative | 13 | -0.45% | -5.9% | 38.5% | 38.5% | -1.30% |
| strong_positive | 28 | -1.79% | -50.0% | 32.1% | 32.1% | -2.23% |

**Best regime:** `regime_shift` — 57 trades, 161.2% total return, 56.1% win rate.
**Worst regime:** `strong_positive` — 28 trades, -50.0% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 20 | -4.34% | -86.8% |
| ❌ | ✅ | 27 | 7.27% | 196.4% |
| ✅ | ❌ | 33 | -4.97% | -164.0% |
| ✅ | ✅ | 30 | 8.80% | 264.0% |

### Flip Trades (Signal Wrong → Direction Right)

**36 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **6.7%**
- Total return: **240.2%**
- Average alpha: **5.5%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 16 | 7.59% |
| weak_positive | 7 | 6.75% |
| strong_positive | 5 | 6.07% |
| weak_negative | 5 | 5.36% |
| strong_negative | 3 | 4.81% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 89 | 2.11% | 188.1% | 51.7% | 51.7% |
| low | 10 | 0.78% | 7.8% | 50.0% | 50.0% |
| high | 31 | -0.15% | -4.8% | 48.4% | 48.4% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 81 | 2.15% | 173.8% | 51.9% | 51.9% |
| SHORT | 49 | 0.35% | 17.3% | 49.0% | 49.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 7 | 16.3% | 2.33% | 42.9% | 42.9% | 19.3% |
| 2019 | 14 | -7.3% | -0.52% | 35.7% | 35.7% | -25.0% |
| 2020 | 19 | 67.8% | 3.57% | 42.1% | 42.1% | 41.3% |
| 2021 | 16 | 37.2% | 2.32% | 75.0% | 75.0% | 15.2% |
| 2022 | 22 | 99.0% | 4.50% | 63.6% | 63.6% | 92.2% |
| 2023 | 14 | 5.6% | 0.40% | 42.9% | 42.9% | -8.7% |
| 2024 | 16 | -14.9% | -0.93% | 43.8% | 43.8% | -35.6% |
| 2025 | 21 | 4.4% | 0.21% | 52.4% | 52.4% | -8.1% |
| 2026 | 1 | -17.0% | -17.04% | 0.0% | 0.0% | -16.8% |

### Macro Context by Year

**2018** (Strong year: 16.3%, 7 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -7.3%, 14 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 67.8%, 19 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 37.2%, 16 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 99.0%, 22 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 5.6%, 14 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -14.9%, 16 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 4.4%, 21 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -17.0%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -68.8% cumulative (trade 8 to trade 29)
**Period:** 2019-01-22 to 2020-03-19 (22 trades)
**Peak cumulative return:** 18.5% → **Trough:** -50.2%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2019-01-22 | 2019-01-23 | -1.0000 | 2.23% | strong_positive | ✅ |
| 2019-01-24 | 2019-02-01 | -1.0000 | -5.32% | strong_positive | ❌ |
| 2019-02-04 | 2019-02-21 | -1.0000 | -1.28% | strong_positive | ❌ |
| 2019-02-22 | 2019-03-29 | -1.0000 | -3.88% | strong_negative | ❌ |
| 2019-04-01 | 2019-04-17 | -1.0000 | -3.02% | strong_negative | ❌ |
| 2019-04-17 | 2019-05-02 | 1.0000 | 3.25% | strong_negative | ✅ |
| 2019-05-03 | 2019-05-13 | 1.0000 | -5.60% | strong_negative | ❌ |
| 2019-05-14 | 2019-05-17 | 1.0000 | -5.59% | strong_negative | ❌ |
| 2019-05-20 | 2019-08-01 | 1.0000 | 12.21% | strong_negative | ✅ |
| 2019-08-02 | 2019-08-12 | 1.0000 | -7.26% | weak_negative | ❌ |
| 2019-08-13 | 2019-08-14 | 1.0000 | -5.27% | weak_negative | ❌ |
| 2019-08-15 | 2019-10-02 | 1.0000 | 9.50% | weak_negative | ✅ |
| 2019-10-03 | 2019-12-03 | 1.0000 | 5.99% | weak_negative | ✅ |
| 2019-12-04 | 2020-01-10 | 1.0000 | -3.24% | regime_shift | ❌ |
| 2020-01-13 | 2020-01-27 | 1.0000 | -7.25% | regime_shift | ❌ |
| 2020-01-28 | 2020-02-06 | 1.0000 | -1.58% | regime_shift | ❌ |
| 2020-02-07 | 2020-02-25 | 1.0000 | -3.74% | strong_positive | ❌ |
| 2020-02-26 | 2020-03-09 | 1.0000 | -8.51% | strong_positive | ❌ |
| 2020-03-10 | 2020-03-11 | 1.0000 | -5.61% | strong_positive | ❌ |
| 2020-03-12 | 2020-03-16 | 1.0000 | -4.63% | strong_positive | ❌ |
| 2020-03-17 | 2020-03-18 | 1.0000 | -18.78% | strong_positive | ❌ |
| 2020-03-19 | 2020-03-20 | 1.0000 | -9.17% | strong_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 26 | -3.76% | -97.8% | 23.1% |
| 16-30d | 30 | 6.43% | 193.0% | 76.7% |
| 31-50d | 8 | 12.08% | 96.6% | 100.0% |
| 50d+ | 2 | 7.76% | 15.5% | 100.0% |
| 6-15d | 64 | -0.25% | -16.2% | 42.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 8
- **Max consecutive losses:** 9

## Conclusions & Observations

**Statistical robustness:** With 130 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (118.9% remaining).
**Edge:** Genuine structural edge: 50.8% win rate with 1.61× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Signal accuracy (57.3%) exceeds direction accuracy (51.8%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities

- **Worst year:** 2026 (-17.0%, 1 trades). Macro: No flagged events
- **Losing regime:** `strong_negative` — 13 trades, -5.9% total return
- **Losing regime:** `strong_positive` — 28 trades, -50.0% total return