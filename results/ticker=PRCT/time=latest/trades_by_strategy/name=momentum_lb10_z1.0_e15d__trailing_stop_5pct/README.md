# Strategy Analysis: momentum_lb10_z1.0_e15d × trailing_stop_5%

**Ticker:** PRCT
**Entry:** `momentum_lb10_z1.0_e15d`
**Exit:** `trailing_stop_5%`
**Period:** 2022-02-14 to 2024-10-24
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `10`
- **zscore_threshold:** `1.0`
- **zscore_window:** `60`
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 14.5% |
| **Annualized Return** | 12.1% |
| **Sharpe Ratio** | 1.507 |
| **Max Drawdown** | -7.4% |
| **Total Trades** | 18 |
| **Win Rate** | 50.0% |
| **Signal Accuracy** | 100.0% |
| **Direction Accuracy** | 50.0% |
| **Skill Ratio** | 50.0% |
| **Profit Factor** | 1.55 |
| **Expectancy** | 0.0087 |
| **Tail Ratio** | 1.08 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0841 | Ideal for 18 trades: 0.0556 |
| Top-1 Trade | 23.5% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 57.2% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 3.7% | Positive without best trade |
| Return ex-Top-3 | -10.1% | Negative without top 3 |
| Max Single Trade | 10.4% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 9 | 4.90% | 44.1% | 4.90% | 2.44 |
| direction_wrong_loss | 9 | -3.16% | -28.4% | -3.16% | 1.78 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 18 | 0.87% | 15.7% | 50.0% | 50.0% | 0.87% |

**Best-performing regime:** `unknown` — 18 trades, 15.7% total return, 50.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 2 | -1.60% | -3.2% |
| ❌ | ✅ | 1 | 9.15% | 9.1% |
| ✅ | ❌ | 7 | -3.60% | -25.2% |
| ✅ | ✅ | 8 | 4.37% | 35.0% |

### Flip Trades (Signal Wrong → Direction Right)

**1 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **9.1%**
- Total return: **9.1%**
- Average alpha: **9.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 1 | 9.15% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 18 | 0.87% | 15.7% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 12 | 0.48% | 5.8% | 33.3% | 33.3% |
| SHORT | 6 | 1.65% | 9.9% | 83.3% | 83.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2022 | 3 | 5.9% | 1.98% | 33.3% | 33.3% | 5.9% |
| 2023 | 6 | 8.8% | 1.47% | 66.7% | 66.7% | 8.8% |
| 2024 | 9 | 1.0% | 0.11% | 44.4% | 44.4% | 1.0% |

### Macro Context by Year

**2022** (Modestly positive: 5.9%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 8.8%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 1.0%, 9 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.


## Worst Drawdown Period

**Drawdown:** -12.0% cumulative (trade 5 to trade 15)
**Period:** 2023-04-12 to 2024-07-19 (11 trades)
**Peak cumulative return:** 18.7% → **Trough:** 6.7%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-04-12 | 2023-04-13 | 1.0000 | 2.40% | unknown | ✅ |
| 2023-04-14 | 2023-04-19 | 1.0000 | -4.83% | unknown | ❌ |
| 2023-10-11 | 2023-10-12 | -1.0000 | 4.70% | unknown | ✅ |
| 2023-10-13 | 2023-10-16 | -1.0000 | -9.58% | unknown | ❌ |
| 2023-10-17 | 2023-10-23 | -1.0000 | 5.75% | unknown | ✅ |
| 2024-04-10 | 2024-04-12 | 1.0000 | -2.91% | unknown | ❌ |
| 2024-04-15 | 2024-04-16 | 1.0000 | 2.75% | unknown | ✅ |
| 2024-04-17 | 2024-04-18 | 1.0000 | -1.37% | unknown | ❌ |
| 2024-07-11 | 2024-07-15 | 1.0000 | -2.17% | unknown | ❌ |
| 2024-07-16 | 2024-07-18 | 1.0000 | -4.31% | unknown | ❌ |
| 2024-07-19 | 2024-07-24 | 1.0000 | -0.03% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 18 | 0.87% | 15.7% | 50.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 3
- **Max consecutive losses:** 4

## Observations & Caveats

**Sample size:** ⚠️ Only 18 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-10.1%).
**Win/loss profile:** Profit factor of 1.55 with 50.0% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (100.0%) exceeded direction accuracy (50.0%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities


### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.