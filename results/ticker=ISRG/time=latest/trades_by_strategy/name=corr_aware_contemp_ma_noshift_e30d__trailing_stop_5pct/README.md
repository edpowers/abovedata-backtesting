# Strategy Analysis: corr_aware_contemp_ma_noshift_e30d × trailing_stop_5%

**Ticker:** ISRG
**Entry:** `corr_aware_contemp_ma_noshift_e30d`
**Exit:** `trailing_stop_5%`
**Period:** 2020-03-04 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
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
| **Total Return** | 415.6% |
| **Annualized Return** | 34.6% |
| **Sharpe Ratio** | 1.968 |
| **Max Drawdown** | -23.5% |
| **Total Trades** | 155 |
| **Win Rate** | 38.7% |
| **Signal Accuracy** | 43.4% |
| **Direction Accuracy** | 39.5% |
| **Skill Ratio** | 39.5% |
| **Profit Factor** | 1.68 |
| **Expectancy** | 0.0132 |
| **Tail Ratio** | 2.52 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 730.6% | 415.6% | -314.9% |
| Annualized Return | 21.1% | 34.6% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.1×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0138 | Ideal for 155 trades: 0.0065 |
| Top-1 Trade | 6.4% of gross profit | ✅ Low concentration |
| Top-3 Trades | 16.7% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 289.6% | Strategy survives without best trade |
| Return ex-Top-3 | 145.3% | Strategy survives without top 3 |
| Max Single Trade | 32.3% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 51 | 8.74% | 446.0% | 9.51% | 11.84 |
| no_signal | 26 | 0.06% | 1.5% | 0.71% | 6.65 |
| direction_wrong_loss | 78 | -3.11% | -242.5% | -4.27% | 4.81 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 49 | 1.67% | 81.8% | 34.7% | 34.7% | 2.33% |
| strong_negative | 23 | 2.53% | 58.2% | 47.8% | 47.8% | 0.75% |
| strong_positive | 20 | 1.23% | 24.7% | 45.0% | 45.0% | 0.29% |
| weak_positive | 20 | 0.92% | 18.3% | 35.0% | 35.0% | 0.38% |
| weak_negative | 16 | 0.80% | 12.9% | 31.2% | 31.2% | 0.24% |
| unknown | 27 | 0.33% | 9.0% | 40.7% | 40.7% | 0.79% |

**Best regime:** `regime_shift` — 49 trades, 81.8% total return, 34.7% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 43 | -3.23% | -138.9% |
| ❌ | ✅ | 30 | 7.83% | 234.8% |
| ✅ | ❌ | 35 | -2.96% | -103.6% |
| ✅ | ✅ | 21 | 10.05% | 211.1% |

### Flip Trades (Signal Wrong → Direction Right)

**39 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **7.5%**
- Total return: **292.9%**
- Average alpha: **9.2%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 12 | 8.55% |
| unknown | 7 | 8.12% |
| weak_positive | 6 | 7.43% |
| strong_negative | 5 | 7.08% |
| weak_negative | 5 | 7.75% |
| strong_positive | 4 | 3.68% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 98 | 1.60% | 157.3% | 40.8% | 40.8% |
| high | 14 | 3.59% | 50.3% | 42.9% | 42.9% |
| no_data | 1 | -0.00% | -0.0% | 0.0% | 0.0% |
| low | 42 | -0.06% | -2.7% | 33.3% | 33.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 58 | 2.51% | 145.4% | 44.8% | 44.8% |
| SHORT | 97 | 0.61% | 59.4% | 35.1% | 35.1% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 42 | 12.6% | 0.30% | 38.1% | 38.1% | -1.1% |
| 2021 | 24 | 80.0% | 3.33% | 45.8% | 45.8% | 68.9% |
| 2022 | 33 | 17.3% | 0.53% | 33.3% | 33.3% | 36.8% |
| 2023 | 12 | 65.1% | 5.43% | 50.0% | 50.0% | 44.3% |
| 2024 | 17 | 28.4% | 1.67% | 41.2% | 41.2% | 5.9% |
| 2025 | 25 | -18.1% | -0.72% | 32.0% | 32.0% | -5.7% |
| 2026 | 2 | 19.6% | 9.79% | 50.0% | 50.0% | 21.3% |

### Macro Context by Year

**2020** (Strong year: 12.6%, 42 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 80.0%, 24 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 17.3%, 33 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 65.1%, 12 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 28.4%, 17 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -18.1%, 25 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 19.6%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -58.7% cumulative (trade 5 to trade 25)
**Period:** 2020-03-19 to 2020-06-12 (21 trades)
**Peak cumulative return:** 49.3% → **Trough:** -9.4%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-03-19 | 2020-03-20 | -1.0000 | 3.43% | unknown | ✅ |
| 2020-03-23 | 2020-03-24 | -1.0000 | -17.44% | unknown | ❌ |
| 2020-03-25 | 2020-03-26 | -1.0000 | -8.94% | unknown | ❌ |
| 2020-03-27 | 2020-03-30 | -1.0000 | -2.82% | unknown | ❌ |
| 2020-03-31 | 2020-04-01 | -1.0000 | 7.46% | unknown | ✅ |
| 2020-04-02 | 2020-04-06 | -1.0000 | -6.95% | unknown | ❌ |
| 2020-04-07 | 2020-04-08 | -1.0000 | -4.19% | unknown | ❌ |
| 2020-04-09 | 2020-04-14 | -1.0000 | -0.82% | unknown | ❌ |
| 2020-04-15 | 2020-04-16 | -1.0000 | 0.11% | unknown | ✅ |
| 2020-04-17 | 2020-04-20 | -1.0000 | 1.52% | unknown | ✅ |
| 2020-04-21 | 2020-04-22 | -1.0000 | -3.12% | unknown | ❌ |
| 2020-04-23 | 2020-04-29 | -1.0000 | -1.27% | unknown | ❌ |
| 2020-04-30 | 2020-05-05 | -1.0000 | -0.39% | unknown | ❌ |
| 2020-05-06 | 2020-05-07 | -1.0000 | -4.71% | unknown | ❌ |
| 2020-05-08 | 2020-05-13 | -1.0000 | 5.36% | unknown | ✅ |
| 2020-05-14 | 2020-05-18 | -1.0000 | -4.09% | unknown | ❌ |
| 2020-05-19 | 2020-05-22 | -1.0000 | -5.99% | unknown | ❌ |
| 2020-05-26 | 2020-05-28 | -1.0000 | -2.01% | unknown | ❌ |
| 2020-05-29 | 2020-06-05 | -1.0000 | -2.19% | unknown | ❌ |
| 2020-06-08 | 2020-06-11 | 1.0000 | -7.57% | unknown | ❌ |
| 2020-06-12 | 2020-06-24 | 1.0000 | -0.62% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 93 | -1.24% | -115.6% | 25.8% |
| 16-30d | 17 | 8.18% | 139.0% | 70.6% |
| 31-50d | 4 | 20.21% | 80.8% | 100.0% |
| 50d+ | 1 | 15.53% | 15.5% | 100.0% |
| 6-15d | 40 | 2.13% | 85.1% | 47.5% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 9

## Conclusions & Observations

**Statistical robustness:** With 155 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (145.3% remaining).
**Signal vs Direction:** Signal accuracy (43.4%) exceeds direction accuracy (39.5%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities

- **Worst year:** 2025 (-18.1%, 25 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery