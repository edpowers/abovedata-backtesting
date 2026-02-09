# Strategy Analysis: corr_aware_contemp_ma_e5d × trailing_stop_5%

**Ticker:** ISRG
**Entry:** `corr_aware_contemp_ma_e5d`
**Exit:** `trailing_stop_5%`
**Period:** 2020-04-08 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `5` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 87.9% |
| **Annualized Return** | 32.5% |
| **Sharpe Ratio** | 1.791 |
| **Max Drawdown** | -23.5% |
| **Total Trades** | 182 |
| **Win Rate** | 37.4% |
| **Signal Accuracy** | 43.0% |
| **Direction Accuracy** | 38.9% |
| **Skill Ratio** | 38.9% |
| **Profit Factor** | 1.28 |
| **Expectancy** | 0.0052 |
| **Tail Ratio** | 2.08 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 730.6% | 87.9% | -642.7% |
| Annualized Return | 21.1% | 32.5% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.0×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0112 | Ideal for 182 trades: 0.0055 |
| Top-1 Trade | 6.0% of gross profit | ✅ Low concentration |
| Top-3 Trades | 16.3% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 49.0% | Strategy survives without best trade |
| Return ex-Top-3 | -0.8% | Strategy fails without top 3 |
| Max Single Trade | 26.1% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 58 | 6.52% | 377.9% | 6.40% | 11.21 |
| no_signal | 33 | -0.38% | -12.7% | -0.06% | 6.94 |
| direction_wrong_loss | 91 | -2.97% | -270.0% | -3.83% | 4.55 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 32 | 2.40% | 76.7% | 43.8% | 43.8% | 0.81% |
| weak_negative | 16 | 1.21% | 19.4% | 37.5% | 37.5% | 0.57% |
| strong_positive | 28 | 0.54% | 15.1% | 46.4% | 46.4% | 0.02% |
| regime_shift | 64 | 0.07% | 4.6% | 32.8% | 32.8% | 0.51% |
| unknown | 21 | -0.06% | -1.2% | 42.9% | 42.9% | -0.75% |
| weak_positive | 21 | -0.92% | -19.4% | 23.8% | 23.8% | -1.54% |

**Best regime:** `strong_negative` — 32 trades, 76.7% total return, 43.8% win rate.
**Worst regime:** `weak_positive` — 21 trades, -19.4% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 51 | -3.23% | -164.9% |
| ❌ | ✅ | 34 | 5.16% | 175.4% |
| ✅ | ❌ | 40 | -2.63% | -105.1% |
| ✅ | ✅ | 24 | 8.44% | 202.5% |

### Flip Trades (Signal Wrong → Direction Right)

**44 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **5.3%**
- Total return: **235.3%**
- Average alpha: **5.4%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 16 | 4.98% |
| strong_negative | 9 | 7.16% |
| strong_positive | 7 | 4.15% |
| weak_negative | 6 | 6.68% |
| weak_positive | 4 | 5.17% |
| unknown | 2 | 0.71% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 115 | 0.82% | 94.0% | 40.9% | 40.9% |
| high | 30 | 0.47% | 14.1% | 30.0% | 30.0% |
| no_data | 1 | -0.00% | -0.0% | 0.0% | 0.0% |
| low | 36 | -0.36% | -12.8% | 33.3% | 33.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 85 | 0.95% | 80.8% | 41.2% | 41.2% |
| SHORT | 97 | 0.15% | 14.4% | 34.0% | 34.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 34 | 12.8% | 0.38% | 38.2% | 38.2% | -27.7% |
| 2021 | 25 | 36.9% | 1.48% | 40.0% | 40.0% | 27.5% |
| 2022 | 49 | -17.8% | -0.36% | 36.7% | 36.7% | -0.6% |
| 2023 | 22 | 62.9% | 2.86% | 45.5% | 45.5% | 37.7% |
| 2024 | 17 | 22.2% | 1.31% | 41.2% | 41.2% | -1.7% |
| 2025 | 31 | -38.3% | -1.23% | 25.8% | 25.8% | -32.7% |
| 2026 | 4 | 16.5% | 4.13% | 50.0% | 50.0% | 18.0% |

### Macro Context by Year

