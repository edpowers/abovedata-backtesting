# Strategy Analysis: momentum_lb20_z1.0_e1d × fixed_holding_60d

**Ticker:** ZBH
**Entry:** `momentum_lb20_z1.0_e1d`
**Exit:** `fixed_holding_60d`
**Period:** 2018-04-25 to 2025-08-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `1.0`
- **zscore_window:** `60`
- **entry_days_before:** `1` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `fixed_holding_60d`
  - Fixed 60-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 145.0% |
| **Annualized Return** | 8.6% |
| **Sharpe Ratio** | 0.436 |
| **Max Drawdown** | -54.9% |
| **Total Trades** | 31 |
| **Win Rate** | 61.3% |
| **Signal Accuracy** | 27.6% |
| **Direction Accuracy** | 62.1% |
| **Skill Ratio** | 62.1% |
| **Profit Factor** | 3.13 |
| **Expectancy** | 0.0326 |
| **Tail Ratio** | 1.97 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | -10.7% | 145.0% | 155.7% |
| Annualized Return | -1.0% | 8.6% | — |

## Diversity & Concentration

Diversification: **Good** — moderate concentration, acceptable (HHI ratio: 2.0×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0645 | Ideal for 31 trades: 0.0323 |
| Top-1 Trade | 16.7% of gross profit | ✅ Low concentration |
| Top-3 Trades | 39.6% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 96.3% | Strategy survives without best trade |
| Return ex-Top-3 | 43.3% | Strategy survives without top 3 |
| Max Single Trade | 24.8% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 18 | 7.69% | 138.5% | 6.50% | 42.00 |
| no_signal | 2 | 4.83% | 9.7% | -1.99% | 32.00 |
| direction_wrong_loss | 11 | -4.27% | -46.9% | -8.08% | 29.27 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 11 | 5.87% | 64.6% | 72.7% | 72.7% | 4.99% |
| regime_shift | 8 | 4.17% | 33.4% | 50.0% | 50.0% | 3.01% |
| weak_positive | 4 | 4.03% | 16.1% | 75.0% | 75.0% | -5.51% |
| strong_positive | 4 | 0.99% | 3.9% | 75.0% | 75.0% | 1.53% |
| strong_negative | 2 | -2.71% | -5.4% | 0.0% | 0.0% | -5.30% |
| weak_negative | 2 | -5.71% | -11.4% | 50.0% | 50.0% | -14.14% |

**Best regime:** `unknown` — 11 trades, 64.6% total return, 72.7% win rate.
**Worst regime:** `weak_negative` — 2 trades, -11.4% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 9 | -3.32% | -29.9% |
| ❌ | ✅ | 12 | 7.90% | 94.8% |
| ✅ | ❌ | 2 | -8.54% | -17.1% |
| ✅ | ✅ | 6 | 7.28% | 43.7% |

### Flip Trades (Signal Wrong → Direction Right)

**13 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **8.1%**
- Total return: **105.1%**
- Average alpha: **6.5%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 6 | 8.25% |
| regime_shift | 3 | 12.22% |
| strong_positive | 3 | 1.33% |
| weak_positive | 1 | 14.92% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 12 | 5.94% | 71.2% | 75.0% | 75.0% |
| high | 6 | 4.19% | 25.1% | 66.7% | 66.7% |
| medium | 13 | 0.37% | 4.8% | 46.2% | 46.2% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 16 | 2.68% | 42.9% | 62.5% | 62.5% |
| SHORT | 15 | 3.88% | 58.3% | 60.0% | 60.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 4 | 21.1% | 5.28% | 75.0% | 75.0% | 18.6% |
| 2019 | 6 | 24.3% | 4.05% | 66.7% | 66.7% | 7.3% |
| 2020 | 5 | 1.4% | 0.28% | 40.0% | 40.0% | -8.8% |
| 2021 | 2 | -8.7% | -4.33% | 0.0% | 0.0% | -14.2% |
| 2022 | 4 | 15.9% | 3.97% | 100.0% | 100.0% | 24.8% |
| 2023 | 4 | 34.3% | 8.57% | 75.0% | 75.0% | 13.3% |
| 2024 | 4 | 3.2% | 0.81% | 50.0% | 50.0% | -12.8% |
| 2025 | 2 | 9.7% | 4.83% | 50.0% | 50.0% | -4.0% |

### Macro Context by Year

**2018** (Strong year: 21.1%, 4 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 24.3%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Modestly positive: 1.4%, 5 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -8.7%, 2 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 15.9%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 34.3%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 3.2%, 4 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 9.7%, 2 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -26.5% cumulative (trade 11 to trade 17)
**Period:** 2020-02-03 to 2021-07-30 (7 trades)
**Peak cumulative return:** 64.6% → **Trough:** 38.1%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-02-03 | 2020-04-30 | -1.0000 | 19.20% | unknown | ✅ |
| 2020-05-01 | 2020-05-08 | -1.0000 | -4.83% | strong_negative | ❌ |
| 2020-08-03 | 2020-10-28 | 1.0000 | -1.56% | regime_shift | ❌ |
| 2020-10-29 | 2020-11-05 | 1.0000 | 4.12% | weak_negative | ✅ |
| 2020-11-05 | 2021-02-04 | -1.0000 | -15.53% | weak_negative | ❌ |
| 2021-05-03 | 2021-07-29 | 1.0000 | -8.41% | regime_shift | ❌ |
| 2021-07-30 | 2021-08-02 | 1.0000 | -0.25% | regime_shift | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 11 | -0.19% | -2.1% | 45.5% |
| 50d+ | 18 | 6.00% | 108.0% | 72.2% |
| 6-15d | 2 | -2.36% | -4.7% | 50.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 3

## Conclusions & Observations

**Statistical robustness:** 31 trades provides a reasonable sample, though some metrics may have wide confidence intervals.
**Diversification:** Acceptable. Returns survive removal of top 3 trades (43.3% remaining).
**Edge:** Genuine structural edge: 61.3% win rate with 3.13× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (62.1%) exceeds signal accuracy (27.6%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Worst year:** 2021 (-8.7%, 2 trades). Macro: Post-COVID Stimulus Rally
- **Losing regime:** `strong_negative` — 2 trades, -5.4% total return
- **Losing regime:** `weak_negative` — 2 trades, -11.4% total return