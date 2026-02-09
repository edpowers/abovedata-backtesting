# Strategy Analysis: corr_aware_leading_noshift_e15d × trailing_stop_10%

**Ticker:** PRCT
**Entry:** `corr_aware_leading_noshift_e15d`
**Exit:** `trailing_stop_10%`
**Period:** 2023-04-05 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `leading` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
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
| **Total Return** | -14.9% |
| **Annualized Return** | 84.8% |
| **Sharpe Ratio** | 2.403 |
| **Max Drawdown** | -20.6% |
| **Total Trades** | 74 |
| **Win Rate** | 45.9% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 45.9% |
| **Skill Ratio** | 47.1% |
| **Profit Factor** | 1.07 |
| **Expectancy** | 0.0027 |
| **Tail Ratio** | 1.29 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -31.5% | -14.9% | 16.6% |
| Annualized Return | -8.3% | 84.8% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.7×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0234 | Ideal for 74 trades: 0.0135 |
| Top-1 Trade | 9.5% of gross profit | Moderate concentration |
| Top-3 Trades | 26.4% of gross profit | Moderate concentration |
| Return ex-Top-1 | -33.1% | Negative without best trade |
| Return ex-Top-3 | -56.6% | Negative without top 3 |
| Max Single Trade | 27.2% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 24 | 8.70% | 208.9% | 8.69% | 12.12 |
| no_signal | 23 | 0.31% | 7.1% | -1.35% | 8.17 |
| direction_wrong_loss | 27 | -7.27% | -196.3% | -7.99% | 6.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| weak_negative | 34 | 1.42% | 48.2% | 58.8% | 58.8% | 1.20% |
| unknown | 25 | 0.93% | 23.1% | 40.0% | 40.0% | 0.20% |
| strong_negative | 15 | -3.44% | -51.7% | 26.7% | 26.7% | -5.61% |

**Best-performing regime:** `weak_negative` — 34 trades, 48.2% total return, 58.8% win rate.
**Worst-performing regime:** `strong_negative` — 15 trades, -51.7% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ✅ | ❌ | 27 | -7.27% | -196.3% |
| ✅ | ✅ | 24 | 8.70% | 208.9% |

### Flip Trades (Signal Wrong → Direction Right)

**10 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **7.8%**
- Total return: **77.6%**
- Average alpha: **6.4%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 9 | 7.82% |
| strong_negative | 1 | 7.25% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 44 | 0.79% | 34.6% | 47.7% | 47.7% |
| medium | 30 | -0.50% | -14.9% | 43.3% | 43.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 34 | 0.36% | 12.2% | 41.2% | 41.2% |
| SHORT | 40 | 0.19% | 7.5% | 50.0% | 50.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 19 | -1.6% | -0.08% | 36.8% | 36.8% | -13.0% |
| 2024 | 25 | -22.7% | -0.91% | 48.0% | 48.0% | -45.0% |
| 2025 | 29 | 35.7% | 1.23% | 48.3% | 48.3% | 10.8% |
| 2026 | 1 | 8.3% | 8.27% | 100.0% | 100.0% | 8.9% |

### Macro Context by Year

**2023** (Roughly flat: -1.6%, 19 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -22.7%, 25 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 35.7%, 29 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 8.3%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -61.4% cumulative (trade 26 to trade 39)
**Period:** 2024-04-10 to 2024-09-16 (14 trades)
**Peak cumulative return:** 27.0% → **Trough:** -34.4%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-04-10 | 2024-04-19 | -1.0000 | 3.91% | strong_negative | ✅ |
| 2024-04-22 | 2024-04-23 | -1.0000 | -5.00% | strong_negative | ❌ |
| 2024-04-24 | 2024-05-01 | -1.0000 | -15.49% | strong_negative | ❌ |
| 2024-05-02 | 2024-05-14 | -1.0000 | -5.78% | strong_negative | ❌ |
| 2024-05-15 | 2024-06-05 | -1.0000 | 0.64% | strong_negative | ✅ |
| 2024-06-06 | 2024-07-03 | -1.0000 | 6.91% | strong_negative | ✅ |
| 2024-07-05 | 2024-07-12 | -1.0000 | -7.20% | strong_negative | ❌ |
| 2024-07-15 | 2024-07-18 | -1.0000 | 0.13% | weak_negative | ✅ |
| 2024-07-19 | 2024-08-06 | -1.0000 | 10.21% | weak_negative | ✅ |
| 2024-08-07 | 2024-08-15 | -1.0000 | -4.88% | weak_negative | ❌ |
| 2024-08-16 | 2024-08-21 | -1.0000 | -29.00% | weak_negative | ❌ |
| 2024-08-22 | 2024-09-09 | -1.0000 | 4.44% | weak_negative | ✅ |
| 2024-09-10 | 2024-09-13 | -1.0000 | -5.42% | weak_negative | ❌ |
| 2024-09-16 | 2024-10-28 | -1.0000 | -10.99% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 34 | -3.64% | -123.9% | 26.5% |
| 16-30d | 10 | 4.76% | 47.6% | 80.0% |
| 31-50d | 1 | 27.23% | 27.2% | 100.0% |
| 6-15d | 29 | 2.37% | 68.7% | 55.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 3
- **Max consecutive losses:** 7

## Observations & Caveats

**Sample size:** 74 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-56.6%).
**Win/loss profile:** Profit factor of 1.07 with 45.9% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (45.9%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2024 (-22.7%, 25 trades). Macro: 2024 Election Year Uncertainty
- **Losing regime:** `strong_negative` — 15 trades, -51.7% total return

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 9d, std 8d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.