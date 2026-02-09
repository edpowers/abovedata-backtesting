# Strategy Analysis: corr_aware_contemp_sameq_e15d × sl-10%_tp20%

**Ticker:** AGCO
**Entry:** `corr_aware_contemp_sameq_e15d`
**Exit:** `sl-10%_tp20%`
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

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 781.3% |
| **Annualized Return** | 19.8% |
| **Sharpe Ratio** | 0.723 |
| **Max Drawdown** | -25.5% |
| **Total Trades** | 55 |
| **Win Rate** | 54.5% |
| **Signal Accuracy** | 55.1% |
| **Direction Accuracy** | 55.6% |
| **Skill Ratio** | 55.1% |
| **Profit Factor** | 2.32 |
| **Expectancy** | 0.0481 |
| **Tail Ratio** | 1.87 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 157.5% | 781.3% | 623.9% |
| Annualized Return | 13.3% | 19.8% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0229 | Ideal for 55 trades: 0.0182 |
| Top-1 Trade | 5.1% of gross profit | Moderate concentration |
| Top-3 Trades | 14.5% of gross profit | Moderate concentration |
| Return ex-Top-1 | 611.5% | Positive without best trade |
| Return ex-Top-3 | 380.3% | Positive without top 3 |
| Max Single Trade | 23.9% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 27 | 15.87% | 428.6% | 15.87% | 40.56 |
| no_signal | 6 | 2.78% | 16.7% | 2.78% | 34.17 |
| direction_wrong_loss | 22 | -8.23% | -181.0% | -8.23% | 22.64 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| strong_positive | 17 | 5.87% | 99.8% | 52.9% | 52.9% | 5.87% |
| strong_negative | 15 | 5.65% | 84.8% | 60.0% | 60.0% | 5.65% |
| regime_shift | 10 | 8.04% | 80.4% | 70.0% | 70.0% | 8.04% |
| weak_positive | 3 | 3.55% | 10.6% | 66.7% | 66.7% | 3.55% |
| unknown | 3 | 0.52% | 1.6% | 33.3% | 33.3% | 0.52% |
| weak_negative | 7 | -1.84% | -12.9% | 28.6% | 28.6% | -1.84% |

**Best-performing regime:** `strong_positive` — 17 trades, 99.8% total return, 52.9% win rate.
**Worst-performing regime:** `weak_negative` — 7 trades, -12.9% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 10 | -8.87% | -88.7% |
| ❌ | ✅ | 12 | 14.06% | 168.7% |
| ✅ | ❌ | 12 | -7.69% | -92.3% |
| ✅ | ✅ | 15 | 17.32% | 259.8% |

### Flip Trades (Signal Wrong → Direction Right)

**15 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **13.6%**
- Total return: **204.4%**
- Average alpha: **13.6%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 6 | 14.03% |
| strong_negative | 6 | 14.39% |
| weak_positive | 2 | 10.66% |
| weak_negative | 1 | 12.48% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 36 | 7.71% | 277.7% | 66.7% | 66.7% |
| high | 9 | -0.32% | -2.9% | 33.3% | 33.3% |
| low | 10 | -1.05% | -10.5% | 30.0% | 30.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 35 | 5.22% | 182.6% | 60.0% | 60.0% |
| SHORT | 20 | 4.08% | 81.7% | 45.0% | 45.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 3 | 1.6% | 0.52% | 33.3% | 33.3% | 1.6% |
| 2019 | 8 | 10.5% | 1.32% | 37.5% | 37.5% | 10.5% |
| 2020 | 8 | 120.5% | 15.06% | 87.5% | 87.5% | 120.5% |
| 2021 | 7 | 12.2% | 1.74% | 42.9% | 42.9% | 12.2% |
| 2022 | 10 | 63.5% | 6.35% | 60.0% | 60.0% | 63.5% |
| 2023 | 7 | 32.2% | 4.59% | 71.4% | 71.4% | 32.2% |
| 2024 | 4 | 26.9% | 6.73% | 50.0% | 50.0% | 26.9% |
| 2025 | 6 | 6.7% | 1.11% | 50.0% | 50.0% | 6.7% |
| 2026 | 2 | -9.7% | -4.86% | 0.0% | 0.0% | -9.7% |

### Macro Context by Year

**2018** (Modestly positive: 1.6%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 10.5%, 8 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 120.5%, 8 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 12.2%, 7 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 63.5%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 32.2%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 26.9%, 4 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 6.7%, 6 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -9.7%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -31.2% cumulative (trade 22 to trade 25)
**Period:** 2021-03-09 to 2021-07-08 (4 trades)
**Peak cumulative return:** 160.0% → **Trough:** 128.8%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2021-03-09 | 2021-04-26 | 1.0000 | 19.16% | strong_negative | ✅ |
| 2021-04-27 | 2021-05-19 | 1.0000 | -11.33% | weak_negative | ❌ |
| 2021-05-20 | 2021-06-17 | 1.0000 | -7.94% | weak_negative | ❌ |
| 2021-07-08 | 2021-11-30 | 1.0000 | -11.91% | weak_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 5 | 3.46% | 17.3% | 40.0% |
| 16-30d | 17 | -0.35% | -5.9% | 29.4% |
| 31-50d | 12 | 15.75% | 189.0% | 100.0% |
| 50d+ | 9 | 8.16% | 73.5% | 66.7% |
| 6-15d | 12 | -0.79% | -9.5% | 41.7% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 3

## Observations & Caveats

**Sample size:** 55 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Well-distributed. HHI of 0.0229 is near the theoretical minimum of 0.0182 for 55 trades.
**Win/loss profile:** 54.5% win rate with 2.32× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (55.1%) and direction accuracy (55.6%) are similar, suggesting the correlation flip had limited net impact in this sample.

### Known Vulnerabilities

- **Worst year:** 2026 (-9.7%, 2 trades). Macro: No flagged events
- **Losing regime:** `weak_negative` — 7 trades, -12.9% total return

### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 157.5% buy-and-hold return (aligned to strategy period: None to None), yet 20 short trades returned 81.7% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 33d, std 30d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.