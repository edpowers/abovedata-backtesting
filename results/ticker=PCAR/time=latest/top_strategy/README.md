# Strategy Analysis: corr_aware_leading_univResid_tgtQ+1_sameq_e30d × trailing_stop_5%

**Ticker:** PCAR
**Entry:** `corr_aware_leading_univResid_tgtQ+1_sameq_e30d`
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
| **Total Return** | 134.3% |
| **Annualized Return** | 10.2% |
| **Sharpe Ratio** | 1.163 |
| **Max Drawdown** | -9.6% |
| **Total Trades** | 35 |
| **Win Rate** | 62.9% |
| **Signal Accuracy** | 9.5% |
| **Direction Accuracy** | 62.9% |
| **Skill Ratio** | 60.9% |
| **Profit Factor** | 4.55 |
| **Expectancy** | 0.0262 |
| **Tail Ratio** | 4.29 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 98.7% | 134.3% | 35.6% |
| Annualized Return | 26.7% | 10.2% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0702 | Ideal for 35 trades: 0.0286 |
| Top-1 Trade | 24.6% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 40.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 81.7% | Positive without best trade |
| Return ex-Top-3 | 53.0% | Positive without top 3 |
| Max Single Trade | 28.9% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 35 | 2.62% | 91.6% | 62.9% | 62.9% | 2.62% |

**Best-performing regime:** `unknown` — 35 trades, 91.6% total return, 62.9% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 9 | -1.97% | -17.7% |
| ❌ | ✅ | 12 | 6.42% | 77.0% |
| ✅ | ✅ | 2 | 4.43% | 8.9% |

### Flip Trades (Signal Wrong → Direction Right)

**20 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.4%**
- Total return: **108.5%**
- Average alpha: **5.4%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 20 | 5.42% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 28 | 3.10% | 86.9% | 67.9% | 67.9% |
| no_data | 1 | 3.49% | 3.5% | 100.0% | 100.0% |
| low | 3 | 0.59% | 1.8% | 33.3% | 33.3% |
| high | 3 | -0.19% | -0.6% | 33.3% | 33.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 20 | 3.22% | 64.5% | 70.0% | 70.0% |
| SHORT | 15 | 1.81% | 27.1% | 53.3% | 53.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 10 | 10.3% | 1.03% | 50.0% | 50.0% | 10.3% |
| 2024 | 13 | 57.9% | 4.45% | 69.2% | 69.2% | 57.9% |
| 2025 | 11 | 19.9% | 1.81% | 63.6% | 63.6% | 19.9% |
| 2026 | 1 | 3.5% | 3.49% | 100.0% | 100.0% | 3.5% |

### Macro Context by Year

**2023** (Strong year: 10.3%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 57.9%, 13 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 19.9%, 11 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 3.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -6.8% cumulative (trade 20 to trade 22)
**Period:** 2024-10-23 to 2024-12-13 (3 trades)
**Peak cumulative return:** 74.0% → **Trough:** 67.2%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-10-23 | 2024-11-19 | 1.0000 | 7.98% | unknown | ✅ |
| 2024-12-11 | 2024-12-12 | 1.0000 | -2.57% | unknown | ❌ |
| 2024-12-13 | 2024-12-18 | 1.0000 | -4.26% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 12 | 0.07% | 0.8% | 33.3% |
| 16-30d | 9 | 4.43% | 39.9% | 88.9% |
| 31-50d | 1 | 28.91% | 28.9% | 100.0% |
| 6-15d | 13 | 1.69% | 22.0% | 69.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 3

## Observations & Caveats

**Sample size:** 35 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (53.0%).
**Win/loss profile:** 62.9% win rate with 4.55× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (62.9%) exceeded signal accuracy (9.5%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 98.7% buy-and-hold return (aligned to strategy period: None to None), yet 15 short trades returned 27.1% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 12d, std 10d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.