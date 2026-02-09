# Strategy Analysis: corr_aware_leading_ma_noshift_e30d × sl-5%_tp10%

**Ticker:** DE
**Entry:** `corr_aware_leading_ma_noshift_e30d`
**Exit:** `sl-5%_tp10%`
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

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit creates a 2:1 reward/risk ratio — when direction is correct, gains are 2× what losses are when wrong

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 618.3% |
| **Annualized Return** | 12.7% |
| **Sharpe Ratio** | 0.612 |
| **Max Drawdown** | -37.5% |
| **Total Trades** | 110 |
| **Win Rate** | 51.8% |
| **Signal Accuracy** | 53.7% |
| **Direction Accuracy** | 50.5% |
| **Skill Ratio** | 50.5% |
| **Profit Factor** | 1.93 |
| **Expectancy** | 0.0205 |
| **Tail Ratio** | 1.57 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 701.3% | 618.3% | -83.0% |
| Annualized Return | 20.7% | 12.7% | — |

## Diversity & Concentration

Diversification: **Excellent** — nearly perfectly diversified (HHI ratio: 1.3×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0116 | Ideal for 110 trades: 0.0091 |
| Top-1 Trade | 3.4% of gross profit | ✅ Low concentration |
| Top-3 Trades | 9.2% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 519.9% | Strategy survives without best trade |
| Return ex-Top-3 | 381.2% | Strategy survives without top 3 |
| Max Single Trade | 15.9% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 48 | 8.43% | 404.5% | 8.74% | 14.46 |
| no_signal | 15 | 2.84% | 42.6% | 2.27% | 15.33 |
| direction_wrong_loss | 47 | -4.72% | -221.7% | -5.03% | 12.32 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 19 | 6.36% | 120.8% | 73.7% | 73.7% | 5.55% |
| weak_negative | 22 | 1.76% | 38.6% | 50.0% | 50.0% | 3.50% |
| regime_shift | 32 | 0.78% | 25.0% | 43.8% | 43.8% | -0.07% |
| strong_positive | 15 | 1.47% | 22.1% | 53.3% | 53.3% | 1.73% |
| weak_positive | 14 | 1.17% | 16.4% | 50.0% | 50.0% | 0.32% |
| unknown | 8 | 0.31% | 2.5% | 37.5% | 37.5% | 0.78% |

**Best regime:** `strong_negative` — 19 trades, 120.8% total return, 73.7% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 21 | -4.49% | -94.3% |
| ❌ | ✅ | 23 | 8.81% | 202.5% |
| ✅ | ❌ | 26 | -4.90% | -127.4% |
| ✅ | ✅ | 25 | 8.08% | 201.9% |

### Flip Trades (Signal Wrong → Direction Right)

**32 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **8.3%**
- Total return: **266.5%**
- Average alpha: **9.0%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_negative | 8 | 9.61% |
| regime_shift | 8 | 7.05% |
| weak_negative | 7 | 9.23% |
| strong_positive | 4 | 9.23% |
| weak_positive | 3 | 7.06% |
| unknown | 2 | 5.23% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 66 | 3.28% | 216.8% | 60.6% | 60.6% |
| high | 15 | 0.82% | 12.3% | 40.0% | 40.0% |
| low | 29 | -0.13% | -3.7% | 37.9% | 37.9% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 55 | 2.34% | 128.9% | 56.4% | 56.4% |
| SHORT | 55 | 1.75% | 96.5% | 47.3% | 47.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 10 | 13.3% | 1.33% | 50.0% | 50.0% | 29.6% |
| 2019 | 13 | 11.7% | 0.90% | 46.2% | 46.2% | -16.5% |
| 2020 | 18 | 110.6% | 6.15% | 77.8% | 77.8% | 143.5% |
| 2021 | 13 | 42.2% | 3.25% | 61.5% | 61.5% | 27.6% |
| 2022 | 23 | -31.4% | -1.37% | 26.1% | 26.1% | -12.0% |
| 2023 | 6 | 21.8% | 3.64% | 66.7% | 66.7% | 12.6% |
| 2024 | 10 | -6.5% | -0.65% | 30.0% | 30.0% | -20.0% |
| 2025 | 15 | 50.4% | 3.36% | 60.0% | 60.0% | 39.8% |
| 2026 | 2 | 13.2% | 6.61% | 100.0% | 100.0% | 12.2% |

### Macro Context by Year

**2018** (Strong year: 13.3%, 10 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 11.7%, 13 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 110.6%, 18 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 42.2%, 13 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -31.4%, 23 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 21.8%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -6.5%, 10 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 50.4%, 15 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 13.2%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -60.1% cumulative (trade 59 to trade 71)
**Period:** 2022-03-11 to 2022-08-11 (13 trades)
**Peak cumulative return:** 184.7% → **Trough:** 124.5%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-03-11 | 2022-03-22 | 1.0000 | 9.77% | weak_positive | ✅ |
| 2022-03-23 | 2022-03-29 | 1.0000 | -4.31% | weak_positive | ❌ |
| 2022-03-30 | 2022-04-25 | 1.0000 | -7.23% | weak_positive | ❌ |
| 2022-04-26 | 2022-05-09 | 1.0000 | -4.52% | weak_positive | ❌ |
| 2022-05-10 | 2022-05-20 | 1.0000 | -14.10% | weak_positive | ❌ |
| 2022-05-23 | 2022-06-16 | 1.0000 | -5.30% | weak_negative | ❌ |
| 2022-06-17 | 2022-06-23 | 1.0000 | -7.81% | weak_negative | ❌ |
| 2022-06-24 | 2022-07-05 | 1.0000 | -5.68% | weak_negative | ❌ |
| 2022-07-06 | 2022-07-08 | 1.0000 | 5.36% | weak_negative | ✅ |
| 2022-07-08 | 2022-07-22 | -1.0000 | -2.50% | weak_negative | ❌ |
| 2022-07-25 | 2022-07-29 | -1.0000 | -6.26% | weak_negative | ❌ |
| 2022-08-01 | 2022-08-10 | -1.0000 | -4.19% | weak_negative | ❌ |
| 2022-08-11 | 2022-08-23 | -1.0000 | -3.58% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 36 | 2.01% | 72.3% | 50.0% |
| 16-30d | 22 | 3.10% | 68.2% | 59.1% |
| 31-50d | 8 | 3.13% | 25.1% | 62.5% |
| 50d+ | 3 | 2.78% | 8.3% | 66.7% |
| 6-15d | 41 | 1.25% | 51.4% | 46.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 8
- **Max consecutive losses:** 7

## Conclusions & Observations

**Statistical robustness:** With 110 trades, this sample is large enough for reliable inference.
**Diversification:** Excellent. HHI of 0.0116 is near the theoretical minimum of 0.0091. No single trade dominates returns.
**Edge:** Genuine structural edge: 51.8% win rate with 1.93× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Signal accuracy (53.7%) exceeds direction accuracy (50.5%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities

- **Worst year:** 2022 (-31.4%, 23 trades). Macro: Fed Tightening Cycle, 2022 Bear Market