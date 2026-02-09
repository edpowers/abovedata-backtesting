# Strategy Analysis: corr_aware_leading_ma_e1d × trailing_stop_5%

**Ticker:** TTC
**Entry:** `corr_aware_leading_ma_e1d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-08-22 to 2026-02-09
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `leading_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `leading` — Which confidence metric to use for scaling
- **entry_days_before:** `1` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 86.3% |
| **Annualized Return** | 28.4% |
| **Sharpe Ratio** | 1.576 |
| **Max Drawdown** | -15.1% |
| **Total Trades** | 181 |
| **Win Rate** | 42.5% |
| **Signal Accuracy** | 45.6% |
| **Direction Accuracy** | 42.5% |
| **Skill Ratio** | 41.9% |
| **Profit Factor** | 1.28 |
| **Expectancy** | 0.0049 |
| **Tail Ratio** | 1.99 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 259.6% | 86.3% | -173.3% |
| Annualized Return | 12.2% | 28.4% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.0×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0110 | Ideal for 181 trades: 0.0055 |
| Top-1 Trade | 6.5% of gross profit | Moderate concentration |
| Top-3 Trades | 16.2% of gross profit | Moderate concentration |
| Return ex-Top-1 | 47.5% | Positive without best trade |
| Return ex-Top-3 | 3.1% | Positive without top 3 |
| Max Single Trade | 26.3% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 67 | 5.15% | 344.8% | 3.48% | 13.40 |
| no_signal | 21 | 1.30% | 27.2% | 0.60% | 9.67 |
| direction_wrong_loss | 93 | -3.04% | -282.6% | -3.18% | 5.84 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 156 | 0.41% | 63.7% | 42.9% | 42.9% | -0.25% |
| regime_shift | 12 | 1.26% | 15.1% | 50.0% | 50.0% | -0.33% |
| weak_negative | 13 | 0.82% | 10.7% | 30.8% | 30.8% | -0.51% |

**Best-performing regime:** `unknown` — 156 trades, 63.7% total return, 42.9% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 46 | -3.29% | -151.4% |
| ❌ | ✅ | 41 | 5.05% | 207.0% |
| ✅ | ❌ | 47 | -2.79% | -131.1% |
| ✅ | ✅ | 26 | 5.30% | 137.7% |

### Flip Trades (Signal Wrong → Direction Right)

**51 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.3%**
- Total return: **267.9%**
- Average alpha: **3.3%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 46 | 5.27% |
| regime_shift | 3 | 3.90% |
| weak_negative | 2 | 6.81% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 65 | 0.69% | 44.6% | 36.9% | 36.9% |
| no_data | 112 | 0.33% | 36.6% | 44.6% | 44.6% |
| medium | 4 | 2.06% | 8.2% | 75.0% | 75.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 90 | 1.12% | 101.1% | 43.3% | 43.3% |
| SHORT | 91 | -0.13% | -11.7% | 41.8% | 41.8% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 9 | 13.0% | 1.45% | 33.3% | 33.3% | 7.0% |
| 2019 | 13 | 7.6% | 0.58% | 38.5% | 38.5% | -10.2% |
| 2020 | 31 | 20.8% | 0.67% | 41.9% | 41.9% | -10.6% |
| 2021 | 18 | 12.7% | 0.71% | 55.6% | 55.6% | -6.1% |
| 2022 | 30 | 33.2% | 1.11% | 36.7% | 36.7% | 34.8% |
| 2023 | 25 | -12.8% | -0.51% | 40.0% | 40.0% | -36.4% |
| 2024 | 25 | -27.2% | -1.09% | 44.0% | 44.0% | -48.6% |
| 2025 | 28 | 31.8% | 1.13% | 42.9% | 42.9% | 8.9% |
| 2026 | 2 | 10.4% | 5.20% | 100.0% | 100.0% | 10.9% |

### Macro Context by Year

