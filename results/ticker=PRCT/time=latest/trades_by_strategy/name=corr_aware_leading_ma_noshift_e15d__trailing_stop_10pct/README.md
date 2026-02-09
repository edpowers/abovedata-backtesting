# Strategy Analysis: corr_aware_leading_ma_noshift_e15d × trailing_stop_10%

**Ticker:** PRCT
**Entry:** `corr_aware_leading_ma_noshift_e15d`
**Exit:** `trailing_stop_10%`
**Period:** 2023-04-05 to 2026-02-06
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
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_10%`
  - 10% trailing stop. More room for normal volatility, targets larger trends

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 122.9% |
| **Annualized Return** | 87.9% |
| **Sharpe Ratio** | 2.311 |
| **Max Drawdown** | -15.8% |
| **Total Trades** | 75 |
| **Win Rate** | 44.0% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 44.0% |
| **Skill Ratio** | 44.2% |
| **Profit Factor** | 1.52 |
| **Expectancy** | 0.0164 |
| **Tail Ratio** | 2.34 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -31.5% | 122.9% | 154.4% |
| Annualized Return | -8.3% | 87.9% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.0×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0271 | Ideal for 75 trades: 0.0133 |
| Top-1 Trade | 12.5% of gross profit | Moderate concentration |
| Top-3 Trades | 30.9% of gross profit | Moderate concentration |
| Return ex-Top-1 | 54.1% | Positive without best trade |
| Return ex-Top-3 | -12.8% | Negative without top 3 |
| Max Single Trade | 44.7% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 23 | 12.20% | 280.5% | 11.39% | 11.65 |
| no_signal | 23 | 0.31% | 7.1% | -1.35% | 8.17 |
| direction_wrong_loss | 29 | -5.68% | -164.7% | -5.73% | 6.34 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 46 | 2.12% | 97.7% | 41.3% | 41.3% | 1.38% |
| weak_negative | 29 | 0.87% | 25.3% | 48.3% | 48.3% | 0.04% |

**Best-performing regime:** `unknown` — 46 trades, 97.7% total return, 41.3% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ✅ | ❌ | 29 | -5.68% | -164.7% |
| ✅ | ✅ | 23 | 12.20% | 280.5% |

### Flip Trades (Signal Wrong → Direction Right)

**10 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **7.8%**
- Total return: **77.6%**
- Average alpha: **6.4%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 10 | 7.76% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 54 | 1.26% | 68.1% | 37.0% | 37.0% |
| medium | 21 | 2.61% | 54.9% | 61.9% | 61.9% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 55 | 1.58% | 86.8% | 41.8% | 41.8% |
| SHORT | 20 | 1.81% | 36.2% | 50.0% | 50.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 19 | -1.6% | -0.08% | 36.8% | 36.8% | -13.0% |
| 2024 | 24 | 107.3% | 4.47% | 45.8% | 45.8% | 85.5% |
| 2025 | 31 | 9.0% | 0.29% | 45.2% | 45.2% | -16.8% |
| 2026 | 1 | 8.3% | 8.27% | 100.0% | 100.0% | 8.9% |

### Macro Context by Year

**2023** (Roughly flat: -1.6%, 19 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 107.3%, 24 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 9.0%, 31 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 8.3%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -52.5% cumulative (trade 1 to trade 15)
**Period:** 2023-04-05 to 2023-10-24 (15 trades)
**Peak cumulative return:** 6.6% → **Trough:** -45.9%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-04-05 | 2023-04-19 | 1.0000 | 6.59% | unknown | ✅ |
| 2023-04-20 | 2023-04-27 | 1.0000 | -25.06% | unknown | ❌ |
| 2023-04-28 | 2023-05-02 | 1.0000 | -6.05% | unknown | ❌ |
| 2023-05-03 | 2023-05-09 | 1.0000 | -4.05% | unknown | ❌ |
| 2023-05-10 | 2023-06-01 | 1.0000 | 9.95% | unknown | ✅ |
| 2023-06-02 | 2023-06-26 | 1.0000 | 4.65% | unknown | ✅ |
| 2023-06-27 | 2023-07-27 | 1.0000 | 5.76% | unknown | ✅ |
| 2023-07-28 | 2023-08-08 | 1.0000 | -6.74% | unknown | ❌ |
| 2023-08-09 | 2023-08-24 | 1.0000 | -4.75% | unknown | ❌ |
| 2023-08-25 | 2023-09-15 | 1.0000 | 6.28% | unknown | ✅ |
| 2023-09-18 | 2023-10-02 | 1.0000 | -4.27% | unknown | ❌ |
| 2023-10-03 | 2023-10-11 | 1.0000 | -5.82% | unknown | ❌ |
| 2023-10-12 | 2023-10-13 | 1.0000 | -4.50% | unknown | ❌ |
| 2023-10-16 | 2023-10-23 | 1.0000 | -8.30% | unknown | ❌ |
| 2023-10-24 | 2023-10-30 | 1.0000 | -9.62% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 32 | -1.32% | -42.2% | 28.1% |
| 16-30d | 10 | 4.30% | 43.0% | 70.0% |
| 31-50d | 1 | 27.23% | 27.2% | 100.0% |
| 6-15d | 32 | 2.97% | 95.0% | 50.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 3
- **Max consecutive losses:** 7

## Observations & Caveats

**Sample size:** 75 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-12.8%).
**Win/loss profile:** Profit factor of 1.52 with 44.0% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (44.0%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 9d, std 8d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.