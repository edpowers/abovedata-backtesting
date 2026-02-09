# Strategy Analysis: corr_aware_contemp_conf0.3_sameq_e15d × trailing_stop_10%

**Ticker:** AGCO
**Entry:** `corr_aware_contemp_conf0.3_sameq_e15d`
**Exit:** `trailing_stop_10%`
**Period:** 2020-07-09 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **min_confidence:** `0.3`
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `False`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `trailing_stop_10%`
  - 10% trailing stop. More room for normal volatility, targets larger trends

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 267.3% |
| **Annualized Return** | 23.7% |
| **Sharpe Ratio** | 1.199 |
| **Max Drawdown** | -24.7% |
| **Total Trades** | 40 |
| **Win Rate** | 50.0% |
| **Signal Accuracy** | 48.5% |
| **Direction Accuracy** | 50.0% |
| **Skill Ratio** | 51.5% |
| **Profit Factor** | 2.61 |
| **Expectancy** | 0.0388 |
| **Tail Ratio** | 2.84 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 196.0% | 267.3% | 71.3% |
| Annualized Return | 21.5% | 23.7% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.8×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0461 | Ideal for 40 trades: 0.0250 |
| Top-1 Trade | 13.0% of gross profit | Moderate concentration |
| Top-3 Trades | 37.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 176.6% | Positive without best trade |
| Return ex-Top-3 | 63.2% | Positive without top 3 |
| Max Single Trade | 32.8% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 17 | 12.44% | 211.5% | 12.44% | 30.06 |
| no_signal | 7 | 1.05% | 7.4% | 1.05% | 29.00 |
| direction_wrong_loss | 16 | -3.99% | -63.8% | -3.99% | 12.94 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 19 | 3.53% | 67.1% | 47.4% | 47.4% | 3.53% |
| regime_shift | 10 | 6.47% | 64.7% | 60.0% | 60.0% | 6.47% |
| strong_positive | 3 | 7.78% | 23.3% | 66.7% | 66.7% | 7.78% |
| weak_negative | 5 | 0.34% | 1.7% | 40.0% | 40.0% | 0.34% |
| weak_positive | 3 | -0.59% | -1.8% | 33.3% | 33.3% | -0.59% |

**Best-performing regime:** `strong_negative` — 19 trades, 67.1% total return, 47.4% win rate.
**Worst-performing regime:** `weak_positive` — 3 trades, -1.8% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 8 | -3.34% | -26.8% |
| ❌ | ✅ | 9 | 14.79% | 133.1% |
| ✅ | ❌ | 8 | -4.63% | -37.1% |
| ✅ | ✅ | 8 | 9.79% | 78.3% |

### Flip Trades (Signal Wrong → Direction Right)

**12 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **14.4%**
- Total return: **173.2%**
- Average alpha: **14.4%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 6 | 13.39% |
| strong_negative | 5 | 17.03% |
| weak_positive | 1 | 7.77% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 24 | 6.62% | 158.8% | 54.2% | 54.2% |
| high | 16 | -0.23% | -3.8% | 43.8% | 43.8% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 31 | 4.54% | 140.8% | 48.4% | 48.4% |
| SHORT | 9 | 1.58% | 14.3% | 55.6% | 55.6% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 4 | 72.2% | 18.04% | 100.0% | 100.0% | 72.2% |
| 2021 | 4 | 19.1% | 4.77% | 25.0% | 25.0% | 19.1% |
| 2022 | 7 | 45.0% | 6.43% | 57.1% | 57.1% | 45.0% |
| 2023 | 8 | 2.1% | 0.27% | 37.5% | 37.5% | 2.1% |
| 2024 | 8 | 9.7% | 1.21% | 50.0% | 50.0% | 9.7% |
| 2025 | 8 | 24.0% | 3.00% | 50.0% | 50.0% | 24.0% |
| 2026 | 1 | -17.0% | -16.99% | 0.0% | 0.0% | -17.0% |

### Macro Context by Year

**2020** (Strong year: 72.2%, 4 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 19.1%, 4 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 45.0%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 2.1%, 8 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 9.7%, 8 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 24.0%, 8 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -17.0%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -29.9% cumulative (trade 26 to trade 34)
**Period:** 2024-07-09 to 2025-04-09 (9 trades)
**Peak cumulative return:** 170.7% → **Trough:** 140.8%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-07-09 | 2024-07-17 | 1.0000 | 9.85% | strong_negative | ✅ |
| 2024-07-18 | 2024-07-30 | 1.0000 | -5.88% | strong_negative | ❌ |
| 2024-07-31 | 2024-08-05 | 1.0000 | -7.18% | strong_negative | ❌ |
| 2024-10-15 | 2024-11-05 | 1.0000 | -8.63% | strong_negative | ❌ |
| 2024-11-06 | 2024-12-19 | 1.0000 | -3.90% | strong_negative | ❌ |
| 2024-12-20 | 2025-02-11 | 1.0000 | 2.92% | strong_negative | ✅ |
| 2025-02-12 | 2025-03-03 | 1.0000 | -6.58% | strong_negative | ❌ |
| 2025-03-04 | 2025-03-12 | 1.0000 | 6.26% | strong_negative | ✅ |
| 2025-04-09 | 2025-04-21 | 1.0000 | -6.88% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 3 | -1.40% | -4.2% | 33.3% |
| 16-30d | 9 | -0.34% | -3.0% | 33.3% |
| 31-50d | 8 | 8.13% | 65.0% | 75.0% |
| 50d+ | 5 | 19.91% | 99.5% | 100.0% |
| 6-15d | 15 | -0.15% | -2.3% | 33.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 4

## Observations & Caveats

**Sample size:** 40 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (63.2%).
**Win/loss profile:** Profit factor of 2.61 with 50.0% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (48.5%) and direction accuracy (50.0%) are similar, suggesting the correlation flip had limited net impact in this sample.

### Known Vulnerabilities

- **Worst year:** 2026 (-17.0%, 1 trades). Macro: No flagged events
- **Losing regime:** `weak_positive` — 3 trades, -1.8% total return

### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 196.0% buy-and-hold return (aligned to strategy period: None to None), yet 9 short trades returned 14.3% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.