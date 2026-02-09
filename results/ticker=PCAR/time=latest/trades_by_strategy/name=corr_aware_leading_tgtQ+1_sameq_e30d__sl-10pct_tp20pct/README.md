# Strategy Analysis: corr_aware_leading_tgtQ+1_sameq_e30d × sl-10%_tp20%

**Ticker:** PCAR
**Entry:** `corr_aware_leading_tgtQ+1_sameq_e30d`
**Exit:** `sl-10%_tp20%`
**Period:** 2023-03-13 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `leading` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **min_confidence:** `0.0`
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `leading` — Which confidence metric to use for scaling
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `True`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 122.9% |
| **Annualized Return** | 4.0% |
| **Sharpe Ratio** | 0.316 |
| **Max Drawdown** | -20.7% |
| **Total Trades** | 17 |
| **Win Rate** | 64.7% |
| **Signal Accuracy** | 50.0% |
| **Direction Accuracy** | 64.7% |
| **Skill Ratio** | 58.3% |
| **Profit Factor** | 3.69 |
| **Expectancy** | 0.0532 |
| **Tail Ratio** | 1.69 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 98.7% | 122.9% | 24.2% |
| Annualized Return | 26.7% | 4.0% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0889 | Ideal for 17 trades: 0.0588 |
| Top-1 Trade | 16.9% of gross profit | Moderate concentration |
| Top-3 Trades | 48.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 84.2% | Positive without best trade |
| Return ex-Top-3 | 28.5% | Positive without top 3 |
| Max Single Trade | 21.0% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 7 | 14.14% | 99.0% | 14.14% | 44.00 |
| no_signal | 5 | 2.60% | 13.0% | 2.60% | 33.20 |
| direction_wrong_loss | 5 | -4.32% | -21.6% | -4.32% | 49.40 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_positive | 5 | 10.46% | 52.3% | 80.0% | 80.0% | 10.46% |
| regime_shift | 4 | 4.34% | 17.4% | 50.0% | 50.0% | 4.34% |
| strong_negative | 5 | 2.60% | 13.0% | 80.0% | 80.0% | 2.60% |
| unknown | 3 | 2.57% | 7.7% | 33.3% | 33.3% | 2.57% |

**Best-performing regime:** `strong_positive` — 5 trades, 52.3% total return, 80.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 3 | -5.83% | -17.5% |
| ❌ | ✅ | 3 | 13.44% | 40.3% |
| ✅ | ❌ | 2 | -2.05% | -4.1% |
| ✅ | ✅ | 4 | 14.67% | 58.7% |

### Flip Trades (Signal Wrong → Direction Right)

**7 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **9.3%**
- Total return: **65.3%**
- Average alpha: **9.3%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_negative | 4 | 6.26% |
| strong_positive | 2 | 11.95% |
| regime_shift | 1 | 16.41% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 12 | 7.55% | 90.6% | 75.0% | 75.0% |
| low | 3 | 2.57% | 7.7% | 33.3% | 33.3% |
| high | 2 | -3.99% | -8.0% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 10 | 8.61% | 86.1% | 80.0% | 80.0% |
| SHORT | 7 | 0.62% | 4.3% | 42.9% | 42.9% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 4 | 17.0% | 4.26% | 50.0% | 50.0% | 17.0% |
| 2024 | 6 | 54.9% | 9.15% | 66.7% | 66.7% | 54.9% |
| 2025 | 6 | 8.0% | 1.33% | 66.7% | 66.7% | 8.0% |
| 2026 | 1 | 10.5% | 10.45% | 100.0% | 100.0% | 10.5% |

### Macro Context by Year

**2023** (Strong year: 17.0%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 54.9%, 6 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 8.0%, 6 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 10.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -13.3% cumulative (trade 1 to trade 3)
**Period:** 2023-03-13 to 2023-09-12 (3 trades)
**Peak cumulative return:** 21.0% → **Trough:** 7.7%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-03-13 | 2023-07-11 | 1.0000 | 21.01% | unknown | ✅ |
| 2023-07-12 | 2023-09-12 | 1.0000 | -0.86% | unknown | ❌ |
| 2023-09-12 | 2023-12-07 | -1.0000 | -12.43% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 1 | -0.55% | -0.5% | 0.0% |
| 16-30d | 5 | 9.90% | 49.5% | 100.0% |
| 31-50d | 5 | 4.18% | 20.9% | 60.0% |
| 50d+ | 5 | 2.37% | 11.9% | 40.0% |
| 6-15d | 1 | 8.71% | 8.7% | 100.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 3
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 17 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (28.5%).
**Win/loss profile:** 64.7% win rate with 3.69× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (64.7%) exceeded signal accuracy (50.0%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.
**Regime dependence:** `strong_positive` (5 trades, 29% of total) contributed 52.3% — a disproportionate share. Performance may degrade if this regime becomes less common.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 98.7% buy-and-hold return (aligned to strategy period: None to None), yet 7 short trades returned 4.3% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.