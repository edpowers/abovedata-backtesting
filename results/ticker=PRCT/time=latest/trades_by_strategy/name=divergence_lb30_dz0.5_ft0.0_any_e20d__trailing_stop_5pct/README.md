# Strategy Analysis: divergence_lb30_dz0.5_ft0.0_any_e20d × trailing_stop_5%

**Ticker:** PRCT
**Entry:** `divergence_lb30_dz0.5_ft0.0_any_e20d`
**Exit:** `trailing_stop_5%`
**Period:** 2023-03-29 to 2025-10-16
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **divergence**

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **lookback_days:** `30`
- **divergence_zscore:** `0.5`
- **fundamental_threshold:** `0.0`
- **require_strong_divergence:** `False`
- **entry_days_before:** `20` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 15.4% |
| **Annualized Return** | 9.5% |
| **Sharpe Ratio** | 1.443 |
| **Max Drawdown** | -4.2% |
| **Total Trades** | 15 |
| **Win Rate** | 46.7% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 46.7% |
| **Skill Ratio** | 50.0% |
| **Profit Factor** | 1.95 |
| **Expectancy** | 0.0104 |
| **Tail Ratio** | 2.66 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.7×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.1117 | Ideal for 15 trades: 0.0667 |
| Top-1 Trade | 35.9% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 67.0% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 3.6% | Positive without best trade |
| Return ex-Top-3 | -6.0% | Negative without top 3 |
| Max Single Trade | 11.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 6 | 4.51% | 27.1% | 4.51% | 2.67 |
| no_signal | 3 | 0.52% | 1.6% | 0.52% | 1.67 |
| direction_wrong_loss | 6 | -2.17% | -13.0% | -2.17% | 2.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 15 | 1.04% | 15.6% | 46.7% | 46.7% | 1.04% |

**Best-performing regime:** `unknown` — 15 trades, 15.6% total return, 46.7% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ✅ | ❌ | 6 | -2.17% | -13.0% |
| ✅ | ✅ | 6 | 4.51% | 27.1% |

### Flip Trades (Signal Wrong → Direction Right)

**1 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.9%**
- Total return: **4.9%**
- Average alpha: **4.9%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 1 | 4.88% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 3 | 4.27% | 12.8% | 66.7% | 66.7% |
| low | 12 | 0.23% | 2.8% | 41.7% | 41.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 12 | 1.17% | 14.1% | 50.0% | 50.0% |
| SHORT | 3 | 0.52% | 1.6% | 33.3% | 33.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2023 | 3 | 12.8% | 4.27% | 66.7% | 66.7% | 12.8% |
| 2024 | 6 | 7.1% | 1.19% | 66.7% | 66.7% | 7.1% |
| 2025 | 6 | -4.3% | -0.72% | 16.7% | 16.7% | -4.3% |

### Macro Context by Year

**2023** (Strong year: 12.8%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 7.1%, 6 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Roughly flat: -4.3%, 6 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -10.3% cumulative (trade 7 to trade 12)
**Period:** 2024-07-03 to 2025-02-04 (6 trades)
**Peak cumulative return:** 24.3% → **Trough:** 14.1%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-07-03 | 2024-07-15 | 1.0000 | 5.06% | unknown | ✅ |
| 2024-07-16 | 2024-07-18 | 1.0000 | -4.31% | unknown | ❌ |
| 2024-07-19 | 2024-07-24 | 1.0000 | -0.03% | unknown | ❌ |
| 2025-01-27 | 2025-01-28 | 1.0000 | -2.46% | unknown | ❌ |
| 2025-01-29 | 2025-02-03 | 1.0000 | -2.33% | unknown | ❌ |
| 2025-02-04 | 2025-02-06 | 1.0000 | -1.12% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 14 | 0.75% | 10.6% | 42.9% |
| 6-15d | 1 | 5.06% | 5.1% | 100.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 5

## Observations & Caveats

**Sample size:** ⚠️ Only 15 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-6.0%).
**Win/loss profile:** Profit factor of 1.95 with 46.7% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (46.7%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2025 (-4.3%, 6 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.