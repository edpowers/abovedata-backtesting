# Strategy Analysis: corr_aware_contemp_ma_sameq_e25d × trailing_stop_5%

**Ticker:** CAT
**Entry:** `corr_aware_contemp_ma_sameq_e25d`
**Exit:** `trailing_stop_5%`
**Period:** 2020-06-25 to 2026-02-06
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
- **entry_days_before:** `25` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 56.6% |
| **Annualized Return** | 27.2% |
| **Sharpe Ratio** | 1.640 |
| **Max Drawdown** | -15.6% |
| **Total Trades** | 164 |
| **Win Rate** | 42.1% |
| **Signal Accuracy** | 48.0% |
| **Direction Accuracy** | 42.1% |
| **Skill Ratio** | 44.0% |
| **Profit Factor** | 1.22 |
| **Expectancy** | 0.0045 |
| **Tail Ratio** | 2.14 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 954.1% | 56.6% | -897.5% |
| Annualized Return | 23.7% | 27.2% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.8×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0112 | Ideal for 164 trades: 0.0061 |
| Top-1 Trade | 5.7% of gross profit | Moderate concentration |
| Top-3 Trades | 15.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 27.3% | Positive without best trade |
| Return ex-Top-3 | -12.0% | Negative without top 3 |
| Max Single Trade | 23.0% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 55 | 6.40% | 351.8% | 5.56% | 11.71 |
| no_signal | 39 | -1.17% | -45.6% | -2.15% | 5.05 |
| direction_wrong_loss | 70 | -3.33% | -232.8% | -3.59% | 5.94 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 164 | 0.45% | 73.3% | 42.1% | 42.1% | -0.18% |

**Best-performing regime:** `unknown` — 164 trades, 73.3% total return, 42.1% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 37 | -2.81% | -104.1% |
| ❌ | ✅ | 28 | 6.41% | 179.6% |
| ✅ | ❌ | 33 | -3.90% | -128.8% |
| ✅ | ✅ | 27 | 6.38% | 172.2% |

### Flip Trades (Signal Wrong → Direction Right)

**42 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.5%**
- Total return: **230.4%**
- Average alpha: **5.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 42 | 5.49% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 87 | 0.71% | 62.1% | 42.5% | 42.5% |
| high | 53 | 1.06% | 56.0% | 49.1% | 49.1% |
| no_data | 3 | -3.53% | -10.6% | 33.3% | 33.3% |
| low | 21 | -1.63% | -34.3% | 23.8% | 23.8% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 62 | 2.30% | 142.3% | 50.0% | 50.0% |
| SHORT | 102 | -0.68% | -69.0% | 37.3% | 37.3% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 21 | -39.8% | -1.89% | 23.8% | 23.8% | -60.1% |
| 2021 | 23 | 21.6% | 0.94% | 39.1% | 39.1% | -1.1% |
| 2022 | 30 | 85.3% | 2.84% | 60.0% | 60.0% | 100.7% |
| 2023 | 29 | 6.0% | 0.21% | 41.4% | 41.4% | -7.6% |
| 2024 | 20 | 35.9% | 1.80% | 50.0% | 50.0% | 10.7% |
| 2025 | 35 | -15.6% | -0.45% | 40.0% | 40.0% | -46.5% |
| 2026 | 6 | -20.2% | -3.37% | 16.7% | 16.7% | -25.3% |

### Macro Context by Year

**2020** (Losing year: -39.8%, 21 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 21.6%, 23 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 85.3%, 30 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 6.0%, 29 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 35.9%, 20 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -15.6%, 35 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -20.2%, 6 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -53.2% cumulative (trade 130 to trade 164)
**Period:** 2025-04-04 to 2026-02-05 (35 trades)
**Peak cumulative return:** 126.5% → **Trough:** 73.3%

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
| 2025-07-01 | 2025-08-07 | 1.0000 | 7.09% | unknown | ✅ |
| 2025-08-08 | 2025-08-29 | 1.0000 | 0.61% | unknown | ✅ |
| 2025-09-02 | 2025-09-24 | 1.0000 | 12.92% | unknown | ✅ |
| 2025-09-24 | 2025-09-25 | -1.0000 | 1.29% | unknown | ✅ |
| 2025-09-26 | 2025-10-02 | -1.0000 | -5.33% | unknown | ❌ |
| 2025-10-03 | 2025-10-08 | -1.0000 | -0.86% | unknown | ❌ |
| 2025-10-09 | 2025-10-14 | -1.0000 | -5.42% | unknown | ❌ |
| 2025-10-15 | 2025-10-29 | -1.0000 | -9.95% | unknown | ❌ |
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
| 1-5d | 82 | -1.96% | -161.1% | 23.2% |
| 16-30d | 16 | 9.00% | 144.0% | 81.2% |
| 31-50d | 2 | 7.35% | 14.7% | 100.0% |
| 6-15d | 64 | 1.18% | 75.6% | 54.7% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 5

## Observations & Caveats

**Sample size:** 164 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-12.0%).
**Win/loss profile:** Profit factor of 1.22 with 42.1% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (48.0%) exceeded direction accuracy (42.1%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2020 (-39.8%, 21 trades). Macro: COVID-19 Crash & Recovery, Post-COVID Stimulus Rally

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 8d, std 7d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.