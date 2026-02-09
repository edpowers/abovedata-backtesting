# Strategy Analysis: corr_aware_contemp_noshift_sameq_e20d × trailing_stop_10%

**Ticker:** PRCT
**Entry:** `corr_aware_contemp_noshift_sameq_e20d`
**Exit:** `trailing_stop_10%`
**Period:** 2023-03-29 to 2026-01-26
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
- **skip_regime_shifts:** `True` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `20` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `False`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `trailing_stop_10%`
  - 10% trailing stop. More room for normal volatility, targets larger trends

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 73.1% |
| **Annualized Return** | 33.3% |
| **Sharpe Ratio** | 1.602 |
| **Max Drawdown** | -14.5% |
| **Total Trades** | 27 |
| **Win Rate** | 63.0% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 63.0% |
| **Skill Ratio** | 72.2% |
| **Profit Factor** | 1.89 |
| **Expectancy** | 0.0255 |
| **Tail Ratio** | 0.99 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0559 | Ideal for 27 trades: 0.0370 |
| Top-1 Trade | 12.7% of gross profit | Moderate concentration |
| Top-3 Trades | 36.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 46.1% | Positive without best trade |
| Return ex-Top-3 | 6.8% | Positive without top 3 |
| Max Single Trade | 18.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 13 | 7.78% | 101.1% | 7.78% | 9.38 |
| no_signal | 9 | 1.78% | 16.0% | 1.78% | 6.22 |
| direction_wrong_loss | 5 | -9.69% | -48.5% | -9.69% | 6.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_positive | 6 | 6.64% | 39.8% | 83.3% | 83.3% | 6.64% |
| weak_negative | 6 | 3.35% | 20.1% | 66.7% | 66.7% | 3.35% |
| weak_positive | 6 | 2.32% | 13.9% | 50.0% | 50.0% | 2.32% |
| strong_negative | 3 | 1.35% | 4.0% | 66.7% | 66.7% | 1.35% |
| unknown | 6 | -1.53% | -9.2% | 50.0% | 50.0% | -1.53% |

**Best-performing regime:** `strong_positive` — 6 trades, 39.8% total return, 83.3% win rate.
**Worst-performing regime:** `unknown` — 6 trades, -9.2% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ✅ | ❌ | 5 | -9.69% | -48.5% |
| ✅ | ✅ | 13 | 7.78% | 101.1% |

### Flip Trades (Signal Wrong → Direction Right)

**4 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **11.1%**
- Total return: **44.6%**
- Average alpha: **11.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_positive | 3 | 8.71% |
| weak_negative | 1 | 18.45% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 15 | 4.27% | 64.0% | 73.3% | 73.3% |
| low | 12 | 0.39% | 4.7% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 15 | 2.18% | 32.7% | 60.0% | 60.0% |
| SHORT | 12 | 3.00% | 36.0% | 66.7% | 66.7% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 9 | -5.1% | -0.57% | 55.6% | 55.6% | -5.1% |
| 2024 | 6 | 39.8% | 6.64% | 83.3% | 83.3% | 39.8% |
| 2025 | 9 | 32.0% | 3.56% | 66.7% | 66.7% | 32.0% |
| 2026 | 3 | 2.0% | 0.68% | 33.3% | 33.3% | 2.0% |

### Macro Context by Year

**2023** (Losing year: -5.1%, 9 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 39.8%, 6 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 32.0%, 9 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 2.0%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -35.7% cumulative (trade 2 to trade 8)
**Period:** 2023-04-04 to 2023-10-12 (7 trades)
**Peak cumulative return:** 26.5% → **Trough:** -9.2%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-04-04 | 2023-04-19 | 1.0000 | 10.97% | unknown | ✅ |
| 2023-04-20 | 2023-04-27 | 1.0000 | -25.06% | unknown | ❌ |
| 2023-06-28 | 2023-07-27 | 1.0000 | 0.85% | unknown | ✅ |
| 2023-07-28 | 2023-08-08 | 1.0000 | -6.74% | unknown | ❌ |
| 2023-08-09 | 2023-08-24 | 1.0000 | -4.75% | unknown | ❌ |
| 2023-10-04 | 2023-10-11 | -1.0000 | 4.61% | strong_negative | ✅ |
| 2023-10-12 | 2023-10-16 | -1.0000 | -4.64% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 12 | -0.93% | -11.2% | 50.0% |
| 16-30d | 2 | 4.83% | 9.7% | 100.0% |
| 6-15d | 13 | 5.40% | 70.2% | 69.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 3

## Observations & Caveats

**Sample size:** ⚠️ Only 27 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (6.8%).
**Win/loss profile:** 63.0% win rate with 1.89× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (63.0%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.
**Regime dependence:** `strong_positive` (6 trades, 22% of total) contributed 39.8% — a disproportionate share. Performance may degrade if this regime becomes less common.

### Known Vulnerabilities

- **Worst year:** 2023 (-5.1%, 9 trades). Macro: Fed Tightening Cycle, 2023 Soft Landing Rally
- **Losing regime:** `unknown` — 6 trades, -9.2% total return

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.