# Strategy Analysis: corr_aware_leading_tgtQ+1_sameq_e20d × trailing_stop_5%

**Ticker:** PCAR
**Entry:** `corr_aware_leading_tgtQ+1_sameq_e20d`
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
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
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
| **Total Return** | 105.2% |
| **Annualized Return** | 8.8% |
| **Sharpe Ratio** | 1.147 |
| **Max Drawdown** | -7.7% |
| **Total Trades** | 35 |
| **Win Rate** | 71.4% |
| **Signal Accuracy** | 53.8% |
| **Direction Accuracy** | 71.4% |
| **Skill Ratio** | 65.4% |
| **Profit Factor** | 3.77 |
| **Expectancy** | 0.0220 |
| **Tail Ratio** | 2.66 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 100.0% | 105.2% | 5.2% |
| Annualized Return | 27.5% | 8.8% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.1×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0604 | Ideal for 35 trades: 0.0286 |
| Top-1 Trade | 19.8% of gross profit | Moderate concentration |
| Top-3 Trades | 40.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 70.0% | Positive without best trade |
| Return ex-Top-3 | 39.1% | Positive without top 3 |
| Max Single Trade | 20.7% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_positive | 8 | 5.27% | 42.2% | 75.0% | 75.0% | 5.27% |
| strong_negative | 9 | 2.31% | 20.8% | 88.9% | 88.9% | 2.31% |
| unknown | 9 | 0.85% | 7.7% | 55.6% | 55.6% | 0.85% |
| regime_shift | 9 | 0.69% | 6.2% | 66.7% | 66.7% | 0.69% |

**Best-performing regime:** `strong_positive` — 8 trades, 42.2% total return, 75.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 3 | -1.19% | -3.6% |
| ❌ | ✅ | 9 | 3.90% | 35.1% |
| ✅ | ❌ | 6 | -3.55% | -21.3% |
| ✅ | ✅ | 8 | 5.73% | 45.9% |

### Flip Trades (Signal Wrong → Direction Right)

**17 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **3.5%**
- Total return: **58.7%**
- Average alpha: **3.5%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_negative | 8 | 2.95% |
| strong_positive | 4 | 6.07% |
| regime_shift | 3 | 3.35% |
| unknown | 2 | 0.38% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 20 | 2.80% | 56.0% | 80.0% | 80.0% |
| high | 6 | 2.20% | 13.2% | 66.7% | 66.7% |
| low | 9 | 0.85% | 7.7% | 55.6% | 55.6% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 20 | 2.81% | 56.3% | 75.0% | 75.0% |
| SHORT | 15 | 1.37% | 20.5% | 66.7% | 66.7% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 10 | 7.9% | 0.79% | 60.0% | 60.0% | 7.9% |
| 2024 | 11 | 53.1% | 4.83% | 81.8% | 81.8% | 53.1% |
| 2025 | 12 | 7.6% | 0.63% | 66.7% | 66.7% | 7.6% |
| 2026 | 2 | 8.3% | 4.13% | 100.0% | 100.0% | 8.3% |

### Macro Context by Year

**2023** (Modestly positive: 7.9%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 53.1%, 11 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 7.6%, 12 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 8.3%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -8.7% cumulative (trade 25 to trade 26)
**Period:** 2025-04-04 to 2025-04-08 (2 trades)
**Peak cumulative return:** 64.8% → **Trough:** 56.1%

**Macro context during drawdown:**
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-04-04 | 2025-04-07 | -1.0000 | 3.01% | regime_shift | ✅ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -8.72% | regime_shift | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 13 | 0.69% | 9.0% | 53.8% |
| 16-30d | 4 | 3.62% | 14.5% | 75.0% |
| 31-50d | 1 | 20.69% | 20.7% | 100.0% |
| 6-15d | 17 | 1.92% | 32.7% | 82.4% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** 35 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (39.1%).
**Win/loss profile:** 71.4% win rate with 3.77× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (71.4%) exceeded signal accuracy (53.8%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.
**Regime dependence:** `strong_positive` (8 trades, 23% of total) contributed 42.2% — a disproportionate share. Performance may degrade if this regime becomes less common.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 100.0% buy-and-hold return (aligned to strategy period: None to None), yet 15 short trades returned 20.5% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 10d, std 9d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.