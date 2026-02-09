# Strategy Analysis: corr_aware_contemp_e30d × trailing_stop_5%

**Ticker:** DE
**Entry:** `corr_aware_contemp_e30d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-07-06 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 124.0% |
| **Annualized Return** | 34.0% |
| **Sharpe Ratio** | 1.703 |
| **Max Drawdown** | -24.1% |
| **Total Trades** | 243 |
| **Win Rate** | 46.9% |
| **Signal Accuracy** | 51.2% |
| **Direction Accuracy** | 47.4% |
| **Skill Ratio** | 47.4% |
| **Profit Factor** | 1.29 |
| **Expectancy** | 0.0047 |
| **Tail Ratio** | 1.86 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 701.3% | 124.0% | -577.3% |
| Annualized Return | 20.7% | 34.0% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.1×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0088 | Ideal for 243 trades: 0.0041 |
| Top-1 Trade | 7.3% of gross profit | ✅ Low concentration |
| Top-3 Trades | 16.3% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 62.9% | Strategy survives without best trade |
| Return ex-Top-3 | 7.8% | Strategy survives without top 3 |
| Max Single Trade | 37.5% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 100 | 4.76% | 475.7% | 3.45% | 9.15 |
| no_signal | 32 | -0.62% | -20.0% | -1.26% | 6.75 |
| direction_wrong_loss | 111 | -3.07% | -341.3% | -2.87% | 4.88 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 30 | 2.85% | 85.6% | 53.3% | 53.3% | 1.72% |
| regime_shift | 67 | 0.34% | 22.5% | 46.3% | 46.3% | -0.46% |
| unknown | 12 | 1.54% | 18.5% | 58.3% | 58.3% | 1.93% |
| weak_positive | 38 | 0.06% | 2.4% | 42.1% | 42.1% | -0.44% |
| strong_positive | 51 | -0.02% | -1.2% | 47.1% | 47.1% | -0.47% |
| weak_negative | 45 | -0.29% | -13.2% | 44.4% | 44.4% | -0.40% |

**Best regime:** `strong_negative` — 30 trades, 85.6% total return, 53.3% win rate.
**Worst regime:** `weak_negative` — 45 trades, -13.2% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 56 | -3.41% | -190.7% |
| ❌ | ✅ | 47 | 5.29% | 248.5% |
| ✅ | ❌ | 55 | -2.74% | -150.6% |
| ✅ | ✅ | 53 | 4.29% | 227.3% |

### Flip Trades (Signal Wrong → Direction Right)

**61 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **4.7%**
- Total return: **284.2%**
- Average alpha: **3.7%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 18 | 3.55% |
| strong_positive | 13 | 4.21% |
| weak_negative | 11 | 4.51% |
| strong_negative | 10 | 8.65% |
| unknown | 5 | 4.44% |
| weak_positive | 4 | 1.82% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 162 | 0.54% | 88.1% | 50.6% | 50.6% |
| low | 47 | 0.89% | 41.9% | 44.7% | 44.7% |
| high | 34 | -0.46% | -15.5% | 32.4% | 32.4% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 153 | 1.04% | 159.9% | 51.6% | 51.6% |
| SHORT | 90 | -0.50% | -45.4% | 38.9% | 38.9% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 21 | 26.8% | 1.28% | 66.7% | 66.7% | 40.4% |
| 2019 | 31 | 13.8% | 0.45% | 45.2% | 45.2% | -16.8% |
| 2020 | 39 | 67.8% | 1.74% | 56.4% | 56.4% | 59.7% |
| 2021 | 35 | -54.1% | -1.55% | 34.3% | 34.3% | -85.2% |
| 2022 | 37 | 48.3% | 1.31% | 45.9% | 45.9% | 42.7% |
| 2023 | 26 | 17.3% | 0.66% | 42.3% | 42.3% | -5.4% |
| 2024 | 19 | 3.0% | 0.16% | 42.1% | 42.1% | -18.3% |
| 2025 | 29 | 12.4% | 0.43% | 55.2% | 55.2% | -10.6% |
| 2026 | 6 | -20.8% | -3.46% | 0.0% | 0.0% | -20.8% |

### Macro Context by Year

**2018** (Strong year: 26.8%, 21 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 13.8%, 31 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 67.8%, 39 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -54.1%, 35 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 48.3%, 37 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 17.3%, 26 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 3.0%, 19 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 12.4%, 29 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -20.8%, 6 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -59.3% cumulative (trade 93 to trade 133)
**Period:** 2021-01-13 to 2022-02-18 (41 trades)
**Peak cumulative return:** 110.4% → **Trough:** 51.2%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2021-01-13 | 2021-01-28 | -1.0000 | 2.74% | strong_negative | ✅ |
| 2021-01-29 | 2021-02-02 | -1.0000 | -4.76% | strong_negative | ❌ |
| 2021-02-03 | 2021-02-08 | -1.0000 | -5.28% | strong_negative | ❌ |
| 2021-02-09 | 2021-02-19 | -1.0000 | -4.65% | strong_negative | ❌ |
| 2021-02-22 | 2021-02-24 | -1.0000 | -2.41% | weak_negative | ❌ |
| 2021-02-25 | 2021-03-01 | -1.0000 | -3.30% | weak_negative | ❌ |
| 2021-03-02 | 2021-03-05 | -1.0000 | 0.46% | weak_negative | ✅ |
| 2021-03-08 | 2021-03-11 | -1.0000 | -3.04% | weak_negative | ❌ |
| 2021-03-12 | 2021-03-18 | -1.0000 | -2.96% | weak_negative | ❌ |
| 2021-03-19 | 2021-03-26 | -1.0000 | 0.05% | weak_negative | ✅ |
| 2021-03-29 | 2021-04-09 | -1.0000 | -2.71% | weak_negative | ❌ |
| 2021-04-09 | 2021-04-15 | 1.0000 | 1.36% | weak_negative | ✅ |
| 2021-04-16 | 2021-04-20 | 1.0000 | -3.34% | weak_negative | ❌ |
| 2021-04-21 | 2021-05-11 | 1.0000 | 2.02% | weak_negative | ✅ |
| 2021-05-12 | 2021-05-13 | 1.0000 | 1.20% | weak_negative | ✅ |
| 2021-05-14 | 2021-05-19 | 1.0000 | -6.66% | weak_negative | ❌ |
| 2021-05-20 | 2021-06-09 | 1.0000 | -1.60% | weak_negative | ❌ |
| 2021-06-10 | 2021-06-14 | 1.0000 | -1.73% | regime_shift | ❌ |
| 2021-06-15 | 2021-06-17 | 1.0000 | -2.87% | regime_shift | ❌ |
| 2021-06-18 | 2021-07-19 | 1.0000 | 2.08% | regime_shift | ✅ |
| 2021-07-20 | 2021-08-19 | 1.0000 | 3.15% | regime_shift | ✅ |
| 2021-08-20 | 2021-09-07 | 1.0000 | 5.78% | regime_shift | ✅ |
| 2021-09-08 | 2021-09-16 | 1.0000 | -4.02% | strong_positive | ❌ |
| 2021-09-17 | 2021-09-20 | 1.0000 | -2.68% | strong_positive | ❌ |
| 2021-09-21 | 2021-09-30 | 1.0000 | -0.26% | strong_positive | ❌ |
| 2021-10-01 | 2021-10-12 | 1.0000 | -3.39% | strong_positive | ❌ |
| 2021-10-13 | 2021-10-19 | -1.0000 | -4.28% | strong_positive | ❌ |
| 2021-10-20 | 2021-11-01 | -1.0000 | -4.27% | strong_positive | ❌ |
| 2021-11-02 | 2021-11-05 | -1.0000 | 0.03% | strong_positive | ✅ |
| 2021-11-08 | 2021-11-24 | -1.0000 | -1.94% | strong_positive | ❌ |
| 2021-11-26 | 2021-11-29 | -1.0000 | 3.12% | strong_positive | ✅ |
| 2021-11-30 | 2021-12-07 | -1.0000 | -4.57% | strong_positive | ❌ |
| 2021-12-08 | 2021-12-28 | -1.0000 | 3.13% | strong_positive | ✅ |
| 2021-12-29 | 2022-01-04 | -1.0000 | -7.73% | strong_positive | ❌ |
| 2022-01-05 | 2022-01-06 | -1.0000 | -1.16% | strong_positive | ❌ |
| 2022-01-06 | 2022-01-18 | 1.0000 | 2.01% | strong_positive | ✅ |
| 2022-01-19 | 2022-01-20 | 1.0000 | -2.37% | strong_positive | ❌ |
| 2022-01-21 | 2022-01-24 | 1.0000 | -0.07% | strong_positive | ❌ |
| 2022-01-25 | 2022-02-04 | 1.0000 | 0.34% | strong_positive | ✅ |
| 2022-02-07 | 2022-02-17 | 1.0000 | 2.24% | strong_positive | ✅ |
| 2022-02-18 | 2022-02-22 | 1.0000 | -4.15% | strong_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 146 | -0.81% | -118.3% | 37.7% |
| 16-30d | 22 | 5.05% | 111.1% | 72.7% |
| 31-50d | 5 | 12.98% | 64.9% | 100.0% |
| 6-15d | 70 | 0.81% | 56.8% | 54.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 13
- **Max consecutive losses:** 9

## Conclusions & Observations

**Statistical robustness:** With 243 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (7.8% remaining).
**Signal vs Direction:** Signal accuracy (51.2%) exceeds direction accuracy (47.4%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.
**Regime dependence:** `strong_negative` (30 trades, 12% of total) generates 85.6% — a disproportionate share of returns.

### Known Vulnerabilities

- **Worst year:** 2021 (-54.1%, 35 trades). Macro: Post-COVID Stimulus Rally
- **Losing regime:** `strong_positive` — 51 trades, -1.2% total return
- **Losing regime:** `weak_negative` — 45 trades, -13.2% total return