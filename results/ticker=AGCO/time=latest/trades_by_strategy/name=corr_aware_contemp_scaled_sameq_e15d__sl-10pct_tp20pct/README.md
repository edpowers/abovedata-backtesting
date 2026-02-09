# Strategy Analysis: corr_aware_contemp_scaled_sameq_e15d × sl-10%_tp20%

**Ticker:** AGCO
**Entry:** `corr_aware_contemp_scaled_sameq_e15d`
**Exit:** `sl-10%_tp20%`
**Period:** 2020-07-09 to 2026-02-06
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
- **scale_by_confidence:** `True` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `False`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 609.7% |
| **Annualized Return** | 7.5% |
| **Sharpe Ratio** | 0.658 |
| **Max Drawdown** | -17.5% |
| **Total Trades** | 33 |
| **Win Rate** | 69.7% |
| **Signal Accuracy** | 40.7% |
| **Direction Accuracy** | 71.9% |
| **Skill Ratio** | 74.1% |
| **Profit Factor** | 3.43 |
| **Expectancy** | 0.0688 |
| **Tail Ratio** | 2.23 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 196.0% | 609.7% | 413.6% |
| Annualized Return | 21.5% | 7.5% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0398 | Ideal for 33 trades: 0.0303 |
| Top-1 Trade | 8.5% of gross profit | Moderate concentration |
| Top-3 Trades | 24.1% of gross profit | Moderate concentration |
| Return ex-Top-1 | 458.2% | Positive without best trade |
| Return ex-Top-3 | 257.3% | Positive without top 3 |
| Max Single Trade | 27.1% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 20 | 14.26% | 285.1% | 14.26% | 35.30 |
| no_signal | 6 | 2.78% | 16.7% | 2.78% | 34.17 |
| direction_wrong_loss | 7 | -10.67% | -74.7% | -10.67% | 18.86 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_negative | 14 | 6.07% | 85.0% | 71.4% | 71.4% | 6.07% |
| regime_shift | 8 | 8.02% | 64.1% | 75.0% | 75.0% | 8.02% |
| strong_positive | 5 | 9.68% | 48.4% | 60.0% | 60.0% | 9.68% |
| weak_negative | 3 | 6.30% | 18.9% | 66.7% | 66.7% | 6.30% |
| weak_positive | 3 | 3.55% | 10.6% | 66.7% | 66.7% | 3.55% |

**Best-performing regime:** `strong_negative` — 14 trades, 85.0% total return, 71.4% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 4 | -10.41% | -41.6% |
| ❌ | ✅ | 12 | 12.70% | 152.4% |
| ✅ | ❌ | 3 | -11.01% | -33.0% |
| ✅ | ✅ | 8 | 16.59% | 132.7% |

### Flip Trades (Signal Wrong → Direction Right)

**15 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **12.5%**
- Total return: **188.0%**
- Average alpha: **12.5%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| strong_negative | 7 | 11.64% |
| regime_shift | 6 | 14.20% |
| weak_positive | 2 | 10.66% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 23 | 9.23% | 212.3% | 78.3% | 78.3% |
| high | 10 | 1.48% | 14.8% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 24 | 7.33% | 175.9% | 70.8% | 70.8% |
| SHORT | 9 | 5.69% | 51.2% | 66.7% | 66.7% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 4 | 81.7% | 20.44% | 100.0% | 100.0% | 81.7% |
| 2021 | 5 | 23.6% | 4.71% | 60.0% | 60.0% | 23.6% |
| 2022 | 7 | 69.9% | 9.99% | 85.7% | 85.7% | 69.9% |
| 2023 | 6 | 19.7% | 3.28% | 66.7% | 66.7% | 19.7% |
| 2024 | 3 | 35.3% | 11.75% | 100.0% | 100.0% | 35.3% |
| 2025 | 6 | 6.7% | 1.11% | 50.0% | 50.0% | 6.7% |
| 2026 | 2 | -9.7% | -4.86% | 0.0% | 0.0% | -9.7% |

### Macro Context by Year

**2020** (Strong year: 81.7%, 4 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 23.6%, 5 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 69.9%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 19.7%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 35.3%, 3 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 6.7%, 6 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -9.7%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -19.7% cumulative (trade 25 to trade 27)
**Period:** 2024-07-09 to 2025-02-14 (3 trades)
**Peak cumulative return:** 230.2% → **Trough:** 210.4%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-07-09 | 2025-01-23 | 1.0000 | 13.08% | strong_negative | ✅ |
| 2025-01-24 | 2025-02-13 | 1.0000 | -10.33% | strong_negative | ❌ |
| 2025-02-14 | 2025-03-04 | 1.0000 | -9.41% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 3 | 3.23% | 9.7% | 66.7% |
| 16-30d | 8 | 5.46% | 43.6% | 62.5% |
| 31-50d | 10 | 13.37% | 133.7% | 90.0% |
| 50d+ | 4 | 10.38% | 41.5% | 75.0% |
| 6-15d | 8 | -0.19% | -1.5% | 50.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** 33 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Well-distributed. HHI of 0.0398 is near the theoretical minimum of 0.0303 for 33 trades.
**Win/loss profile:** 69.7% win rate with 3.43× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (71.9%) exceeded signal accuracy (40.7%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2026 (-9.7%, 2 trades). Macro: No flagged events

### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 196.0% buy-and-hold return (aligned to strategy period: None to None), yet 9 short trades returned 51.2% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 32d, std 27d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.