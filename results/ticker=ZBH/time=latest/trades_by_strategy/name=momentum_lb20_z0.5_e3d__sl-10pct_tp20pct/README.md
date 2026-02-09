# Strategy Analysis: momentum_lb20_z0.5_e3d × sl-10%_tp20%

**Ticker:** ZBH
**Entry:** `momentum_lb20_z0.5_e3d`
**Exit:** `sl-10%_tp20%`
**Period:** 2018-04-23 to 2025-08-04
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `3` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 140.9% |
| **Annualized Return** | 6.9% |
| **Sharpe Ratio** | 0.331 |
| **Max Drawdown** | -46.7% |
| **Total Trades** | 41 |
| **Win Rate** | 56.1% |
| **Signal Accuracy** | 25.6% |
| **Direction Accuracy** | 53.8% |
| **Skill Ratio** | 53.8% |
| **Profit Factor** | 1.85 |
| **Expectancy** | 0.0272 |
| **Tail Ratio** | 1.68 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Alpha |
|---|---|---|---|
| Total Return | -10.7% | 140.9% | 151.6% |
| Annualized Return | -1.0% | 6.9% | — |

## Diversity & Concentration

Diversification: **Excellent** — nearly perfectly diversified (HHI ratio: 1.5×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0355 | Ideal for 41 trades: 0.0244 |
| Top-1 Trade | 10.9% of gross profit | ✅ Low concentration |
| Top-3 Trades | 27.3% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 90.6% | Strategy survives without best trade |
| Return ex-Top-3 | 32.5% | Strategy survives without top 3 |
| Max Single Trade | 26.4% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 21 | 10.83% | 227.5% | 9.28% | 38.14 |
| no_signal | 2 | 7.93% | 15.9% | -1.74% | 35.50 |
| direction_wrong_loss | 18 | -7.32% | -131.7% | -9.65% | 31.78 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 11 | 7.44% | 81.8% | 72.7% | 72.7% | 7.26% |
| weak_positive | 5 | 5.14% | 25.7% | 80.0% | 80.0% | 2.00% |
| regime_shift | 12 | 1.75% | 21.0% | 50.0% | 50.0% | -2.79% |
| strong_positive | 3 | 3.47% | 10.4% | 33.3% | 33.3% | 2.66% |
| strong_negative | 6 | 1.32% | 7.9% | 50.0% | 50.0% | -1.16% |
| weak_negative | 4 | -8.80% | -35.2% | 25.0% | 25.0% | -9.92% |

**Best regime:** `unknown` — 11 trades, 81.8% total return, 72.7% win rate.
**Worst regime:** `weak_negative` — 4 trades, -35.2% total return.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 13 | -7.27% | -94.5% |
| ❌ | ✅ | 16 | 10.44% | 167.0% |
| ✅ | ❌ | 5 | -7.45% | -37.3% |
| ✅ | ✅ | 5 | 12.09% | 60.4% |

### Flip Trades (Signal Wrong → Direction Right)

**18 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **10.2%**
- Total return: **182.9%**
- Average alpha: **7.2%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 7 | 10.30% |
| regime_shift | 4 | 10.93% |
| strong_negative | 3 | 11.01% |
| weak_positive | 2 | 8.80% |
| weak_negative | 1 | 1.01% |
| strong_positive | 1 | 15.42% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| low | 12 | 7.58% | 90.9% | 75.0% | 75.0% |
| high | 8 | 2.07% | 16.5% | 37.5% | 37.5% |
| medium | 21 | 0.20% | 4.1% | 52.4% | 52.4% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 22 | 3.10% | 68.2% | 54.5% | 54.5% |
| SHORT | 19 | 2.28% | 43.4% | 57.9% | 57.9% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 4 | 28.5% | 7.12% | 75.0% | 75.0% | 26.5% |
| 2019 | 6 | 26.9% | 4.49% | 66.7% | 66.7% | 10.6% |
| 2020 | 11 | 26.3% | 2.39% | 45.5% | 45.5% | 6.6% |
| 2021 | 4 | -17.3% | -4.33% | 50.0% | 50.0% | -29.0% |
| 2022 | 1 | 15.4% | 15.42% | 100.0% | 100.0% | 14.5% |
| 2023 | 8 | 32.1% | 4.01% | 62.5% | 62.5% | 12.5% |
| 2024 | 4 | -5.3% | -1.33% | 25.0% | 25.0% | -23.4% |
| 2025 | 3 | 5.0% | 1.65% | 66.7% | 66.7% | -0.6% |

### Macro Context by Year

**2018** (Strong year: 28.5%, 4 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 26.9%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 26.3%, 11 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -17.3%, 4 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 15.4%, 1 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 32.1%, 8 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Losing year: -5.3%, 4 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 5.0%, 3 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -38.1% cumulative (trade 19 to trade 24)
**Period:** 2020-06-25 to 2021-06-03 (6 trades)
**Peak cumulative return:** 102.3% → **Trough:** 64.2%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-06-25 | 2020-07-29 | 1.0000 | 21.31% | regime_shift | ✅ |
| 2020-07-30 | 2020-11-03 | 1.0000 | -1.19% | regime_shift | ❌ |
| 2020-11-03 | 2021-01-14 | -1.0000 | -19.41% | weak_negative | ❌ |
| 2021-01-15 | 2021-02-02 | -1.0000 | 1.01% | weak_negative | ✅ |
| 2021-04-29 | 2021-06-02 | 1.0000 | -9.83% | regime_shift | ❌ |
| 2021-06-03 | 2021-08-10 | 1.0000 | -8.73% | regime_shift | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 6 | 5.07% | 30.4% | 83.3% |
| 16-30d | 9 | 6.58% | 59.2% | 55.6% |
| 31-50d | 7 | -1.27% | -8.9% | 42.9% |
| 50d+ | 12 | 5.19% | 62.3% | 66.7% |
| 6-15d | 7 | -4.49% | -31.5% | 28.6% |

## Win/Loss Streaks

- **Max consecutive wins:** 4
- **Max consecutive losses:** 3

## Conclusions & Observations

**Statistical robustness:** 41 trades provides a reasonable sample, though some metrics may have wide confidence intervals.
**Diversification:** Excellent. HHI of 0.0355 is near the theoretical minimum of 0.0244. No single trade dominates returns.
**Edge:** Genuine structural edge: 56.1% win rate with 1.85× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (53.8%) exceeds signal accuracy (25.6%), confirming the correlation flip adds value beyond raw signal prediction.
**Regime dependence:** `unknown` (11 trades, 27% of total) generates 81.8% — a disproportionate share of returns.

### Known Vulnerabilities

- **Worst year:** 2021 (-17.3%, 4 trades). Macro: Post-COVID Stimulus Rally
- **Losing regime:** `weak_negative` — 4 trades, -35.2% total return