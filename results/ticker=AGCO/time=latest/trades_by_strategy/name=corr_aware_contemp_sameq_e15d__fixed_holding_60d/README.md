# Strategy Analysis: corr_aware_contemp_sameq_e15d × fixed_holding_60d

**Ticker:** AGCO
**Entry:** `corr_aware_contemp_sameq_e15d`
**Exit:** `fixed_holding_60d`
**Period:** 2018-07-10 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **min_confidence:** `0.0`
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `False`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `fixed_holding_60d`
  - Fixed 60-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 766.4% |
| **Annualized Return** | 17.4% |
| **Sharpe Ratio** | 0.561 |
| **Max Drawdown** | -40.9% |
| **Total Trades** | 32 |
| **Win Rate** | 75.0% |
| **Signal Accuracy** | 53.6% |
| **Direction Accuracy** | 75.0% |
| **Skill Ratio** | 78.6% |
| **Profit Factor** | 4.91 |
| **Expectancy** | 0.0812 |
| **Tail Ratio** | 2.92 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 157.5% | 766.4% | 609.0% |
| Annualized Return | 13.3% | 17.4% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0708 | Ideal for 32 trades: 0.0312 |
| Top-1 Trade | 21.4% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 42.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 410.1% | Positive without best trade |
| Return ex-Top-3 | 181.0% | Positive without top 3 |
| Max Single Trade | 69.8% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 22 | 14.52% | 319.5% | 14.52% | 67.41 |
| no_signal | 4 | -2.78% | -11.1% | -2.78% | 32.50 |
| direction_wrong_loss | 6 | -8.10% | -48.6% | -8.10% | 45.33 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 7 | 12.22% | 85.5% | 85.7% | 85.7% | 12.22% |
| strong_positive | 10 | 8.15% | 81.5% | 50.0% | 50.0% | 8.15% |
| strong_negative | 6 | 10.98% | 65.9% | 100.0% | 100.0% | 10.98% |
| weak_positive | 3 | 7.05% | 21.1% | 100.0% | 100.0% | 7.05% |
| weak_negative | 4 | 0.79% | 3.2% | 75.0% | 75.0% | 0.79% |
| unknown | 2 | 1.29% | 2.6% | 50.0% | 50.0% | 1.29% |

**Best-performing regime:** `regime_shift` — 7 trades, 85.5% total return, 85.7% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 4 | -7.07% | -28.3% |
| ❌ | ✅ | 9 | 13.83% | 124.5% |
| ✅ | ❌ | 2 | -10.16% | -20.3% |
| ✅ | ✅ | 13 | 15.00% | 195.0% |

### Flip Trades (Signal Wrong → Direction Right)

**11 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **11.9%**
- Total return: **131.1%**
- Average alpha: **11.9%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 4 | 17.75% |
| weak_negative | 3 | 4.71% |
| weak_positive | 2 | 6.39% |
| strong_negative | 2 | 16.62% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 18 | 12.64% | 227.4% | 77.8% | 77.8% |
| low | 8 | 3.91% | 31.3% | 75.0% | 75.0% |
| high | 6 | 0.17% | 1.0% | 66.7% | 66.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 17 | 11.60% | 197.3% | 82.4% | 82.4% |
| SHORT | 15 | 4.17% | 62.5% | 66.7% | 66.7% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 2 | 2.6% | 1.29% | 50.0% | 50.0% | 2.6% |
| 2019 | 6 | 9.4% | 1.57% | 66.7% | 66.7% | 9.4% |
| 2020 | 4 | 139.2% | 34.79% | 75.0% | 75.0% | 139.2% |
| 2021 | 3 | 10.3% | 3.44% | 66.7% | 66.7% | 10.3% |
| 2022 | 4 | 58.8% | 14.69% | 100.0% | 100.0% | 58.8% |
| 2023 | 5 | 12.7% | 2.53% | 80.0% | 80.0% | 12.7% |
| 2024 | 3 | 33.2% | 11.06% | 100.0% | 100.0% | 33.2% |
| 2025 | 3 | 11.5% | 3.83% | 100.0% | 100.0% | 11.5% |
| 2026 | 2 | -17.8% | -8.89% | 0.0% | 0.0% | -17.8% |

### Macro Context by Year

**2018** (Modestly positive: 2.6%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 9.4%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 139.2%, 4 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 10.3%, 3 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 58.8%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 12.7%, 5 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 33.2%, 3 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 11.5%, 3 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -17.8%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -17.8% cumulative (trade 30 to trade 32)
**Period:** 2025-10-27 to 2026-01-30 (3 trades)
**Peak cumulative return:** 277.6% → **Trough:** 259.8%

**Macro context during drawdown:**
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-10-27 | 2026-01-08 | 1.0000 | 4.48% | regime_shift | ✅ |
| 2026-01-08 | 2026-01-29 | -1.0000 | -0.89% | strong_positive | ❌ |
| 2026-01-30 | 2026-02-06 | -1.0000 | -16.89% | strong_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 2 | -4.49% | -9.0% | 50.0% |
| 31-50d | 3 | 1.43% | 4.3% | 66.7% |
| 50d+ | 21 | 12.27% | 257.8% | 85.7% |
| 6-15d | 6 | 1.12% | 6.7% | 50.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 8
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** 32 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (181.0%).
**Win/loss profile:** 75.0% win rate with 4.91× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (75.0%) exceeded signal accuracy (53.6%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2026 (-17.8%, 2 trades). Macro: No flagged events

### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 157.5% buy-and-hold return (aligned to strategy period: None to None), yet 15 short trades returned 62.5% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.