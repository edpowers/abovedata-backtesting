# Strategy Analysis: corr_aware_contemp_sameq_e15d × trailing_stop_5%

**Ticker:** AGCO
**Entry:** `corr_aware_contemp_sameq_e15d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-07-10 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

This is a **correlation-aware** entry strategy that uses UCC (Uniform Commercial Code) filing data as a leading indicator of corporate revenue trends. Unlike simple signal-threshold strategies, it determines trade **direction** by combining the signal value with the historical correlation between UCC filings and revenue outcomes:

> `trade_direction = sign(UCC_signal) × sign(correlation)`

When UCC filings and revenue are positively correlated (more filings → more revenue), a positive signal means go long. When they're **negatively** correlated (more filings → less revenue), a positive signal means go **short** — the correlation flip.

### Entry Parameters

- **signal_col:** `visible_revenue_resid` — UCC signal column used as the fundamental input
- **corr_col:** `contemp` — Correlation variant for direction determination. 'leading_ma' uses the smoothed leading correlation between UCC filings and next-quarter revenue, which captures the predictive relationship
- **min_signal_abs:** `0.0` — Minimum absolute signal value to trigger a trade. 0.0 means any non-zero signal generates a trade
- **skip_regime_shifts:** `False` — Whether to skip entries during correlation regime shifts. When True, avoids trading during unstable correlation periods
- **scale_by_confidence:** `False` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 519.1% |
| **Annualized Return** | 63.7% |
| **Sharpe Ratio** | 2.344 |
| **Max Drawdown** | -21.6% |
| **Total Trades** | 132 |
| **Win Rate** | 47.7% |
| **Signal Accuracy** | 60.2% |
| **Direction Accuracy** | 49.6% |
| **Skill Ratio** | 49.6% |
| **Profit Factor** | 1.77 |
| **Expectancy** | 0.0170 |
| **Tail Ratio** | 2.45 |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.9×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0140 | Ideal for 132 trades: 0.0076 |
| Top-1 Trade | 5.9% of gross profit | ✅ Low concentration |
| Top-3 Trades | 16.6% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 374.4% | Strategy survives without best trade |
| Return ex-Top-3 | 191.2% | Strategy survives without top 3 |
| Max Single Trade | 30.5% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 56 | 8.35% | 467.6% | 6.55% | 18.84 |
| no_signal | 19 | -0.46% | -8.8% | -1.69% | 12.26 |
| direction_wrong_loss | 57 | -4.11% | -234.1% | -4.72% | 8.72 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 56 | 2.84% | 159.0% | 48.2% | 48.2% | 1.52% |
| strong_negative | 14 | 3.43% | 48.0% | 64.3% | 64.3% | 1.98% |
| weak_positive | 15 | 1.48% | 22.2% | 53.3% | 53.3% | 0.34% |
| weak_negative | 16 | 0.46% | 7.3% | 43.8% | 43.8% | 0.50% |
| unknown | 6 | -0.05% | -0.3% | 33.3% | 33.3% | -0.24% |
| strong_positive | 25 | -0.46% | -11.5% | 40.0% | 40.0% | -2.33% |

**Best regime:** `regime_shift` — 56 trades, 159.0% total return, 48.2% win rate.
**Worst regime:** `strong_positive` — 25 trades, -11.5% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 23 | -4.19% | -96.4% |
| ❌ | ✅ | 22 | 8.30% | 182.5% |
| ✅ | ❌ | 34 | -4.05% | -137.7% |
| ✅ | ✅ | 34 | 8.38% | 285.1% |

### Flip Trades (Signal Wrong → Direction Right)

**29 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **8.0%**
- Total return: **231.8%**
- Average alpha: **6.2%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 8 | 10.46% |
| weak_positive | 6 | 7.94% |
| weak_negative | 5 | 4.80% |
| strong_positive | 5 | 5.80% |
| strong_negative | 5 | 9.49% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 90 | 2.10% | 189.0% | 46.7% | 46.7% |
| high | 29 | 1.31% | 37.9% | 51.7% | 51.7% |
| low | 13 | -0.16% | -2.1% | 46.2% | 46.2% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 81 | 2.38% | 192.8% | 48.1% | 48.1% |
| SHORT | 51 | 0.62% | 31.9% | 47.1% | 47.1% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 8 | 7.9% | 0.99% | 37.5% | 37.5% | 13.0% |
| 2019 | 18 | -2.5% | -0.14% | 38.9% | 38.9% | -27.2% |
| 2020 | 18 | 106.1% | 5.90% | 55.6% | 55.6% | 58.2% |
| 2021 | 17 | 25.3% | 1.49% | 52.9% | 52.9% | 3.0% |
| 2022 | 21 | 65.5% | 3.12% | 57.1% | 57.1% | 66.4% |
| 2023 | 17 | 16.1% | 0.95% | 47.1% | 47.1% | -6.7% |
| 2024 | 13 | 20.3% | 1.56% | 53.8% | 53.8% | -2.6% |
| 2025 | 19 | 3.0% | 0.16% | 36.8% | 36.8% | -21.0% |
| 2026 | 1 | -17.0% | -16.99% | 0.0% | 0.0% | -17.1% |

### Macro Context by Year

**2018** (Modestly positive: 7.9%, 8 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Flat: -2.5%, 18 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 106.1%, 18 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 25.3%, 17 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 65.5%, 21 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 16.1%, 17 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 20.3%, 13 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 3.0%, 19 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -17.0%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -29.7% cumulative (trade 105 to trade 119)
**Period:** 2024-07-09 to 2025-03-31 (15 trades)
**Peak cumulative return:** 245.0% → **Trough:** 215.3%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-07-09 | 2024-07-15 | 1.0000 | 5.58% | strong_negative | ✅ |
| 2024-07-16 | 2024-07-30 | 1.0000 | -5.01% | strong_negative | ❌ |
| 2024-07-31 | 2024-08-02 | 1.0000 | -5.14% | regime_shift | ❌ |
| 2024-08-05 | 2024-11-05 | 1.0000 | 3.31% | regime_shift | ✅ |
| 2024-11-06 | 2024-11-13 | 1.0000 | -5.35% | weak_positive | ❌ |
| 2024-11-14 | 2024-12-16 | 1.0000 | 4.69% | weak_positive | ✅ |
| 2024-12-17 | 2024-12-19 | 1.0000 | -6.51% | weak_positive | ❌ |
| 2024-12-20 | 2025-02-03 | 1.0000 | 7.75% | weak_positive | ✅ |
| 2025-02-04 | 2025-02-06 | 1.0000 | -5.23% | weak_positive | ❌ |
| 2025-02-07 | 2025-02-13 | 1.0000 | -5.84% | weak_positive | ❌ |
| 2025-02-14 | 2025-02-24 | 1.0000 | -1.56% | weak_positive | ❌ |
| 2025-02-25 | 2025-03-03 | 1.0000 | -7.27% | weak_positive | ❌ |
| 2025-03-04 | 2025-03-12 | 1.0000 | 6.26% | weak_positive | ✅ |
| 2025-03-13 | 2025-03-28 | 1.0000 | 1.46% | weak_positive | ✅ |
| 2025-03-31 | 2025-04-03 | 1.0000 | -11.28% | weak_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 32 | -3.16% | -101.2% | 21.9% |
| 16-30d | 33 | 6.76% | 223.0% | 72.7% |
| 31-50d | 6 | 16.71% | 100.3% | 100.0% |
| 50d+ | 2 | 5.78% | 11.6% | 100.0% |
| 6-15d | 59 | -0.15% | -9.0% | 40.7% |

## Win/Loss Streaks

- **Max consecutive wins:** 8
- **Max consecutive losses:** 7

## Conclusions & Observations

**Statistical robustness:** With 132 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (191.2% remaining).
**Signal vs Direction:** Signal accuracy (60.2%) exceeds direction accuracy (49.6%), suggesting the correlation flip occasionally inverts a correct signal. The flip helps more than it hurts overall.

### Known Vulnerabilities

- **Worst year:** 2026 (-17.0%, 1 trades). Macro: No flagged events
- **Losing regime:** `unknown` — 6 trades, -0.3% total return
- **Losing regime:** `strong_positive` — 25 trades, -11.5% total return