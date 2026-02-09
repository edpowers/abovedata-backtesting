# Strategy Analysis: corr_aware_leading_tgtQ+1_conf0.3_sameq_e5d × sl-10%_tp20%

**Ticker:** DE
**Entry:** `corr_aware_leading_tgtQ+1_conf0.3_sameq_e5d`
**Exit:** `sl-10%_tp20%`
**Period:** 2019-11-20 to 2025-11-19
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
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `leading` — Which confidence metric to use for scaling
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
| **Total Return** | 184.2% |
| **Annualized Return** | 8.1% |
| **Sharpe Ratio** | 0.567 |
| **Max Drawdown** | -25.1% |
| **Total Trades** | 21 |
| **Win Rate** | 71.4% |
| **Signal Accuracy** | 30.0% |
| **Direction Accuracy** | 71.4% |
| **Skill Ratio** | 75.0% |
| **Profit Factor** | 4.03 |
| **Expectancy** | 0.0559 |
| **Tail Ratio** | 1.99 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.6×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0741 | Ideal for 21 trades: 0.0476 |
| Top-1 Trade | 13.9% of gross profit | Moderate concentration |
| Top-3 Trades | 39.4% of gross profit | Moderate concentration |
| Return ex-Top-1 | 133.5% | Positive without best trade |
| Return ex-Top-3 | 62.6% | Positive without top 3 |
| Max Single Trade | 21.7% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 15 | 10.40% | 156.0% | 10.40% | 38.73 |
| no_signal | 1 | -5.96% | -6.0% | -5.96% | 73.00 |
| direction_wrong_loss | 5 | -6.54% | -32.7% | -6.54% | 25.20 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 7 | 9.80% | 68.6% | 100.0% | 100.0% | 9.80% |
| strong_negative | 8 | 3.59% | 28.8% | 50.0% | 50.0% | 3.59% |
| strong_positive | 4 | 4.57% | 18.3% | 75.0% | 75.0% | 4.57% |
| weak_negative | 2 | 0.85% | 1.7% | 50.0% | 50.0% | 0.85% |

**Best-performing regime:** `regime_shift` — 7 trades, 68.6% total return, 100.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 2 | -9.86% | -19.7% |
| ❌ | ✅ | 12 | 10.04% | 120.5% |
| ✅ | ❌ | 3 | -4.33% | -13.0% |
| ✅ | ✅ | 3 | 11.85% | 35.5% |

### Flip Trades (Signal Wrong → Direction Right)

**12 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **10.0%**
- Total return: **120.5%**
- Average alpha: **10.0%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 7 | 9.80% |
| strong_negative | 4 | 12.89% |
| strong_positive | 1 | 0.33% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 12 | 6.94% | 83.3% | 83.3% | 83.3% |
| high | 9 | 3.78% | 34.0% | 55.6% | 55.6% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 14 | 6.62% | 92.7% | 71.4% | 71.4% |
| SHORT | 7 | 3.53% | 24.7% | 71.4% | 71.4% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2019 | 1 | 0.3% | 0.33% | 100.0% | 100.0% | 0.3% |
| 2020 | 3 | 47.1% | 15.71% | 100.0% | 100.0% | 47.1% |
| 2021 | 3 | 9.3% | 3.10% | 66.7% | 66.7% | 9.3% |
| 2022 | 3 | 18.0% | 5.99% | 66.7% | 66.7% | 18.0% |
| 2023 | 5 | 32.8% | 6.57% | 100.0% | 100.0% | 32.8% |
| 2024 | 1 | 8.8% | 8.82% | 100.0% | 100.0% | 8.8% |
| 2025 | 5 | 1.0% | 0.19% | 20.0% | 20.0% | 1.0% |

### Macro Context by Year

**2019** (Modestly positive: 0.3%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 47.1%, 3 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 9.3%, 3 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 18.0%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 32.8%, 5 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 8.8%, 1 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 1.0%, 5 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -11.1% cumulative (trade 4 to trade 5)
**Period:** 2020-08-06 to 2021-05-14 (2 trades)
**Peak cumulative return:** 47.5% → **Trough:** 36.4%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-08-06 | 2020-08-14 | 1.0000 | 5.45% | regime_shift | ✅ |
| 2021-05-14 | 2021-06-10 | 1.0000 | -11.08% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 1 | -1.15% | -1.1% | 0.0% |
| 16-30d | 2 | 3.78% | 7.6% | 50.0% |
| 31-50d | 4 | 10.94% | 43.8% | 75.0% |
| 50d+ | 7 | 1.62% | 11.4% | 71.4% |
| 6-15d | 7 | 7.97% | 55.8% | 85.7% |

## Win/Loss Streaks

- **Max consecutive wins:** 8
- **Max consecutive losses:** 3

## Observations & Caveats

**Sample size:** ⚠️ Only 21 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (62.6%).
**Win/loss profile:** 71.4% win rate with 4.03× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (71.4%) exceeded signal accuracy (30.0%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities


### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 37d, std 31d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.