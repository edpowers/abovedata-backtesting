# Strategy Analysis: corr_aware_contemp_e20d × trailing_stop_5%

**Ticker:** PRCT
**Entry:** `corr_aware_contemp_e20d`
**Exit:** `trailing_stop_5%`
**Period:** 2023-03-29 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `20` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 435.7% |
| **Annualized Return** | 44.3% |
| **Sharpe Ratio** | 1.418 |
| **Max Drawdown** | -28.3% |
| **Total Trades** | 241 |
| **Win Rate** | 52.7% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 52.9% |
| **Skill Ratio** | 50.6% |
| **Profit Factor** | 1.59 |
| **Expectancy** | 0.0085 |
| **Tail Ratio** | 1.67 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -31.5% | 435.7% | 467.2% |
| Annualized Return | -8.3% | 44.3% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0097 | Ideal for 241 trades: 0.0041 |
| Top-1 Trade | 6.6% of gross profit | Moderate concentration |
| Top-3 Trades | 16.7% of gross profit | Moderate concentration |
| Return ex-Top-1 | 293.4% | Positive without best trade |
| Return ex-Top-3 | 142.4% | Positive without top 3 |
| Max Single Trade | 36.2% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 83 | 4.75% | 394.0% | 4.48% | 2.28 |
| no_signal | 77 | 0.63% | 48.5% | 0.46% | 1.86 |
| direction_wrong_loss | 81 | -2.94% | -238.5% | -3.00% | 1.83 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 48 | 1.82% | 87.3% | 58.3% | 58.3% | 1.83% |
| weak_negative | 48 | 1.11% | 53.5% | 68.8% | 68.8% | 0.72% |
| unknown | 77 | 0.54% | 41.5% | 54.5% | 54.5% | 0.45% |
| strong_positive | 40 | 0.72% | 28.9% | 32.5% | 32.5% | 0.47% |
| weak_positive | 12 | -0.17% | -2.0% | 41.7% | 41.7% | -0.14% |
| strong_negative | 16 | -0.33% | -5.3% | 37.5% | 37.5% | -0.62% |

**Best-performing regime:** `regime_shift` — 48 trades, 87.3% total return, 58.3% win rate.
**Worst-performing regime:** `strong_negative` — 16 trades, -5.3% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ✅ | ❌ | 81 | -2.94% | -238.5% |
| ✅ | ✅ | 83 | 4.75% | 394.0% |

### Flip Trades (Signal Wrong → Direction Right)

**44 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **3.5%**
- Total return: **153.2%**
- Average alpha: **3.6%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 33 | 3.12% |
| regime_shift | 6 | 5.51% |
| weak_positive | 5 | 3.42% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 152 | 1.08% | 164.5% | 52.6% | 52.6% |
| low | 89 | 0.44% | 39.5% | 52.8% | 52.8% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 147 | 0.87% | 128.1% | 48.3% | 48.3% |
| SHORT | 94 | 0.81% | 75.9% | 59.6% | 59.6% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 71 | 19.5% | 0.27% | 54.9% | 54.9% | 15.4% |
| 2024 | 75 | 119.8% | 1.60% | 42.7% | 42.7% | 98.5% |
| 2025 | 83 | 66.7% | 0.80% | 61.4% | 61.4% | 52.1% |
| 2026 | 12 | -2.0% | -0.17% | 41.7% | 41.7% | -1.7% |

### Macro Context by Year

**2023** (Strong year: 19.5%, 71 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 119.8%, 75 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 66.7%, 83 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Roughly flat: -2.0%, 12 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -29.9% cumulative (trade 5 to trade 8)
**Period:** 2023-04-12 to 2023-04-26 (4 trades)
**Peak cumulative return:** 21.8% → **Trough:** -8.1%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-04-12 | 2023-04-13 | 1.0000 | 2.40% | unknown | ✅ |
| 2023-04-14 | 2023-04-19 | 1.0000 | -4.83% | unknown | ❌ |
| 2023-04-20 | 2023-04-25 | 1.0000 | 0.22% | unknown | ✅ |
| 2023-04-26 | 2023-04-27 | 1.0000 | -25.31% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 230 | 0.58% | 132.8% | 50.9% |
| 6-15d | 11 | 6.47% | 71.2% | 90.9% |

## Win/Loss Streaks

- **Max consecutive wins:** 11
- **Max consecutive losses:** 7

## Observations & Caveats

**Sample size:** 241 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (142.4%).
**Win/loss profile:** 52.7% win rate with 1.59× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (52.9%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Losing regime:** `weak_positive` — 12 trades, -2.0% total return
- **Losing regime:** `strong_negative` — 16 trades, -5.3% total return

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 2d, std 2d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.