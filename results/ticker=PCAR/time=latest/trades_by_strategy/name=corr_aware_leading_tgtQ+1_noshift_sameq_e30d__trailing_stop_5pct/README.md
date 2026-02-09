# Strategy Analysis: corr_aware_leading_tgtQ+1_noshift_sameq_e30d × trailing_stop_5%

**Ticker:** PCAR
**Entry:** `corr_aware_leading_tgtQ+1_noshift_sameq_e30d`
**Exit:** `trailing_stop_5%`
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
- **skip_regime_shifts:** `True` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `leading` — Which confidence metric to use for scaling
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `True`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 127.1% |
| **Annualized Return** | 7.1% |
| **Sharpe Ratio** | 0.960 |
| **Max Drawdown** | -9.6% |
| **Total Trades** | 26 |
| **Win Rate** | 65.4% |
| **Signal Accuracy** | 47.1% |
| **Direction Accuracy** | 65.4% |
| **Skill Ratio** | 58.8% |
| **Profit Factor** | 6.67 |
| **Expectancy** | 0.0339 |
| **Tail Ratio** | 6.43 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 98.7% | 127.1% | 28.4% |
| Annualized Return | 26.7% | 7.1% | — |

## Diversity & Concentration

Diversification: **Somewhat concentrated** — noticeable dependence on top trades (HHI ratio: 2.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0976 | Ideal for 26 trades: 0.0385 |
| Top-1 Trade | 27.9% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 48.2% of gross profit | Moderate concentration |
| Return ex-Top-1 | 76.2% | Positive without best trade |
| Return ex-Top-3 | 44.1% | Positive without top 3 |
| Max Single Trade | 28.9% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 10 | 7.57% | 75.7% | 7.57% | 19.30 |
| no_signal | 9 | 2.47% | 22.2% | 2.47% | 10.33 |
| direction_wrong_loss | 7 | -1.39% | -9.8% | -1.39% | 9.43 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_positive | 8 | 6.42% | 51.4% | 62.5% | 62.5% | 6.42% |
| strong_negative | 9 | 2.47% | 22.2% | 77.8% | 77.8% | 2.47% |
| unknown | 9 | 1.62% | 14.6% | 55.6% | 55.6% | 1.62% |

**Best-performing regime:** `strong_positive` — 8 trades, 51.4% total return, 62.5% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 4 | -0.91% | -3.6% |
| ❌ | ✅ | 5 | 5.28% | 26.4% |
| ✅ | ❌ | 3 | -2.04% | -6.1% |
| ✅ | ✅ | 5 | 9.86% | 49.3% |

### Flip Trades (Signal Wrong → Direction Right)

**12 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.5%**
- Total return: **54.4%**
- Average alpha: **4.5%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_negative | 7 | 4.00% |
| strong_positive | 3 | 8.01% |
| unknown | 2 | 1.18% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 11 | 5.39% | 59.2% | 72.7% | 72.7% |
| low | 9 | 1.62% | 14.6% | 55.6% | 55.6% |
| high | 6 | 2.39% | 14.3% | 66.7% | 66.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 14 | 4.67% | 65.4% | 71.4% | 71.4% |
| SHORT | 12 | 1.90% | 22.8% | 58.3% | 58.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 10 | 16.1% | 1.61% | 60.0% | 60.0% | 16.1% |
| 2024 | 7 | 49.9% | 7.13% | 57.1% | 57.1% | 49.9% |
| 2025 | 8 | 18.7% | 2.34% | 75.0% | 75.0% | 18.7% |
| 2026 | 1 | 3.5% | 3.49% | 100.0% | 100.0% | 3.5% |

### Macro Context by Year

**2023** (Strong year: 16.1%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 49.9%, 7 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 18.7%, 8 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 3.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -3.3% cumulative (trade 1 to trade 2)
**Period:** 2023-03-13 to 2023-03-16 (2 trades)
**Peak cumulative return:** -1.0% → **Trough:** -4.4%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-03-13 | 2023-03-15 | 1.0000 | -1.02% | unknown | ❌ |
| 2023-03-16 | 2023-04-05 | 1.0000 | -3.35% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 7 | 2.12% | 14.8% | 42.9% |
| 16-30d | 7 | 4.10% | 28.7% | 85.7% |
| 31-50d | 1 | 28.91% | 28.9% | 100.0% |
| 6-15d | 11 | 1.43% | 15.7% | 63.6% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 26 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (44.1%).
**Win/loss profile:** 65.4% win rate with 6.67× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (65.4%) exceeded signal accuracy (47.1%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 98.7% buy-and-hold return (aligned to strategy period: None to None), yet 12 short trades returned 22.8% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 14d, std 11d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.