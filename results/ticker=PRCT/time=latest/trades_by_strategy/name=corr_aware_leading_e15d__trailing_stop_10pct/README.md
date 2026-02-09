# Strategy Analysis: corr_aware_leading_e15d × trailing_stop_10%

**Ticker:** PRCT
**Entry:** `corr_aware_leading_e15d`
**Exit:** `trailing_stop_10%`
**Period:** 2023-04-05 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `leading` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_10%`
  - 10% trailing stop. More room for normal volatility, captures larger trends

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | -14.9% |
| **Annualized Return** | 84.8% |
| **Sharpe Ratio** | 2.403 |
| **Max Drawdown** | -20.6% |
| **Total Trades** | 74 |
| **Win Rate** | 45.9% |
| **Signal Accuracy** | 53.2% |
| **Direction Accuracy** | 44.7% |
| **Skill Ratio** | 44.7% |
| **Profit Factor** | 1.07 |
| **Expectancy** | 0.0027 |
| **Tail Ratio** | 1.29 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | -31.5% | -14.9% | 16.6% |
| Annualized Return | -8.3% | 84.8% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.7×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0234 | Ideal for 74 trades: 0.0135 |
| Top-1 Trade | 9.5% of gross profit | ✅ Low concentration |
| Top-3 Trades | 26.4% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | -33.1% | Strategy fails without best trade |
| Return ex-Top-3 | -56.6% | Strategy fails without top 3 |
| Max Single Trade | 27.2% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 21 | 8.62% | 181.0% | 7.75% | 13.05 |
| no_signal | 27 | 0.98% | 26.3% | 0.06% | 7.85 |
| direction_wrong_loss | 26 | -7.22% | -187.6% | -7.80% | 5.96 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| weak_negative | 34 | 0.62% | 21.0% | 50.0% | 50.0% | 0.30% |
| strong_negative | 17 | 0.69% | 11.8% | 41.2% | 41.2% | 0.78% |
| regime_shift | 16 | -0.31% | -4.9% | 37.5% | 37.5% | -2.82% |
| unknown | 7 | -1.17% | -8.2% | 57.1% | 57.1% | -2.36% |

**Best regime:** `weak_negative` — 34 trades, 21.0% total return, 50.0% win rate.
**Worst regime:** `unknown` — 7 trades, -8.2% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 14 | -7.60% | -106.3% |
| ❌ | ✅ | 8 | 9.03% | 72.3% |
| ✅ | ❌ | 12 | -6.77% | -81.3% |
| ✅ | ✅ | 13 | 8.36% | 108.7% |

### Flip Trades (Signal Wrong → Direction Right)

**21 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **8.5%**
- Total return: **177.7%**
- Average alpha: **8.5%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 11 | 8.72% |
| strong_negative | 7 | 9.69% |
| regime_shift | 3 | 4.67% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 67 | 0.42% | 27.9% | 44.8% | 44.8% |
| low | 7 | -1.17% | -8.2% | 57.1% | 57.1% |

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

**2023** (Flat: -1.6%, 19 trades)
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
| 2024-04-10 | 2024-04-19 | -1.0000 | 3.91% | weak_negative | ✅ |
| 2024-04-22 | 2024-04-23 | -1.0000 | -5.00% | weak_negative | ❌ |
| 2024-04-24 | 2024-05-01 | -1.0000 | -15.49% | weak_negative | ❌ |
| 2024-05-02 | 2024-05-14 | -1.0000 | -5.78% | weak_negative | ❌ |
| 2024-05-15 | 2024-06-05 | -1.0000 | 0.64% | weak_negative | ✅ |
| 2024-06-06 | 2024-07-03 | -1.0000 | 6.91% | weak_negative | ✅ |
| 2024-07-05 | 2024-07-12 | -1.0000 | -7.20% | weak_negative | ❌ |
| 2024-07-15 | 2024-07-18 | -1.0000 | 0.13% | weak_negative | ✅ |
| 2024-07-19 | 2024-08-06 | -1.0000 | 10.21% | weak_negative | ✅ |
| 2024-08-07 | 2024-08-15 | -1.0000 | -4.88% | regime_shift | ❌ |
| 2024-08-16 | 2024-08-21 | -1.0000 | -29.00% | regime_shift | ❌ |
| 2024-08-22 | 2024-09-09 | -1.0000 | 4.44% | regime_shift | ✅ |
| 2024-09-10 | 2024-09-13 | -1.0000 | -5.42% | regime_shift | ❌ |
| 2024-09-16 | 2024-10-28 | -1.0000 | -10.99% | regime_shift | ❌ |

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

## Conclusions & Observations

**Statistical robustness:** 74 trades provides a reasonable sample, though some metrics may have wide confidence intervals.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (-56.6% remaining).
**Signal vs Direction:** Signal accuracy (53.2%) exceeds direction accuracy (44.7%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities

- **Worst year:** 2024 (-22.7%, 25 trades). Macro: 2024 Election Year Uncertainty
- **Losing regime:** `regime_shift` — 16 trades, -4.9% total return
- **Losing regime:** `unknown` — 7 trades, -8.2% total return