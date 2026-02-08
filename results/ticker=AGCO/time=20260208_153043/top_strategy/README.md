# Strategy Analysis: corr_aware_contemp_sameq_e10d × sl-5%_tp10%

**Ticker:** AGCO
**Entry:** `corr_aware_contemp_sameq_e10d`
**Exit:** `sl-5%_tp10%`
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

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit creates a 2:1 reward/risk ratio — when direction is correct, gains are 2× what losses are when wrong

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 1252.9% |
| **Annualized Return** | 9.7% |
| **Sharpe Ratio** | 0.360 |
| **Max Drawdown** | -38.0% |
| **Total Trades** | 120 |
| **Win Rate** | 51.7% |
| **Signal Accuracy** | 59.8% |
| **Direction Accuracy** | 53.3% |
| **Skill Ratio** | 53.3% |
| **Profit Factor** | 1.87 |
| **Expectancy** | 0.0257 |
| **Tail Ratio** | 1.76 |

## Diversity & Concentration

Diversification: **Excellent** — nearly perfectly diversified (HHI ratio: 1.2×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0097 | Ideal for 120 trades: 0.0083 |
| Top-1 Trade | 2.8% of gross profit | ✅ Low concentration |
| Top-3 Trades | 8.2% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 1039.0% | Strategy survives without best trade |
| Return ex-Top-3 | 719.6% | Strategy survives without top 3 |
| Max Single Trade | 18.8% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 57 | 10.47% | 597.0% | 9.59% | 15.68 |
| no_signal | 13 | 0.98% | 12.7% | -0.80% | 18.15 |
| direction_wrong_loss | 50 | -6.03% | -301.5% | -6.31% | 13.20 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 55 | 3.95% | 217.2% | 60.0% | 60.0% | 2.35% |
| strong_positive | 22 | 2.62% | 57.5% | 50.0% | 50.0% | 3.42% |
| weak_positive | 12 | 2.83% | 34.0% | 50.0% | 50.0% | 1.66% |
| strong_negative | 13 | 0.52% | 6.7% | 46.2% | 46.2% | -0.04% |
| weak_negative | 14 | -0.16% | -2.2% | 35.7% | 35.7% | 0.14% |
| unknown | 4 | -1.25% | -5.0% | 25.0% | 25.0% | -1.39% |

**Best regime:** `regime_shift` — 55 trades, 217.2% total return, 60.0% win rate.
**Worst regime:** `unknown` — 4 trades, -5.0% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 22 | -6.31% | -138.9% |
| ❌ | ✅ | 21 | 10.29% | 216.1% |
| ✅ | ❌ | 28 | -5.81% | -162.6% |
| ✅ | ✅ | 36 | 10.58% | 380.9% |

### Flip Trades (Signal Wrong → Direction Right)

**26 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **10.8%**
- Total return: **281.5%**
- Average alpha: **9.4%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 12 | 10.68% |
| strong_positive | 4 | 9.40% |
| weak_negative | 4 | 11.17% |
| weak_positive | 4 | 13.51% |
| strong_negative | 2 | 8.53% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 87 | 3.50% | 304.2% | 57.5% | 57.5% |
| high | 26 | 0.43% | 11.1% | 38.5% | 38.5% |
| low | 6 | -0.08% | -0.5% | 33.3% | 33.3% |
| no_data | 1 | -6.62% | -6.6% | 0.0% | 0.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 71 | 2.88% | 204.8% | 54.9% | 54.9% |
| SHORT | 49 | 2.11% | 103.4% | 46.9% | 46.9% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 6 | -1.7% | -0.29% | 33.3% | 33.3% | 10.5% |
| 2019 | 15 | 12.2% | 0.81% | 46.7% | 46.7% | -10.0% |
| 2020 | 24 | 172.5% | 7.19% | 75.0% | 75.0% | 178.8% |
| 2021 | 11 | 15.4% | 1.40% | 45.5% | 45.5% | -12.6% |
| 2022 | 24 | 83.5% | 3.48% | 58.3% | 58.3% | 97.4% |
| 2023 | 13 | 14.8% | 1.14% | 46.2% | 46.2% | -7.9% |
| 2024 | 13 | 4.3% | 0.33% | 38.5% | 38.5% | -18.5% |
| 2025 | 11 | 22.1% | 2.00% | 45.5% | 45.5% | -1.4% |
| 2026 | 3 | -14.7% | -4.91% | 0.0% | 0.0% | -15.7% |

### Macro Context by Year

**2018** (Flat: -1.7%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 12.2%, 15 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 172.5%, 24 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 15.4%, 11 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 83.5%, 24 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 14.8%, 13 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 4.3%, 13 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 22.1%, 11 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -14.7%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -28.3% cumulative (trade 49 to trade 65)
**Period:** 2021-03-16 to 2022-03-22 (17 trades)
**Peak cumulative return:** 208.1% → **Trough:** 179.8%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2021-03-16 | 2021-04-27 | 1.0000 | 10.20% | weak_positive | ✅ |
| 2021-04-28 | 2021-04-29 | 1.0000 | -5.26% | weak_positive | ❌ |
| 2021-04-30 | 2021-05-20 | 1.0000 | -6.86% | regime_shift | ❌ |
| 2021-05-21 | 2021-06-16 | 1.0000 | -5.49% | regime_shift | ❌ |
| 2021-06-17 | 2021-08-03 | 1.0000 | 10.27% | regime_shift | ✅ |
| 2021-08-04 | 2021-09-20 | 1.0000 | -6.88% | regime_shift | ❌ |
| 2021-09-21 | 2021-11-29 | 1.0000 | -6.84% | regime_shift | ❌ |
| 2021-11-30 | 2022-01-04 | 1.0000 | 11.31% | regime_shift | ✅ |
| 2022-01-05 | 2022-01-25 | 1.0000 | -4.30% | regime_shift | ❌ |
| 2022-01-25 | 2022-01-27 | -1.0000 | 2.80% | regime_shift | ✅ |
| 2022-01-28 | 2022-02-08 | -1.0000 | -9.37% | regime_shift | ❌ |
| 2022-02-09 | 2022-02-23 | -1.0000 | 10.29% | weak_negative | ✅ |
| 2022-02-24 | 2022-03-02 | -1.0000 | -8.78% | weak_negative | ❌ |
| 2022-03-03 | 2022-03-07 | -1.0000 | 10.21% | weak_negative | ✅ |
| 2022-03-08 | 2022-03-11 | -1.0000 | -5.76% | weak_negative | ❌ |
| 2022-03-14 | 2022-03-21 | -1.0000 | -6.32% | weak_negative | ❌ |
| 2022-03-22 | 2022-03-25 | -1.0000 | -7.30% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 33 | 1.33% | 44.0% | 42.4% |
| 16-30d | 21 | 6.13% | 128.8% | 71.4% |
| 31-50d | 11 | 2.00% | 22.0% | 54.5% |
| 50d+ | 5 | 4.10% | 20.5% | 60.0% |
| 6-15d | 50 | 1.86% | 92.9% | 48.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 3

## Conclusions & Observations

**Statistical robustness:** With 120 trades, this sample is large enough for reliable inference.
**Diversification:** Excellent. HHI of 0.0097 is near the theoretical minimum of 0.0083. No single trade dominates returns.
**Edge:** Genuine structural edge: 51.7% win rate with 1.87× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Signal accuracy (59.8%) exceeds direction accuracy (53.3%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities

- **Worst year:** 2026 (-14.7%, 3 trades). Macro: No flagged events
- **Losing regime:** `weak_negative` — 14 trades, -2.2% total return
- **Losing regime:** `unknown` — 4 trades, -5.0% total return