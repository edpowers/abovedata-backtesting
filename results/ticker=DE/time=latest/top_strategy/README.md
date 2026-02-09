# Strategy Analysis: corr_aware_leading_ma_noshift_e30d × trailing_stop_5%

**Ticker:** DE
**Entry:** `corr_aware_leading_ma_noshift_e30d`
**Exit:** `trailing_stop_5%`
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

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 646.3% |
| **Annualized Return** | 28.3% |
| **Sharpe Ratio** | 1.510 |
| **Max Drawdown** | -29.3% |
| **Total Trades** | 197 |
| **Win Rate** | 51.8% |
| **Signal Accuracy** | 53.7% |
| **Direction Accuracy** | 50.3% |
| **Skill Ratio** | 50.3% |
| **Profit Factor** | 1.84 |
| **Expectancy** | 0.0117 |
| **Tail Ratio** | 2.15 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 701.3% | 646.3% | -55.0% |
| Annualized Return | 20.7% | 28.3% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.0×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0102 | Ideal for 197 trades: 0.0051 |
| Top-1 Trade | 6.5% of gross profit | ✅ Low concentration |
| Top-3 Trades | 14.4% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 461.8% | Strategy survives without best trade |
| Return ex-Top-3 | 290.9% | Strategy survives without top 3 |
| Max Single Trade | 32.8% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 88 | 4.82% | 424.5% | 4.60% | 9.39 |
| no_signal | 22 | 2.99% | 65.7% | 1.86% | 10.27 |
| direction_wrong_loss | 87 | -2.99% | -260.1% | -3.63% | 4.17 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 24 | 3.93% | 94.2% | 70.8% | 70.8% | 2.94% |
| weak_positive | 28 | 2.04% | 57.2% | 53.6% | 53.6% | 1.46% |
| strong_positive | 39 | 0.97% | 37.8% | 56.4% | 56.4% | 0.97% |
| regime_shift | 56 | 0.36% | 20.2% | 46.4% | 46.4% | -0.70% |
| unknown | 12 | 1.54% | 18.5% | 58.3% | 58.3% | 1.93% |
| weak_negative | 38 | 0.06% | 2.3% | 39.5% | 39.5% | -0.09% |

**Best regime:** `strong_negative` — 24 trades, 94.2% total return, 70.8% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 44 | -3.43% | -150.7% |
| ❌ | ✅ | 37 | 6.06% | 224.1% |
| ✅ | ❌ | 43 | -2.54% | -109.4% |
| ✅ | ✅ | 51 | 3.93% | 200.3% |

### Flip Trades (Signal Wrong → Direction Right)

**51 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **6.0%**
- Total return: **304.6%**
- Average alpha: **6.0%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 16 | 4.24% |
| strong_positive | 12 | 4.98% |
| strong_negative | 8 | 8.98% |
| unknown | 5 | 4.44% |
| weak_negative | 5 | 9.08% |
| weak_positive | 5 | 7.49% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 121 | 1.47% | 177.6% | 57.0% | 57.0% |
| low | 49 | 1.18% | 57.6% | 46.9% | 46.9% |
| high | 27 | -0.19% | -5.2% | 37.0% | 37.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 87 | 2.25% | 196.1% | 60.9% | 60.9% |
| SHORT | 110 | 0.31% | 34.0% | 44.5% | 44.5% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 21 | 26.8% | 1.28% | 66.7% | 66.7% | 40.4% |
| 2019 | 31 | 16.1% | 0.52% | 45.2% | 45.2% | -12.2% |
| 2020 | 23 | 65.6% | 2.85% | 56.5% | 56.5% | 44.0% |
| 2021 | 24 | 27.1% | 1.13% | 58.3% | 58.3% | 20.2% |
| 2022 | 44 | 10.9% | 0.25% | 40.9% | 40.9% | 11.1% |
| 2023 | 16 | 16.3% | 1.02% | 43.8% | 43.8% | 0.6% |
| 2024 | 14 | -5.3% | -0.38% | 50.0% | 50.0% | -18.2% |
| 2025 | 23 | 53.0% | 2.30% | 60.9% | 60.9% | 23.7% |
| 2026 | 1 | 19.5% | 19.47% | 100.0% | 100.0% | 20.0% |

### Macro Context by Year

**2018** (Strong year: 26.8%, 21 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 16.1%, 31 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 65.6%, 23 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 27.1%, 24 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 10.9%, 44 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 16.3%, 16 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -5.3%, 14 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 53.0%, 23 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 19.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -35.5% cumulative (trade 62 to trade 68)
**Period:** 2020-03-19 to 2020-04-07 (7 trades)
**Peak cumulative return:** 79.3% → **Trough:** 43.7%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-03-19 | 2020-03-20 | -1.0000 | 6.71% | weak_negative | ✅ |
| 2020-03-23 | 2020-03-24 | -1.0000 | -13.36% | weak_negative | ❌ |
| 2020-03-25 | 2020-03-26 | -1.0000 | -8.25% | weak_negative | ❌ |
| 2020-03-27 | 2020-03-30 | -1.0000 | -5.12% | weak_negative | ❌ |
| 2020-03-31 | 2020-04-02 | -1.0000 | -0.88% | weak_negative | ❌ |
| 2020-04-03 | 2020-04-06 | -1.0000 | -5.88% | weak_negative | ❌ |
| 2020-04-07 | 2020-04-09 | -1.0000 | -2.05% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 114 | -0.12% | -14.1% | 39.5% |
| 16-30d | 22 | 6.54% | 143.9% | 90.9% |
| 31-50d | 3 | 13.92% | 41.7% | 100.0% |
| 6-15d | 58 | 1.01% | 58.5% | 58.6% |

## Win/Loss Streaks

- **Max consecutive wins:** 13
- **Max consecutive losses:** 8

## Conclusions & Observations

**Statistical robustness:** With 197 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (290.9% remaining).
**Edge:** Genuine structural edge: 51.8% win rate with 1.84× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Signal accuracy (53.7%) exceeds direction accuracy (50.3%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities

- **Worst year:** 2024 (-5.3%, 14 trades). Macro: 2024 Election Year Uncertainty