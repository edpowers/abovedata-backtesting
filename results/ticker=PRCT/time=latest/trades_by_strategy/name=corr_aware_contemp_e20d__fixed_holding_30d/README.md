# Strategy Analysis: corr_aware_contemp_e20d × fixed_holding_30d

**Ticker:** PRCT
**Entry:** `corr_aware_contemp_e20d`
**Exit:** `fixed_holding_30d`
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

- **Exit type:** `fixed_holding_30d`
  - Fixed 30-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 405.0% |
| **Annualized Return** | 38.3% |
| **Sharpe Ratio** | 0.793 |
| **Max Drawdown** | -33.1% |
| **Total Trades** | 23 |
| **Win Rate** | 73.9% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 73.9% |
| **Skill Ratio** | 75.0% |
| **Profit Factor** | 4.00 |
| **Expectancy** | 0.0857 |
| **Tail Ratio** | 2.26 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.8×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0762 | Ideal for 23 trades: 0.0435 |
| Top-1 Trade | 20.0% of gross profit | Moderate concentration |
| Top-3 Trades | 44.2% of gross profit | Moderate concentration |
| Return ex-Top-1 | 231.1% | Positive without best trade |
| Return ex-Top-3 | 90.5% | Positive without top 3 |
| Max Single Trade | 52.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 12 | 17.37% | 208.5% | 17.37% | 31.42 |
| no_signal | 7 | 4.67% | 32.7% | 4.67% | 29.00 |
| direction_wrong_loss | 4 | -11.01% | -44.1% | -11.01% | 29.75 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 7 | 10.63% | 74.4% | 85.7% | 85.7% | 10.63% |
| unknown | 6 | 11.75% | 70.5% | 66.7% | 66.7% | 11.75% |
| weak_negative | 4 | 7.71% | 30.8% | 75.0% | 75.0% | 7.71% |
| strong_positive | 3 | 7.24% | 21.7% | 66.7% | 66.7% | 7.24% |
| strong_negative | 2 | 3.10% | 6.2% | 100.0% | 100.0% | 3.10% |
| weak_positive | 1 | -6.57% | -6.6% | 0.0% | 0.0% | -6.57% |

**Best-performing regime:** `regime_shift` — 7 trades, 74.4% total return, 85.7% win rate.
**Worst-performing regime:** `weak_positive` — 1 trades, -6.6% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ✅ | ❌ | 4 | -11.01% | -44.1% |
| ✅ | ✅ | 12 | 17.37% | 208.5% |

### Flip Trades (Signal Wrong → Direction Right)

**5 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **10.9%**
- Total return: **54.3%**
- Average alpha: **10.9%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 3 | 15.29% |
| regime_shift | 2 | 4.21% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 16 | 8.32% | 133.1% | 81.2% | 81.2% |
| low | 7 | 9.13% | 63.9% | 57.1% | 57.1% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 13 | 8.93% | 116.1% | 61.5% | 61.5% |
| SHORT | 10 | 8.10% | 81.0% | 90.0% | 90.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 6 | 70.5% | 11.75% | 66.7% | 66.7% | 70.5% |
| 2024 | 8 | 58.4% | 7.30% | 75.0% | 75.0% | 58.4% |
| 2025 | 8 | 74.8% | 9.35% | 87.5% | 87.5% | 74.8% |
| 2026 | 1 | -6.6% | -6.57% | 0.0% | 0.0% | -6.6% |

### Macro Context by Year

**2023** (Strong year: 70.5%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 58.4%, 8 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 74.8%, 8 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -6.6%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -25.7% cumulative (trade 2 to trade 4)
**Period:** 2023-06-12 to 2023-09-11 (3 trades)
**Peak cumulative return:** 32.1% → **Trough:** 6.4%

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
| 1-5d | 3 | 6.35% | 19.1% | 100.0% |
| 16-30d | 10 | 1.48% | 14.8% | 50.0% |
| 31-50d | 8 | 18.25% | 146.0% | 87.5% |
| 50d+ | 1 | 11.20% | 11.2% | 100.0% |
| 6-15d | 1 | 6.02% | 6.0% | 100.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 23 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (90.5%).
**Win/loss profile:** 73.9% win rate with 4.00× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (73.9%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2026 (-6.6%, 1 trades). Macro: No flagged events
- **Losing regime:** `weak_positive` — 1 trades, -6.6% total return

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.