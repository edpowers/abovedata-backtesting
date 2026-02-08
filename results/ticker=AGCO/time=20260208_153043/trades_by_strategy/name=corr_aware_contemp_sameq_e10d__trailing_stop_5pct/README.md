# Strategy Analysis: corr_aware_contemp_sameq_e10d × trailing_stop_5%

**Ticker:** AGCO
**Entry:** `corr_aware_contemp_sameq_e10d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-07-17 to 2026-02-06
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
- **entry_days_before:** `10` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 455.1% |
| **Annualized Return** | 62.4% |
| **Sharpe Ratio** | 2.293 |
| **Max Drawdown** | -20.3% |
| **Total Trades** | 130 |
| **Win Rate** | 46.2% |
| **Signal Accuracy** | 60.4% |
| **Direction Accuracy** | 47.7% |
| **Skill Ratio** | 47.7% |
| **Profit Factor** | 1.73 |
| **Expectancy** | 0.0163 |
| **Tail Ratio** | 2.32 |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.8×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0140 | Ideal for 130 trades: 0.0077 |
| Top-1 Trade | 6.0% of gross profit | ✅ Low concentration |
| Top-3 Trades | 17.0% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 325.4% | Strategy survives without best trade |
| Return ex-Top-3 | 161.2% | Strategy survives without top 3 |
| Max Single Trade | 30.5% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 53 | 8.58% | 454.8% | 6.58% | 19.51 |
| no_signal | 19 | -0.47% | -8.9% | -1.70% | 12.26 |
| direction_wrong_loss | 58 | -4.03% | -233.5% | -4.64% | 8.86 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 56 | 2.86% | 160.3% | 46.4% | 46.4% | 1.55% |
| strong_negative | 13 | 2.26% | 29.3% | 53.8% | 53.8% | 0.68% |
| weak_positive | 15 | 1.48% | 22.2% | 53.3% | 53.3% | 0.34% |
| unknown | 5 | 1.24% | 6.2% | 40.0% | 40.0% | 1.05% |
| strong_positive | 26 | -0.08% | -2.2% | 42.3% | 42.3% | -1.91% |
| weak_negative | 15 | -0.23% | -3.5% | 40.0% | 40.0% | -0.59% |

**Best regime:** `regime_shift` — 56 trades, 160.3% total return, 46.4% win rate.
**Worst regime:** `weak_negative` — 15 trades, -3.5% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 24 | -4.30% | -103.1% |
| ❌ | ✅ | 20 | 8.62% | 172.3% |
| ✅ | ❌ | 34 | -3.84% | -130.4% |
| ✅ | ✅ | 33 | 8.56% | 282.5% |

### Flip Trades (Signal Wrong → Direction Right)

**27 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **8.2%**
- Total return: **221.5%**
- Average alpha: **6.0%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 8 | 10.83% |
| weak_positive | 6 | 7.94% |
| strong_positive | 5 | 6.50% |
| strong_negative | 4 | 8.10% |
| weak_negative | 4 | 5.58% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 91 | 2.06% | 187.0% | 45.1% | 45.1% |
| high | 27 | 0.78% | 21.0% | 48.1% | 48.1% |
| low | 12 | 0.37% | 4.4% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 78 | 2.50% | 195.0% | 48.7% | 48.7% |
| SHORT | 52 | 0.34% | 17.4% | 42.3% | 42.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 7 | 16.3% | 2.33% | 42.9% | 42.9% | 19.3% |
| 2019 | 18 | -4.5% | -0.25% | 33.3% | 33.3% | -27.1% |
| 2020 | 19 | 112.0% | 5.89% | 57.9% | 57.9% | 63.4% |
| 2021 | 17 | 18.0% | 1.06% | 52.9% | 52.9% | -2.1% |
| 2022 | 21 | 64.9% | 3.09% | 52.4% | 52.4% | 59.8% |
| 2023 | 16 | 9.9% | 0.62% | 43.8% | 43.8% | -14.7% |
| 2024 | 12 | 10.0% | 0.84% | 50.0% | 50.0% | -13.0% |
| 2025 | 19 | 2.9% | 0.15% | 36.8% | 36.8% | -21.4% |
| 2026 | 1 | -17.0% | -17.04% | 0.0% | 0.0% | -16.8% |

### Macro Context by Year

**2018** (Strong year: 16.3%, 7 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Flat: -4.5%, 18 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 112.0%, 19 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 18.0%, 17 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 64.9%, 21 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 9.9%, 16 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 10.0%, 12 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 2.9%, 19 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -17.0%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -29.7% cumulative (trade 103 to trade 117)
**Period:** 2024-05-08 to 2025-03-31 (15 trades)
**Peak cumulative return:** 232.8% → **Trough:** 203.1%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-05-08 | 2024-07-15 | -1.0000 | 11.10% | strong_negative | ✅ |
| 2024-07-16 | 2024-07-30 | 1.0000 | -5.01% | strong_negative | ❌ |
| 2024-07-31 | 2024-08-02 | 1.0000 | -5.14% | regime_shift | ❌ |
| 2024-08-05 | 2024-11-05 | 1.0000 | 3.31% | regime_shift | ✅ |
| 2024-11-06 | 2024-11-13 | 1.0000 | -5.35% | weak_positive | ❌ |
| 2024-11-14 | 2024-12-16 | 1.0000 | 4.69% | weak_positive | ✅ |
| 2024-12-17 | 2024-12-19 | 1.0000 | -6.51% | weak_positive | ❌ |
| 2024-12-20 | 2025-02-03 | 1.0000 | 7.75% | weak_positive | ✅ |
| 2025-02-04 | 2025-02-06 | 1.0000 | -5.23% | weak_positive | ❌ |
| 2025-02-07 | 2025-02-13 | 1.0000 | -5.84% | weak_positive | ❌ |
| 2025-02-14 | 2025-02-24 | 1.0000 | -1.56% | weak_positive | ❌ |
| 2025-02-25 | 2025-03-03 | 1.0000 | -7.27% | weak_positive | ❌ |
| 2025-03-04 | 2025-03-12 | 1.0000 | 6.26% | weak_positive | ✅ |
| 2025-03-13 | 2025-03-28 | 1.0000 | 1.46% | weak_positive | ✅ |
| 2025-03-31 | 2025-04-03 | 1.0000 | -11.28% | weak_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 36 | -2.70% | -97.1% | 25.0% |
| 16-30d | 33 | 7.49% | 247.1% | 75.8% |
| 31-50d | 7 | 12.78% | 89.5% | 85.7% |
| 50d+ | 2 | 5.78% | 11.6% | 100.0% |
| 6-15d | 52 | -0.74% | -38.6% | 34.6% |

## Win/Loss Streaks

- **Max consecutive wins:** 8
- **Max consecutive losses:** 7

## Conclusions & Observations

**Statistical robustness:** With 130 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (161.2% remaining).
**Signal vs Direction:** Signal accuracy (60.4%) exceeds direction accuracy (47.7%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities

- **Worst year:** 2026 (-17.0%, 1 trades). Macro: No flagged events
- **Losing regime:** `strong_positive` — 26 trades, -2.2% total return
- **Losing regime:** `weak_negative` — 15 trades, -3.5% total return