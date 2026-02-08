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
| **Total Return** | 405.0% |
| **Annualized Return** | 13.8% |
| **Sharpe Ratio** | 0.605 |
| **Max Drawdown** | -30.6% |
| **Total Trades** | 42 |
| **Win Rate** | 61.9% |
| **Signal Accuracy** | 57.1% |
| **Direction Accuracy** | 60.0% |
| **Skill Ratio** | 60.0% |
| **Profit Factor** | 2.31 |
| **Expectancy** | 0.0478 |
| **Tail Ratio** | 1.44 |

## Diversity & Concentration

Diversification: **Excellent** — nearly perfectly diversified (HHI ratio: 1.4×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0322 | Ideal for 42 trades: 0.0238 |
| Top-1 Trade | 7.3% of gross profit | ✅ Low concentration |
| Top-3 Trades | 20.4% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 301.2% | Strategy survives without best trade |
| Return ex-Top-3 | 164.6% | Strategy survives without top 3 |
| Max Single Trade | 25.9% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 21 | 13.85% | 290.8% | 12.56% | 42.24 |
| no_signal | 7 | 6.90% | 48.3% | 4.63% | 34.00 |
| direction_wrong_loss | 14 | -9.88% | -138.3% | -10.95% | 32.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 8 | 17.66% | 141.3% | 100.0% | 100.0% | 15.11% |
| regime_shift | 10 | 7.31% | 73.1% | 80.0% | 80.0% | 6.87% |
| unknown | 2 | 3.81% | 7.6% | 100.0% | 100.0% | 8.93% |
| weak_positive | 7 | 0.25% | 1.8% | 42.9% | 42.9% | -1.95% |
| strong_positive | 7 | -0.59% | -4.1% | 28.6% | 28.6% | -2.69% |
| weak_negative | 8 | -2.36% | -18.9% | 37.5% | 37.5% | -4.01% |

**Best regime:** `strong_negative` — 8 trades, 141.3% total return, 100.0% win rate.
**Worst regime:** `weak_negative` — 8 trades, -18.9% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 7 | -8.26% | -57.8% |
| ❌ | ✅ | 8 | 16.50% | 132.0% |
| ✅ | ❌ | 7 | -11.50% | -80.5% |
| ✅ | ✅ | 13 | 12.22% | 158.9% |

### Flip Trades (Signal Wrong → Direction Right)

**13 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **15.0%**
- Total return: **195.1%**
- Average alpha: **13.0%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_negative | 4 | 21.65% |
| regime_shift | 4 | 11.16% |
| weak_positive | 2 | 10.86% |
| strong_positive | 1 | 20.30% |
| unknown | 1 | 1.80% |
| weak_negative | 1 | 20.01% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 26 | 7.74% | 201.1% | 69.2% | 69.2% |
| high | 5 | 0.58% | 2.9% | 40.0% | 40.0% |
| low | 11 | -0.30% | -3.3% | 54.5% | 54.5% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 23 | 7.15% | 164.5% | 65.2% | 65.2% |
| SHORT | 19 | 1.91% | 36.3% | 57.9% | 57.9% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 2 | 7.6% | 3.81% | 100.0% | 100.0% | 17.9% |
| 2019 | 7 | 9.5% | 1.36% | 42.9% | 42.9% | -24.4% |
| 2020 | 7 | 93.1% | 13.30% | 71.4% | 71.4% | 100.8% |
| 2021 | 3 | 36.5% | 12.15% | 100.0% | 100.0% | 22.3% |
| 2022 | 10 | -33.6% | -3.36% | 30.0% | 30.0% | -10.2% |
| 2023 | 3 | 21.4% | 7.13% | 100.0% | 100.0% | 5.5% |
| 2024 | 3 | 18.1% | 6.03% | 66.7% | 66.7% | -1.7% |
| 2025 | 6 | 34.9% | 5.82% | 66.7% | 66.7% | 18.9% |
| 2026 | 1 | 13.4% | 13.36% | 100.0% | 100.0% | 13.5% |

### Macro Context by Year

**2018** (Modestly positive: 7.6%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 9.5%, 7 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 93.1%, 7 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 36.5%, 3 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -33.6%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 21.4%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 18.1%, 3 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 34.9%, 6 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 13.4%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -64.2% cumulative (trade 21 to trade 26)
**Period:** 2022-02-24 to 2022-07-08 (6 trades)
**Peak cumulative return:** 156.9% → **Trough:** 92.7%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-02-24 | 2022-03-18 | 1.0000 | 20.54% | weak_positive | ✅ |
| 2022-03-21 | 2022-04-29 | 1.0000 | -10.37% | weak_positive | ❌ |
| 2022-05-02 | 2022-05-20 | 1.0000 | -17.82% | weak_positive | ❌ |
| 2022-05-23 | 2022-06-23 | 1.0000 | -11.29% | weak_negative | ❌ |
| 2022-06-24 | 2022-07-08 | 1.0000 | -1.64% | weak_negative | ❌ |
| 2022-07-08 | 2022-08-23 | -1.0000 | -23.06% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 1 | -10.39% | -10.4% | 0.0% |
| 16-30d | 12 | 8.41% | 100.9% | 75.0% |
| 31-50d | 11 | 5.16% | 56.8% | 63.6% |
| 50d+ | 10 | 7.29% | 72.9% | 80.0% |
| 6-15d | 8 | -2.43% | -19.4% | 25.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 5

## Conclusions & Observations

**Statistical robustness:** 42 trades provides a reasonable sample, though some metrics may have wide confidence intervals.
**Diversification:** Excellent. HHI of 0.0322 is near the theoretical minimum of 0.0238. No single trade dominates returns.
**Edge:** Genuine structural edge: 61.9% win rate with 2.31× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (60.0%) exceeds signal accuracy (57.1%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Worst year:** 2022 (-33.6%, 10 trades). Macro: Fed Tightening Cycle, 2022 Bear Market
- **Losing regime:** `strong_positive` — 7 trades, -4.1% total return
- **Losing regime:** `weak_negative` — 8 trades, -18.9% total return