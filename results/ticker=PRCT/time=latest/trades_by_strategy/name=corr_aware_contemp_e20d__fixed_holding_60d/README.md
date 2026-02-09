# Strategy Analysis: corr_aware_contemp_e20d × fixed_holding_60d

**Ticker:** PRCT
**Entry:** `corr_aware_contemp_e20d`
**Exit:** `fixed_holding_60d`
**Period:** 2023-03-29 to 2026-02-06
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
- **entry_days_before:** `20` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `False`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `fixed_holding_60d`
  - Fixed 60-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 280.6% |
| **Annualized Return** | 37.6% |
| **Sharpe Ratio** | 0.771 |
| **Max Drawdown** | -34.8% |
| **Total Trades** | 12 |
| **Win Rate** | 66.7% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 66.7% |
| **Skill Ratio** | 66.7% |
| **Profit Factor** | 4.47 |
| **Expectancy** | 0.1503 |
| **Tail Ratio** | 2.93 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.8×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.1499 | Ideal for 12 trades: 0.0833 |
| Top-1 Trade | 34.0% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 68.0% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 112.7% | Positive without best trade |
| Return ex-Top-3 | 9.4% | Positive without top 3 |
| Max Single Trade | 78.9% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 6 | 29.29% | 175.8% | 29.29% | 68.17 |
| no_signal | 3 | 16.65% | 49.9% | 16.65% | 45.33 |
| direction_wrong_loss | 3 | -15.12% | -45.4% | -15.12% | 54.67 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 3 | 27.86% | 83.6% | 66.7% | 66.7% | 27.86% |
| regime_shift | 3 | 21.58% | 64.8% | 100.0% | 100.0% | 21.58% |
| weak_negative | 1 | 45.10% | 45.1% | 100.0% | 100.0% | 45.10% |
| strong_negative | 2 | 0.82% | 1.6% | 50.0% | 50.0% | 0.82% |
| weak_positive | 1 | -6.57% | -6.6% | 0.0% | 0.0% | -6.57% |
| strong_positive | 2 | -4.09% | -8.2% | 50.0% | 50.0% | -4.09% |

**Best-performing regime:** `unknown` — 3 trades, 83.6% total return, 66.7% win rate.
**Worst-performing regime:** `strong_positive` — 2 trades, -8.2% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ✅ | ❌ | 3 | -15.12% | -45.4% |
| ✅ | ✅ | 6 | 29.29% | 175.8% |

### Flip Trades (Signal Wrong → Direction Right)

**2 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **28.3%**
- Total return: **56.5%**
- Average alpha: **28.3%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 1 | 11.41% |
| weak_negative | 1 | 45.10% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 8 | 12.92% | 103.3% | 75.0% | 75.0% |
| low | 4 | 19.25% | 77.0% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 7 | 14.69% | 102.9% | 57.1% | 57.1% |
| SHORT | 5 | 15.50% | 77.5% | 80.0% | 80.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 3 | 83.6% | 27.86% | 66.7% | 66.7% | 83.6% |
| 2024 | 5 | 27.5% | 5.50% | 60.0% | 60.0% | 27.5% |
| 2025 | 3 | 75.9% | 25.28% | 100.0% | 100.0% | 75.9% |
| 2026 | 1 | -6.6% | -6.57% | 0.0% | 0.0% | -6.6% |

### Macro Context by Year

**2023** (Strong year: 83.6%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 27.5%, 5 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 75.9%, 3 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -6.6%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -26.9% cumulative (trade 1 to trade 2)
**Period:** 2023-03-29 to 2023-07-26 (2 trades)
**Peak cumulative return:** 31.6% → **Trough:** 4.7%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-03-29 | 2023-07-25 | 1.0000 | 31.57% | unknown | ✅ |
| 2023-07-26 | 2023-10-20 | 1.0000 | -26.89% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 1 | 2.19% | 2.2% | 100.0% |
| 16-30d | 1 | -6.57% | -6.6% | 0.0% |
| 31-50d | 1 | -0.54% | -0.5% | 0.0% |
| 50d+ | 9 | 20.59% | 185.3% | 77.8% |

## Win/Loss Streaks

- **Max consecutive wins:** 3
- **Max consecutive losses:** 1

## Observations & Caveats

**Sample size:** ⚠️ Only 12 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (9.4%).
**Win/loss profile:** 66.7% win rate with 4.47× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (66.7%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2026 (-6.6%, 1 trades). Macro: No flagged events
- **Losing regime:** `weak_positive` — 1 trades, -6.6% total return
- **Losing regime:** `strong_positive` — 2 trades, -8.2% total return

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.