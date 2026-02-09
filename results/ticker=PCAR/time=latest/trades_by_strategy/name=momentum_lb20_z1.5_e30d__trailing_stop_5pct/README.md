# Strategy Analysis: momentum_lb20_z1.5_e30d × trailing_stop_5%

**Ticker:** PCAR
**Entry:** `momentum_lb20_z1.5_e30d`
**Exit:** `trailing_stop_5%`
**Period:** 2021-06-14 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `1.5`
- **zscore_window:** `60`
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 95.0% |
| **Annualized Return** | 6.2% |
| **Sharpe Ratio** | 1.050 |
| **Max Drawdown** | -9.9% |
| **Total Trades** | 16 |
| **Win Rate** | 81.2% |
| **Signal Accuracy** | 50.0% |
| **Direction Accuracy** | 81.2% |
| **Skill Ratio** | 78.6% |
| **Profit Factor** | 14.16 |
| **Expectancy** | 0.0449 |
| **Tail Ratio** | 9.27 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 150.9% | 95.0% | -55.9% |
| Annualized Return | 21.9% | 6.2% | — |

## Diversity & Concentration

Diversification: **Somewhat concentrated** — noticeable dependence on top trades (HHI ratio: 2.7×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.1685 | Ideal for 16 trades: 0.0625 |
| Top-1 Trade | 37.4% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 61.8% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 51.3% | Positive without best trade |
| Return ex-Top-3 | 26.5% | Positive without top 3 |
| Max Single Trade | 28.9% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 11 | 5.59% | 61.5% | 5.59% | 17.55 |
| no_signal | 2 | 7.91% | 15.8% | 7.91% | 19.50 |
| direction_wrong_loss | 3 | -1.82% | -5.5% | -1.82% | 10.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 16 | 4.49% | 71.8% | 81.2% | 81.2% | 4.49% |

**Best-performing regime:** `unknown` — 16 trades, 71.8% total return, 81.2% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 1 | -3.12% | -3.1% |
| ❌ | ✅ | 9 | 6.06% | 54.5% |
| ✅ | ❌ | 2 | -1.17% | -2.3% |
| ✅ | ✅ | 2 | 3.47% | 6.9% |

### Flip Trades (Signal Wrong → Direction Right)

**11 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **6.4%**
- Total return: **70.3%**
- Average alpha: **6.4%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 11 | 6.39% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 16 | 4.49% | 71.8% | 81.2% | 81.2% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 10 | 5.71% | 57.1% | 80.0% | 80.0% |
| SHORT | 6 | 2.46% | 14.7% | 83.3% | 83.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2021 | 6 | 9.6% | 1.60% | 83.3% | 83.3% | 9.6% |
| 2023 | 4 | 11.1% | 2.77% | 75.0% | 75.0% | 11.1% |
| 2024 | 2 | 33.7% | 16.84% | 100.0% | 100.0% | 33.7% |
| 2025 | 3 | 13.9% | 4.64% | 66.7% | 66.7% | 13.9% |
| 2026 | 1 | 3.5% | 3.49% | 100.0% | 100.0% | 3.5% |

### Macro Context by Year

**2021** (Modestly positive: 9.6%, 6 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2023** (Strong year: 11.1%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 33.7%, 2 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 13.9%, 3 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 3.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -3.1% cumulative (trade 4 to trade 5)
**Period:** 2021-09-14 to 2021-09-16 (2 trades)
**Peak cumulative return:** 9.2% → **Trough:** 6.0%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2021-09-14 | 2021-09-15 | 1.0000 | 0.77% | unknown | ✅ |
| 2021-09-16 | 2021-09-20 | 1.0000 | -3.12% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 3 | -0.98% | -2.9% | 33.3% |
| 16-30d | 5 | 2.96% | 14.8% | 80.0% |
| 31-50d | 3 | 15.07% | 45.2% | 100.0% |
| 6-15d | 5 | 2.94% | 14.7% | 100.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 1

## Observations & Caveats

**Sample size:** ⚠️ Only 16 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (26.5%).
**Win/loss profile:** 81.2% win rate with 14.16× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (81.2%) exceeded signal accuracy (50.0%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 150.9% buy-and-hold return (aligned to strategy period: None to None), yet 6 short trades returned 14.7% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **SUSPICIOUSLY_PERFECT:** Profit factor of 14.2 with only 16 trades suggests the strategy may be avoiding losses through exit timing rather than signal skill. These results almost always degrade catastrophically out of sample.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 16d, std 13d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.