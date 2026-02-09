# Strategy Analysis: corr_aware_contemp_e1d × trailing_stop_5%

**Ticker:** DE
**Entry:** `corr_aware_contemp_e1d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-08-16 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `1` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 80.7% |
| **Annualized Return** | 30.5% |
| **Sharpe Ratio** | 1.492 |
| **Max Drawdown** | -30.5% |
| **Total Trades** | 234 |
| **Win Rate** | 43.6% |
| **Signal Accuracy** | 35.0% |
| **Direction Accuracy** | 43.6% |
| **Skill Ratio** | 43.8% |
| **Profit Factor** | 1.23 |
| **Expectancy** | 0.0040 |
| **Tail Ratio** | 1.90 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 701.3% | 80.7% | -620.6% |
| Annualized Return | 20.7% | 30.5% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.1×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0089 | Ideal for 234 trades: 0.0043 |
| Top-1 Trade | 7.5% of gross profit | Moderate concentration |
| Top-3 Trades | 15.9% of gross profit | Moderate concentration |
| Return ex-Top-1 | 31.4% | Positive without best trade |
| Return ex-Top-3 | -10.1% | Negative without top 3 |
| Max Single Trade | 37.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 95 | 4.87% | 462.6% | 3.22% | 9.20 |
| no_signal | 17 | 0.72% | 12.2% | -0.15% | 9.94 |
| direction_wrong_loss | 122 | -3.13% | -381.5% | -2.73% | 5.01 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| weak_negative | 66 | 1.77% | 116.8% | 43.9% | 43.9% | 1.08% |
| weak_positive | 21 | 0.98% | 20.5% | 52.4% | 52.4% | -0.07% |
| strong_negative | 13 | 0.59% | 7.6% | 46.2% | 46.2% | -0.86% |
| regime_shift | 52 | 0.03% | 1.5% | 44.2% | 44.2% | 0.07% |
| strong_positive | 54 | -0.39% | -21.2% | 38.9% | 38.9% | -0.98% |
| unknown | 28 | -1.15% | -32.1% | 42.9% | 42.9% | -1.41% |

**Best-performing regime:** `weak_negative` — 66 trades, 116.8% total return, 43.9% win rate.
**Worst-performing regime:** `unknown` — 28 trades, -32.1% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 78 | -3.29% | -256.8% |
| ❌ | ✅ | 63 | 5.28% | 332.6% |
| ✅ | ❌ | 44 | -2.83% | -124.7% |
| ✅ | ✅ | 32 | 4.06% | 129.9% |

### Flip Trades (Signal Wrong → Direction Right)

**70 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.3%**
- Total return: **369.5%**
- Average alpha: **3.8%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 25 | 7.96% |
| regime_shift | 15 | 5.29% |
| strong_positive | 15 | 3.07% |
| strong_negative | 6 | 3.55% |
| unknown | 5 | 0.79% |
| weak_positive | 4 | 4.92% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 132 | 0.29% | 38.2% | 40.9% | 40.9% |
| low | 81 | 0.44% | 35.5% | 45.7% | 45.7% |
| high | 21 | 0.93% | 19.6% | 52.4% | 52.4% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 157 | 0.96% | 150.8% | 46.5% | 46.5% |
| SHORT | 77 | -0.75% | -57.5% | 37.7% | 37.7% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 17 | -9.8% | -0.58% | 47.1% | 47.1% | -3.1% |
| 2019 | 34 | -35.2% | -1.03% | 35.3% | 35.3% | -61.6% |
| 2020 | 39 | 67.8% | 1.74% | 56.4% | 56.4% | 59.7% |
| 2021 | 33 | -26.6% | -0.81% | 39.4% | 39.4% | -48.5% |
| 2022 | 36 | 42.6% | 1.18% | 41.7% | 41.7% | 40.7% |
| 2023 | 27 | 11.8% | 0.44% | 37.0% | 37.0% | -11.1% |
| 2024 | 19 | 3.0% | 0.16% | 42.1% | 42.1% | -18.3% |
| 2025 | 27 | 27.0% | 1.00% | 48.1% | 48.1% | -1.3% |
| 2026 | 2 | 12.8% | 6.42% | 50.0% | 50.0% | 13.3% |

### Macro Context by Year

**2018** (Losing year: -9.8%, 17 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -35.2%, 34 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 67.8%, 39 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -26.6%, 33 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 42.6%, 36 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 11.8%, 27 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 3.0%, 19 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 27.0%, 27 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 12.8%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -90.5% cumulative (trade 7 to trade 63)
**Period:** 2018-10-30 to 2020-03-19 (57 trades)
**Peak cumulative return:** 8.0% → **Trough:** -82.5%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2018-10-30 | 2018-11-15 | 1.0000 | 10.50% | unknown | ✅ |
| 2018-11-16 | 2018-11-20 | 1.0000 | -6.32% | unknown | ❌ |
| 2018-11-21 | 2018-11-23 | -1.0000 | -0.68% | unknown | ❌ |
| 2018-11-26 | 2018-11-28 | -1.0000 | -2.07% | unknown | ❌ |
| 2018-11-29 | 2018-12-03 | -1.0000 | -8.16% | unknown | ❌ |
| 2018-12-04 | 2018-12-06 | -1.0000 | -1.85% | unknown | ❌ |
| 2018-12-07 | 2018-12-11 | -1.0000 | 0.18% | unknown | ✅ |
| 2018-12-12 | 2018-12-19 | -1.0000 | 1.39% | unknown | ✅ |
| 2018-12-20 | 2018-12-26 | -1.0000 | 0.95% | unknown | ✅ |
| 2018-12-27 | 2018-12-28 | -1.0000 | 0.47% | unknown | ✅ |
| 2018-12-31 | 2019-01-04 | -1.0000 | -1.68% | unknown | ❌ |
| 2019-01-07 | 2019-01-10 | -1.0000 | -3.22% | unknown | ❌ |
| 2019-01-11 | 2019-01-18 | -1.0000 | -4.00% | unknown | ❌ |
| 2019-01-22 | 2019-01-30 | -1.0000 | -2.56% | unknown | ❌ |
| 2019-01-31 | 2019-02-14 | -1.0000 | 0.96% | unknown | ✅ |
| 2019-02-14 | 2019-02-21 | 1.0000 | 0.26% | unknown | ✅ |
| 2019-02-22 | 2019-03-06 | 1.0000 | -4.66% | unknown | ❌ |
| 2019-03-07 | 2019-04-10 | 1.0000 | 0.87% | unknown | ✅ |
| 2019-04-11 | 2019-04-25 | 1.0000 | 1.03% | unknown | ✅ |
| 2019-04-26 | 2019-05-06 | 1.0000 | -2.93% | unknown | ❌ |
| 2019-05-07 | 2019-05-13 | 1.0000 | -7.28% | unknown | ❌ |
| 2019-05-14 | 2019-05-16 | 1.0000 | -0.76% | unknown | ❌ |
| 2019-05-16 | 2019-05-17 | -1.0000 | 7.65% | strong_positive | ✅ |
| 2019-05-20 | 2019-05-21 | -1.0000 | -2.60% | strong_positive | ❌ |
| 2019-05-22 | 2019-05-30 | -1.0000 | -2.09% | strong_positive | ❌ |
| 2019-05-31 | 2019-06-04 | -1.0000 | -3.89% | strong_positive | ❌ |
| 2019-06-05 | 2019-06-11 | -1.0000 | -2.59% | strong_positive | ❌ |
| 2019-06-12 | 2019-06-17 | -1.0000 | -3.75% | strong_positive | ❌ |
| 2019-06-18 | 2019-06-21 | -1.0000 | -3.07% | strong_positive | ❌ |
| 2019-06-24 | 2019-07-15 | -1.0000 | 0.07% | strong_positive | ✅ |
| 2019-07-16 | 2019-07-26 | -1.0000 | -2.55% | strong_positive | ❌ |
| 2019-07-29 | 2019-08-05 | -1.0000 | 11.28% | strong_positive | ✅ |
| 2019-08-06 | 2019-08-12 | -1.0000 | 3.75% | strong_positive | ✅ |
| 2019-08-13 | 2019-08-16 | -1.0000 | -1.40% | strong_positive | ❌ |
| 2019-08-19 | 2019-08-23 | -1.0000 | 3.52% | strong_positive | ✅ |
| 2019-08-26 | 2019-08-29 | -1.0000 | -3.76% | strong_positive | ❌ |
| 2019-08-30 | 2019-09-06 | -1.0000 | -1.04% | strong_positive | ❌ |
| 2019-09-09 | 2019-09-11 | -1.0000 | -4.29% | strong_positive | ❌ |
| 2019-09-12 | 2019-09-27 | -1.0000 | -2.30% | strong_positive | ❌ |
| 2019-09-30 | 2019-10-07 | -1.0000 | 1.26% | strong_positive | ✅ |
| 2019-10-08 | 2019-10-11 | -1.0000 | -3.62% | strong_positive | ❌ |
| 2019-10-14 | 2019-11-04 | -1.0000 | -6.02% | strong_positive | ❌ |
| 2019-11-05 | 2019-11-26 | -1.0000 | 1.27% | strong_positive | ✅ |
| 2019-11-27 | 2019-12-03 | 1.0000 | -3.29% | strong_positive | ❌ |
| 2019-12-04 | 2020-01-23 | 1.0000 | 4.56% | strong_positive | ✅ |
| 2020-01-24 | 2020-01-27 | 1.0000 | -4.02% | strong_positive | ❌ |
| 2020-01-28 | 2020-01-31 | 1.0000 | -2.70% | strong_positive | ❌ |
| 2020-02-03 | 2020-02-18 | 1.0000 | 5.06% | strong_positive | ✅ |
| 2020-02-19 | 2020-02-24 | 1.0000 | 4.20% | strong_positive | ✅ |
| 2020-02-25 | 2020-02-27 | 1.0000 | -4.00% | regime_shift | ❌ |
| 2020-02-28 | 2020-03-03 | 1.0000 | 0.83% | regime_shift | ✅ |
| 2020-03-04 | 2020-03-06 | 1.0000 | 0.59% | regime_shift | ✅ |
| 2020-03-09 | 2020-03-10 | 1.0000 | 3.33% | regime_shift | ✅ |
| 2020-03-11 | 2020-03-12 | 1.0000 | -10.62% | regime_shift | ❌ |
| 2020-03-13 | 2020-03-16 | 1.0000 | -13.61% | regime_shift | ❌ |
| 2020-03-17 | 2020-03-18 | 1.0000 | -9.87% | regime_shift | ❌ |
| 2020-03-19 | 2020-03-20 | 1.0000 | -6.71% | regime_shift | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 133 | -0.96% | -127.8% | 34.6% |
| 16-30d | 19 | 5.61% | 106.7% | 68.4% |
| 31-50d | 5 | 12.97% | 64.9% | 100.0% |
| 6-15d | 77 | 0.64% | 49.5% | 49.4% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 234 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-10.1%).
**Win/loss profile:** Profit factor of 1.23 with 43.6% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (43.6%) exceeded signal accuracy (35.0%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.
**Regime dependence:** `weak_negative` (66 trades, 28% of total) contributed 116.8% — a disproportionate share. Performance may degrade if this regime becomes less common.

### Known Vulnerabilities

- **Worst year:** 2019 (-35.2%, 34 trades). Macro: US-China Trade War Escalation, Fed Rate Cuts (2019)
- **Losing regime:** `strong_positive` — 54 trades, -21.2% total return
- **Losing regime:** `unknown` — 28 trades, -32.1% total return

### ⚠️ Robustness Red Flags

- **REGIME_CONCENTRATION:** `weak_negative` regime (66 trades, 28% of total) contributes 125% of total return. Performance is fragile if this regime becomes less common or behaves differently.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 7d, std 8d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.