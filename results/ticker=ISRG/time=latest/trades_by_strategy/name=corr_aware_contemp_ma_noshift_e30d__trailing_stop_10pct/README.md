# Strategy Analysis: corr_aware_contemp_ma_noshift_e30d × trailing_stop_10%

**Ticker:** ISRG
**Entry:** `corr_aware_contemp_ma_noshift_e30d`
**Exit:** `trailing_stop_10%`
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

- **Exit type:** `trailing_stop_10%`
  - 10% trailing stop. More room for normal volatility, captures larger trends

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 467.6% |
| **Annualized Return** | 26.3% |
| **Sharpe Ratio** | 1.212 |
| **Max Drawdown** | -26.9% |
| **Total Trades** | 51 |
| **Win Rate** | 51.0% |
| **Signal Accuracy** | 36.4% |
| **Direction Accuracy** | 47.7% |
| **Skill Ratio** | 47.7% |
| **Profit Factor** | 2.43 |
| **Expectancy** | 0.0440 |
| **Tail Ratio** | 3.24 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 730.6% | 467.6% | -263.0% |
| Annualized Return | 21.1% | 26.3% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.2×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0434 | Ideal for 51 trades: 0.0196 |
| Top-1 Trade | 19.6% of gross profit | ✅ Low concentration |
| Top-3 Trades | 36.0% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 225.2% | Strategy survives without best trade |
| Return ex-Top-3 | 88.8% | Strategy survives without top 3 |
| Max Single Trade | 74.5% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 21 | 15.17% | 318.6% | 14.82% | 37.05 |
| no_signal | 7 | 6.73% | 47.1% | 4.07% | 23.57 |
| direction_wrong_loss | 23 | -6.15% | -141.5% | -9.66% | 13.78 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 18 | 6.58% | 118.5% | 66.7% | 66.7% | 6.48% |
| strong_negative | 7 | 13.64% | 95.4% | 71.4% | 71.4% | 9.56% |
| weak_positive | 4 | 7.30% | 29.2% | 75.0% | 75.0% | 5.04% |
| weak_negative | 6 | 0.75% | 4.5% | 50.0% | 50.0% | -1.14% |
| unknown | 10 | 0.15% | 1.5% | 20.0% | 20.0% | -3.63% |
| strong_positive | 6 | -4.16% | -25.0% | 16.7% | 16.7% | -7.17% |

**Best regime:** `regime_shift` — 18 trades, 118.5% total return, 66.7% win rate.
**Worst regime:** `strong_positive` — 6 trades, -25.0% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 15 | -6.15% | -92.2% |
| ❌ | ✅ | 13 | 16.13% | 209.7% |
| ✅ | ❌ | 8 | -6.15% | -49.2% |
| ✅ | ✅ | 8 | 13.61% | 108.9% |

### Flip Trades (Signal Wrong → Direction Right)

**18 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **15.1%**
- Total return: **272.0%**
- Average alpha: **13.5%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 8 | 10.39% |
| weak_negative | 3 | 10.06% |
| weak_positive | 3 | 13.04% |
| strong_negative | 2 | 48.18% |
| unknown | 1 | 19.20% |
| strong_positive | 1 | 3.96% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| high | 5 | 24.41% | 122.0% | 80.0% | 80.0% |
| medium | 32 | 3.44% | 110.0% | 59.4% | 59.4% |
| low | 14 | -0.56% | -7.8% | 21.4% | 21.4% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 14 | 15.03% | 210.4% | 78.6% | 78.6% |
| SHORT | 37 | 0.37% | 13.8% | 40.5% | 40.5% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 17 | 0.0% | 0.00% | 29.4% | 29.4% | -47.0% |
| 2021 | 9 | 77.8% | 8.65% | 77.8% | 77.8% | 64.8% |
| 2022 | 12 | 13.1% | 1.10% | 41.7% | 41.7% | 25.9% |
| 2023 | 4 | 100.2% | 25.05% | 75.0% | 75.0% | 65.5% |
| 2024 | 2 | -14.1% | -7.05% | 50.0% | 50.0% | -20.2% |
| 2025 | 6 | 37.3% | 6.21% | 66.7% | 66.7% | 18.4% |
| 2026 | 1 | 9.8% | 9.83% | 100.0% | 100.0% | 10.1% |

### Macro Context by Year

**2020** (Modestly positive: 0.0%, 17 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 77.8%, 9 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 13.1%, 12 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 100.2%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -14.1%, 2 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 37.3%, 6 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 9.8%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -46.8% cumulative (trade 1 to trade 9)
**Period:** 2020-03-04 to 2020-05-21 (9 trades)
**Peak cumulative return:** 19.2% → **Trough:** -27.6%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-03-04 | 2020-03-13 | -1.0000 | 19.20% | unknown | ✅ |
| 2020-03-16 | 2020-03-17 | -1.0000 | -5.24% | unknown | ❌ |
| 2020-03-18 | 2020-03-19 | -1.0000 | -0.37% | unknown | ❌ |
| 2020-03-20 | 2020-03-24 | -1.0000 | -9.57% | unknown | ❌ |
| 2020-03-25 | 2020-03-26 | -1.0000 | -8.94% | unknown | ❌ |
| 2020-03-27 | 2020-04-06 | -1.0000 | -2.00% | unknown | ❌ |
| 2020-04-07 | 2020-05-07 | -1.0000 | -9.38% | unknown | ❌ |
| 2020-05-08 | 2020-05-20 | -1.0000 | -2.70% | unknown | ❌ |
| 2020-05-21 | 2020-06-05 | -1.0000 | -8.57% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 11 | -2.96% | -32.6% | 18.2% |
| 16-30d | 17 | 1.34% | 22.8% | 52.9% |
| 31-50d | 2 | 6.73% | 13.5% | 50.0% |
| 50d+ | 8 | 23.77% | 190.2% | 87.5% |
| 6-15d | 13 | 2.33% | 30.3% | 53.8% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 8

## Conclusions & Observations

**Statistical robustness:** 51 trades provides a reasonable sample, though some metrics may have wide confidence intervals.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (88.8% remaining).
**Edge:** Genuine structural edge: 51.0% win rate with 2.43× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (47.7%) exceeds signal accuracy (36.4%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Worst year:** 2024 (-14.1%, 2 trades). Macro: 2024 Election Year Uncertainty
- **Losing regime:** `strong_positive` — 6 trades, -25.0% total return