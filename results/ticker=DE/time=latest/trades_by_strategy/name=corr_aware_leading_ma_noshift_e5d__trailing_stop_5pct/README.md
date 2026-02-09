# Strategy Analysis: corr_aware_leading_ma_noshift_e5d × trailing_stop_5%

**Ticker:** DE
**Entry:** `corr_aware_leading_ma_noshift_e5d`
**Exit:** `trailing_stop_5%`
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

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 241.2% |
| **Annualized Return** | 25.5% |
| **Sharpe Ratio** | 1.358 |
| **Max Drawdown** | -27.2% |
| **Total Trades** | 212 |
| **Win Rate** | 48.6% |
| **Signal Accuracy** | 35.9% |
| **Direction Accuracy** | 48.6% |
| **Skill Ratio** | 49.2% |
| **Profit Factor** | 1.46 |
| **Expectancy** | 0.0070 |
| **Tail Ratio** | 1.94 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 701.3% | 241.2% | -460.1% |
| Annualized Return | 20.7% | 25.5% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.9×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0088 | Ideal for 212 trades: 0.0047 |
| Top-1 Trade | 5.3% of gross profit | Moderate concentration |
| Top-3 Trades | 12.9% of gross profit | Moderate concentration |
| Return ex-Top-1 | 172.8% | Positive without best trade |
| Return ex-Top-3 | 96.1% | Positive without top 3 |
| Max Single Trade | 25.1% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 96 | 4.48% | 430.3% | 4.27% | 8.31 |
| no_signal | 17 | 1.66% | 28.3% | 0.92% | 9.47 |
| direction_wrong_loss | 99 | -3.12% | -309.1% | -3.88% | 4.21 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| weak_negative | 35 | 1.85% | 64.9% | 48.6% | 48.6% | 1.07% |
| weak_positive | 50 | 0.74% | 37.0% | 50.0% | 50.0% | -0.12% |
| strong_negative | 23 | 1.15% | 26.5% | 60.9% | 60.9% | 0.59% |
| strong_positive | 24 | 0.57% | 13.6% | 37.5% | 37.5% | 0.24% |
| unknown | 80 | 0.09% | 7.5% | 47.5% | 47.5% | -0.12% |

**Best-performing regime:** `weak_negative` — 35 trades, 64.9% total return, 48.6% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 67 | -3.34% | -223.6% |
| ❌ | ✅ | 58 | 4.74% | 275.0% |
| ✅ | ❌ | 32 | -2.67% | -85.5% |
| ✅ | ✅ | 38 | 4.09% | 155.3% |

### Flip Trades (Signal Wrong → Direction Right)

**65 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.9%**
- Total return: **317.7%**
- Average alpha: **5.3%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 28 | 4.40% |
| weak_negative | 17 | 6.06% |
| strong_positive | 9 | 5.82% |
| weak_positive | 6 | 3.83% |
| strong_negative | 5 | 3.20% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 119 | 0.85% | 101.3% | 47.1% | 47.1% |
| low | 93 | 0.52% | 48.1% | 50.5% | 50.5% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 90 | 1.67% | 150.4% | 53.3% | 53.3% |
| SHORT | 122 | -0.01% | -1.0% | 45.1% | 45.1% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 18 | 16.3% | 0.90% | 66.7% | 66.7% | 27.5% |
| 2019 | 35 | -16.4% | -0.47% | 40.0% | 40.0% | -42.8% |
| 2020 | 34 | 50.3% | 1.48% | 52.9% | 52.9% | 34.3% |
| 2021 | 25 | 22.7% | 0.91% | 60.0% | 60.0% | 7.5% |
| 2022 | 40 | 19.2% | 0.48% | 40.0% | 40.0% | 14.4% |
| 2023 | 18 | 23.9% | 1.33% | 50.0% | 50.0% | 7.4% |
| 2024 | 12 | -8.9% | -0.75% | 41.7% | 41.7% | -20.5% |
| 2025 | 29 | 22.9% | 0.79% | 44.8% | 44.8% | -6.4% |
| 2026 | 1 | 19.5% | 19.47% | 100.0% | 100.0% | 20.0% |

### Macro Context by Year

**2018** (Strong year: 16.3%, 18 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -16.4%, 35 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 50.3%, 34 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 22.7%, 25 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 19.2%, 40 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 23.9%, 18 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -8.9%, 12 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 22.9%, 29 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 19.5%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -35.5% cumulative (trade 65 to trade 71)
**Period:** 2020-03-19 to 2020-04-07 (7 trades)
**Peak cumulative return:** 34.1% → **Trough:** -1.4%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-03-19 | 2020-03-20 | -1.0000 | 6.71% | unknown | ✅ |
| 2020-03-23 | 2020-03-24 | -1.0000 | -13.36% | unknown | ❌ |
| 2020-03-25 | 2020-03-26 | -1.0000 | -8.25% | unknown | ❌ |
| 2020-03-27 | 2020-03-30 | -1.0000 | -5.12% | unknown | ❌ |
| 2020-03-31 | 2020-04-02 | -1.0000 | -0.88% | unknown | ❌ |
| 2020-04-03 | 2020-04-06 | -1.0000 | -5.88% | unknown | ❌ |
| 2020-04-07 | 2020-04-09 | -1.0000 | -2.05% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 132 | -0.39% | -50.9% | 38.6% |
| 16-30d | 18 | 7.08% | 127.4% | 83.3% |
| 31-50d | 3 | 3.90% | 11.7% | 100.0% |
| 6-15d | 59 | 1.04% | 61.2% | 57.6% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 212 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (96.1%).
**Win/loss profile:** Profit factor of 1.46 with 48.6% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (48.6%) exceeded signal accuracy (35.9%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2019 (-16.4%, 35 trades). Macro: US-China Trade War Escalation, Fed Rate Cuts (2019)

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 6d, std 7d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.