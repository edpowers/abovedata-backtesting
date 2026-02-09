# Strategy Analysis: corr_aware_leading_tgtQ+1_sameq_e15d × trailing_stop_5%

**Ticker:** PCAR
**Entry:** `corr_aware_leading_tgtQ+1_sameq_e15d`
**Exit:** `trailing_stop_5%`
**Period:** 2023-04-03 to 2026-02-06
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
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `True`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 59.3% |
| **Annualized Return** | 7.5% |
| **Sharpe Ratio** | 0.984 |
| **Max Drawdown** | -8.9% |
| **Total Trades** | 36 |
| **Win Rate** | 58.3% |
| **Signal Accuracy** | 55.6% |
| **Direction Accuracy** | 58.3% |
| **Skill Ratio** | 48.1% |
| **Profit Factor** | 2.30 |
| **Expectancy** | 0.0143 |
| **Tail Ratio** | 2.13 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 94.3% | 59.3% | -34.9% |
| Annualized Return | 26.4% | 7.5% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.1×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0594 | Ideal for 36 trades: 0.0278 |
| Top-1 Trade | 21.5% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 43.3% of gross profit | Moderate concentration |
| Return ex-Top-1 | 33.3% | Positive without best trade |
| Return ex-Top-3 | 10.3% | Positive without top 3 |
| Max Single Trade | 19.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 13 | 5.12% | 66.5% | 5.12% | 12.15 |
| no_signal | 9 | 2.32% | 20.9% | 2.32% | 5.56 |
| direction_wrong_loss | 14 | -2.58% | -36.1% | -2.58% | 6.29 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_positive | 9 | 3.61% | 32.5% | 44.4% | 44.4% | 3.61% |
| strong_negative | 9 | 2.32% | 20.9% | 88.9% | 88.9% | 2.32% |
| unknown | 9 | -0.04% | -0.4% | 44.4% | 44.4% | -0.04% |
| regime_shift | 9 | -0.18% | -1.7% | 55.6% | 55.6% | -0.18% |

**Best-performing regime:** `strong_positive` — 9 trades, 32.5% total return, 44.4% win rate.
**Worst-performing regime:** `regime_shift` — 9 trades, -1.7% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 4 | -1.56% | -6.2% |
| ❌ | ✅ | 8 | 4.06% | 32.5% |
| ✅ | ❌ | 10 | -2.99% | -29.9% |
| ✅ | ✅ | 5 | 6.81% | 34.1% |

### Flip Trades (Signal Wrong → Direction Right)

**16 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **3.6%**
- Total return: **56.9%**
- Average alpha: **3.6%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_negative | 8 | 3.05% |
| regime_shift | 3 | 3.74% |
| strong_positive | 3 | 6.76% |
| unknown | 2 | 0.49% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 21 | 1.94% | 40.7% | 61.9% | 61.9% |
| high | 6 | 1.84% | 11.0% | 66.7% | 66.7% |
| low | 9 | -0.04% | -0.4% | 44.4% | 44.4% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 21 | 2.10% | 44.1% | 57.1% | 57.1% |
| SHORT | 15 | 0.48% | 7.2% | 60.0% | 60.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 10 | -0.9% | -0.09% | 40.0% | 40.0% | -0.9% |
| 2024 | 11 | 44.2% | 4.02% | 63.6% | 63.6% | 44.2% |
| 2025 | 13 | -0.2% | -0.02% | 61.5% | 61.5% | -0.2% |
| 2026 | 2 | 8.3% | 4.13% | 100.0% | 100.0% | 8.3% |

### Macro Context by Year

**2023** (Roughly flat: -0.9%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 44.2%, 11 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Roughly flat: -0.2%, 13 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 8.3%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -15.0% cumulative (trade 22 to trade 26)
**Period:** 2025-01-03 to 2025-04-10 (5 trades)
**Peak cumulative return:** 44.9% → **Trough:** 29.9%

**Macro context during drawdown:**
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-01-03 | 2025-01-10 | 1.0000 | 1.60% | regime_shift | ✅ |
| 2025-01-13 | 2025-01-28 | 1.0000 | -0.84% | regime_shift | ❌ |
| 2025-01-29 | 2025-02-05 | 1.0000 | -3.52% | regime_shift | ❌ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -8.72% | regime_shift | ❌ |
| 2025-04-10 | 2025-04-11 | -1.0000 | -1.92% | regime_shift | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 18 | 0.22% | 3.9% | 50.0% |
| 16-30d | 3 | 4.34% | 13.0% | 66.7% |
| 31-50d | 1 | 19.52% | 19.5% | 100.0% |
| 6-15d | 14 | 1.06% | 14.9% | 64.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 7
- **Max consecutive losses:** 4

## Observations & Caveats

**Sample size:** 36 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (10.3%).
**Win/loss profile:** 58.3% win rate with 2.30× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (58.3%) exceeded signal accuracy (55.6%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.
**Regime dependence:** `strong_positive` (9 trades, 25% of total) contributed 32.5% — a disproportionate share. Performance may degrade if this regime becomes less common.

### Known Vulnerabilities

- **Losing regime:** `unknown` — 9 trades, -0.4% total return
- **Losing regime:** `regime_shift` — 9 trades, -1.7% total return

### ⚠️ Robustness Red Flags

- **REGIME_CONCENTRATION:** `strong_positive` regime (9 trades, 25% of total) contributes 63% of total return. Performance is fragile if this regime becomes less common or behaves differently.
- **BETA_DISGUISED:** Stock had 94.3% buy-and-hold return (aligned to strategy period: None to None), yet 15 short trades returned 7.2% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 8d, std 9d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.