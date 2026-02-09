# Strategy Analysis: corr_aware_contemp_e30d × fixed_holding_30d

**Ticker:** PRCT
**Entry:** `corr_aware_contemp_e30d`
**Exit:** `fixed_holding_30d`
**Period:** 2023-03-15 to 2026-02-06
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
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `False`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `fixed_holding_30d`
  - Fixed 30-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 310.5% |
| **Annualized Return** | 37.6% |
| **Sharpe Ratio** | 0.774 |
| **Max Drawdown** | -38.9% |
| **Total Trades** | 22 |
| **Win Rate** | 68.2% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 68.2% |
| **Skill Ratio** | 68.8% |
| **Profit Factor** | 3.73 |
| **Expectancy** | 0.0787 |
| **Tail Ratio** | 2.42 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.8×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0836 | Ideal for 22 trades: 0.0455 |
| Top-1 Trade | 22.2% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 49.1% of gross profit | Moderate concentration |
| Return ex-Top-1 | 169.1% | Positive without best trade |
| Return ex-Top-3 | 54.8% | Positive without top 3 |
| Max Single Trade | 52.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 11 | 17.12% | 188.3% | 17.12% | 33.18 |
| no_signal | 6 | 3.50% | 21.0% | 3.50% | 33.83 |
| direction_wrong_loss | 5 | -7.25% | -36.3% | -7.25% | 28.20 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 6 | 12.36% | 74.2% | 83.3% | 83.3% | 12.36% |
| unknown | 6 | 8.27% | 49.6% | 66.7% | 66.7% | 8.27% |
| strong_positive | 3 | 11.71% | 35.1% | 66.7% | 66.7% | 11.71% |
| weak_negative | 4 | 7.71% | 30.8% | 75.0% | 75.0% | 7.71% |
| strong_negative | 2 | -2.25% | -4.5% | 50.0% | 50.0% | -2.25% |
| weak_positive | 1 | -12.19% | -12.2% | 0.0% | 0.0% | -12.19% |

**Best-performing regime:** `regime_shift` — 6 trades, 74.2% total return, 83.3% win rate.
**Worst-performing regime:** `weak_positive` — 1 trades, -12.2% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ✅ | ❌ | 5 | -7.25% | -36.3% |
| ✅ | ✅ | 11 | 17.12% | 188.3% |

### Flip Trades (Signal Wrong → Direction Right)

**4 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **12.1%**
- Total return: **48.3%**
- Average alpha: **12.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 3 | 15.29% |
| regime_shift | 1 | 2.40% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 15 | 9.04% | 135.6% | 73.3% | 73.3% |
| low | 7 | 5.35% | 37.4% | 57.1% | 57.1% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 13 | 7.32% | 95.2% | 61.5% | 61.5% |
| SHORT | 9 | 8.66% | 77.9% | 77.8% | 77.8% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 6 | 49.6% | 8.27% | 66.7% | 66.7% | 49.6% |
| 2024 | 8 | 53.2% | 6.65% | 62.5% | 62.5% | 53.2% |
| 2025 | 8 | 70.2% | 8.78% | 75.0% | 75.0% | 70.2% |

### Macro Context by Year

**2023** (Strong year: 49.6%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 53.2%, 8 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 70.2%, 8 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -25.7% cumulative (trade 2 to trade 4)
**Period:** 2023-06-12 to 2023-09-11 (3 trades)
**Peak cumulative return:** 15.0% → **Trough:** -10.7%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-06-12 | 2023-07-26 | 1.0000 | 7.95% | unknown | ✅ |
| 2023-07-27 | 2023-09-08 | 1.0000 | -5.39% | unknown | ❌ |
| 2023-09-11 | 2023-10-23 | 1.0000 | -20.29% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 16-30d | 9 | 3.45% | 31.0% | 55.6% |
| 31-50d | 8 | 12.78% | 102.3% | 62.5% |
| 50d+ | 2 | 9.11% | 18.2% | 100.0% |
| 6-15d | 3 | 7.19% | 21.6% | 100.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 22 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (54.8%).
**Win/loss profile:** 68.2% win rate with 3.73× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (68.2%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Losing regime:** `strong_negative` — 2 trades, -4.5% total return
- **Losing regime:** `weak_positive` — 1 trades, -12.2% total return

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.