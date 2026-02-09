# Strategy Analysis: corr_aware_contemp_ma_noshift_e30d × sl-10%_tp20%

**Ticker:** ISRG
**Entry:** `corr_aware_contemp_ma_noshift_e30d`
**Exit:** `sl-10%_tp20%`
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

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 483.4% |
| **Annualized Return** | 14.1% |
| **Sharpe Ratio** | 0.621 |
| **Max Drawdown** | -37.8% |
| **Total Trades** | 42 |
| **Win Rate** | 57.1% |
| **Signal Accuracy** | 41.2% |
| **Direction Accuracy** | 58.8% |
| **Skill Ratio** | 58.8% |
| **Profit Factor** | 2.46 |
| **Expectancy** | 0.0510 |
| **Tail Ratio** | 1.96 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 730.6% | 483.4% | -247.2% |
| Annualized Return | 21.1% | 14.1% | — |

## Diversity & Concentration

Diversification: **Excellent** — nearly perfectly diversified (HHI ratio: 1.3×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0320 | Ideal for 42 trades: 0.0238 |
| Top-1 Trade | 8.3% of gross profit | ✅ Low concentration |
| Top-3 Trades | 22.1% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 348.3% | Strategy survives without best trade |
| Return ex-Top-3 | 187.4% | Strategy survives without top 3 |
| Max Single Trade | 30.1% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 20 | 15.24% | 304.8% | 14.19% | 40.00 |
| no_signal | 8 | 5.19% | 41.5% | 3.45% | 20.50 |
| direction_wrong_loss | 14 | -9.43% | -132.1% | -12.93% | 21.79 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 10 | 7.83% | 78.3% | 60.0% | 60.0% | 7.59% |
| weak_positive | 7 | 9.43% | 66.0% | 71.4% | 71.4% | 6.55% |
| strong_negative | 10 | 5.73% | 57.3% | 60.0% | 60.0% | 3.26% |
| unknown | 6 | 3.16% | 19.0% | 50.0% | 50.0% | 2.02% |
| weak_negative | 5 | -0.53% | -2.6% | 40.0% | 40.0% | -3.45% |
| strong_positive | 4 | -0.91% | -3.7% | 50.0% | 50.0% | -4.74% |

**Best regime:** `regime_shift` — 10 trades, 78.3% total return, 60.0% win rate.
**Worst regime:** `strong_positive` — 4 trades, -3.7% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 9 | -9.22% | -83.0% |
| ❌ | ✅ | 11 | 15.85% | 174.4% |
| ✅ | ❌ | 5 | -9.81% | -49.1% |
| ✅ | ✅ | 9 | 14.49% | 130.4% |

### Flip Trades (Signal Wrong → Direction Right)

**15 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **15.4%**
- Total return: **230.9%**
- Average alpha: **13.9%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_positive | 4 | 13.97% |
| regime_shift | 4 | 19.28% |
| strong_negative | 3 | 15.45% |
| weak_negative | 2 | 10.19% |
| unknown | 2 | 15.58% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 26 | 4.99% | 129.7% | 57.7% | 57.7% |
| high | 5 | 11.13% | 55.7% | 60.0% | 60.0% |
| low | 10 | 2.57% | 25.7% | 50.0% | 50.0% |
| no_data | 1 | 3.19% | 3.2% | 100.0% | 100.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 20 | 9.96% | 199.2% | 70.0% | 70.0% |
| SHORT | 22 | 0.68% | 15.1% | 45.5% | 45.5% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 12 | 28.7% | 2.39% | 50.0% | 50.0% | 11.8% |
| 2021 | 4 | 76.3% | 19.07% | 100.0% | 100.0% | 55.5% |
| 2022 | 7 | -4.6% | -0.66% | 42.9% | 42.9% | -1.1% |
| 2023 | 5 | 63.2% | 12.65% | 80.0% | 80.0% | 43.7% |
| 2024 | 5 | 17.7% | 3.54% | 60.0% | 60.0% | -3.5% |
| 2025 | 8 | 29.7% | 3.72% | 37.5% | 37.5% | 20.5% |
| 2026 | 1 | 3.2% | 3.19% | 100.0% | 100.0% | 3.4% |

### Macro Context by Year

**2020** (Strong year: 28.7%, 12 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 76.3%, 4 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Flat: -4.6%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 63.2%, 5 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 17.7%, 5 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 29.7%, 8 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 3.2%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -32.7% cumulative (trade 19 to trade 22)
**Period:** 2022-08-03 to 2022-10-26 (4 trades)
**Peak cumulative return:** 123.6% → **Trough:** 90.9%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-08-03 | 2022-09-22 | -1.0000 | 21.10% | regime_shift | ✅ |
| 2022-09-23 | 2022-10-19 | -1.0000 | -10.82% | regime_shift | ❌ |
| 2022-10-20 | 2022-10-25 | -1.0000 | -12.20% | weak_negative | ❌ |
| 2022-10-26 | 2022-11-11 | -1.0000 | -9.69% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 6 | -2.68% | -16.1% | 50.0% |
| 16-30d | 11 | -1.13% | -12.5% | 27.3% |
| 31-50d | 13 | 12.53% | 162.9% | 84.6% |
| 50d+ | 6 | 11.78% | 70.7% | 83.3% |
| 6-15d | 6 | 1.53% | 9.2% | 33.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 3

## Conclusions & Observations

**Statistical robustness:** 42 trades provides a reasonable sample, though some metrics may have wide confidence intervals.
**Diversification:** Excellent. HHI of 0.0320 is near the theoretical minimum of 0.0238. No single trade dominates returns.
**Edge:** Genuine structural edge: 57.1% win rate with 2.46× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (58.8%) exceeds signal accuracy (41.2%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Worst year:** 2022 (-4.6%, 7 trades). Macro: Fed Tightening Cycle, 2022 Bear Market
- **Losing regime:** `weak_negative` — 5 trades, -2.6% total return
- **Losing regime:** `strong_positive` — 4 trades, -3.7% total return