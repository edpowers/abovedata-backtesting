# Strategy Analysis: corr_aware_leading_tgtQ+1_noshift_sameq_e20d × trailing_stop_5%

**Ticker:** PCAR
**Entry:** `corr_aware_leading_tgtQ+1_noshift_sameq_e20d`
**Exit:** `trailing_stop_5%`
**Period:** 2023-03-27 to 2026-02-06
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
- **skip_regime_shifts:** `True` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `leading` — Which confidence metric to use for scaling
- **entry_days_before:** `20` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `True`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 85.7% |
| **Annualized Return** | 6.7% |
| **Sharpe Ratio** | 1.007 |
| **Max Drawdown** | -7.5% |
| **Total Trades** | 26 |
| **Win Rate** | 69.2% |
| **Signal Accuracy** | 47.1% |
| **Direction Accuracy** | 69.2% |
| **Skill Ratio** | 64.7% |
| **Profit Factor** | 4.44 |
| **Expectancy** | 0.0254 |
| **Tail Ratio** | 4.03 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 100.0% | 85.7% | -14.4% |
| Annualized Return | 27.5% | 6.7% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.2×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0833 | Ideal for 26 trades: 0.0385 |
| Top-1 Trade | 24.3% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 49.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 53.8% | Positive without best trade |
| Return ex-Top-3 | 25.9% | Positive without top 3 |
| Max Single Trade | 20.7% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 11 | 5.61% | 61.7% | 5.61% | 14.91 |
| no_signal | 9 | 1.80% | 16.2% | 1.80% | 8.11 |
| direction_wrong_loss | 6 | -1.97% | -11.8% | -1.97% | 8.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_positive | 8 | 5.27% | 42.2% | 75.0% | 75.0% | 5.27% |
| strong_negative | 9 | 1.80% | 16.2% | 77.8% | 77.8% | 1.80% |
| unknown | 9 | 0.85% | 7.7% | 55.6% | 55.6% | 0.85% |

**Best-performing regime:** `strong_positive` — 8 trades, 42.2% total return, 75.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 3 | -1.19% | -3.6% |
| ❌ | ✅ | 6 | 4.18% | 25.1% |
| ✅ | ❌ | 3 | -2.75% | -8.3% |
| ✅ | ✅ | 5 | 7.32% | 36.6% |

### Flip Trades (Signal Wrong → Direction Right)

**13 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **3.7%**
- Total return: **48.7%**
- Average alpha: **3.7%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_negative | 7 | 3.38% |
| strong_positive | 4 | 6.07% |
| unknown | 2 | 0.38% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 11 | 4.11% | 45.2% | 81.8% | 81.8% |
| high | 6 | 2.20% | 13.2% | 66.7% | 66.7% |
| low | 9 | 0.85% | 7.7% | 55.6% | 55.6% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 14 | 3.21% | 45.0% | 71.4% | 71.4% |
| SHORT | 12 | 1.76% | 21.1% | 66.7% | 66.7% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 10 | 7.9% | 0.79% | 60.0% | 60.0% | 7.9% |
| 2024 | 7 | 42.0% | 6.00% | 71.4% | 71.4% | 42.0% |
| 2025 | 7 | 8.0% | 1.14% | 71.4% | 71.4% | 8.0% |
| 2026 | 2 | 8.3% | 4.13% | 100.0% | 100.0% | 8.3% |

### Macro Context by Year

**2023** (Modestly positive: 7.9%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 42.0%, 7 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 8.0%, 7 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 8.3%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -7.4% cumulative (trade 19 to trade 21)
**Period:** 2025-07-15 to 2025-09-23 (3 trades)
**Peak cumulative return:** 58.0% → **Trough:** 50.6%

**Macro context during drawdown:**
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-07-15 | 2025-07-22 | 1.0000 | 3.63% | strong_negative | ✅ |
| 2025-07-23 | 2025-08-01 | 1.0000 | -4.58% | strong_negative | ❌ |
| 2025-09-23 | 2025-09-26 | -1.0000 | -2.81% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 8 | 1.21% | 9.7% | 50.0% |
| 16-30d | 3 | 2.62% | 7.9% | 66.7% |
| 31-50d | 1 | 20.69% | 20.7% | 100.0% |
| 6-15d | 14 | 1.99% | 27.9% | 78.6% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 26 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (25.9%).
**Win/loss profile:** 69.2% win rate with 4.44× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (69.2%) exceeded signal accuracy (47.1%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 100.0% buy-and-hold return (aligned to strategy period: None to None), yet 12 short trades returned 21.1% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 11d, std 10d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.