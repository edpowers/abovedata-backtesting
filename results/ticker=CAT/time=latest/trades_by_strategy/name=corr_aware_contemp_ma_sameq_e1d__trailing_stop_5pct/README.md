# Strategy Analysis: corr_aware_contemp_ma_sameq_e1d × trailing_stop_5%

**Ticker:** CAT
**Entry:** `corr_aware_contemp_ma_sameq_e1d`
**Exit:** `trailing_stop_5%`
**Period:** 2020-07-30 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `1` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 11.8% |
| **Annualized Return** | 26.7% |
| **Sharpe Ratio** | 1.643 |
| **Max Drawdown** | -24.5% |
| **Total Trades** | 164 |
| **Win Rate** | 40.2% |
| **Signal Accuracy** | 50.4% |
| **Direction Accuracy** | 40.2% |
| **Skill Ratio** | 42.3% |
| **Profit Factor** | 1.11 |
| **Expectancy** | 0.0023 |
| **Tail Ratio** | 1.93 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 954.1% | 11.8% | -942.2% |
| Annualized Return | 23.7% | 26.7% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.9×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0116 | Ideal for 164 trades: 0.0061 |
| Top-1 Trade | 6.4% of gross profit | Moderate concentration |
| Top-3 Trades | 16.6% of gross profit | Moderate concentration |
| Return ex-Top-1 | -9.1% | Negative without best trade |
| Return ex-Top-3 | -35.2% | Negative without top 3 |
| Max Single Trade | 23.0% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 52 | 5.88% | 305.5% | 5.13% | 12.60 |
| no_signal | 41 | -1.15% | -47.2% | -2.08% | 4.78 |
| direction_wrong_loss | 71 | -3.12% | -221.2% | -3.38% | 5.41 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 164 | 0.23% | 37.1% | 40.2% | 40.2% | -0.36% |

**Best-performing regime:** `unknown` — 164 trades, 37.1% total return, 40.2% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 33 | -2.72% | -89.8% |
| ❌ | ✅ | 28 | 5.88% | 164.5% |
| ✅ | ❌ | 38 | -3.46% | -131.4% |
| ✅ | ✅ | 24 | 5.88% | 141.0% |

### Flip Trades (Signal Wrong → Direction Right)

**42 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.2%**
- Total return: **219.4%**
- Average alpha: **4.9%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 42 | 5.22% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 89 | 0.58% | 51.8% | 41.6% | 41.6% |
| high | 52 | 0.72% | 37.4% | 44.2% | 44.2% |
| no_data | 3 | -3.53% | -10.6% | 33.3% | 33.3% |
| low | 20 | -2.08% | -41.6% | 25.0% | 25.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 59 | 1.89% | 111.4% | 47.5% | 47.5% |
| SHORT | 105 | -0.71% | -74.3% | 36.2% | 36.2% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 16 | -37.7% | -2.36% | 18.8% | 18.8% | -54.1% |
| 2021 | 24 | 32.6% | 1.36% | 45.8% | 45.8% | 11.7% |
| 2022 | 31 | 36.4% | 1.17% | 48.4% | 48.4% | 54.5% |
| 2023 | 28 | -17.7% | -0.63% | 28.6% | 28.6% | -31.3% |
| 2024 | 22 | 61.0% | 2.77% | 63.6% | 63.6% | 34.2% |
| 2025 | 37 | -17.2% | -0.46% | 37.8% | 37.8% | -48.1% |
| 2026 | 6 | -20.2% | -3.37% | 16.7% | 16.7% | -25.3% |

### Macro Context by Year

