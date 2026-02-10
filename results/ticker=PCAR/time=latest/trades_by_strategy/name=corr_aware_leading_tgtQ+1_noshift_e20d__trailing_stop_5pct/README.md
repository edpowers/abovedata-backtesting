# Strategy Analysis: corr_aware_leading_tgtQ+1_noshift_e20d × trailing_stop_5%

**Ticker:** PCAR
**Entry:** `corr_aware_leading_tgtQ+1_noshift_e20d`
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
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `True`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 75.5% |
| **Annualized Return** | 6.0% |
| **Sharpe Ratio** | 0.919 |
| **Max Drawdown** | -11.3% |
| **Total Trades** | 26 |
| **Win Rate** | 65.4% |
| **Signal Accuracy** | 40.0% |
| **Direction Accuracy** | 65.4% |
| **Skill Ratio** | 60.0% |
| **Profit Factor** | 4.01 |
| **Expectancy** | 0.0232 |
| **Tail Ratio** | 4.80 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 100.0% | 75.5% | -24.5% |
| Annualized Return | 27.5% | 6.0% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0875 | Ideal for 26 trades: 0.0385 |
| Top-1 Trade | 25.8% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 52.1% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 45.4% | Positive without best trade |
| Return ex-Top-3 | 19.0% | Positive without top 3 |
| Max Single Trade | 20.7% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 11 | 2.60% | 28.6% | 63.6% | 63.6% | 2.60% |
| strong_positive | 9 | 2.12% | 19.1% | 55.6% | 55.6% | 2.12% |
| strong_negative | 6 | 2.11% | 12.7% | 83.3% | 83.3% | 2.11% |

**Best-performing regime:** `unknown` — 11 trades, 28.6% total return, 63.6% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 5 | -1.79% | -8.9% |
| ❌ | ✅ | 7 | 4.03% | 28.2% |
| ✅ | ❌ | 3 | -2.75% | -8.3% |
| ✅ | ✅ | 5 | 7.32% | 36.6% |

### Flip Trades (Signal Wrong → Direction Right)

**12 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **3.6%**
- Total return: **43.7%**
- Average alpha: **3.6%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_positive | 5 | 5.49% |
| strong_negative | 5 | 3.10% |
| unknown | 2 | 0.38% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 11 | 2.60% | 28.6% | 63.6% | 63.6% |
| medium | 9 | 2.32% | 20.9% | 66.7% | 66.7% |
| high | 6 | 1.81% | 10.9% | 66.7% | 66.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 11 | 3.77% | 41.4% | 72.7% | 72.7% |
| SHORT | 15 | 1.26% | 18.9% | 60.0% | 60.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 10 | 7.9% | 0.79% | 60.0% | 60.0% | 7.9% |
| 2024 | 10 | 39.8% | 3.98% | 60.0% | 60.0% | 39.8% |
| 2025 | 4 | 4.4% | 1.10% | 75.0% | 75.0% | 4.4% |
| 2026 | 2 | 8.3% | 4.13% | 100.0% | 100.0% | 8.3% |

### Macro Context by Year

**2023** (Modestly positive: 7.9%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 39.8%, 10 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 4.4%, 4 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 8.3%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -5.4% cumulative (trade 17 to trade 19)
**Period:** 2024-07-18 to 2024-10-04 (3 trades)
**Peak cumulative return:** 49.8% → **Trough:** 44.5%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-07-18 | 2024-07-23 | -1.0000 | 11.71% | strong_positive | ✅ |
| 2024-09-24 | 2024-10-03 | -1.0000 | -2.10% | strong_positive | ❌ |
| 2024-10-04 | 2024-10-11 | -1.0000 | -3.28% | strong_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 8 | 0.34% | 2.7% | 37.5% |
| 16-30d | 3 | 2.62% | 7.9% | 66.7% |
| 31-50d | 1 | 20.69% | 20.7% | 100.0% |
| 6-15d | 14 | 2.07% | 29.0% | 78.6% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 26 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (19.0%).
**Win/loss profile:** 65.4% win rate with 4.01× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (65.4%) exceeded signal accuracy (40.0%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 100.0% buy-and-hold return (aligned to strategy period: None to None), yet 15 short trades returned 18.9% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 11d, std 10d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.