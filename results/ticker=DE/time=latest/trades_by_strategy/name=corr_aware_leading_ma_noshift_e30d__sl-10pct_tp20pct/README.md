# Strategy Analysis: corr_aware_leading_ma_noshift_e30d × sl-10%_tp20%

**Ticker:** DE
**Entry:** `corr_aware_leading_ma_noshift_e30d`
**Exit:** `sl-10%_tp20%`
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

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 504.2% |
| **Annualized Return** | 13.7% |
| **Sharpe Ratio** | 0.604 |
| **Max Drawdown** | -30.5% |
| **Total Trades** | 48 |
| **Win Rate** | 64.6% |
| **Signal Accuracy** | 52.5% |
| **Direction Accuracy** | 62.5% |
| **Skill Ratio** | 62.5% |
| **Profit Factor** | 2.43 |
| **Expectancy** | 0.0451 |
| **Tail Ratio** | 1.33 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 701.3% | 504.2% | -197.1% |
| Annualized Return | 20.7% | 13.7% | — |

## Diversity & Concentration

Diversification: **Excellent** — nearly perfectly diversified (HHI ratio: 1.4×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0287 | Ideal for 48 trades: 0.0208 |
| Top-1 Trade | 6.6% of gross profit | ✅ Low concentration |
| Top-3 Trades | 17.7% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 386.8% | Strategy survives without best trade |
| Return ex-Top-3 | 235.4% | Strategy survives without top 3 |
| Max Single Trade | 24.1% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 25 | 12.04% | 301.0% | 11.30% | 31.48 |
| no_signal | 8 | 6.38% | 51.1% | 4.19% | 29.62 |
| direction_wrong_loss | 15 | -9.04% | -135.7% | -11.23% | 36.20 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 9 | 15.37% | 138.3% | 100.0% | 100.0% | 11.59% |
| regime_shift | 15 | 4.14% | 62.1% | 60.0% | 60.0% | 1.39% |
| unknown | 2 | 3.81% | 7.6% | 100.0% | 100.0% | 8.93% |
| weak_negative | 10 | 0.76% | 7.6% | 50.0% | 50.0% | 3.44% |
| weak_positive | 6 | 0.10% | 0.6% | 50.0% | 50.0% | -2.98% |
| strong_positive | 6 | 0.02% | 0.1% | 50.0% | 50.0% | -1.99% |

**Best regime:** `strong_negative` — 9 trades, 138.3% total return, 100.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 7 | -7.39% | -51.7% |
| ❌ | ✅ | 12 | 14.20% | 170.3% |
| ✅ | ❌ | 8 | -10.49% | -83.9% |
| ✅ | ✅ | 13 | 10.05% | 130.6% |

### Flip Trades (Signal Wrong → Direction Right)

**18 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **13.1%**
- Total return: **236.5%**
- Average alpha: **12.2%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 6 | 11.41% |
| strong_negative | 5 | 19.14% |
| weak_positive | 2 | 8.49% |
| weak_negative | 2 | 20.97% |
| strong_positive | 2 | 5.84% |
| unknown | 1 | 1.80% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 32 | 6.14% | 196.4% | 68.8% | 68.8% |
| high | 3 | 7.84% | 23.5% | 66.7% | 66.7% |
| low | 13 | -0.28% | -3.6% | 53.8% | 53.8% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 28 | 6.37% | 178.2% | 71.4% | 71.4% |
| SHORT | 20 | 1.91% | 38.1% | 55.0% | 55.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 2 | 7.6% | 3.81% | 100.0% | 100.0% | 17.9% |
| 2019 | 7 | 13.8% | 1.98% | 57.1% | 57.1% | -17.2% |
| 2020 | 10 | 103.7% | 10.37% | 70.0% | 70.0% | 100.0% |
| 2021 | 5 | 35.0% | 7.00% | 80.0% | 80.0% | 23.3% |
| 2022 | 10 | -35.9% | -3.59% | 40.0% | 40.0% | -14.6% |
| 2023 | 3 | 22.9% | 7.64% | 66.7% | 66.7% | 6.4% |
| 2024 | 3 | 18.1% | 6.03% | 66.7% | 66.7% | -1.7% |
| 2025 | 7 | 48.0% | 6.86% | 71.4% | 71.4% | 32.3% |
| 2026 | 1 | 3.1% | 3.07% | 100.0% | 100.0% | 1.2% |

### Macro Context by Year

**2018** (Modestly positive: 7.6%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 13.8%, 7 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 103.7%, 10 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 35.0%, 5 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -35.9%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 22.9%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 18.1%, 3 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 48.0%, 7 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 3.1%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -60.8% cumulative (trade 26 to trade 31)
**Period:** 2022-02-24 to 2022-07-08 (6 trades)
**Peak cumulative return:** 170.4% → **Trough:** 109.6%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-02-24 | 2022-03-18 | 1.0000 | 20.54% | weak_positive | ✅ |
| 2022-03-21 | 2022-04-25 | 1.0000 | -8.48% | weak_positive | ❌ |
| 2022-04-26 | 2022-05-20 | 1.0000 | -17.93% | weak_positive | ❌ |
| 2022-05-23 | 2022-06-23 | 1.0000 | -11.29% | weak_negative | ❌ |
| 2022-06-24 | 2022-07-08 | 1.0000 | -1.64% | weak_negative | ❌ |
| 2022-07-08 | 2022-08-16 | -1.0000 | -21.45% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 4 | 2.84% | 11.4% | 50.0% |
| 16-30d | 15 | 3.35% | 50.3% | 66.7% |
| 31-50d | 14 | 4.88% | 68.4% | 64.3% |
| 50d+ | 8 | 7.06% | 56.5% | 75.0% |
| 6-15d | 7 | 4.27% | 29.9% | 57.1% |

## Win/Loss Streaks

- **Max consecutive wins:** 7
- **Max consecutive losses:** 5

## Conclusions & Observations

**Statistical robustness:** 48 trades provides a reasonable sample, though some metrics may have wide confidence intervals.
**Diversification:** Excellent. HHI of 0.0287 is near the theoretical minimum of 0.0208. No single trade dominates returns.
**Edge:** Genuine structural edge: 64.6% win rate with 2.43× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (62.5%) exceeds signal accuracy (52.5%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Worst year:** 2022 (-35.9%, 10 trades). Macro: Fed Tightening Cycle, 2022 Bear Market