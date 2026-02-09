# Strategy Analysis: corr_aware_contemp_e1d × sl-5%_tp10%

**Ticker:** PRCT
**Entry:** `corr_aware_contemp_e1d`
**Exit:** `sl-5%_tp10%`
**Period:** 2023-04-26 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **min_confidence:** `0.0`
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `1` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `False`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit targets a 2:1 reward/risk ratio

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 60.4% |
| **Annualized Return** | 27.5% |
| **Sharpe Ratio** | 1.530 |
| **Max Drawdown** | -16.1% |
| **Total Trades** | 36 |
| **Win Rate** | 41.7% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 42.9% |
| **Skill Ratio** | 37.5% |
| **Profit Factor** | 1.59 |
| **Expectancy** | 0.0198 |
| **Tail Ratio** | 2.01 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.9×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0531 | Ideal for 36 trades: 0.0278 |
| Top-1 Trade | 18.1% of gross profit | Moderate concentration |
| Top-3 Trades | 46.1% of gross profit | Moderate concentration |
| Return ex-Top-1 | 19.0% | Positive without best trade |
| Return ex-Top-3 | -26.1% | Negative without top 3 |
| Max Single Trade | 34.8% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 9 | 15.19% | 136.7% | 15.19% | 4.00 |
| no_signal | 12 | 2.18% | 26.1% | 2.18% | 3.08 |
| direction_wrong_loss | 15 | -6.10% | -91.4% | -6.10% | 4.80 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_positive | 6 | 10.51% | 63.1% | 66.7% | 66.7% | 10.51% |
| regime_shift | 9 | 4.20% | 37.8% | 66.7% | 66.7% | 4.20% |
| weak_negative | 6 | 3.08% | 18.5% | 50.0% | 50.0% | 3.08% |
| weak_positive | 3 | -1.50% | -4.5% | 33.3% | 33.3% | -1.50% |
| strong_negative | 3 | -3.14% | -9.4% | 0.0% | 0.0% | -3.14% |
| unknown | 9 | -3.79% | -34.1% | 11.1% | 11.1% | -3.79% |

**Best-performing regime:** `strong_positive` — 6 trades, 63.1% total return, 66.7% win rate.
**Worst-performing regime:** `unknown` — 9 trades, -34.1% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ✅ | ❌ | 15 | -6.10% | -91.4% |
| ✅ | ✅ | 9 | 15.19% | 136.7% |

### Flip Trades (Signal Wrong → Direction Right)

**6 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **9.3%**
- Total return: **56.0%**
- Average alpha: **9.3%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 3 | 12.01% |
| regime_shift | 2 | 9.59% |
| weak_positive | 1 | 0.79% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 24 | 4.58% | 110.0% | 54.2% | 54.2% |
| low | 12 | -3.21% | -38.6% | 16.7% | 16.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 21 | 2.17% | 45.6% | 38.1% | 38.1% |
| SHORT | 15 | 1.72% | 25.8% | 46.7% | 46.7% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 9 | -34.1% | -3.79% | 11.1% | 11.1% | -34.1% |
| 2024 | 12 | 74.7% | 6.23% | 50.0% | 50.0% | 74.7% |
| 2025 | 12 | 35.2% | 2.94% | 58.3% | 58.3% | 35.2% |
| 2026 | 3 | -4.5% | -1.50% | 33.3% | 33.3% | -4.5% |

### Macro Context by Year

**2023** (Losing year: -34.1%, 9 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 74.7%, 12 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 35.2%, 12 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Roughly flat: -4.5%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -25.9% cumulative (trade 1 to trade 6)
**Period:** 2023-04-26 to 2023-08-02 (6 trades)
**Peak cumulative return:** -25.3% → **Trough:** -51.2%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-04-26 | 2023-04-27 | 1.0000 | -25.31% | unknown | ❌ |
| 2023-04-28 | 2023-05-02 | 1.0000 | -6.05% | unknown | ❌ |
| 2023-05-03 | 2023-05-08 | 1.0000 | -5.25% | unknown | ❌ |
| 2023-07-26 | 2023-07-27 | 1.0000 | -7.14% | unknown | ❌ |
| 2023-07-28 | 2023-08-01 | 1.0000 | -3.88% | unknown | ❌ |
| 2023-08-02 | 2023-08-07 | 1.0000 | -3.53% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 28 | 0.81% | 22.7% | 39.3% |
| 16-30d | 1 | -6.87% | -6.9% | 0.0% |
| 6-15d | 7 | 7.93% | 55.5% | 57.1% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 36 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-26.1%).
**Win/loss profile:** Profit factor of 1.59 with 41.7% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (42.9%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.
**Regime dependence:** `strong_positive` (6 trades, 17% of total) contributed 63.1% — a disproportionate share. Performance may degrade if this regime becomes less common.

### Known Vulnerabilities

- **Worst year:** 2023 (-34.1%, 9 trades). Macro: Fed Tightening Cycle, 2023 Soft Landing Rally
- **Losing regime:** `weak_positive` — 3 trades, -4.5% total return
- **Losing regime:** `strong_negative` — 3 trades, -9.4% total return
- **Losing regime:** `unknown` — 9 trades, -34.1% total return

### ⚠️ Robustness Red Flags

- **REGIME_CONCENTRATION:** `strong_positive` regime (6 trades, 17% of total) contributes 88% of total return. Performance is fragile if this regime becomes less common or behaves differently.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 4d, std 5d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.