**2018** (Strong year: 13.0%, 9 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 7.6%, 13 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 20.8%, 31 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 12.7%, 18 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 33.2%, 30 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Losing year: -12.8%, 25 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -27.2%, 25 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 31.8%, 28 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 10.4%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -55.4% cumulative (trade 98 to trade 160)
**Period:** 2022-11-03 to 2025-04-04 (63 trades)
**Peak cumulative return:** 93.7% → **Trough:** 38.4%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-11-03 | 2022-12-20 | 1.0000 | 7.48% | unknown | ✅ |
| 2022-12-20 | 2022-12-21 | -1.0000 | -0.76% | unknown | ❌ |
| 2022-12-22 | 2022-12-27 | -1.0000 | -3.51% | unknown | ❌ |
| 2022-12-28 | 2023-01-12 | -1.0000 | -2.18% | unknown | ❌ |
| 2023-01-13 | 2023-02-01 | -1.0000 | 3.37% | unknown | ✅ |
| 2023-02-02 | 2023-02-17 | -1.0000 | -0.37% | unknown | ❌ |
| 2023-02-21 | 2023-03-09 | -1.0000 | -4.22% | unknown | ❌ |
| 2023-03-10 | 2023-03-21 | -1.0000 | -1.13% | unknown | ❌ |
| 2023-03-22 | 2023-04-03 | -1.0000 | -0.86% | unknown | ❌ |
| 2023-04-04 | 2023-04-14 | -1.0000 | 0.30% | unknown | ✅ |
| 2023-04-17 | 2023-05-03 | -1.0000 | 0.52% | unknown | ✅ |
| 2023-05-04 | 2023-05-19 | -1.0000 | -1.93% | unknown | ❌ |
| 2023-05-22 | 2023-05-30 | -1.0000 | 4.29% | unknown | ✅ |
| 2023-05-31 | 2023-06-02 | -1.0000 | -4.30% | unknown | ❌ |
| 2023-06-05 | 2023-06-07 | -1.0000 | -3.61% | unknown | ❌ |
| 2023-06-08 | 2023-06-09 | 1.0000 | -0.30% | unknown | ❌ |
| 2023-06-12 | 2023-07-26 | 1.0000 | 4.64% | unknown | ✅ |
| 2023-07-27 | 2023-08-17 | 1.0000 | -2.14% | unknown | ❌ |
| 2023-08-18 | 2023-09-06 | 1.0000 | 1.48% | unknown | ✅ |
| 2023-09-07 | 2023-09-08 | -1.0000 | 5.43% | unknown | ✅ |
| 2023-09-11 | 2023-09-27 | -1.0000 | -0.48% | unknown | ❌ |
| 2023-09-28 | 2023-10-06 | -1.0000 | -1.84% | unknown | ❌ |
| 2023-10-09 | 2023-10-17 | -1.0000 | -2.93% | unknown | ❌ |
| 2023-10-18 | 2023-11-02 | -1.0000 | 0.90% | unknown | ✅ |
| 2023-11-03 | 2023-11-14 | -1.0000 | -0.51% | unknown | ❌ |
| 2023-11-15 | 2023-12-04 | -1.0000 | 0.70% | unknown | ✅ |
| 2023-12-05 | 2023-12-13 | -1.0000 | -4.32% | unknown | ❌ |
| 2023-12-14 | 2023-12-20 | -1.0000 | -10.17% | unknown | ❌ |
| 2023-12-21 | 2024-01-22 | -1.0000 | 4.70% | unknown | ✅ |
| 2024-01-23 | 2024-02-08 | -1.0000 | -3.40% | unknown | ❌ |
| 2024-02-09 | 2024-03-06 | -1.0000 | 3.29% | unknown | ✅ |
| 2024-03-06 | 2024-03-07 | 1.0000 | -5.54% | unknown | ❌ |
| 2024-03-08 | 2024-04-02 | 1.0000 | -2.30% | unknown | ❌ |
| 2024-04-03 | 2024-04-17 | 1.0000 | -3.15% | unknown | ❌ |
| 2024-04-18 | 2024-05-21 | 1.0000 | 2.04% | unknown | ✅ |
| 2024-05-22 | 2024-05-23 | 1.0000 | -3.65% | unknown | ❌ |
| 2024-05-24 | 2024-05-28 | 1.0000 | -4.61% | unknown | ❌ |
| 2024-05-29 | 2024-06-05 | 1.0000 | 1.07% | unknown | ✅ |
| 2024-06-05 | 2024-06-06 | -1.0000 | -14.40% | unknown | ❌ |
| 2024-06-07 | 2024-06-10 | -1.0000 | -0.55% | unknown | ❌ |
| 2024-06-11 | 2024-06-14 | -1.0000 | -1.24% | unknown | ❌ |
| 2024-06-17 | 2024-06-28 | -1.0000 | 2.80% | unknown | ✅ |
| 2024-07-01 | 2024-07-11 | -1.0000 | 0.18% | unknown | ✅ |
| 2024-07-12 | 2024-07-16 | -1.0000 | -6.53% | unknown | ❌ |
| 2024-07-17 | 2024-08-05 | -1.0000 | 8.26% | unknown | ✅ |
| 2024-08-06 | 2024-08-22 | -1.0000 | 0.10% | unknown | ✅ |
| 2024-08-23 | 2024-09-05 | -1.0000 | 10.04% | unknown | ✅ |
| 2024-09-06 | 2024-09-17 | -1.0000 | -5.27% | unknown | ❌ |
| 2024-09-18 | 2024-11-06 | -1.0000 | 0.21% | unknown | ✅ |
| 2024-11-07 | 2024-11-22 | -1.0000 | 1.52% | unknown | ✅ |
| 2024-11-25 | 2024-12-11 | -1.0000 | -1.35% | unknown | ❌ |
| 2024-12-12 | 2024-12-17 | -1.0000 | 2.76% | unknown | ✅ |
| 2024-12-17 | 2024-12-18 | 1.0000 | -4.54% | unknown | ❌ |
| 2024-12-19 | 2025-01-07 | 1.0000 | -2.91% | unknown | ❌ |
| 2025-01-08 | 2025-01-31 | 1.0000 | 5.07% | unknown | ✅ |
| 2025-02-03 | 2025-02-12 | 1.0000 | -1.75% | unknown | ❌ |
| 2025-02-13 | 2025-02-28 | 1.0000 | 0.05% | unknown | ✅ |
| 2025-03-03 | 2025-03-04 | 1.0000 | -2.60% | unknown | ❌ |
| 2025-03-05 | 2025-03-06 | 1.0000 | -4.90% | unknown | ❌ |
| 2025-03-07 | 2025-03-10 | 1.0000 | 5.45% | unknown | ✅ |
| 2025-03-11 | 2025-03-12 | 1.0000 | -2.86% | unknown | ❌ |
| 2025-03-13 | 2025-04-03 | 1.0000 | -5.27% | unknown | ❌ |
| 2025-04-04 | 2025-04-07 | 1.0000 | -2.13% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 79 | -1.39% | -109.5% | 30.4% |
| 16-30d | 19 | 5.24% | 99.6% | 78.9% |
| 31-50d | 7 | 11.36% | 79.5% | 85.7% |
| 50d+ | 1 | 3.60% | 3.6% | 100.0% |
| 6-15d | 75 | 0.22% | 16.3% | 41.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 7

## Observations & Caveats

**Sample size:** 181 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (3.1%).
**Win/loss profile:** Profit factor of 1.28 with 42.5% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (45.6%) exceeded direction accuracy (42.5%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2024 (-27.2%, 25 trades). Macro: 2024 Election Year Uncertainty

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 9d, std 10d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.