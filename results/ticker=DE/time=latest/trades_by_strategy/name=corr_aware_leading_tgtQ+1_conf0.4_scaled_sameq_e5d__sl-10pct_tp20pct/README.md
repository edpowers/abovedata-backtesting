# Strategy Analysis: corr_aware_leading_tgtQ+1_conf0.4_scaled_sameq_e5d × sl-10%_tp20%

**Ticker:** DE
**Entry:** `corr_aware_leading_tgtQ+1_conf0.4_scaled_sameq_e5d`
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
- **min_confidence:** `0.4`
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
| **Total Return** | 94.0% |
| **Annualized Return** | 2.3% |
| **Sharpe Ratio** | 0.307 |
| **Max Drawdown** | -25.1% |
| **Total Trades** | 18 |
| **Win Rate** | 66.7% |
| **Signal Accuracy** | 17.6% |
| **Direction Accuracy** | 66.7% |
| **Skill Ratio** | 64.7% |
| **Profit Factor** | 3.02 |
| **Expectancy** | 0.0421 |
| **Tail Ratio** | 2.00 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.6×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0908 | Ideal for 18 trades: 0.0556 |
| Top-1 Trade | 19.1% of gross profit | Moderate concentration |
| Top-3 Trades | 54.1% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 59.4% | Positive without best trade |
| Return ex-Top-3 | 11.0% | Positive without top 3 |
| Max Single Trade | 21.7% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 11 | 9.86% | 108.5% | 9.86% | 34.64 |
| no_signal | 1 | 4.94% | 4.9% | 4.94% | 121.00 |
| direction_wrong_loss | 6 | -6.26% | -37.6% | -6.26% | 24.50 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 5 | 11.62% | 58.1% | 100.0% | 100.0% | 11.62% |
| strong_positive | 2 | 7.32% | 14.6% | 100.0% | 100.0% | 7.32% |
| weak_negative | 2 | 6.30% | 12.6% | 100.0% | 100.0% | 6.30% |
| strong_negative | 7 | 0.84% | 5.9% | 42.9% | 42.9% | 0.84% |
| weak_positive | 2 | -7.69% | -15.4% | 0.0% | 0.0% | -7.69% |

**Best-performing regime:** `regime_shift` — 5 trades, 58.1% total return, 100.0% win rate.
**Worst-performing regime:** `weak_positive` — 2 trades, -15.4% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 4 | -8.62% | -34.5% |
| ❌ | ✅ | 10 | 10.08% | 100.8% |
| ✅ | ❌ | 2 | -1.54% | -3.1% |
| ✅ | ✅ | 1 | 7.66% | 7.7% |

### Flip Trades (Signal Wrong → Direction Right)

**11 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **9.6%**
- Total return: **105.7%**
- Average alpha: **9.6%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 5 | 11.62% |
| strong_negative | 3 | 9.36% |
| strong_positive | 2 | 7.32% |
| weak_negative | 1 | 4.94% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 12 | 7.49% | 89.8% | 83.3% | 83.3% |
| high | 6 | -2.34% | -14.0% | 33.3% | 33.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 9 | 6.78% | 61.0% | 77.8% | 77.8% |
| SHORT | 9 | 1.64% | 14.8% | 55.6% | 55.6% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2019 | 1 | 0.3% | 0.33% | 100.0% | 100.0% | 0.3% |
| 2020 | 3 | 47.1% | 15.71% | 100.0% | 100.0% | 47.1% |
| 2021 | 1 | 7.7% | 7.66% | 100.0% | 100.0% | 7.7% |
| 2023 | 4 | 31.2% | 7.79% | 100.0% | 100.0% | 31.2% |
| 2024 | 3 | -1.1% | -0.36% | 33.3% | 33.3% | -1.1% |
| 2025 | 6 | -9.4% | -1.57% | 33.3% | 33.3% | -9.4% |

### Macro Context by Year

**2019** (Modestly positive: 0.3%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 47.1%, 3 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 7.7%, 1 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2023** (Strong year: 31.2%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Roughly flat: -1.1%, 3 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -9.4%, 6 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -29.7% cumulative (trade 10 to trade 17)
**Period:** 2024-05-09 to 2025-05-13 (8 trades)
**Peak cumulative return:** 100.6% → **Trough:** 70.9%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-05-09 | 2024-08-08 | -1.0000 | 14.30% | strong_positive | ✅ |
| 2024-11-14 | 2024-11-21 | -1.0000 | -10.87% | weak_positive | ❌ |
| 2024-11-22 | 2025-02-06 | -1.0000 | -4.50% | weak_positive | ❌ |
| 2025-02-06 | 2025-02-18 | 1.0000 | 7.87% | strong_negative | ✅ |
| 2025-02-19 | 2025-03-04 | 1.0000 | -9.99% | strong_negative | ❌ |
| 2025-03-05 | 2025-04-07 | 1.0000 | -9.13% | strong_negative | ❌ |
| 2025-05-08 | 2025-05-12 | -1.0000 | -1.15% | strong_negative | ❌ |
| 2025-05-13 | 2025-08-07 | -1.0000 | -1.94% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 2 | -6.01% | -12.0% | 0.0% |
| 16-30d | 1 | -9.13% | -9.1% | 0.0% |
| 31-50d | 3 | 11.73% | 35.2% | 66.7% |
| 50d+ | 6 | 4.35% | 26.1% | 83.3% |
| 6-15d | 6 | 5.95% | 35.7% | 83.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 10
- **Max consecutive losses:** 4

## Observations & Caveats

**Sample size:** ⚠️ Only 18 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (11.0%).
**Win/loss profile:** 66.7% win rate with 3.02× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (66.7%) exceeded signal accuracy (17.6%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.
**Regime dependence:** `regime_shift` (5 trades, 28% of total) contributed 58.1% — a disproportionate share. Performance may degrade if this regime becomes less common.

### Known Vulnerabilities

- **Worst year:** 2025 (-9.4%, 6 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery
- **Losing regime:** `weak_positive` — 2 trades, -15.4% total return

### ⚠️ Robustness Red Flags

- **REGIME_CONCENTRATION:** `regime_shift` regime (5 trades, 28% of total) contributes 77% of total return. Performance is fragile if this regime becomes less common or behaves differently.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 36d, std 33d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.