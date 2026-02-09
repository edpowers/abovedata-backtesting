# Strategy Analysis: corr_aware_leading_ma_noshift_e0d × trailing_stop_5%

**Ticker:** PRCT
**Entry:** `corr_aware_leading_ma_noshift_e0d`
**Exit:** `trailing_stop_5%`
**Period:** 2023-04-27 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `leading_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `True` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `0` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 735.8% |
| **Annualized Return** | 17.6% |
| **Sharpe Ratio** | 0.549 |
| **Max Drawdown** | -31.7% |
| **Total Trades** | 240 |
| **Win Rate** | 53.8% |
| **Signal Accuracy** | 55.0% |
| **Direction Accuracy** | 51.7% |
| **Skill Ratio** | 51.7% |
| **Profit Factor** | 1.78 |
| **Expectancy** | 0.0102 |
| **Tail Ratio** | 2.07 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | -31.5% | 735.8% | 767.2% |
| Annualized Return | -8.3% | 17.6% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.3×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0095 | Ideal for 240 trades: 0.0042 |
| Top-1 Trade | 6.5% of gross profit | ✅ Low concentration |
| Top-3 Trades | 16.4% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 513.8% | Strategy survives without best trade |
| Return ex-Top-3 | 278.3% | Strategy survives without top 3 |
| Max Single Trade | 36.2% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 77 | 4.90% | 377.0% | 4.54% | 2.32 |
| no_signal | 91 | 0.77% | 69.6% | 0.57% | 1.65 |
| direction_wrong_loss | 72 | -2.80% | -201.6% | -2.59% | 1.82 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 64 | 1.50% | 95.9% | 51.6% | 51.6% | 1.22% |
| weak_negative | 99 | 0.87% | 86.3% | 53.5% | 53.5% | 0.73% |
| unknown | 27 | 1.56% | 42.1% | 59.3% | 59.3% | 1.43% |
| strong_negative | 50 | 0.41% | 20.6% | 54.0% | 54.0% | 0.52% |

**Best regime:** `regime_shift` — 64 trades, 95.9% total return, 51.6% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 33 | -3.37% | -111.3% |
| ❌ | ✅ | 34 | 5.33% | 181.3% |
| ✅ | ❌ | 39 | -2.32% | -90.4% |
| ✅ | ✅ | 43 | 4.55% | 195.6% |

### Flip Trades (Signal Wrong → Direction Right)

**86 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **4.2%**
- Total return: **361.7%**
- Average alpha: **4.1%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 39 | 3.54% |
| strong_negative | 27 | 3.69% |
| regime_shift | 19 | 6.25% |
| unknown | 1 | 5.29% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 213 | 0.95% | 202.9% | 53.1% | 53.1% |
| low | 25 | 1.47% | 36.8% | 60.0% | 60.0% |
| no_data | 2 | 2.64% | 5.3% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 148 | 0.95% | 141.3% | 47.3% | 47.3% |
| SHORT | 92 | 1.13% | 103.7% | 64.1% | 64.1% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 64 | 27.6% | 0.43% | 51.6% | 51.6% | 28.7% |
| 2024 | 75 | 123.6% | 1.65% | 48.0% | 48.0% | 111.7% |
| 2025 | 89 | 93.2% | 1.05% | 61.8% | 61.8% | 72.8% |
| 2026 | 12 | 0.6% | 0.05% | 41.7% | 41.7% | 1.5% |

### Macro Context by Year

**2023** (Strong year: 27.6%, 64 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 123.6%, 75 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 93.2%, 89 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 0.6%, 12 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -22.2% cumulative (trade 116 to trade 122)
**Period:** 2024-09-13 to 2024-10-18 (7 trades)
**Peak cumulative return:** 123.1% → **Trough:** 100.9%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-09-13 | 2024-09-18 | 1.0000 | 2.29% | regime_shift | ✅ |
| 2024-09-19 | 2024-09-23 | 1.0000 | -3.09% | regime_shift | ❌ |
| 2024-09-24 | 2024-10-01 | 1.0000 | -3.92% | regime_shift | ❌ |
| 2024-10-02 | 2024-10-03 | 1.0000 | -1.98% | regime_shift | ❌ |
| 2024-10-04 | 2024-10-07 | 1.0000 | -4.18% | regime_shift | ❌ |
| 2024-10-08 | 2024-10-17 | 1.0000 | -6.65% | regime_shift | ❌ |
| 2024-10-18 | 2024-10-23 | 1.0000 | -2.36% | regime_shift | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 233 | 0.82% | 190.8% | 52.8% |
| 6-15d | 7 | 7.74% | 54.2% | 85.7% |

## Win/Loss Streaks

- **Max consecutive wins:** 10
- **Max consecutive losses:** 6

## Conclusions & Observations

**Statistical robustness:** With 240 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (278.3% remaining).
**Edge:** Genuine structural edge: 53.8% win rate with 1.78× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Signal accuracy (55.0%) exceeds direction accuracy (51.7%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities
