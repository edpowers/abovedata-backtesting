# Strategy Analysis: corr_aware_leading_ma_noshift_sameq_e25d × fixed_holding_60d

**Ticker:** PRCT
**Entry:** `corr_aware_leading_ma_noshift_sameq_e25d`
**Exit:** `fixed_holding_60d`
**Period:** 2023-03-22 to 2026-02-06
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
- **entry_days_before:** `25` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `fixed_holding_60d`
  - Fixed 60-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 486.7% |
| **Annualized Return** | 42.7% |
| **Sharpe Ratio** | 0.871 |
| **Max Drawdown** | -39.6% |
| **Total Trades** | 12 |
| **Win Rate** | 75.0% |
| **Signal Accuracy** | 50.0% |
| **Direction Accuracy** | 87.5% |
| **Skill Ratio** | 87.5% |
| **Profit Factor** | 6.58 |
| **Expectancy** | 0.1850 |
| **Tail Ratio** | 2.79 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | -31.5% | 486.7% | 518.1% |
| Annualized Return | -8.3% | 42.7% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.5×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.1264 | Ideal for 12 trades: 0.0833 |
| Top-1 Trade | 28.6% of gross profit | ⚠️ High concentration |
| Top-3 Trades | 57.4% of gross profit | ⚠️ High concentration |
| Return ex-Top-1 | 235.3% | Strategy survives without best trade |
| Return ex-Top-3 | 77.0% | Strategy survives without top 3 |
| Max Single Trade | 75.0% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 7 | 29.81% | 208.7% | 20.87% | 73.86 |
| no_signal | 4 | 10.06% | 40.2% | 8.00% | 34.00 |
| direction_wrong_loss | 1 | -26.89% | -26.9% | -19.68% | 61.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 4 | 26.88% | 107.5% | 100.0% | 100.0% | 20.87% |
| strong_negative | 2 | 47.17% | 94.3% | 100.0% | 100.0% | 36.23% |
| weak_negative | 4 | 6.93% | 27.7% | 50.0% | 50.0% | 4.84% |
| unknown | 2 | -3.76% | -7.5% | 50.0% | 50.0% | -8.45% |

**Best regime:** `regime_shift` — 4 trades, 107.5% total return, 100.0% win rate.
**Worst regime:** `unknown` — 2 trades, -7.5% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ✅ | 4 | 31.63% | 126.5% |
| ✅ | ❌ | 1 | -26.89% | -26.9% |
| ✅ | ✅ | 3 | 27.38% | 82.1% |

### Flip Trades (Signal Wrong → Direction Right)

**6 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **30.0%**
- Total return: **179.7%**
- Average alpha: **24.5%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 3 | 24.26% |
| strong_negative | 2 | 47.17% |
| weak_negative | 1 | 12.59% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 10 | 22.96% | 229.6% | 80.0% | 80.0% |
| low | 2 | -3.76% | -7.5% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 7 | 16.76% | 117.3% | 57.1% | 57.1% |
| SHORT | 5 | 20.94% | 104.7% | 100.0% | 100.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 3 | 67.5% | 22.49% | 66.7% | 66.7% | 40.9% |
| 2024 | 4 | 95.0% | 23.74% | 100.0% | 100.0% | 70.8% |
| 2025 | 5 | 59.6% | 11.92% | 60.0% | 60.0% | 46.7% |

### Macro Context by Year

**2023** (Strong year: 67.5%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 95.0%, 4 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 59.6%, 5 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -26.9% cumulative (trade 1 to trade 2)
**Period:** 2023-03-22 to 2023-07-26 (2 trades)
**Peak cumulative return:** 19.4% → **Trough:** -7.5%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-03-22 | 2023-07-25 | 1.0000 | 19.37% | unknown | ✅ |
| 2023-07-26 | 2023-10-20 | 1.0000 | -26.89% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 16-30d | 2 | 13.44% | 26.9% | 100.0% |
| 31-50d | 3 | 21.11% | 63.3% | 66.7% |
| 50d+ | 6 | 23.24% | 139.5% | 83.3% |
| 6-15d | 1 | -7.62% | -7.6% | 0.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 7
- **Max consecutive losses:** 2

## Conclusions & Observations

**Statistical robustness:** ⚠️ Only 12 trades — interpret cautiously.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (77.0% remaining).
**Edge:** Genuine structural edge: 75.0% win rate with 6.58× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (87.5%) exceeds signal accuracy (50.0%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Losing regime:** `unknown` — 2 trades, -7.5% total return