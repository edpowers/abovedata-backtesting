# Strategy Analysis: corr_aware_contemp_ma_min0.1_sameq_e5d × sl-5%_tp10%

**Ticker:** DE
**Entry:** `corr_aware_contemp_ma_min0.1_sameq_e5d`
**Exit:** `sl-5%_tp10%`
**Period:** 2018-08-10 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.1` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `5` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit targets a 2:1 reward/risk ratio

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 310.3% |
| **Annualized Return** | 6.5% |
| **Sharpe Ratio** | 0.428 |
| **Max Drawdown** | -36.2% |
| **Total Trades** | 56 |
| **Win Rate** | 53.6% |
| **Signal Accuracy** | 30.4% |
| **Direction Accuracy** | 53.6% |
| **Skill Ratio** | 54.3% |
| **Profit Factor** | 2.50 |
| **Expectancy** | 0.0278 |
| **Tail Ratio** | 1.96 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 701.3% | 310.3% | -391.0% |
| Annualized Return | 20.7% | 6.5% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0228 | Ideal for 56 trades: 0.0179 |
| Top-1 Trade | 6.1% of gross profit | Moderate concentration |
| Top-3 Trades | 16.2% of gross profit | Moderate concentration |
| Return ex-Top-1 | 254.1% | Positive without best trade |
| Return ex-Top-3 | 177.1% | Positive without top 3 |
| Max Single Trade | 15.9% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 25 | 8.91% | 222.8% | 9.68% | 12.48 |
| no_signal | 10 | 1.77% | 17.7% | -0.42% | 18.00 |
| direction_wrong_loss | 21 | -4.05% | -85.1% | -3.66% | 10.29 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| weak_positive | 29 | 2.72% | 79.0% | 51.7% | 51.7% | 4.74% |
| weak_negative | 8 | 6.21% | 49.7% | 75.0% | 75.0% | 3.21% |
| regime_shift | 8 | 2.84% | 22.7% | 50.0% | 50.0% | 1.40% |
| strong_negative | 3 | 1.38% | 4.1% | 33.3% | 33.3% | -2.53% |
| unknown | 8 | -0.01% | -0.1% | 50.0% | 50.0% | -0.74% |

**Best-performing regime:** `weak_positive` — 29 trades, 79.0% total return, 51.7% win rate.
**Worst-performing regime:** `unknown` — 8 trades, -0.1% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 14 | -3.77% | -52.7% |
| ❌ | ✅ | 18 | 9.60% | 172.9% |
| ✅ | ❌ | 7 | -4.62% | -32.3% |
| ✅ | ✅ | 7 | 7.14% | 50.0% |

### Flip Trades (Signal Wrong → Direction Right)

**23 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **9.1%**
- Total return: **209.3%**
- Average alpha: **9.7%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_positive | 11 | 9.65% |
| weak_negative | 6 | 9.06% |
| regime_shift | 4 | 9.06% |
| unknown | 1 | 3.83% |
| strong_negative | 1 | 8.70% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 47 | 2.50% | 117.7% | 48.9% | 48.9% |
| low | 9 | 4.20% | 37.8% | 77.8% | 77.8% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 35 | 2.83% | 99.2% | 54.3% | 54.3% |
| SHORT | 21 | 2.68% | 56.3% | 52.4% | 52.4% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 4 | 12.0% | 3.01% | 75.0% | 75.0% | 12.7% |
| 2019 | 4 | -12.1% | -3.03% | 25.0% | 25.0% | -18.6% |
| 2020 | 14 | 68.7% | 4.91% | 64.3% | 64.3% | 121.1% |
| 2021 | 1 | 8.9% | 8.93% | 100.0% | 100.0% | 11.1% |
| 2022 | 2 | 3.5% | 1.74% | 50.0% | 50.0% | 4.7% |
| 2023 | 6 | 23.5% | 3.92% | 50.0% | 50.0% | 8.2% |
| 2024 | 6 | 18.5% | 3.08% | 50.0% | 50.0% | 0.5% |
| 2025 | 17 | 19.1% | 1.13% | 41.2% | 41.2% | 9.0% |
| 2026 | 2 | 13.3% | 6.67% | 100.0% | 100.0% | 12.2% |

### Macro Context by Year

**2018** (Strong year: 12.0%, 4 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -12.1%, 4 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 68.7%, 14 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 8.9%, 1 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Modestly positive: 3.5%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 23.5%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 18.5%, 6 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 19.1%, 17 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 13.3%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -21.7% cumulative (trade 41 to trade 52)
**Period:** 2025-03-04 to 2025-09-16 (12 trades)
**Peak cumulative return:** 145.2% → **Trough:** 123.5%

**Macro context during drawdown:**
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-03-04 | 2025-03-10 | 1.0000 | 6.63% | weak_positive | ✅ |
| 2025-03-11 | 2025-04-03 | 1.0000 | -5.57% | weak_positive | ❌ |
| 2025-04-04 | 2025-04-08 | 1.0000 | -3.92% | weak_positive | ❌ |
| 2025-04-09 | 2025-04-10 | 1.0000 | -1.86% | weak_positive | ❌ |
| 2025-04-11 | 2025-04-21 | 1.0000 | -3.83% | weak_positive | ❌ |
| 2025-04-22 | 2025-05-08 | 1.0000 | 7.77% | weak_positive | ✅ |
| 2025-05-08 | 2025-05-12 | -1.0000 | -1.15% | regime_shift | ❌ |
| 2025-05-13 | 2025-05-15 | -1.0000 | -3.56% | regime_shift | ❌ |
| 2025-05-16 | 2025-08-07 | -1.0000 | 4.37% | regime_shift | ✅ |
| 2025-08-07 | 2025-08-14 | 1.0000 | -5.49% | weak_positive | ❌ |
| 2025-08-15 | 2025-09-15 | 1.0000 | -4.03% | weak_positive | ❌ |
| 2025-09-16 | 2025-10-10 | 1.0000 | -4.44% | weak_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 22 | 2.43% | 53.4% | 50.0% |
| 16-30d | 14 | 1.55% | 21.8% | 42.9% |
| 31-50d | 3 | 9.42% | 28.2% | 100.0% |
| 50d+ | 1 | 4.37% | 4.4% | 100.0% |
| 6-15d | 16 | 2.98% | 47.7% | 56.2% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 4

## Observations & Caveats

**Sample size:** 56 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Well-distributed. HHI of 0.0228 is near the theoretical minimum of 0.0179 for 56 trades.
**Win/loss profile:** 53.6% win rate with 2.50× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (53.6%) exceeded signal accuracy (30.4%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2019 (-12.1%, 4 trades). Macro: US-China Trade War Escalation, Fed Rate Cuts (2019)
- **Losing regime:** `unknown` — 8 trades, -0.1% total return

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 13d, std 12d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.