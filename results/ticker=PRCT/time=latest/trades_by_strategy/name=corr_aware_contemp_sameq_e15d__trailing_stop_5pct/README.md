# Strategy Analysis: corr_aware_contemp_sameq_e15d × trailing_stop_5%

**Ticker:** PRCT
**Entry:** `corr_aware_contemp_sameq_e15d`
**Exit:** `trailing_stop_5%`
**Period:** 2023-04-05 to 2026-01-21
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **min_confidence:** `0.0`
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `False`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | -7.0% |
| **Annualized Return** | 16.9% |
| **Sharpe Ratio** | 1.558 |
| **Max Drawdown** | -7.9% |
| **Total Trades** | 36 |
| **Win Rate** | 44.4% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 44.4% |
| **Skill Ratio** | 50.0% |
| **Profit Factor** | 0.94 |
| **Expectancy** | -0.0010 |
| **Tail Ratio** | 0.89 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.6×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0454 | Ideal for 36 trades: 0.0278 |
| Top-1 Trade | 17.2% of gross profit | Moderate concentration |
| Top-3 Trades | 39.6% of gross profit | Moderate concentration |
| Return ex-Top-1 | -15.7% | Negative without best trade |
| Return ex-Top-3 | -26.0% | Negative without top 3 |
| Max Single Trade | 10.4% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 12 | 4.16% | 50.0% | 4.16% | 2.25 |
| no_signal | 12 | -1.41% | -17.0% | -1.41% | 1.50 |
| direction_wrong_loss | 12 | -3.06% | -36.7% | -3.06% | 2.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 6 | 2.98% | 17.9% | 66.7% | 66.7% | 2.98% |
| regime_shift | 9 | 0.39% | 3.5% | 44.4% | 44.4% | 0.39% |
| strong_negative | 3 | 0.29% | 0.9% | 66.7% | 66.7% | 0.29% |
| weak_negative | 6 | -1.21% | -7.3% | 66.7% | 66.7% | -1.21% |
| strong_positive | 6 | -1.34% | -8.1% | 16.7% | 16.7% | -1.34% |
| weak_positive | 6 | -1.78% | -10.7% | 16.7% | 16.7% | -1.78% |

**Best-performing regime:** `unknown` — 6 trades, 17.9% total return, 66.7% win rate.
**Worst-performing regime:** `weak_positive` — 6 trades, -10.7% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ✅ | ❌ | 12 | -3.06% | -36.7% |
| ✅ | ✅ | 12 | 4.16% | 50.0% |

### Flip Trades (Signal Wrong → Direction Right)

**4 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **2.6%**
- Total return: **10.3%**
- Average alpha: **2.6%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 2 | 2.95% |
| weak_positive | 1 | 2.11% |
| regime_shift | 1 | 2.30% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 12 | 0.60% | 7.2% | 41.7% | 41.7% |
| medium | 24 | -0.45% | -10.9% | 45.8% | 45.8% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 21 | 0.04% | 0.9% | 33.3% | 33.3% |
| SHORT | 15 | -0.31% | -4.6% | 60.0% | 60.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 9 | 18.8% | 2.09% | 66.7% | 66.7% | 18.8% |
| 2024 | 12 | -4.3% | -0.36% | 33.3% | 33.3% | -4.3% |
| 2025 | 12 | -14.7% | -1.22% | 41.7% | 41.7% | -14.7% |
| 2026 | 3 | -3.4% | -1.15% | 33.3% | 33.3% | -3.4% |

### Macro Context by Year

**2023** (Strong year: 18.8%, 9 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Roughly flat: -4.3%, 12 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -14.7%, 12 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Roughly flat: -3.4%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -28.4% cumulative (trade 7 to trade 35)
**Period:** 2023-10-11 to 2026-01-14 (29 trades)
**Peak cumulative return:** 22.6% → **Trough:** -5.8%

**Macro context during drawdown:**
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-10-11 | 2023-10-12 | -1.0000 | 4.70% | strong_negative | ✅ |
| 2023-10-13 | 2023-10-16 | -1.0000 | -9.58% | strong_negative | ❌ |
| 2023-10-17 | 2023-10-23 | -1.0000 | 5.75% | strong_negative | ✅ |
| 2024-02-06 | 2024-02-13 | 1.0000 | -1.41% | regime_shift | ❌ |
| 2024-02-14 | 2024-02-15 | 1.0000 | -1.91% | regime_shift | ❌ |
| 2024-02-16 | 2024-02-20 | 1.0000 | -1.98% | regime_shift | ❌ |
| 2024-04-10 | 2024-04-12 | 1.0000 | -2.91% | strong_positive | ❌ |
| 2024-04-15 | 2024-04-16 | 1.0000 | 2.75% | strong_positive | ✅ |
| 2024-04-17 | 2024-04-18 | 1.0000 | -1.37% | strong_positive | ❌ |
| 2024-07-11 | 2024-07-15 | 1.0000 | -2.17% | strong_positive | ❌ |
| 2024-07-16 | 2024-07-18 | 1.0000 | -4.31% | strong_positive | ❌ |
| 2024-07-19 | 2024-07-24 | 1.0000 | -0.03% | strong_positive | ❌ |
| 2024-10-08 | 2024-10-10 | -1.0000 | 2.28% | regime_shift | ✅ |
| 2024-10-11 | 2024-10-17 | -1.0000 | 3.65% | regime_shift | ✅ |
| 2024-10-18 | 2024-10-24 | -1.0000 | 3.07% | regime_shift | ✅ |
| 2025-02-03 | 2025-02-05 | -1.0000 | -3.59% | weak_negative | ❌ |
| 2025-02-06 | 2025-02-07 | -1.0000 | 1.74% | weak_negative | ✅ |
| 2025-02-10 | 2025-02-13 | -1.0000 | 0.69% | weak_negative | ✅ |
| 2025-04-02 | 2025-04-03 | -1.0000 | 5.13% | weak_negative | ✅ |
| 2025-04-04 | 2025-04-07 | -1.0000 | 0.78% | weak_negative | ✅ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -12.00% | weak_negative | ❌ |
| 2025-07-03 | 2025-07-11 | 1.0000 | -2.19% | regime_shift | ❌ |
| 2025-07-14 | 2025-07-15 | 1.0000 | -0.28% | regime_shift | ❌ |
| 2025-07-16 | 2025-07-18 | 1.0000 | 2.30% | regime_shift | ✅ |
| 2025-10-15 | 2025-10-16 | -1.0000 | -0.53% | weak_positive | ❌ |
| 2025-10-17 | 2025-10-20 | -1.0000 | -5.31% | weak_positive | ❌ |
| 2025-10-21 | 2025-10-22 | -1.0000 | -1.42% | weak_positive | ❌ |
| 2026-01-12 | 2026-01-13 | 1.0000 | -2.39% | weak_positive | ❌ |
| 2026-01-14 | 2026-01-16 | 1.0000 | -3.16% | weak_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 36 | -0.10% | -3.7% | 44.4% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 5

## Observations & Caveats

**Sample size:** 36 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-26.0%).
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (44.4%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.
**Regime dependence:** `unknown` (6 trades, 17% of total) contributed 17.9% — a disproportionate share. Performance may degrade if this regime becomes less common.

### Known Vulnerabilities

- **Worst year:** 2025 (-14.7%, 12 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery
- **Losing regime:** `weak_negative` — 6 trades, -7.3% total return
- **Losing regime:** `strong_positive` — 6 trades, -8.1% total return
- **Losing regime:** `weak_positive` — 6 trades, -10.7% total return

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.