# Strategy Analysis: corr_aware_contemp_sameq_e5d × sl-5%_tp10%

**Ticker:** AGCO
**Entry:** `corr_aware_contemp_sameq_e5d`
**Exit:** `sl-5%_tp10%`
**Period:** 2018-07-24 to 2026-02-06
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
- **entry_days_before:** `5` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit creates a 2:1 reward/risk ratio — when direction is correct, gains are 2× what losses are when wrong

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 894.9% |
| **Annualized Return** | 5.6% |
| **Sharpe Ratio** | 0.206 |
| **Max Drawdown** | -41.9% |
| **Total Trades** | 116 |
| **Win Rate** | 52.6% |
| **Signal Accuracy** | 61.5% |
| **Direction Accuracy** | 53.8% |
| **Skill Ratio** | 53.8% |
| **Profit Factor** | 1.80 |
| **Expectancy** | 0.0237 |
| **Tail Ratio** | 1.74 |

## Diversity & Concentration

Diversification: **Excellent** — nearly perfectly diversified (HHI ratio: 1.2×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0101 | Ideal for 116 trades: 0.0086 |
| Top-1 Trade | 3.0% of gross profit | ✅ Low concentration |
| Top-3 Trades | 8.8% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 737.6% | Strategy survives without best trade |
| Return ex-Top-3 | 502.7% | Strategy survives without top 3 |
| Max Single Trade | 18.8% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 56 | 9.89% | 554.0% | 8.78% | 15.21 |
| no_signal | 12 | 1.26% | 15.1% | -0.67% | 19.67 |
| direction_wrong_loss | 48 | -6.13% | -294.2% | -6.16% | 14.62 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 55 | 3.55% | 195.0% | 60.0% | 60.0% | 1.98% |
| strong_positive | 21 | 2.04% | 42.8% | 47.6% | 47.6% | 2.87% |
| weak_positive | 12 | 2.83% | 34.0% | 50.0% | 50.0% | 1.66% |
| strong_negative | 14 | 1.09% | 15.3% | 57.1% | 57.1% | 0.56% |
| unknown | 4 | -1.28% | -5.1% | 25.0% | 25.0% | -1.32% |
| weak_negative | 10 | -0.70% | -7.0% | 30.0% | 30.0% | -0.35% |

**Best regime:** `regime_shift` — 55 trades, 195.0% total return, 60.0% win rate.
**Worst regime:** `weak_negative` — 10 trades, -7.0% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 20 | -6.41% | -128.3% |
| ❌ | ✅ | 20 | 9.34% | 186.8% |
| ✅ | ❌ | 28 | -5.93% | -165.9% |
| ✅ | ✅ | 36 | 10.20% | 367.3% |

### Flip Trades (Signal Wrong → Direction Right)

**25 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **10.1%**
- Total return: **253.4%**
- Average alpha: **8.4%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 12 | 9.67% |
| weak_positive | 4 | 13.51% |
| strong_positive | 4 | 9.50% |
| strong_negative | 3 | 7.05% |
| weak_negative | 2 | 12.10% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 83 | 3.11% | 258.0% | 56.6% | 56.6% |
| high | 26 | 0.93% | 24.2% | 46.2% | 46.2% |
| low | 6 | -0.10% | -0.6% | 33.3% | 33.3% |
| no_data | 1 | -6.62% | -6.6% | 0.0% | 0.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 70 | 2.69% | 188.6% | 54.3% | 54.3% |
| SHORT | 46 | 1.88% | 86.3% | 50.0% | 50.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 6 | -1.8% | -0.31% | 33.3% | 33.3% | 10.8% |
| 2019 | 15 | 18.4% | 1.23% | 53.3% | 53.3% | -3.8% |
| 2020 | 24 | 155.7% | 6.49% | 70.8% | 70.8% | 162.4% |
| 2021 | 11 | 15.4% | 1.40% | 45.5% | 45.5% | -12.6% |
| 2022 | 20 | 60.3% | 3.01% | 60.0% | 60.0% | 72.0% |
| 2023 | 13 | 9.6% | 0.73% | 46.2% | 46.2% | -12.3% |
| 2024 | 14 | 7.6% | 0.55% | 42.9% | 42.9% | -13.5% |
| 2025 | 11 | 23.3% | 2.12% | 45.5% | 45.5% | 0.4% |
| 2026 | 2 | -13.6% | -6.78% | 0.0% | 0.0% | -15.0% |

### Macro Context by Year

**2018** (Flat: -1.8%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 18.4%, 15 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 155.7%, 24 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 15.4%, 11 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 60.3%, 20 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 9.6%, 13 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 7.6%, 14 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 23.3%, 11 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -13.6%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -37.5% cumulative (trade 49 to trade 61)
**Period:** 2021-03-16 to 2022-03-22 (13 trades)
**Peak cumulative return:** 197.5% → **Trough:** 160.0%

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
| 2022-01-05 | 2022-01-27 | 1.0000 | -6.98% | regime_shift | ❌ |
| 2022-01-28 | 2022-02-01 | 1.0000 | 2.49% | regime_shift | ✅ |
| 2022-02-01 | 2022-02-09 | -1.0000 | -10.79% | regime_shift | ❌ |
| 2022-02-10 | 2022-03-21 | -1.0000 | -5.17% | weak_negative | ❌ |
| 2022-03-22 | 2022-03-25 | -1.0000 | -7.30% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 29 | 2.56% | 74.3% | 55.2% |
| 16-30d | 23 | 5.05% | 116.1% | 65.2% |
| 31-50d | 11 | 0.98% | 10.8% | 45.5% |
| 50d+ | 5 | 2.95% | 14.7% | 60.0% |
| 6-15d | 48 | 1.23% | 59.1% | 45.8% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 3

## Conclusions & Observations

**Statistical robustness:** With 116 trades, this sample is large enough for reliable inference.
**Diversification:** Excellent. HHI of 0.0101 is near the theoretical minimum of 0.0086. No single trade dominates returns.
**Edge:** Genuine structural edge: 52.6% win rate with 1.80× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Signal accuracy (61.5%) exceeds direction accuracy (53.8%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities

- **Worst year:** 2026 (-13.6%, 2 trades). Macro: No flagged events
- **Losing regime:** `unknown` — 4 trades, -5.1% total return
- **Losing regime:** `weak_negative` — 10 trades, -7.0% total return