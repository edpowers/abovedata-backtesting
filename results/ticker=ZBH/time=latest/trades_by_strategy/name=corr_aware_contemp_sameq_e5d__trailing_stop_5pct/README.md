# Strategy Analysis: corr_aware_contemp_sameq_e5d × trailing_stop_5%

**Ticker:** ZBH
**Entry:** `corr_aware_contemp_sameq_e5d`
**Exit:** `trailing_stop_5%`
**Period:** 2019-10-29 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. It determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `total_universe_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `5` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 30.3% |
| **Annualized Return** | 24.9% |
| **Sharpe Ratio** | 1.375 |
| **Max Drawdown** | -23.7% |
| **Total Trades** | 168 |
| **Win Rate** | 44.6% |
| **Signal Accuracy** | 31.7% |
| **Direction Accuracy** | 46.0% |
| **Skill Ratio** | 46.0% |
| **Profit Factor** | 1.15 |
| **Expectancy** | 0.0028 |
| **Tail Ratio** | 1.33 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -10.7% | 30.3% | 41.0% |
| Annualized Return | -1.0% | 24.9% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.5×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0089 | Ideal for 168 trades: 0.0060 |
| Top-1 Trade | 3.4% of gross profit | Moderate concentration |
| Top-3 Trades | 10.0% of gross profit | Moderate concentration |
| Return ex-Top-1 | 16.2% | Positive without best trade |
| Return ex-Top-3 | -7.1% | Negative without top 3 |
| Max Single Trade | 12.2% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 64 | 4.99% | 319.4% | 3.70% | 12.84 |
| no_signal | 29 | -0.78% | -22.6% | -1.91% | 7.72 |
| direction_wrong_loss | 75 | -3.34% | -250.4% | -3.43% | 4.96 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 58 | 0.89% | 51.4% | 51.7% | 51.7% | 0.11% |
| weak_positive | 12 | 2.15% | 25.8% | 50.0% | 50.0% | 2.19% |
| unknown | 2 | 5.26% | 10.5% | 50.0% | 50.0% | 0.88% |
| strong_negative | 28 | 0.07% | 1.8% | 46.4% | 46.4% | -0.55% |
| weak_negative | 34 | -0.26% | -8.9% | 44.1% | 44.1% | -1.14% |
| strong_positive | 34 | -1.01% | -34.2% | 29.4% | 29.4% | -1.66% |

**Best-performing regime:** `regime_shift` — 58 trades, 51.4% total return, 51.7% win rate.
**Worst-performing regime:** `strong_positive` — 34 trades, -34.2% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 52 | -3.43% | -178.2% |
| ❌ | ✅ | 43 | 4.89% | 210.1% |
| ✅ | ❌ | 23 | -3.14% | -72.2% |
| ✅ | ✅ | 21 | 5.21% | 109.3% |

### Flip Trades (Signal Wrong → Direction Right)

**54 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **4.6%**
- Total return: **249.7%**
- Average alpha: **3.2%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 17 | 5.09% |
| strong_negative | 13 | 5.27% |
| weak_negative | 12 | 3.78% |
| strong_positive | 8 | 3.47% |
| weak_positive | 4 | 5.41% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 115 | 0.65% | 74.9% | 50.4% | 50.4% |
| low | 11 | 0.06% | 0.7% | 36.4% | 36.4% |
| no_data | 1 | -1.33% | -1.3% | 0.0% | 0.0% |
| high | 41 | -0.68% | -27.9% | 31.7% | 31.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 96 | 0.20% | 19.5% | 45.8% | 45.8% |
| SHORT | 72 | 0.37% | 26.8% | 43.1% | 43.1% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2019 | 1 | 11.9% | 11.86% | 100.0% | 100.0% | 5.0% |
| 2020 | 45 | 9.8% | 0.22% | 48.9% | 48.9% | -16.6% |
| 2021 | 21 | 46.1% | 2.20% | 61.9% | 61.9% | 28.7% |
| 2022 | 31 | -20.1% | -0.65% | 38.7% | 38.7% | -16.9% |
| 2023 | 20 | 19.1% | 0.96% | 40.0% | 40.0% | -4.7% |
| 2024 | 19 | -0.1% | -0.00% | 36.8% | 36.8% | -14.9% |
| 2025 | 27 | -15.7% | -0.58% | 40.7% | 40.7% | -50.3% |
| 2026 | 4 | -4.7% | -1.18% | 25.0% | 25.0% | -6.1% |

### Macro Context by Year

**2019** (Strong year: 11.9%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Modestly positive: 9.8%, 45 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 46.1%, 21 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -20.1%, 31 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 19.1%, 20 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Roughly flat: -0.1%, 19 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -15.7%, 27 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Roughly flat: -4.7%, 4 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -42.0% cumulative (trade 1 to trade 9)
**Period:** 2019-10-29 to 2020-03-16 (9 trades)
**Peak cumulative return:** 11.9% → **Trough:** -30.1%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2019-10-29 | 2020-02-24 | 1.0000 | 11.86% | unknown | ✅ |
| 2020-02-25 | 2020-02-26 | 1.0000 | -2.12% | strong_negative | ❌ |
| 2020-02-27 | 2020-02-28 | 1.0000 | -2.72% | strong_negative | ❌ |
| 2020-03-02 | 2020-03-03 | 1.0000 | -3.87% | strong_negative | ❌ |
| 2020-03-04 | 2020-03-05 | 1.0000 | -6.43% | strong_negative | ❌ |
| 2020-03-06 | 2020-03-09 | 1.0000 | -10.35% | strong_negative | ❌ |
| 2020-03-10 | 2020-03-11 | 1.0000 | -6.02% | strong_negative | ❌ |
| 2020-03-12 | 2020-03-13 | 1.0000 | -4.15% | strong_negative | ❌ |
| 2020-03-16 | 2020-03-17 | 1.0000 | -6.35% | strong_negative | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 84 | -1.14% | -96.0% | 32.1% |
| 16-30d | 16 | 5.38% | 86.1% | 87.5% |
| 31-50d | 5 | 5.34% | 26.7% | 100.0% |
| 50d+ | 2 | 11.83% | 23.7% | 100.0% |
| 6-15d | 61 | 0.10% | 5.8% | 44.3% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 8

## Observations & Caveats

**Sample size:** 168 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-7.1%).
**Win/loss profile:** Profit factor of 1.15 with 44.6% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (46.0%) exceeded signal accuracy (31.7%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2022 (-20.1%, 31 trades). Macro: Fed Tightening Cycle, 2022 Bear Market
- **Losing regime:** `weak_negative` — 34 trades, -8.9% total return
- **Losing regime:** `strong_positive` — 34 trades, -34.2% total return

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.