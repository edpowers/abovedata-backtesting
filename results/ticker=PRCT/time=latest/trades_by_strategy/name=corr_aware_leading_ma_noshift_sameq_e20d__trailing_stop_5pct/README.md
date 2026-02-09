# Strategy Analysis: corr_aware_leading_ma_noshift_sameq_e20d × trailing_stop_5%

**Ticker:** PRCT
**Entry:** `corr_aware_leading_ma_noshift_sameq_e20d`
**Exit:** `trailing_stop_5%`
**Period:** 2023-03-29 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `leading_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `True` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `leading` — Which confidence metric to use for scaling
- **entry_days_before:** `20` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 466.9% |
| **Annualized Return** | 35.9% |
| **Sharpe Ratio** | 1.161 |
| **Max Drawdown** | -28.3% |
| **Total Trades** | 246 |
| **Win Rate** | 58.5% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 59.0% |
| **Skill Ratio** | 57.0% |
| **Profit Factor** | 1.61 |
| **Expectancy** | 0.0086 |
| **Tail Ratio** | 1.36 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -31.5% | 466.9% | 498.4% |
| Annualized Return | -8.3% | 35.9% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0092 | Ideal for 246 trades: 0.0041 |
| Top-1 Trade | 6.2% of gross profit | Moderate concentration |
| Top-3 Trades | 12.9% of gross profit | Moderate concentration |
| Return ex-Top-1 | 320.5% | Positive without best trade |
| Return ex-Top-3 | 198.8% | Positive without top 3 |
| Max Single Trade | 34.8% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 94 | 4.27% | 401.2% | 4.05% | 2.24 |
| no_signal | 81 | 0.68% | 55.1% | 0.43% | 1.73 |
| direction_wrong_loss | 71 | -3.45% | -244.9% | -3.40% | 1.76 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 125 | 0.90% | 112.9% | 52.0% | 52.0% | 0.77% |
| weak_negative | 121 | 0.81% | 98.5% | 65.3% | 65.3% | 0.64% |

**Best-performing regime:** `unknown` — 125 trades, 112.9% total return, 52.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ✅ | ❌ | 71 | -3.45% | -244.9% |
| ✅ | ✅ | 94 | 4.27% | 401.2% |

### Flip Trades (Signal Wrong → Direction Right)

**50 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **3.1%**
- Total return: **156.0%**
- Average alpha: **3.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 50 | 3.12% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 138 | 1.04% | 143.6% | 55.1% | 55.1% |
| medium | 108 | 0.63% | 67.8% | 63.0% | 63.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 147 | 0.76% | 111.4% | 50.3% | 50.3% |
| SHORT | 99 | 1.01% | 100.0% | 70.7% | 70.7% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 71 | 19.5% | 0.27% | 54.9% | 54.9% | 15.4% |
| 2024 | 76 | 97.3% | 1.28% | 53.9% | 53.9% | 84.9% |
| 2025 | 88 | 86.7% | 0.99% | 63.6% | 63.6% | 64.5% |
| 2026 | 11 | 7.9% | 0.72% | 72.7% | 72.7% | 9.5% |

### Macro Context by Year

**2023** (Strong year: 19.5%, 71 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 97.3%, 76 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 86.7%, 88 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 7.9%, 11 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -32.3% cumulative (trade 130 to trade 131)
**Period:** 2024-10-18 to 2024-10-25 (2 trades)
**Peak cumulative return:** 135.0% → **Trough:** 102.6%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-10-18 | 2024-10-24 | -1.0000 | 3.07% | weak_negative | ✅ |
| 2024-10-25 | 2024-10-28 | -1.0000 | -32.33% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 240 | 0.63% | 150.6% | 57.5% |
| 6-15d | 6 | 10.14% | 60.8% | 100.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 10
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 246 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (198.8%).
**Win/loss profile:** 58.5% win rate with 1.61× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (59.0%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 2d, std 2d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.