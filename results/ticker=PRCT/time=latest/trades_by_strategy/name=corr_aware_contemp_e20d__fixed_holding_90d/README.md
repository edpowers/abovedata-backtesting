# Strategy Analysis: corr_aware_contemp_e20d × fixed_holding_90d

**Ticker:** PRCT
**Entry:** `corr_aware_contemp_e20d`
**Exit:** `fixed_holding_90d`
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

- **Exit type:** `fixed_holding_90d`
  - Fixed 90-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 337.2% |
| **Annualized Return** | 38.3% |
| **Sharpe Ratio** | 0.785 |
| **Max Drawdown** | -35.9% |
| **Total Trades** | 5 |
| **Win Rate** | 80.0% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 80.0% |
| **Skill Ratio** | 100.0% |
| **Profit Factor** | 30.44 |
| **Expectancy** | 0.3867 |
| **Tail Ratio** | 11.69 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.3064 | Ideal for 5 trades: 0.2000 |
| Top-1 Trade | 38.4% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 98.1% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 147.3% | Positive without best trade |
| Return ex-Top-3 | -2.9% | Negative without top 3 |
| Max Single Trade | 76.8% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 4 | 49.98% | 199.9% | 49.98% | 173.25 |
| no_signal | 1 | -6.57% | -6.6% | -6.57% | 24.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 2 | 59.63% | 119.3% | 100.0% | 100.0% | 59.63% |
| unknown | 1 | 76.75% | 76.8% | 100.0% | 100.0% | 76.75% |
| strong_negative | 1 | 3.88% | 3.9% | 100.0% | 100.0% | 3.88% |
| weak_positive | 1 | -6.57% | -6.6% | 0.0% | 0.0% | -6.57% |

**Best-performing regime:** `regime_shift` — 2 trades, 119.3% total return, 100.0% win rate.
**Worst-performing regime:** `weak_positive` — 1 trades, -6.6% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ✅ | ✅ | 4 | 49.98% | 199.9% |


## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 3 | 41.05% | 123.1% | 100.0% | 100.0% |
| low | 2 | 35.09% | 70.2% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 3 | 43.55% | 130.6% | 66.7% | 66.7% |
| SHORT | 2 | 31.35% | 62.7% | 100.0% | 100.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 1 | 76.8% | 76.75% | 100.0% | 100.0% | 76.8% |
| 2024 | 2 | 64.3% | 32.17% | 100.0% | 100.0% | 64.3% |
| 2025 | 1 | 58.8% | 58.82% | 100.0% | 100.0% | 58.8% |
| 2026 | 1 | -6.6% | -6.57% | 0.0% | 0.0% | -6.6% |

### Macro Context by Year

**2023** (Strong year: 76.8%, 1 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 64.3%, 2 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 58.8%, 1 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -6.6%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -6.6% cumulative (trade 4 to trade 5)
**Period:** 2025-01-27 to 2026-01-02 (2 trades)
**Peak cumulative return:** 199.9% → **Trough:** 193.3%

**Macro context during drawdown:**
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-01-27 | 2026-01-02 | -1.0000 | 58.82% | regime_shift | ✅ |
| 2026-01-02 | 2026-02-06 | 1.0000 | -6.57% | weak_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 16-30d | 1 | -6.57% | -6.6% | 0.0% |
| 31-50d | 1 | 3.88% | 3.9% | 100.0% |
| 50d+ | 3 | 65.34% | 196.0% | 100.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 1

## Observations & Caveats

**Sample size:** ⚠️ Only 5 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-2.9%).
**Win/loss profile:** 80.0% win rate with 30.44× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (80.0%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2026 (-6.6%, 1 trades). Macro: No flagged events
- **Losing regime:** `weak_positive` — 1 trades, -6.6% total return

### ⚠️ Robustness Red Flags

- **SUSPICIOUSLY_PERFECT:** Profit factor of 30.4 with only 5 trades suggests the strategy may be avoiding losses through exit timing rather than signal skill. These results almost always degrade catastrophically out of sample.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.