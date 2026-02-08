# Strategy Analysis: momentum_lb10_z0.5_e0d × trailing_stop_5%

**Ticker:** AGCO
**Entry:** `momentum_lb10_z0.5_e0d`
**Exit:** `trailing_stop_5%`
**Period:** 2016-10-26 to 2026-01-30
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `10`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `0` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Lets winners run while cutting losses, but can exit too early in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 289.1% |
| **Annualized Return** | 56.2% |
| **Sharpe Ratio** | 2.195 |
| **Max Drawdown** | -26.5% |
| **Total Trades** | 122 |
| **Win Rate** | 44.3% |
| **Signal Accuracy** | 48.9% |
| **Direction Accuracy** | 48.9% |
| **Skill Ratio** | 48.9% |
| **Profit Factor** | 1.68 |
| **Expectancy** | 0.0136 |
| **Tail Ratio** | 2.48 |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 1.9×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0152 | Ideal for 122 trades: 0.0082 |
| Top-1 Trade | 7.4% of gross profit | ✅ Low concentration |
| Top-3 Trades | 19.6% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 198.2% | Strategy survives without best trade |
| Return ex-Top-3 | 91.4% | Strategy survives without top 3 |
| Max Single Trade | 30.5% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 46 | 7.75% | 356.6% | 6.65% | 17.57 |
| no_signal | 28 | -0.34% | -9.5% | -1.30% | 14.93 |
| direction_wrong_loss | 48 | -3.78% | -181.3% | -4.65% | 8.92 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 51 | 2.97% | 151.7% | 47.1% | 47.1% | 1.87% |
| weak_negative | 7 | 2.63% | 18.4% | 71.4% | 71.4% | 3.69% |
| strong_negative | 4 | 3.74% | 14.9% | 50.0% | 50.0% | 2.60% |
| weak_positive | 10 | -0.15% | -1.5% | 50.0% | 50.0% | 0.05% |
| unknown | 24 | -0.27% | -6.4% | 37.5% | 37.5% | -1.14% |
| strong_positive | 26 | -0.43% | -11.3% | 34.6% | 34.6% | -2.23% |

**Best regime:** `regime_shift` — 51 trades, 151.7% total return, 47.1% win rate.
**Worst regime:** `strong_positive` — 26 trades, -11.3% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 27 | -3.57% | -96.3% |
| ❌ | ✅ | 21 | 6.78% | 142.5% |
| ✅ | ❌ | 21 | -4.05% | -85.0% |
| ✅ | ✅ | 25 | 8.57% | 214.1% |

### Flip Trades (Signal Wrong → Direction Right)

**29 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **6.7%**
- Total return: **195.4%**
- Average alpha: **5.8%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 9 | 8.55% |
| unknown | 6 | 5.53% |
| weak_positive | 5 | 5.43% |
| weak_negative | 4 | 5.14% |
| strong_positive | 3 | 4.98% |
| strong_negative | 2 | 11.32% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 71 | 2.03% | 144.3% | 45.1% | 45.1% |
| high | 22 | 0.51% | 11.2% | 40.9% | 40.9% |
| low | 29 | 0.36% | 10.4% | 44.8% | 44.8% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 39 | 3.77% | 147.0% | 53.8% | 53.8% |
| SHORT | 83 | 0.23% | 18.8% | 39.8% | 39.8% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 4 | -15.1% | -3.78% | 0.0% | 0.0% | -20.2% |
| 2017 | 9 | 9.0% | 1.01% | 44.4% | 44.4% | -7.0% |
| 2018 | 12 | -0.5% | -0.04% | 41.7% | 41.7% | 4.4% |
| 2019 | 4 | -6.2% | -1.55% | 25.0% | 25.0% | -12.2% |
| 2020 | 19 | 104.8% | 5.52% | 57.9% | 57.9% | 56.4% |
| 2021 | 15 | 22.1% | 1.47% | 60.0% | 60.0% | 9.6% |
| 2022 | 19 | 35.4% | 1.87% | 42.1% | 42.1% | 39.1% |
| 2023 | 10 | 12.1% | 1.21% | 50.0% | 50.0% | 5.2% |
| 2024 | 11 | 9.4% | 0.85% | 45.5% | 45.5% | -6.5% |
| 2025 | 17 | 1.5% | 0.09% | 35.3% | 35.3% | -15.9% |
| 2026 | 2 | -6.8% | -3.38% | 0.0% | 0.0% | -6.4% |

### Macro Context by Year

**2016** (Losing year: -15.1%, 4 trades)
- No major macro events flagged.

**2017** (Modestly positive: 9.0%, 9 trades)
- No major macro events flagged.

**2018** (Flat: -0.5%, 12 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -6.2%, 4 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 104.8%, 19 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 22.1%, 15 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 35.4%, 19 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 12.1%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 9.4%, 11 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 1.5%, 17 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -6.8%, 2 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -25.1% cumulative (trade 108 to trade 122)
**Period:** 2025-03-27 to 2026-01-09 (15 trades)
**Peak cumulative return:** 190.9% → **Trough:** 165.8%

**Macro context during drawdown:**
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-03-27 | 2025-04-09 | -1.0000 | 13.20% | weak_positive | ✅ |
| 2025-04-10 | 2025-04-24 | -1.0000 | -2.18% | weak_positive | ❌ |
| 2025-04-25 | 2025-05-01 | -1.0000 | -11.46% | weak_positive | ❌ |
| 2025-05-02 | 2025-05-21 | 1.0000 | 7.43% | strong_positive | ✅ |
| 2025-05-22 | 2025-07-15 | 1.0000 | 4.11% | strong_positive | ✅ |
| 2025-07-16 | 2025-07-30 | 1.0000 | -0.46% | strong_positive | ❌ |
| 2025-07-31 | 2025-08-07 | 1.0000 | -5.26% | strong_positive | ❌ |
| 2025-08-08 | 2025-08-29 | 1.0000 | -1.03% | regime_shift | ❌ |
| 2025-09-02 | 2025-10-01 | 1.0000 | -1.75% | regime_shift | ❌ |
| 2025-10-02 | 2025-10-10 | 1.0000 | -3.40% | regime_shift | ❌ |
| 2025-10-13 | 2025-10-31 | 1.0000 | -1.02% | regime_shift | ❌ |
| 2025-11-03 | 2025-11-21 | -1.0000 | -0.98% | strong_positive | ❌ |
| 2025-11-24 | 2026-01-06 | -1.0000 | -2.33% | strong_positive | ❌ |
| 2026-01-07 | 2026-01-08 | -1.0000 | -5.40% | strong_positive | ❌ |
| 2026-01-09 | 2026-01-30 | -1.0000 | -1.35% | strong_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 28 | -1.63% | -45.6% | 32.1% |
| 16-30d | 30 | 4.50% | 135.0% | 66.7% |
| 31-50d | 8 | 10.55% | 84.4% | 100.0% |
| 50d+ | 1 | 8.99% | 9.0% | 100.0% |
| 6-15d | 55 | -0.31% | -16.9% | 29.1% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 10

## Conclusions & Observations

**Statistical robustness:** With 122 trades, this sample is large enough for reliable inference.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (91.4% remaining).

### Known Vulnerabilities

- **Worst year:** 2016 (-15.1%, 4 trades). Macro: No flagged events
- **Losing regime:** `weak_positive` — 10 trades, -1.5% total return
- **Losing regime:** `unknown` — 24 trades, -6.4% total return
- **Losing regime:** `strong_positive` — 26 trades, -11.3% total return