**2020** (Strong year: 12.8%, 34 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 36.9%, 25 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -17.8%, 49 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 62.9%, 22 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 22.2%, 17 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -38.3%, 31 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 16.5%, 4 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -83.4% cumulative (trade 143 to trade 174)
**Period:** 2024-10-08 to 2025-09-16 (32 trades)
**Peak cumulative return:** 131.5% → **Trough:** 48.1%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-10-08 | 2024-10-10 | 1.0000 | 0.63% | strong_positive | ✅ |
| 2024-10-10 | 2024-10-18 | -1.0000 | -7.71% | strong_positive | ❌ |
| 2024-10-21 | 2024-11-08 | -1.0000 | -3.39% | weak_positive | ❌ |
| 2024-11-11 | 2024-12-06 | -1.0000 | -2.74% | weak_positive | ❌ |
| 2024-12-09 | 2025-01-06 | -1.0000 | -0.65% | weak_positive | ❌ |
| 2025-01-07 | 2025-01-15 | -1.0000 | -9.07% | weak_positive | ❌ |
| 2025-01-16 | 2025-01-24 | 1.0000 | -0.01% | weak_positive | ❌ |
| 2025-01-27 | 2025-02-25 | 1.0000 | 0.05% | regime_shift | ✅ |
| 2025-02-26 | 2025-02-28 | 1.0000 | -1.34% | regime_shift | ❌ |
| 2025-03-03 | 2025-03-04 | 1.0000 | -1.59% | regime_shift | ❌ |
| 2025-03-05 | 2025-03-06 | 1.0000 | -5.18% | regime_shift | ❌ |
| 2025-03-07 | 2025-03-10 | 1.0000 | -6.88% | regime_shift | ❌ |
| 2025-03-11 | 2025-03-13 | 1.0000 | -3.43% | regime_shift | ❌ |
| 2025-03-14 | 2025-03-28 | 1.0000 | 1.53% | regime_shift | ✅ |
| 2025-03-31 | 2025-04-04 | 1.0000 | -8.82% | regime_shift | ❌ |
| 2025-04-07 | 2025-04-08 | 1.0000 | -1.29% | regime_shift | ❌ |
| 2025-04-09 | 2025-04-10 | 1.0000 | -6.39% | regime_shift | ❌ |
| 2025-04-11 | 2025-04-16 | 1.0000 | -2.48% | regime_shift | ❌ |
| 2025-04-17 | 2025-04-21 | 1.0000 | -2.99% | regime_shift | ❌ |
| 2025-04-22 | 2025-04-23 | 1.0000 | 1.92% | regime_shift | ✅ |
| 2025-04-24 | 2025-05-23 | 1.0000 | 6.18% | strong_negative | ✅ |
| 2025-05-27 | 2025-06-09 | 1.0000 | -4.37% | strong_negative | ❌ |
| 2025-06-10 | 2025-06-13 | 1.0000 | -3.29% | strong_negative | ❌ |
| 2025-06-16 | 2025-07-09 | 1.0000 | 1.75% | strong_negative | ✅ |
| 2025-07-10 | 2025-07-23 | 1.0000 | -4.58% | strong_negative | ❌ |
| 2025-07-24 | 2025-07-31 | 1.0000 | -1.54% | strong_negative | ❌ |
| 2025-08-01 | 2025-08-07 | 1.0000 | -2.76% | strong_negative | ❌ |
| 2025-08-08 | 2025-08-21 | 1.0000 | -0.04% | strong_negative | ❌ |
| 2025-08-22 | 2025-09-03 | 1.0000 | -7.35% | strong_negative | ❌ |
| 2025-09-04 | 2025-09-10 | 1.0000 | -1.00% | strong_negative | ❌ |
| 2025-09-11 | 2025-09-15 | 1.0000 | -4.80% | strong_negative | ❌ |
| 2025-09-16 | 2025-10-10 | 1.0000 | -1.13% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 111 | -1.36% | -150.8% | 26.1% |
| 16-30d | 22 | 6.60% | 145.3% | 72.7% |
| 31-50d | 4 | 14.39% | 57.6% | 100.0% |
| 50d+ | 1 | 15.53% | 15.5% | 100.0% |
| 6-15d | 44 | 0.63% | 27.6% | 40.9% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 9

## Conclusions & Observations

**Statistical robustness:** With 182 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (-0.8% remaining).
**Signal vs Direction:** Signal accuracy (43.0%) exceeds direction accuracy (38.9%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.
**Regime dependence:** `strong_negative` (32 trades, 18% of total) generates 76.7% — a disproportionate share of returns.

### Known Vulnerabilities

- **Worst year:** 2025 (-38.3%, 31 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery
- **Losing regime:** `unknown` — 21 trades, -1.2% total return
- **Losing regime:** `weak_positive` — 21 trades, -19.4% total return