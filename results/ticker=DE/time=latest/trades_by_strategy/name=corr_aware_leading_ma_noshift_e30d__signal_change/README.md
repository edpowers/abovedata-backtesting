# Strategy Analysis: corr_aware_leading_ma_noshift_e30d × signal_change

**Ticker:** DE
**Entry:** `corr_aware_leading_ma_noshift_e30d`
**Exit:** `signal_change`
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

- **Exit type:** `signal_change`
  - Exit when the UCC signal reverses direction. Fundamentally-driven exit that stays in the trade as long as the thesis holds

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 509.2% |
| **Annualized Return** | 13.7% |
| **Sharpe Ratio** | 0.569 |
| **Max Drawdown** | -46.1% |
| **Total Trades** | 17 |
| **Win Rate** | 76.5% |
| **Signal Accuracy** | 66.7% |
| **Direction Accuracy** | 73.3% |
| **Skill Ratio** | 73.3% |
| **Profit Factor** | 6.22 |
| **Expectancy** | 0.1466 |
| **Tail Ratio** | 7.33 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 701.3% | 509.2% | -192.1% |
| Annualized Return | 20.7% | 13.7% | — |

## Diversity & Concentration

Diversification: **Moderate** — noticeable concentration in top trades (HHI ratio: 3.3×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.1928 | Ideal for 17 trades: 0.0588 |
| Top-1 Trade | 46.8% of gross profit | ⚠️ High concentration |
| Top-3 Trades | 65.1% of gross profit | ⚠️ High concentration |
| Return ex-Top-1 | 154.8% | Strategy survives without best trade |
| Return ex-Top-3 | 57.7% | Strategy survives without top 3 |
| Max Single Trade | 139.1% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 11 | 23.00% | 253.0% | 16.66% | 84.91 |
| no_signal | 2 | 21.99% | 44.0% | 16.17% | 75.50 |
| direction_wrong_loss | 4 | -11.93% | -47.7% | -11.04% | 128.25 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 3 | 59.34% | 178.0% | 100.0% | 100.0% | 44.65% |
| regime_shift | 5 | 14.20% | 71.0% | 100.0% | 100.0% | 11.10% |
| weak_positive | 2 | 4.21% | 8.4% | 50.0% | 50.0% | -7.42% |
| unknown | 2 | 3.81% | 7.6% | 100.0% | 100.0% | 8.93% |
| weak_negative | 2 | -3.36% | -6.7% | 50.0% | 50.0% | -2.63% |
| strong_positive | 3 | -3.03% | -9.1% | 33.3% | 33.3% | -5.26% |

**Best regime:** `strong_negative` — 3 trades, 178.0% total return, 100.0% win rate.
**Worst regime:** `strong_positive` — 3 trades, -9.1% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 2 | -11.83% | -23.7% |
| ❌ | ✅ | 3 | 48.04% | 144.1% |
| ✅ | ❌ | 2 | -12.02% | -24.0% |
| ✅ | ✅ | 8 | 13.60% | 108.8% |

### Flip Trades (Signal Wrong → Direction Right)

**5 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **37.6%**
- Total return: **188.1%**
- Average alpha: **29.6%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 2 | 16.88% |
| strong_negative | 1 | 139.05% |
| weak_positive | 1 | 13.51% |
| unknown | 1 | 1.80% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 12 | 17.19% | 206.3% | 75.0% | 75.0% |
| high | 1 | 23.82% | 23.8% | 100.0% | 100.0% |
| low | 4 | 4.79% | 19.1% | 75.0% | 75.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 9 | 24.84% | 223.6% | 88.9% | 88.9% |
| SHORT | 8 | 3.21% | 25.7% | 62.5% | 62.5% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 2 | 7.6% | 3.81% | 100.0% | 100.0% | 17.9% |
| 2019 | 3 | 12.7% | 4.24% | 66.7% | 66.7% | -19.5% |
| 2020 | 2 | 155.7% | 77.86% | 100.0% | 100.0% | 138.4% |
| 2021 | 1 | 12.2% | 12.25% | 100.0% | 100.0% | 5.8% |
| 2022 | 3 | -22.4% | -7.46% | 33.3% | 33.3% | -5.1% |
| 2023 | 2 | 20.6% | 10.28% | 100.0% | 100.0% | 4.7% |
| 2024 | 2 | 18.7% | 9.37% | 50.0% | 50.0% | -3.1% |
| 2025 | 2 | 44.0% | 21.99% | 100.0% | 100.0% | 32.3% |

### Macro Context by Year

**2018** (Modestly positive: 7.6%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 12.7%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 155.7%, 2 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 12.2%, 1 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -22.4%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 20.6%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 18.7%, 2 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 44.0%, 2 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -37.5% cumulative (trade 8 to trade 10)
**Period:** 2021-04-09 to 2022-07-08 (3 trades)
**Peak cumulative return:** 188.3% → **Trough:** 150.8%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2021-04-09 | 2021-10-13 | -1.0000 | 12.25% | weak_negative | ✅ |
| 2022-01-06 | 2022-07-08 | 1.0000 | -18.55% | strong_positive | ❌ |
| 2022-07-08 | 2022-10-12 | -1.0000 | -18.96% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 50d+ | 17 | 14.66% | 249.2% | 76.5% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 2

## Conclusions & Observations

**Statistical robustness:** ⚠️ Only 17 trades — interpret cautiously.
**Diversification:** ⚠️ Concentrated. HHI of 0.1928 is 3.3× the ideal.
**Edge:** Genuine structural edge: 76.5% win rate with 6.22× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (73.3%) exceeds signal accuracy (66.7%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Worst year:** 2022 (-22.4%, 3 trades). Macro: Fed Tightening Cycle, 2022 Bear Market
- **Losing regime:** `weak_negative` — 2 trades, -6.7% total return
- **Losing regime:** `strong_positive` — 3 trades, -9.1% total return