**2020** (Losing year: -37.7%, 16 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 32.6%, 24 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 36.4%, 31 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Losing year: -17.7%, 28 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 61.0%, 22 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -17.2%, 37 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -20.2%, 6 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -54.7% cumulative (trade 128 to trade 164)
**Period:** 2025-04-04 to 2026-02-05 (37 trades)
**Peak cumulative return:** 91.8% → **Trough:** 37.1%

**Macro context during drawdown:**
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-04-04 | 2025-04-07 | -1.0000 | 2.78% | unknown | ✅ |
| 2025-04-08 | 2025-04-09 | -1.0000 | -9.88% | unknown | ❌ |
| 2025-04-10 | 2025-04-11 | -1.0000 | -1.48% | unknown | ❌ |
| 2025-04-14 | 2025-04-23 | -1.0000 | 0.31% | unknown | ✅ |
| 2025-04-24 | 2025-04-30 | -1.0000 | -0.79% | unknown | ❌ |
| 2025-05-01 | 2025-05-08 | -1.0000 | -3.28% | unknown | ❌ |
| 2025-05-09 | 2025-05-12 | -1.0000 | -5.20% | unknown | ❌ |
| 2025-05-13 | 2025-05-27 | -1.0000 | 0.29% | unknown | ✅ |
| 2025-05-28 | 2025-06-06 | -1.0000 | -1.10% | unknown | ❌ |
| 2025-06-09 | 2025-06-24 | -1.0000 | -4.18% | unknown | ❌ |
| 2025-06-25 | 2025-06-30 | -1.0000 | -4.48% | unknown | ❌ |
| 2025-07-01 | 2025-07-09 | -1.0000 | -2.88% | unknown | ❌ |
| 2025-07-10 | 2025-07-23 | -1.0000 | -5.10% | unknown | ❌ |
| 2025-07-24 | 2025-08-04 | -1.0000 | -0.97% | unknown | ❌ |
| 2025-08-04 | 2025-08-22 | 1.0000 | 0.45% | unknown | ✅ |
| 2025-08-25 | 2025-08-29 | 1.0000 | -3.07% | unknown | ❌ |
| 2025-09-02 | 2025-09-25 | 1.0000 | 11.46% | unknown | ✅ |
| 2025-09-26 | 2025-10-14 | 1.0000 | 13.25% | unknown | ✅ |
| 2025-10-15 | 2025-10-22 | 1.0000 | -3.49% | unknown | ❌ |
| 2025-10-23 | 2025-10-28 | 1.0000 | 0.76% | unknown | ✅ |
| 2025-10-28 | 2025-10-29 | -1.0000 | -11.63% | unknown | ❌ |
| 2025-10-30 | 2025-11-05 | -1.0000 | 2.40% | unknown | ✅ |
| 2025-11-06 | 2025-11-12 | -1.0000 | -0.57% | unknown | ❌ |
| 2025-11-13 | 2025-11-20 | -1.0000 | 1.34% | unknown | ✅ |
| 2025-11-21 | 2025-11-24 | -1.0000 | -1.67% | unknown | ❌ |
| 2025-11-25 | 2025-11-28 | -1.0000 | -1.61% | unknown | ❌ |
| 2025-12-01 | 2025-12-03 | -1.0000 | -4.12% | unknown | ❌ |
| 2025-12-04 | 2025-12-10 | -1.0000 | -2.70% | unknown | ❌ |
| 2025-12-11 | 2025-12-12 | -1.0000 | 4.43% | unknown | ✅ |
| 2025-12-15 | 2025-12-17 | -1.0000 | 4.73% | unknown | ✅ |
| 2025-12-18 | 2026-01-02 | -1.0000 | -5.76% | unknown | ❌ |
| 2026-01-05 | 2026-01-12 | -1.0000 | -2.22% | unknown | ❌ |
| 2026-01-13 | 2026-01-16 | -1.0000 | -1.63% | unknown | ❌ |
| 2026-01-20 | 2026-01-29 | -1.0000 | -5.76% | unknown | ❌ |
| 2026-01-30 | 2026-02-02 | -1.0000 | -5.10% | unknown | ❌ |
| 2026-02-03 | 2026-02-04 | -1.0000 | 1.57% | unknown | ✅ |
| 2026-02-05 | 2026-02-06 | -1.0000 | -7.06% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 85 | -2.08% | -177.0% | 23.5% |
| 16-30d | 13 | 7.59% | 98.7% | 92.3% |
| 31-50d | 4 | 11.41% | 45.6% | 100.0% |
| 6-15d | 62 | 1.12% | 69.7% | 48.4% |

## Win/Loss Streaks

- **Max consecutive wins:** 7
- **Max consecutive losses:** 8

## Observations & Caveats

**Sample size:** 164 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-35.2%).
**Win/loss profile:** Profit factor of 1.11 with 40.2% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (50.4%) exceeded direction accuracy (40.2%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2020 (-37.7%, 16 trades). Macro: COVID-19 Crash & Recovery, Post-COVID Stimulus Rally

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 8d, std 7d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.