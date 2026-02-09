# Strategy Analysis: momentum_lb20_z1.5_e30d × sl-10%_tp20%

**Ticker:** PCAR
**Entry:** `momentum_lb20_z1.5_e30d`
**Exit:** `sl-10%_tp20%`
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

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 118.4% |
| **Annualized Return** | 6.9% |
| **Sharpe Ratio** | 0.870 |
| **Max Drawdown** | -12.4% |
| **Total Trades** | 8 |
| **Win Rate** | 87.5% |
| **Signal Accuracy** | 25.0% |
| **Direction Accuracy** | 87.5% |
| **Skill Ratio** | 100.0% |
| **Profit Factor** | 1520.19 |
| **Expectancy** | 0.1043 |
| **Tail Ratio** | 362.50 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 150.9% | 118.4% | -32.6% |
| Annualized Return | 21.9% | 6.9% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.4×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.1697 | Ideal for 8 trades: 0.1250 |
| Top-1 Trade | 23.8% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 61.0% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 82.1% | Positive without best trade |
| Return ex-Top-3 | 36.7% | Positive without top 3 |
| Max Single Trade | 19.9% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 6 | 10.63% | 63.8% | 10.63% | 53.33 |
| no_signal | 2 | 9.85% | 19.7% | 9.85% | 19.50 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 8 | 10.43% | 83.5% | 87.5% | 87.5% | 10.43% |

**Best-performing regime:** `unknown` — 8 trades, 83.5% total return, 87.5% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ✅ | 5 | 10.78% | 53.9% |
| ✅ | ✅ | 1 | 9.88% | 9.9% |

### Flip Trades (Signal Wrong → Direction Right)

**6 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **12.3%**
- Total return: **73.6%**
- Average alpha: **12.3%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 6 | 12.27% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 8 | 10.43% | 83.5% | 87.5% | 87.5% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 6 | 11.02% | 66.1% | 83.3% | 83.3% |
| SHORT | 2 | 8.67% | 17.3% | 100.0% | 100.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2021 | 2 | 14.1% | 7.03% | 100.0% | 100.0% | 14.1% |
| 2023 | 2 | 31.2% | 15.59% | 100.0% | 100.0% | 31.2% |
| 2024 | 2 | 18.5% | 9.26% | 100.0% | 100.0% | 18.5% |
| 2025 | 1 | 19.7% | 19.75% | 100.0% | 100.0% | 19.7% |
| 2026 | 1 | -0.1% | -0.05% | 0.0% | 0.0% | -0.1% |

### Macro Context by Year

**2021** (Strong year: 14.1%, 2 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2023** (Strong year: 31.2%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 18.5%, 2 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 19.7%, 1 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Roughly flat: -0.1%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -0.1% cumulative (trade 7 to trade 8)
**Period:** 2025-12-09 to 2026-02-05 (2 trades)
**Peak cumulative return:** 83.5% → **Trough:** 83.5%

**Macro context during drawdown:**
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-12-09 | 2026-02-04 | 1.0000 | 19.75% | unknown | ✅ |
| 2026-02-05 | 2026-02-06 | 1.0000 | -0.05% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 1 | -0.05% | -0.1% | 0.0% |
| 16-30d | 1 | 8.63% | 8.6% | 100.0% |
| 31-50d | 1 | 19.75% | 19.7% | 100.0% |
| 50d+ | 5 | 11.03% | 55.1% | 100.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 7
- **Max consecutive losses:** 1

## Observations & Caveats

**Sample size:** ⚠️ Only 8 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Well-distributed. HHI of 0.1697 is near the theoretical minimum of 0.1250 for 8 trades.
**Win/loss profile:** 87.5% win rate with 1520.19× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (87.5%) exceeded signal accuracy (25.0%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **FLIP_OVERFITTING:** Signal accuracy is only 25.0% but win rate is 87.5%. The correlation flip mechanism is compensating for poor signal quality. This suggests the flip is overfitting to historical correlation regimes, which may not persist.
- **SUSPICIOUSLY_PERFECT:** Profit factor of 1520.2 with only 8 trades suggests the strategy may be avoiding losses through exit timing rather than signal skill. These results almost always degrade catastrophically out of sample.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.