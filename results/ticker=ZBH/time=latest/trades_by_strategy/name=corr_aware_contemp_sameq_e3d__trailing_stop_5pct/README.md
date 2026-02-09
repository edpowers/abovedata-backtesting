# Strategy Analysis: corr_aware_contemp_sameq_e3d × trailing_stop_5%

**Ticker:** ZBH
**Entry:** `corr_aware_contemp_sameq_e3d`
**Exit:** `trailing_stop_5%`
**Period:** 2019-10-31 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `3` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 21.3% |
| **Annualized Return** | 25.6% |
| **Sharpe Ratio** | 1.417 |
| **Max Drawdown** | -23.7% |
| **Total Trades** | 166 |
| **Win Rate** | 44.0% |
| **Signal Accuracy** | 31.9% |
| **Direction Accuracy** | 45.7% |
| **Skill Ratio** | 45.7% |
| **Profit Factor** | 1.12 |
| **Expectancy** | 0.0024 |
| **Tail Ratio** | 1.33 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -10.7% | 21.3% | 32.0% |
| Annualized Return | -1.0% | 25.6% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0090 | Ideal for 166 trades: 0.0060 |
| Top-1 Trade | 3.8% of gross profit | Moderate concentration |
| Top-3 Trades | 10.4% of gross profit | Moderate concentration |
| Return ex-Top-1 | 6.8% | Positive without best trade |
| Return ex-Top-3 | -14.6% | Negative without top 3 |
| Max Single Trade | 13.6% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 63 | 5.06% | 318.5% | 3.65% | 13.02 |
| no_signal | 28 | -1.00% | -28.0% | -2.18% | 8.00 |
| direction_wrong_loss | 75 | -3.35% | -250.9% | -3.36% | 4.96 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 57 | 0.84% | 47.8% | 50.9% | 50.9% | 0.05% |
| weak_positive | 12 | 1.89% | 22.7% | 50.0% | 50.0% | 1.94% |
| unknown | 2 | 5.25% | 10.5% | 50.0% | 50.0% | 0.88% |
| strong_negative | 28 | 0.07% | 1.8% | 46.4% | 46.4% | -0.55% |
| weak_negative | 33 | -0.36% | -12.0% | 42.4% | 42.4% | -1.26% |
| strong_positive | 34 | -0.92% | -31.3% | 29.4% | 29.4% | -1.57% |

**Best-performing regime:** `regime_shift` — 57 trades, 47.8% total return, 50.9% win rate.
**Worst-performing regime:** `strong_positive` — 34 trades, -31.3% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 52 | -3.38% | -176.0% |
| ❌ | ✅ | 42 | 5.04% | 211.9% |
| ✅ | ❌ | 23 | -3.26% | -75.0% |
| ✅ | ✅ | 21 | 5.08% | 106.6% |

### Flip Trades (Signal Wrong → Direction Right)

**52 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.8%**
- Total return: **250.0%**
- Average alpha: **3.3%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 16 | 5.34% |
| strong_negative | 13 | 5.27% |
| weak_negative | 11 | 3.99% |
| strong_positive | 8 | 3.81% |
| weak_positive | 4 | 5.41% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 113 | 0.63% | 70.7% | 49.6% | 49.6% |
| no_data | 1 | -1.33% | -1.3% | 0.0% | 0.0% |
| low | 11 | -0.22% | -2.4% | 36.4% | 36.4% |
| high | 41 | -0.67% | -27.4% | 31.7% | 31.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 95 | 0.17% | 16.3% | 45.3% | 45.3% |
| SHORT | 71 | 0.33% | 23.3% | 42.3% | 42.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2019 | 1 | 11.8% | 11.83% | 100.0% | 100.0% | 5.0% |
| 2020 | 45 | 9.8% | 0.22% | 48.9% | 48.9% | -16.6% |
| 2021 | 21 | 48.8% | 2.32% | 61.9% | 61.9% | 31.3% |
| 2022 | 30 | -16.4% | -0.55% | 36.7% | 36.7% | -13.2% |
| 2023 | 20 | 16.2% | 0.81% | 40.0% | 40.0% | -7.6% |
| 2024 | 19 | -4.9% | -0.26% | 36.8% | 36.8% | -19.6% |
| 2025 | 27 | -18.0% | -0.67% | 40.7% | 40.7% | -52.7% |
| 2026 | 3 | -7.7% | -2.58% | 0.0% | 0.0% | -9.1% |

