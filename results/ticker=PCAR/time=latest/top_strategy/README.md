# Strategy Analysis: corr_aware_leading_tgtQ+1_sameq_e30d × trailing_stop_5%

**Ticker:** PCAR
**Entry:** `corr_aware_leading_tgtQ+1_sameq_e30d`
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
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
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
| **Total Return** | 161.4% |
| **Annualized Return** | 10.2% |
| **Sharpe Ratio** | 1.163 |
| **Max Drawdown** | -9.6% |
| **Total Trades** | 35 |
| **Win Rate** | 68.6% |
| **Signal Accuracy** | 53.8% |
| **Direction Accuracy** | 68.6% |
| **Skill Ratio** | 61.5% |
| **Profit Factor** | 4.63 |
| **Expectancy** | 0.0296 |
| **Tail Ratio** | 3.07 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 98.7% | 161.4% | 62.7% |
| Annualized Return | 26.7% | 10.2% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0652 | Ideal for 35 trades: 0.0286 |
| Top-1 Trade | 21.9% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 38.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 102.8% | Positive without best trade |
| Return ex-Top-3 | 64.1% | Positive without top 3 |
| Max Single Trade | 28.9% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_positive | 8 | 6.42% | 51.4% | 62.5% | 62.5% | 6.42% |
| strong_negative | 9 | 2.48% | 22.3% | 88.9% | 88.9% | 2.48% |
| regime_shift | 9 | 1.71% | 15.4% | 66.7% | 66.7% | 1.71% |
| unknown | 9 | 1.62% | 14.6% | 55.6% | 55.6% | 1.62% |

**Best-performing regime:** `strong_positive` — 8 trades, 51.4% total return, 62.5% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 4 | -0.91% | -3.6% |
| ❌ | ✅ | 8 | 5.14% | 41.1% |
| ✅ | ❌ | 6 | -3.68% | -22.1% |
| ✅ | ✅ | 8 | 8.24% | 66.0% |

### Flip Trades (Signal Wrong → Direction Right)

**16 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.1%**
- Total return: **66.3%**
- Average alpha: **4.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_negative | 8 | 3.14% |
| strong_positive | 3 | 8.01% |
| regime_shift | 3 | 4.92% |
| unknown | 2 | 1.18% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 20 | 3.74% | 74.8% | 75.0% | 75.0% |
| low | 9 | 1.62% | 14.6% | 55.6% | 55.6% |
| high | 6 | 2.39% | 14.3% | 66.7% | 66.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 20 | 3.75% | 75.0% | 75.0% | 75.0% |
| SHORT | 15 | 1.91% | 28.7% | 60.0% | 60.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 10 | 16.1% | 1.61% | 60.0% | 60.0% | 16.1% |
| 2024 | 13 | 59.3% | 4.56% | 61.5% | 61.5% | 59.3% |
| 2025 | 11 | 24.8% | 2.25% | 81.8% | 81.8% | 24.8% |
| 2026 | 1 | 3.5% | 3.49% | 100.0% | 100.0% | 3.5% |

### Macro Context by Year

**2023** (Strong year: 16.1%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 59.3%, 13 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 24.8%, 11 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 3.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -8.7% cumulative (trade 25 to trade 26)
**Period:** 2025-03-24 to 2025-04-08 (2 trades)
**Peak cumulative return:** 90.1% → **Trough:** 81.4%

**Macro context during drawdown:**
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-03-24 | 2025-04-07 | -1.0000 | 10.64% | regime_shift | ✅ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -8.72% | regime_shift | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 12 | 0.34% | 4.1% | 41.7% |
| 16-30d | 9 | 4.70% | 42.3% | 88.9% |
| 31-50d | 1 | 28.91% | 28.9% | 100.0% |
| 6-15d | 13 | 2.19% | 28.5% | 76.9% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** 35 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (64.1%).
**Win/loss profile:** 68.6% win rate with 4.63× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (68.6%) exceeded signal accuracy (53.8%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 98.7% buy-and-hold return (aligned to strategy period: None to None), yet 15 short trades returned 28.7% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 12d, std 10d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.