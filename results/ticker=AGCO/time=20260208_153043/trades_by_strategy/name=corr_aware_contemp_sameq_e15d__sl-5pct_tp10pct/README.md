# Strategy Analysis: corr_aware_contemp_sameq_e15d × sl-5%_tp10%

**Ticker:** AGCO
**Entry:** `corr_aware_contemp_sameq_e15d`
**Exit:** `sl-5%_tp10%`
**Period:** 2018-07-10 to 2026-02-06
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
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit creates a 2:1 reward/risk ratio — when direction is correct, gains are 2× what losses are when wrong

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 1138.7% |
| **Annualized Return** | 12.1% |
| **Sharpe Ratio** | 0.449 |
| **Max Drawdown** | -35.7% |
| **Total Trades** | 122 |
| **Win Rate** | 53.3% |
| **Signal Accuracy** | 58.7% |
| **Direction Accuracy** | 55.0% |
| **Skill Ratio** | 55.0% |
| **Profit Factor** | 1.83 |
| **Expectancy** | 0.0246 |
| **Tail Ratio** | 1.66 |

## Diversity & Concentration

Diversification: **Excellent** — nearly perfectly diversified (HHI ratio: 1.2×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0097 | Ideal for 122 trades: 0.0082 |
| Top-1 Trade | 2.8% of gross profit | ✅ Low concentration |
| Top-3 Trades | 8.3% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 942.8% | Strategy survives without best trade |
| Return ex-Top-3 | 650.4% | Strategy survives without top 3 |
| Max Single Trade | 18.8% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 60 | 9.93% | 595.5% | 9.18% | 14.62 |
| no_signal | 13 | 0.98% | 12.8% | -0.80% | 18.15 |
| direction_wrong_loss | 49 | -6.29% | -308.4% | -6.69% | 13.92 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 56 | 3.78% | 211.5% | 60.7% | 60.7% | 2.30% |
| weak_positive | 12 | 2.83% | 34.0% | 50.0% | 50.0% | 1.66% |
| strong_negative | 14 | 2.29% | 32.1% | 64.3% | 64.3% | 1.78% |
| strong_positive | 20 | 1.15% | 23.0% | 45.0% | 45.0% | 2.03% |
| weak_negative | 15 | 0.72% | 10.9% | 40.0% | 40.0% | 0.72% |
| unknown | 5 | -2.30% | -11.5% | 20.0% | 20.0% | -2.44% |

**Best regime:** `regime_shift` — 56 trades, 211.5% total return, 60.7% win rate.
**Worst regime:** `unknown` — 5 trades, -11.5% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 21 | -6.45% | -135.5% |
| ❌ | ✅ | 24 | 9.55% | 229.3% |
| ✅ | ❌ | 28 | -6.17% | -172.9% |
| ✅ | ✅ | 36 | 10.17% | 366.3% |

### Flip Trades (Signal Wrong → Direction Right)

**29 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **10.2%**
- Total return: **294.7%**
- Average alpha: **9.1%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 13 | 10.09% |
| strong_negative | 4 | 7.23% |
| weak_positive | 4 | 13.51% |
| weak_negative | 4 | 11.17% |
| strong_positive | 4 | 8.96% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 86 | 3.19% | 274.4% | 58.1% | 58.1% |
| high | 28 | 1.40% | 39.1% | 46.4% | 46.4% |
| no_data | 1 | -6.62% | -6.6% | 0.0% | 0.0% |
| low | 7 | -1.00% | -7.0% | 28.6% | 28.6% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 75 | 2.61% | 195.7% | 54.7% | 54.7% |
| SHORT | 47 | 2.22% | 104.2% | 51.1% | 51.1% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 7 | -8.2% | -1.18% | 28.6% | 28.6% | 3.9% |
| 2019 | 15 | 12.5% | 0.84% | 53.3% | 53.3% | -9.7% |
| 2020 | 22 | 141.4% | 6.43% | 72.7% | 72.7% | 148.0% |
| 2021 | 11 | 15.4% | 1.40% | 45.5% | 45.5% | -12.6% |
| 2022 | 25 | 84.5% | 3.38% | 60.0% | 60.0% | 99.2% |
| 2023 | 14 | 26.1% | 1.86% | 50.0% | 50.0% | 2.7% |
| 2024 | 14 | 20.8% | 1.48% | 50.0% | 50.0% | -2.0% |
| 2025 | 11 | 22.1% | 2.01% | 45.5% | 45.5% | -0.9% |
| 2026 | 3 | -14.7% | -4.89% | 0.0% | 0.0% | -16.1% |

### Macro Context by Year

**2018** (Losing year: -8.2%, 7 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 12.5%, 15 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 141.4%, 22 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 15.4%, 11 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 84.5%, 25 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 26.1%, 14 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 20.8%, 14 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 22.1%, 11 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -14.7%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -32.4% cumulative (trade 27 to trade 32)
**Period:** 2020-03-19 to 2020-04-17 (6 trades)
**Peak cumulative return:** 76.6% → **Trough:** 44.1%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-03-19 | 2020-03-23 | -1.0000 | 11.02% | strong_positive | ✅ |
| 2020-03-24 | 2020-03-26 | -1.0000 | -10.56% | strong_positive | ❌ |
| 2020-03-27 | 2020-04-07 | -1.0000 | -6.36% | strong_positive | ❌ |
| 2020-04-08 | 2020-04-14 | -1.0000 | 2.33% | strong_positive | ✅ |
| 2020-04-14 | 2020-04-16 | 1.0000 | -9.91% | strong_positive | ❌ |
| 2020-04-17 | 2020-05-13 | 1.0000 | -7.92% | strong_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 35 | 0.75% | 26.3% | 45.7% |
| 16-30d | 21 | 5.70% | 119.7% | 66.7% |
| 31-50d | 11 | 1.49% | 16.4% | 45.5% |
| 50d+ | 5 | 4.32% | 21.6% | 60.0% |
| 6-15d | 50 | 2.32% | 115.9% | 54.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 3

## Conclusions & Observations

**Statistical robustness:** With 122 trades, this sample is large enough for reliable inference.
**Diversification:** Excellent. HHI of 0.0097 is near the theoretical minimum of 0.0082. No single trade dominates returns.
**Edge:** Genuine structural edge: 53.3% win rate with 1.83× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Signal accuracy (58.7%) exceeds direction accuracy (55.0%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities

- **Worst year:** 2026 (-14.7%, 3 trades). Macro: No flagged events
- **Losing regime:** `unknown` — 5 trades, -11.5% total return