### Macro Context by Year

**2019** (Strong year: 11.8%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Modestly positive: 9.8%, 45 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 48.8%, 21 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -16.4%, 30 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 16.2%, 20 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Roughly flat: -4.9%, 19 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -18.0%, 27 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -7.7%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -48.9% cumulative (trade 110 to trade 166)
**Period:** 2023-09-29 to 2026-02-05 (57 trades)
**Peak cumulative return:** 88.4% → **Trough:** 39.5%

**Macro context during drawdown:**
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-09-29 | 2023-10-11 | -1.0000 | 6.12% | weak_positive | ✅ |
| 2023-10-12 | 2023-10-17 | -1.0000 | -3.77% | weak_positive | ❌ |
| 2023-10-18 | 2023-11-02 | -1.0000 | -3.78% | weak_positive | ❌ |
| 2023-11-03 | 2023-11-13 | -1.0000 | 2.69% | weak_positive | ✅ |
| 2023-11-14 | 2023-11-17 | -1.0000 | -3.33% | strong_positive | ❌ |
| 2023-11-20 | 2023-12-01 | -1.0000 | -4.86% | strong_positive | ❌ |
| 2023-12-04 | 2023-12-20 | -1.0000 | -2.66% | strong_positive | ❌ |
| 2023-12-21 | 2024-01-11 | -1.0000 | -2.49% | strong_positive | ❌ |
| 2024-01-12 | 2024-01-31 | -1.0000 | -2.06% | strong_positive | ❌ |
| 2024-02-01 | 2024-02-09 | -1.0000 | 3.50% | strong_positive | ✅ |
| 2024-02-12 | 2024-02-21 | -1.0000 | -1.99% | weak_positive | ❌ |
| 2024-02-22 | 2024-03-27 | -1.0000 | -3.36% | weak_positive | ❌ |
| 2024-03-28 | 2024-04-29 | -1.0000 | 7.78% | weak_positive | ✅ |
| 2024-04-29 | 2024-05-02 | 1.0000 | -2.67% | weak_positive | ❌ |
| 2024-05-03 | 2024-05-23 | 1.0000 | -4.78% | regime_shift | ❌ |
| 2024-05-24 | 2024-06-10 | 1.0000 | -3.03% | regime_shift | ❌ |
| 2024-06-11 | 2024-06-12 | 1.0000 | -1.63% | regime_shift | ❌ |
| 2024-06-13 | 2024-08-02 | 1.0000 | 3.40% | regime_shift | ✅ |
| 2024-08-02 | 2024-08-05 | -1.0000 | 3.01% | regime_shift | ✅ |
| 2024-08-06 | 2024-08-16 | -1.0000 | -0.99% | regime_shift | ❌ |
| 2024-08-19 | 2024-08-26 | -1.0000 | -2.56% | weak_negative | ❌ |
| 2024-08-27 | 2024-09-27 | -1.0000 | 5.62% | weak_negative | ✅ |
| 2024-09-30 | 2024-10-18 | -1.0000 | 1.52% | weak_negative | ✅ |
| 2024-10-21 | 2024-10-30 | -1.0000 | -4.38% | weak_negative | ❌ |
| 2024-10-31 | 2024-11-06 | -1.0000 | -3.04% | weak_negative | ❌ |
| 2024-11-07 | 2024-11-18 | -1.0000 | -3.98% | weak_negative | ❌ |
| 2024-11-19 | 2025-01-13 | -1.0000 | 4.71% | weak_negative | ✅ |
| 2025-01-14 | 2025-01-16 | -1.0000 | -4.04% | weak_negative | ❌ |
| 2025-01-17 | 2025-02-06 | -1.0000 | 6.27% | weak_negative | ✅ |
| 2025-02-07 | 2025-02-19 | -1.0000 | -2.39% | regime_shift | ❌ |
| 2025-02-20 | 2025-03-07 | -1.0000 | -4.21% | regime_shift | ❌ |
| 2025-03-10 | 2025-03-14 | -1.0000 | 0.61% | regime_shift | ✅ |
| 2025-03-17 | 2025-04-03 | -1.0000 | -0.99% | regime_shift | ❌ |
| 2025-04-04 | 2025-04-07 | -1.0000 | 2.33% | regime_shift | ✅ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -0.63% | regime_shift | ❌ |
| 2025-04-10 | 2025-04-15 | -1.0000 | 4.88% | regime_shift | ✅ |
| 2025-04-16 | 2025-04-23 | -1.0000 | -2.59% | regime_shift | ❌ |
| 2025-04-24 | 2025-04-30 | -1.0000 | -1.53% | regime_shift | ❌ |
| 2025-04-30 | 2025-05-05 | 1.0000 | -12.20% | regime_shift | ❌ |
| 2025-05-06 | 2025-05-19 | 1.0000 | 3.79% | strong_negative | ✅ |
| 2025-05-20 | 2025-05-22 | 1.0000 | -3.86% | strong_negative | ❌ |
| 2025-05-23 | 2025-06-03 | 1.0000 | -0.85% | strong_negative | ❌ |
| 2025-06-04 | 2025-06-16 | 1.0000 | 0.77% | strong_negative | ✅ |
| 2025-06-17 | 2025-07-30 | 1.0000 | 3.72% | strong_negative | ✅ |
| 2025-07-31 | 2025-08-07 | 1.0000 | 7.40% | strong_negative | ✅ |
| 2025-08-08 | 2025-09-10 | 1.0000 | 3.06% | weak_negative | ✅ |
| 2025-09-11 | 2025-09-16 | 1.0000 | -4.93% | weak_negative | ❌ |
| 2025-09-17 | 2025-09-25 | 1.0000 | -2.95% | weak_negative | ❌ |
| 2025-09-26 | 2025-10-10 | 1.0000 | -3.36% | weak_negative | ❌ |
| 2025-10-13 | 2025-10-28 | 1.0000 | 6.36% | weak_negative | ✅ |
| 2025-10-29 | 2025-11-05 | 1.0000 | -12.20% | weak_negative | ❌ |
| 2025-11-06 | 2025-12-03 | 1.0000 | 5.19% | weak_negative | ✅ |
| 2025-12-04 | 2025-12-19 | 1.0000 | -4.33% | weak_negative | ❌ |
| 2025-12-22 | 2026-01-13 | 1.0000 | -1.36% | weak_negative | ❌ |
| 2026-01-14 | 2026-01-27 | 1.0000 | -3.64% | weak_negative | ❌ |
| 2026-01-28 | 2026-02-04 | -1.0000 | -2.78% | weak_negative | ❌ |
| 2026-02-05 | 2026-02-06 | -1.0000 | -1.33% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 82 | -1.27% | -104.5% | 30.5% |
| 16-30d | 16 | 5.49% | 87.9% | 87.5% |
| 31-50d | 5 | 5.15% | 25.8% | 100.0% |
| 50d+ | 2 | 11.82% | 23.6% | 100.0% |
| 6-15d | 61 | 0.11% | 6.7% | 44.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 8

## Observations & Caveats

**Sample size:** 166 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Well-distributed. HHI of 0.0090 is near the theoretical minimum of 0.0060 for 166 trades.
**Win/loss profile:** Profit factor of 1.12 with 44.0% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (45.7%) exceeded signal accuracy (31.9%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2025 (-18.0%, 27 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery
- **Losing regime:** `weak_negative` — 33 trades, -12.0% total return
- **Losing regime:** `strong_positive` — 34 trades, -31.3% total return

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.