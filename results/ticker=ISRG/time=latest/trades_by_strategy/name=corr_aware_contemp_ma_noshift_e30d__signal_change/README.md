# Strategy Analysis: corr_aware_contemp_ma_noshift_e30d × signal_change

**Ticker:** ISRG
**Entry:** `corr_aware_contemp_ma_noshift_e30d`
**Exit:** `signal_change`
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

- **Exit type:** `signal_change`
  - Exit when the UCC signal reverses direction. Fundamentally-driven exit that stays in the trade as long as the thesis holds

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 554.0% |
| **Annualized Return** | 13.6% |
| **Sharpe Ratio** | 0.561 |
| **Max Drawdown** | -47.1% |
| **Total Trades** | 12 |
| **Win Rate** | 75.0% |
| **Signal Accuracy** | 40.0% |
| **Direction Accuracy** | 70.0% |
| **Skill Ratio** | 70.0% |
| **Profit Factor** | 10.96 |
| **Expectancy** | 0.1905 |
| **Tail Ratio** | 3.90 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 730.6% | 554.0% | -176.6% |
| Annualized Return | 21.1% | 13.6% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.7×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.1399 | Ideal for 12 trades: 0.0833 |
| Top-1 Trade | 24.0% of gross profit | ⚠️ High concentration |
| Top-3 Trades | 60.5% of gross profit | ⚠️ High concentration |
| Return ex-Top-1 | 307.8% | Strategy survives without best trade |
| Return ex-Top-3 | 92.7% | Strategy survives without top 3 |
| Max Single Trade | 60.4% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 7 | 30.78% | 215.4% | 21.66% | 125.57 |
| no_signal | 2 | 18.08% | 36.2% | 14.72% | 52.00 |
| direction_wrong_loss | 3 | -7.65% | -23.0% | -12.12% | 105.67 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 3 | 30.91% | 92.7% | 100.0% | 100.0% | 18.13% |
| regime_shift | 3 | 28.68% | 86.0% | 66.7% | 66.7% | 20.74% |
| unknown | 2 | 13.70% | 27.4% | 50.0% | 50.0% | 6.17% |
| weak_positive | 2 | 11.81% | 23.6% | 100.0% | 100.0% | 14.56% |
| weak_negative | 1 | 14.32% | 14.3% | 100.0% | 100.0% | 13.03% |
| strong_positive | 1 | -15.46% | -15.5% | 0.0% | 0.0% | -26.39% |

**Best regime:** `strong_negative` — 3 trades, 92.7% total return, 100.0% win rate.
**Worst regime:** `strong_positive` — 1 trades, -15.5% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 2 | -3.75% | -7.5% |
| ❌ | ✅ | 4 | 35.36% | 141.4% |
| ✅ | ❌ | 1 | -15.46% | -15.5% |
| ✅ | ✅ | 3 | 24.67% | 74.0% |

### Flip Trades (Signal Wrong → Direction Right)

**6 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **29.6%**
- Total return: **177.6%**
- Average alpha: **22.0%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_negative | 2 | 41.12% |
| weak_positive | 2 | 11.81% |
| weak_negative | 1 | 14.32% |
| regime_shift | 1 | 57.42% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| high | 3 | 38.89% | 116.7% | 100.0% | 100.0% |
| medium | 7 | 12.08% | 84.6% | 71.4% | 71.4% |
| low | 2 | 13.70% | 27.4% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 6 | 34.06% | 204.4% | 100.0% | 100.0% |
| SHORT | 6 | 4.04% | 24.3% | 50.0% | 50.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 3 | 37.9% | 12.63% | 66.7% | 66.7% | 15.2% |
| 2021 | 2 | 79.8% | 39.92% | 100.0% | 100.0% | 65.5% |
| 2022 | 1 | -5.8% | -5.81% | 0.0% | 0.0% | -4.4% |
| 2023 | 2 | 94.8% | 47.41% | 100.0% | 100.0% | 63.3% |
| 2024 | 2 | -14.3% | -7.13% | 50.0% | 50.0% | -24.4% |
| 2025 | 2 | 36.2% | 18.08% | 100.0% | 100.0% | 29.4% |

### Macro Context by Year

**2020** (Strong year: 37.9%, 3 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 79.8%, 2 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -5.8%, 1 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 94.8%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -14.3%, 2 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 36.2%, 2 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -15.5% cumulative (trade 8 to trade 9)
**Period:** 2023-09-07 to 2024-09-05 (2 trades)
**Peak cumulative return:** 206.7% → **Trough:** 191.3%

**Macro context during drawdown:**
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-09-07 | 2024-09-05 | 1.0000 | 60.38% | strong_negative | ✅ |
| 2024-09-05 | 2024-12-06 | -1.0000 | -15.46% | strong_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 31-50d | 1 | 14.32% | 14.3% | 100.0% |
| 50d+ | 11 | 19.48% | 214.3% | 72.7% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 1

## Conclusions & Observations

**Statistical robustness:** ⚠️ Only 12 trades — interpret cautiously.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (92.7% remaining).
**Edge:** Genuine structural edge: 75.0% win rate with 10.96× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (70.0%) exceeds signal accuracy (40.0%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Worst year:** 2024 (-14.3%, 2 trades). Macro: 2024 Election Year Uncertainty
- **Losing regime:** `strong_positive` — 1 trades, -15.5% total return