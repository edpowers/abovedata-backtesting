# Strategy Analysis: corr_aware_contemp_noshift_e30d × trailing_stop_5%

**Ticker:** DE
**Entry:** `corr_aware_contemp_noshift_e30d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-07-06 to 2025-12-09
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
- **skip_regime_shifts:** `True` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
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
| **Total Return** | 165.0% |
| **Annualized Return** | 17.5% |
| **Sharpe Ratio** | 1.509 |
| **Max Drawdown** | -12.8% |
| **Total Trades** | 75 |
| **Win Rate** | 52.0% |
| **Signal Accuracy** | 34.8% |
| **Direction Accuracy** | 52.0% |
| **Skill Ratio** | 52.2% |
| **Profit Factor** | 2.11 |
| **Expectancy** | 0.0150 |
| **Tail Ratio** | 3.18 |

## Diversity & Concentration

Diversification: **Somewhat concentrated** — noticeable dependence on top trades (HHI ratio: 2.6×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0344 | Ideal for 75 trades: 0.0133 |
| Top-1 Trade | 15.4% of gross profit | Moderate concentration |
| Top-3 Trades | 36.8% of gross profit | Moderate concentration |
| Return ex-Top-1 | 99.5% | Positive without best trade |
| Return ex-Top-3 | 32.0% | Positive without top 3 |
| Max Single Trade | 32.8% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 36 | 5.53% | 199.2% | 5.53% | 10.03 |
| no_signal | 6 | 0.24% | 1.4% | 0.24% | 6.83 |
| direction_wrong_loss | 33 | -2.66% | -87.9% | -2.66% | 6.30 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| weak_positive | 9 | 4.59% | 41.3% | 77.8% | 77.8% | 4.59% |
| weak_negative | 30 | 0.91% | 27.3% | 43.3% | 43.3% | 0.91% |
| unknown | 9 | 2.71% | 24.4% | 77.8% | 77.8% | 2.71% |
| strong_positive | 18 | 1.18% | 21.3% | 44.4% | 44.4% | 1.18% |
| strong_negative | 9 | -0.19% | -1.7% | 44.4% | 44.4% | -0.19% |

**Best-performing regime:** `weak_positive` — 9 trades, 41.3% total return, 77.8% win rate.
**Worst-performing regime:** `strong_negative` — 9 trades, -1.7% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 26 | -2.63% | -68.4% |
| ❌ | ✅ | 19 | 6.32% | 120.1% |
| ✅ | ❌ | 7 | -2.79% | -19.6% |
| ✅ | ✅ | 17 | 4.65% | 79.1% |

### Flip Trades (Signal Wrong → Direction Right)

**22 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **6.1%**
- Total return: **134.9%**
- Average alpha: **6.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| weak_negative | 9 | 6.17% |
| strong_positive | 5 | 9.57% |
| strong_negative | 4 | 3.12% |
| unknown | 2 | 6.87% |
| weak_positive | 2 | 2.67% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 33 | 2.62% | 86.4% | 57.6% | 57.6% |
| medium | 36 | 0.90% | 32.3% | 50.0% | 50.0% |
| high | 6 | -0.99% | -5.9% | 33.3% | 33.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 57 | 1.38% | 78.4% | 52.6% | 52.6% |
| SHORT | 18 | 1.90% | 34.3% | 50.0% | 50.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 6 | 15.2% | 2.54% | 66.7% | 66.7% | 15.2% |
| 2019 | 12 | 31.4% | 2.62% | 58.3% | 58.3% | 31.4% |
| 2020 | 9 | 42.2% | 4.69% | 55.6% | 55.6% | 42.2% |
| 2021 | 9 | 2.0% | 0.22% | 55.6% | 55.6% | 2.0% |
| 2022 | 12 | 25.3% | 2.11% | 50.0% | 50.0% | 25.3% |
| 2023 | 9 | -1.3% | -0.14% | 44.4% | 44.4% | -1.3% |
| 2024 | 12 | -3.6% | -0.30% | 41.7% | 41.7% | -3.6% |
| 2025 | 6 | 1.4% | 0.24% | 50.0% | 50.0% | 1.4% |

### Macro Context by Year

**2018** (Strong year: 15.2%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 31.4%, 12 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 42.2%, 9 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 2.0%, 9 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 25.3%, 12 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Roughly flat: -1.3%, 9 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Roughly flat: -3.6%, 12 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 1.4%, 6 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -25.0% cumulative (trade 52 to trade 64)
**Period:** 2023-07-07 to 2024-07-03 (13 trades)
**Peak cumulative return:** 124.8% → **Trough:** 99.7%

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
| 1-5d | 30 | -0.24% | -7.1% | 40.0% |
| 16-30d | 9 | 5.47% | 49.3% | 66.7% |
| 31-50d | 1 | 32.84% | 32.8% | 100.0% |
| 6-15d | 35 | 1.08% | 37.7% | 57.1% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 4

## Observations & Caveats

**Sample size:** 75 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (32.0%).
**Win/loss profile:** 52.0% win rate with 2.11× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Direction accuracy (52.0%) exceeded signal accuracy (34.8%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2024 (-3.6%, 12 trades). Macro: 2024 Election Year Uncertainty
- **Losing regime:** `strong_negative` — 9 trades, -1.7% total return

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 8d, std 7d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.