# Strategy Analysis: corr_aware_contemp_e30d × trailing_stop_5%

**Ticker:** DE
**Entry:** `corr_aware_contemp_e30d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-07-06 to 2026-01-14
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
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates
- **target_next_quarter:** `False`
- **date_col:** `earnings_date`

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 125.4% |
| **Annualized Return** | 18.1% |
| **Sharpe Ratio** | 1.449 |
| **Max Drawdown** | -12.8% |
| **Total Trades** | 93 |
| **Win Rate** | 50.5% |
| **Signal Accuracy** | 37.0% |
| **Direction Accuracy** | 50.5% |
| **Skill Ratio** | 49.4% |
| **Profit Factor** | 1.72 |
| **Expectancy** | 0.0105 |
| **Tail Ratio** | 2.77 |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 2.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0265 | Ideal for 93 trades: 0.0108 |
| Top-1 Trade | 14.1% of gross profit | Moderate concentration |
| Top-3 Trades | 33.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 69.7% | Positive without best trade |
| Return ex-Top-3 | 12.3% | Positive without top 3 |
| Max Single Trade | 32.8% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 40 | 5.41% | 216.4% | 5.41% | 9.75 |
| no_signal | 12 | -0.67% | -8.1% | -0.67% | 6.00 |
| direction_wrong_loss | 41 | -2.70% | -110.9% | -2.70% | 6.02 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| weak_positive | 9 | 4.59% | 41.3% | 77.8% | 77.8% | 4.59% |
| weak_negative | 30 | 0.97% | 29.1% | 46.7% | 46.7% | 0.97% |
| unknown | 9 | 2.71% | 24.4% | 77.8% | 77.8% | 2.71% |
| strong_positive | 18 | 1.17% | 21.1% | 50.0% | 50.0% | 1.17% |
| strong_negative | 9 | -0.19% | -1.7% | 44.4% | 44.4% | -0.19% |
| regime_shift | 18 | -0.93% | -16.8% | 33.3% | 33.3% | -0.93% |

**Best-performing regime:** `weak_positive` — 9 trades, 41.3% total return, 77.8% win rate.
**Worst-performing regime:** `regime_shift` — 18 trades, -16.8% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 31 | -2.60% | -80.6% |
| ❌ | ✅ | 20 | 6.14% | 122.8% |
| ✅ | ❌ | 10 | -3.03% | -30.3% |
| ✅ | ✅ | 20 | 4.68% | 93.7% |

### Flip Trades (Signal Wrong → Direction Right)

**27 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.2%**
- Total return: **139.4%**
- Average alpha: **5.2%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 10 | 5.52% |
| strong_positive | 6 | 7.37% |
| strong_negative | 4 | 3.12% |
| regime_shift | 3 | 2.80% |
| weak_positive | 2 | 2.67% |
| unknown | 2 | 6.87% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 36 | 2.04% | 73.5% | 52.8% | 52.8% |
| medium | 48 | 0.41% | 19.6% | 47.9% | 47.9% |
| high | 9 | 0.49% | 4.4% | 55.6% | 55.6% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 66 | 1.23% | 81.3% | 51.5% | 51.5% |
| SHORT | 27 | 0.60% | 16.2% | 48.1% | 48.1% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 6 | 15.2% | 2.54% | 66.7% | 66.7% | 15.2% |
| 2019 | 12 | 31.4% | 2.62% | 58.3% | 58.3% | 31.4% |
| 2020 | 12 | 33.3% | 2.77% | 41.7% | 41.7% | 33.3% |
| 2021 | 12 | -6.5% | -0.54% | 50.0% | 50.0% | -6.5% |
| 2022 | 12 | 27.1% | 2.26% | 50.0% | 50.0% | 27.1% |
| 2023 | 12 | -1.9% | -0.16% | 41.7% | 41.7% | -1.9% |
| 2024 | 13 | -5.9% | -0.45% | 38.5% | 38.5% | -5.9% |
| 2025 | 12 | 15.1% | 1.26% | 75.0% | 75.0% | 15.1% |
| 2026 | 2 | -10.3% | -5.15% | 0.0% | 0.0% | -10.3% |

### Macro Context by Year

**2018** (Strong year: 15.2%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 31.4%, 12 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 33.3%, 12 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -6.5%, 12 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 27.1%, 12 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Roughly flat: -1.9%, 12 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -5.9%, 13 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 15.1%, 12 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -10.3%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -25.0% cumulative (trade 61 to trade 73)
**Period:** 2023-07-07 to 2024-07-03 (13 trades)
**Peak cumulative return:** 108.5% → **Trough:** 83.5%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2023-07-07 | 2023-07-27 | 1.0000 | 5.76% | strong_negative | ✅ |
| 2023-07-28 | 2023-08-17 | 1.0000 | -1.86% | strong_negative | ❌ |
| 2023-08-18 | 2023-08-21 | 1.0000 | -1.57% | strong_negative | ❌ |
| 2023-10-11 | 2023-10-20 | 1.0000 | -3.65% | strong_negative | ❌ |
| 2023-10-23 | 2023-10-27 | 1.0000 | -3.25% | strong_negative | ❌ |
| 2023-10-30 | 2023-11-07 | 1.0000 | 0.39% | strong_negative | ✅ |
| 2024-01-03 | 2024-01-12 | 1.0000 | -1.74% | weak_negative | ❌ |
| 2024-01-16 | 2024-02-13 | 1.0000 | -1.58% | weak_negative | ❌ |
| 2024-02-14 | 2024-02-15 | 1.0000 | -5.23% | weak_negative | ❌ |
| 2024-04-04 | 2024-04-15 | 1.0000 | -3.27% | weak_negative | ❌ |
| 2024-04-16 | 2024-04-25 | 1.0000 | 0.27% | weak_negative | ✅ |
| 2024-04-26 | 2024-05-16 | 1.0000 | 0.28% | weak_negative | ✅ |
| 2024-07-03 | 2024-07-09 | 1.0000 | -3.85% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 42 | -0.69% | -28.9% | 40.5% |
| 16-30d | 10 | 5.47% | 54.7% | 70.0% |
| 31-50d | 1 | 32.84% | 32.8% | 100.0% |
| 6-15d | 40 | 0.97% | 38.9% | 55.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 7

## Observations & Caveats

**Sample size:** 93 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (12.3%).
**Win/loss profile:** 50.5% win rate with 1.72× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (50.5%) exceeded signal accuracy (37.0%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2026 (-10.3%, 2 trades). Macro: No flagged events
- **Losing regime:** `strong_negative` — 9 trades, -1.7% total return
- **Losing regime:** `regime_shift` — 18 trades, -16.8% total return

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 8d, std 7d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.