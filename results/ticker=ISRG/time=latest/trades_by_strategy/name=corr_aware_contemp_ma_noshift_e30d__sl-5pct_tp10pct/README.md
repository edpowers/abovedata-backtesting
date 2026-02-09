# Strategy Analysis: corr_aware_contemp_ma_noshift_e30d × sl-5%_tp10%

**Ticker:** ISRG
**Entry:** `corr_aware_contemp_ma_noshift_e30d`
**Exit:** `sl-5%_tp10%`
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

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit creates a 2:1 reward/risk ratio — when direction is correct, gains are 2× what losses are when wrong

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 536.9% |
| **Annualized Return** | 12.0% |
| **Sharpe Ratio** | 0.632 |
| **Max Drawdown** | -22.1% |
| **Total Trades** | 88 |
| **Win Rate** | 54.5% |
| **Signal Accuracy** | 46.7% |
| **Direction Accuracy** | 54.7% |
| **Skill Ratio** | 54.7% |
| **Profit Factor** | 1.91 |
| **Expectancy** | 0.0248 |
| **Tail Ratio** | 1.45 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | 730.6% | 536.9% | -193.7% |
| Annualized Return | 21.1% | 12.0% | — |

## Diversity & Concentration

Diversification: **Excellent** — nearly perfectly diversified (HHI ratio: 1.2×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0141 | Ideal for 88 trades: 0.0114 |
| Top-1 Trade | 4.7% of gross profit | ✅ Low concentration |
| Top-3 Trades | 11.8% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 425.1% | Strategy survives without best trade |
| Return ex-Top-3 | 287.2% | Strategy survives without top 3 |
| Max Single Trade | 21.3% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 41 | 9.45% | 387.6% | 10.07% | 14.95 |
| no_signal | 13 | 2.71% | 35.3% | 1.62% | 12.23 |
| direction_wrong_loss | 34 | -6.02% | -204.8% | -7.85% | 13.24 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 28 | 3.19% | 89.4% | 57.1% | 57.1% | 3.21% |
| strong_negative | 15 | 5.84% | 87.5% | 73.3% | 73.3% | 4.55% |
| unknown | 14 | 1.94% | 27.1% | 57.1% | 57.1% | 2.49% |
| weak_positive | 10 | 0.87% | 8.7% | 40.0% | 40.0% | 0.33% |
| weak_negative | 7 | 0.83% | 5.8% | 57.1% | 57.1% | -0.43% |
| strong_positive | 14 | -0.04% | -0.5% | 35.7% | 35.7% | -1.90% |

**Best regime:** `regime_shift` — 28 trades, 89.4% total return, 57.1% win rate.
**Worst regime:** `strong_positive` — 14 trades, -0.5% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 18 | -6.46% | -116.2% |
| ❌ | ✅ | 22 | 8.90% | 195.8% |
| ✅ | ❌ | 16 | -5.54% | -88.6% |
| ✅ | ✅ | 19 | 10.10% | 191.8% |

### Flip Trades (Signal Wrong → Direction Right)

**29 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **9.2%**
- Total return: **265.6%**
- Average alpha: **9.9%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 10 | 9.93% |
| unknown | 6 | 8.22% |
| weak_positive | 4 | 8.20% |
| strong_negative | 4 | 10.45% |
| weak_negative | 4 | 7.87% |
| strong_positive | 1 | 10.90% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 56 | 2.72% | 152.1% | 55.4% | 55.4% |
| high | 9 | 5.30% | 47.7% | 66.7% | 66.7% |
| low | 21 | 0.56% | 11.8% | 47.6% | 47.6% |
| no_data | 2 | 3.26% | 6.5% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 39 | 4.32% | 168.4% | 64.1% | 64.1% |
| SHORT | 49 | 1.01% | 49.7% | 46.9% | 46.9% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 24 | 45.2% | 1.88% | 54.2% | 54.2% | 50.2% |
| 2021 | 11 | 62.4% | 5.67% | 72.7% | 72.7% | 45.5% |
| 2022 | 17 | 3.1% | 0.18% | 41.2% | 41.2% | 14.5% |
| 2023 | 10 | 68.9% | 6.89% | 80.0% | 80.0% | 52.0% |
| 2024 | 12 | 7.7% | 0.64% | 41.7% | 41.7% | -14.5% |
| 2025 | 12 | 24.3% | 2.02% | 50.0% | 50.0% | 14.1% |
| 2026 | 2 | 6.5% | 3.26% | 50.0% | 50.0% | 5.0% |

### Macro Context by Year

**2020** (Strong year: 45.2%, 24 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 62.4%, 11 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Modestly positive: 3.1%, 17 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 68.9%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 7.7%, 12 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 24.3%, 12 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 6.5%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -48.2% cumulative (trade 5 to trade 12)
**Period:** 2020-03-19 to 2020-06-08 (8 trades)
**Peak cumulative return:** 49.3% → **Trough:** 1.1%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-03-19 | 2020-03-20 | -1.0000 | 3.43% | unknown | ✅ |
| 2020-03-23 | 2020-03-24 | -1.0000 | -17.44% | unknown | ❌ |
| 2020-03-25 | 2020-03-26 | -1.0000 | -8.94% | unknown | ❌ |
| 2020-03-27 | 2020-04-07 | -1.0000 | 0.09% | unknown | ✅ |
| 2020-04-08 | 2020-05-07 | -1.0000 | -4.98% | unknown | ❌ |
| 2020-05-08 | 2020-05-26 | -1.0000 | -4.34% | unknown | ❌ |
| 2020-05-27 | 2020-06-05 | -1.0000 | -4.96% | unknown | ❌ |
| 2020-06-08 | 2020-06-11 | 1.0000 | -7.57% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 27 | 0.46% | 12.4% | 44.4% |
| 16-30d | 29 | 4.62% | 134.0% | 65.5% |
| 31-50d | 7 | 2.24% | 15.6% | 57.1% |
| 6-15d | 25 | 2.24% | 56.0% | 52.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 4

## Conclusions & Observations

**Statistical robustness:** With 88 trades, this sample is large enough for reliable inference.
**Diversification:** Excellent. HHI of 0.0141 is near the theoretical minimum of 0.0114. No single trade dominates returns.
**Edge:** Genuine structural edge: 54.5% win rate with 1.91× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (54.7%) exceeds signal accuracy (46.7%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Losing regime:** `strong_positive` — 14 trades, -0.5% total return