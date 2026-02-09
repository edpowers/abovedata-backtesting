# Strategy Analysis: corr_aware_leading_tgtQ+1_conf0.3_scaled_sameq_e5d × sl-10%_tp20%

**Ticker:** DE
**Entry:** `corr_aware_leading_tgtQ+1_conf0.3_scaled_sameq_e5d`
**Exit:** `sl-10%_tp20%`
**Period:** 2019-11-20 to 2026-01-30
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `leading` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **min_confidence:** `0.3`
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `True` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `5` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `True`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 126.0% |
| **Annualized Return** | 2.5% |
| **Sharpe Ratio** | 0.309 |
| **Max Drawdown** | -23.0% |
| **Total Trades** | 18 |
| **Win Rate** | 72.2% |
| **Signal Accuracy** | 17.6% |
| **Direction Accuracy** | 72.2% |
| **Skill Ratio** | 70.6% |
| **Profit Factor** | 4.38 |
| **Expectancy** | 0.0507 |
| **Tail Ratio** | 1.67 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.8×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0993 | Ideal for 18 trades: 0.0556 |
| Top-1 Trade | 18.4% of gross profit | Moderate concentration |
| Top-3 Trades | 52.0% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 85.7% | Positive without best trade |
| Return ex-Top-3 | 29.3% | Positive without top 3 |
| Max Single Trade | 21.7% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 12 | 9.44% | 113.2% | 9.44% | 33.25 |
| no_signal | 1 | 4.94% | 4.9% | 4.94% | 121.00 |
| direction_wrong_loss | 5 | -5.40% | -27.0% | -5.40% | 55.40 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 6 | 9.96% | 59.8% | 100.0% | 100.0% | 9.96% |
| strong_negative | 7 | 4.20% | 29.4% | 57.1% | 57.1% | 4.20% |
| weak_negative | 2 | 6.30% | 12.6% | 100.0% | 100.0% | 6.30% |
| weak_positive | 1 | -0.88% | -0.9% | 0.0% | 0.0% | -0.88% |
| strong_positive | 2 | -4.84% | -9.7% | 50.0% | 50.0% | -4.84% |

**Best-performing regime:** `regime_shift` — 6 trades, 59.8% total return, 100.0% win rate.
**Worst-performing regime:** `strong_positive` — 2 trades, -9.7% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 3 | -7.96% | -23.9% |
| ❌ | ✅ | 11 | 9.60% | 105.6% |
| ✅ | ❌ | 2 | -1.54% | -3.1% |
| ✅ | ✅ | 1 | 7.66% | 7.7% |

### Flip Trades (Signal Wrong → Direction Right)

**12 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **9.2%**
- Total return: **110.5%**
- Average alpha: **9.2%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 6 | 9.96% |
| strong_negative | 4 | 11.37% |
| weak_negative | 1 | 4.94% |
| strong_positive | 1 | 0.33% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 12 | 6.81% | 81.7% | 83.3% | 83.3% |
| high | 6 | 1.59% | 9.5% | 50.0% | 50.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 10 | 8.62% | 86.2% | 90.0% | 90.0% |
| SHORT | 8 | 0.62% | 5.0% | 50.0% | 50.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2019 | 1 | 0.3% | 0.33% | 100.0% | 100.0% | 0.3% |
| 2020 | 3 | 47.1% | 15.71% | 100.0% | 100.0% | 47.1% |
| 2021 | 1 | 7.7% | 7.66% | 100.0% | 100.0% | 7.7% |
| 2023 | 5 | 32.8% | 6.57% | 100.0% | 100.0% | 32.8% |
| 2024 | 2 | -10.9% | -5.45% | 0.0% | 0.0% | -10.9% |
| 2025 | 6 | 14.1% | 2.35% | 50.0% | 50.0% | 14.1% |

### Macro Context by Year

**2019** (Modestly positive: 0.3%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 47.1%, 3 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 7.7%, 1 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2023** (Strong year: 32.8%, 5 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -10.9%, 2 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 14.1%, 6 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -14.4% cumulative (trade 10 to trade 14)
**Period:** 2023-11-15 to 2025-02-20 (5 trades)
**Peak cumulative return:** 88.0% → **Trough:** 73.6%

**Macro context during drawdown:**
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-11-15 | 2024-02-08 | 1.0000 | 1.67% | regime_shift | ✅ |
| 2024-05-09 | 2024-11-22 | -1.0000 | -10.02% | strong_positive | ❌ |
| 2024-11-25 | 2025-02-06 | -1.0000 | -0.88% | weak_positive | ❌ |
| 2025-02-06 | 2025-02-19 | 1.0000 | 9.53% | strong_negative | ✅ |
| 2025-02-20 | 2025-04-04 | 1.0000 | -13.00% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 1 | -1.15% | -1.1% | 0.0% |
| 16-30d | 1 | 15.74% | 15.7% | 100.0% |
| 31-50d | 4 | 6.45% | 25.8% | 50.0% |
| 50d+ | 7 | 0.49% | 3.4% | 71.4% |
| 6-15d | 5 | 9.47% | 47.3% | 100.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 10
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 18 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (29.3%).
**Win/loss profile:** 72.2% win rate with 4.38× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (72.2%) exceeded signal accuracy (17.6%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2024 (-10.9%, 2 trades). Macro: 2024 Election Year Uncertainty
- **Losing regime:** `weak_positive` — 1 trades, -0.9% total return
- **Losing regime:** `strong_positive` — 2 trades, -9.7% total return

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 44d, std 38d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.