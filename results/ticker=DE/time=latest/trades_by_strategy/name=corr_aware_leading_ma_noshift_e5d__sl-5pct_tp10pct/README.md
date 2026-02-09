# Strategy Analysis: corr_aware_leading_ma_noshift_e5d × sl-5%_tp10%

**Ticker:** DE
**Entry:** `corr_aware_leading_ma_noshift_e5d`
**Exit:** `sl-5%_tp10%`
**Period:** 2018-08-10 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `leading_ma` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `True` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `leading` — Which confidence metric to use for scaling
- **entry_days_before:** `5` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `True` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit targets a 2:1 reward/risk ratio

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 279.8% |
| **Annualized Return** | 9.4% |
| **Sharpe Ratio** | 0.449 |
| **Max Drawdown** | -46.4% |
| **Total Trades** | 113 |
| **Win Rate** | 48.7% |
| **Signal Accuracy** | 37.9% |
| **Direction Accuracy** | 48.7% |
| **Skill Ratio** | 46.6% |
| **Profit Factor** | 1.59 |
| **Expectancy** | 0.0142 |
| **Tail Ratio** | 1.48 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 701.3% | 279.8% | -421.5% |
| Annualized Return | 20.7% | 9.4% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0112 | Ideal for 113 trades: 0.0088 |
| Top-1 Trade | 3.7% of gross profit | Moderate concentration |
| Top-3 Trades | 9.7% of gross profit | Moderate concentration |
| Return ex-Top-1 | 227.8% | Positive without best trade |
| Return ex-Top-3 | 156.1% | Positive without top 3 |
| Max Single Trade | 15.9% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 48 | 8.11% | 389.2% | 8.34% | 12.52 |
| no_signal | 10 | 3.37% | 33.7% | 1.69% | 17.80 |
| direction_wrong_loss | 55 | -4.77% | -262.4% | -5.03% | 12.67 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| weak_negative | 19 | 4.03% | 76.6% | 68.4% | 68.4% | 2.41% |
| unknown | 38 | 1.61% | 61.2% | 50.0% | 50.0% | 2.45% |
| strong_negative | 10 | 2.29% | 22.9% | 50.0% | 50.0% | 0.45% |
| weak_positive | 35 | 0.16% | 5.5% | 40.0% | 40.0% | -0.13% |
| strong_positive | 11 | -0.51% | -5.6% | 36.4% | 36.4% | 0.15% |

**Best-performing regime:** `weak_negative` — 19 trades, 76.6% total return, 68.4% win rate.
**Worst-performing regime:** `strong_positive` — 11 trades, -5.6% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 35 | -4.50% | -157.6% |
| ❌ | ✅ | 29 | 8.53% | 247.3% |
| ✅ | ❌ | 20 | -5.24% | -104.8% |
| ✅ | ✅ | 19 | 7.47% | 141.9% |

### Flip Trades (Signal Wrong → Direction Right)

**36 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **8.1%**
- Total return: **291.1%**
- Average alpha: **9.1%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 14 | 8.69% |
| weak_negative | 13 | 7.55% |
| strong_positive | 4 | 7.01% |
| weak_positive | 3 | 9.66% |
| strong_negative | 2 | 7.16% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 46 | 2.79% | 128.5% | 58.7% | 58.7% |
| medium | 67 | 0.48% | 32.0% | 41.8% | 41.8% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 54 | 1.73% | 93.5% | 55.6% | 55.6% |
| SHORT | 59 | 1.14% | 67.1% | 42.4% | 42.4% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 9 | 12.1% | 1.35% | 55.6% | 55.6% | 20.0% |
| 2019 | 14 | -25.7% | -1.83% | 28.6% | 28.6% | -51.1% |
| 2020 | 19 | 111.0% | 5.84% | 73.7% | 73.7% | 150.4% |
| 2021 | 13 | 38.9% | 2.99% | 53.8% | 53.8% | 16.6% |
| 2022 | 21 | -26.3% | -1.25% | 33.3% | 33.3% | -5.4% |
| 2023 | 8 | 25.6% | 3.21% | 62.5% | 62.5% | 10.4% |
| 2024 | 9 | -2.7% | -0.30% | 33.3% | 33.3% | -14.2% |
| 2025 | 18 | 14.4% | 0.80% | 44.4% | 44.4% | 1.5% |
| 2026 | 2 | 13.2% | 6.61% | 100.0% | 100.0% | 12.2% |

### Macro Context by Year

**2018** (Strong year: 12.1%, 9 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -25.7%, 14 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 111.0%, 19 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 38.9%, 13 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -26.3%, 21 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 25.6%, 8 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Roughly flat: -2.7%, 9 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 14.4%, 18 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 13.2%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -43.9% cumulative (trade 60 to trade 66)
**Period:** 2022-03-08 to 2022-06-24 (7 trades)
**Peak cumulative return:** 143.2% → **Trough:** 99.3%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-03-08 | 2022-03-17 | 1.0000 | 11.30% | weak_positive | ✅ |
| 2022-03-18 | 2022-04-25 | 1.0000 | -6.45% | weak_positive | ❌ |
| 2022-04-26 | 2022-05-09 | 1.0000 | -4.52% | weak_positive | ❌ |
| 2022-05-10 | 2022-05-20 | 1.0000 | -14.10% | weak_positive | ❌ |
| 2022-05-23 | 2022-06-16 | 1.0000 | -5.30% | strong_positive | ❌ |
| 2022-06-17 | 2022-06-23 | 1.0000 | -7.81% | strong_positive | ❌ |
| 2022-06-24 | 2022-07-05 | 1.0000 | -5.68% | strong_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 42 | 1.35% | 56.8% | 50.0% |
| 16-30d | 19 | 0.68% | 12.8% | 42.1% |
| 31-50d | 10 | 3.25% | 32.5% | 60.0% |
| 50d+ | 2 | -2.18% | -4.4% | 50.0% |
| 6-15d | 40 | 1.57% | 62.8% | 47.5% |

## Win/Loss Streaks

- **Max consecutive wins:** 7
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 113 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Well-distributed. HHI of 0.0112 is near the theoretical minimum of 0.0088 for 113 trades.
**Win/loss profile:** Profit factor of 1.59 with 48.7% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (48.7%) exceeded signal accuracy (37.9%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2022 (-26.3%, 21 trades). Macro: Fed Tightening Cycle, 2022 Bear Market
- **Losing regime:** `strong_positive` — 11 trades, -5.6% total return

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 13d, std 13d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.