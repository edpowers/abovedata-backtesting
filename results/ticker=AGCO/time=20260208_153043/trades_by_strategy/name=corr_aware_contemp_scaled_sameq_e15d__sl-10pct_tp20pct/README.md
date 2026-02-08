# Strategy Analysis: corr_aware_contemp_scaled_sameq_e15d × sl-10%_tp20%

**Ticker:** AGCO
**Entry:** `corr_aware_contemp_scaled_sameq_e15d`
**Exit:** `sl-10%_tp20%`
**Period:** 2020-07-09 to 2026-02-06
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
- **scale_by_confidence:** `True` — Whether to scale position size by signal confidence score
- **confidence_col:** `contemp` — Which confidence metric to use for scaling
- **entry_days_before:** `15` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves
- **use_prior_quarter_corr:** `False` — Use the prior quarter's correlation for direction (True), or the current quarter's in-progress estimate. Prior quarter avoids look-ahead bias from partial-quarter correlation estimates

### Exit Parameters

- **Exit type:** `sl-10%_tp20%`
  - Stop-loss at -10%, take-profit at +20%. Wider bands allow more time for the thesis to play out but increase per-trade risk

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 766.0% |
| **Annualized Return** | 7.5% |
| **Sharpe Ratio** | 0.640 |
| **Max Drawdown** | -14.9% |
| **Total Trades** | 29 |
| **Win Rate** | 72.4% |
| **Signal Accuracy** | 50.0% |
| **Direction Accuracy** | 75.0% |
| **Skill Ratio** | 75.0% |
| **Profit Factor** | 4.01 |
| **Expectancy** | 0.0865 |
| **Tail Ratio** | 1.61 |

## Diversity & Concentration

Diversification: **Excellent** — nearly perfectly diversified (HHI ratio: 1.3×)

| Metric | Value | Interpretation |
|---|---|---|
| HHI | 0.0443 | Ideal for 29 trades: 0.0345 |
| Top-1 Trade | 8.1% of gross profit | ✅ Low concentration |
| Top-3 Trades | 23.0% of gross profit | ✅ Low concentration |
| Return ex-Top-1 | 581.1% | Strategy survives without best trade |
| Return ex-Top-3 | 337.5% | Strategy survives without top 3 |
| Max Single Trade | 27.1% | Largest individual trade return |

## Outcome Analysis

**Clean binary outcomes:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. Zero ambiguous outcomes (no direction_right_loss or direction_wrong_profit). This indicates the exit mechanism (SL/TP) is perfectly aligned with direction correctness — the asymmetric payoff is the entire edge.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 18 | 16.09% | 289.6% | 13.24% | 35.83 |
| no_signal | 5 | 2.27% | 11.3% | -2.43% | 48.40 |
| direction_wrong_loss | 6 | -8.34% | -50.1% | -7.71% | 30.67 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| regime_shift | 16 | 12.12% | 193.9% | 81.2% | 81.2% | 9.44% |
| weak_negative | 3 | 12.23% | 36.7% | 66.7% | 66.7% | 15.63% |
| strong_negative | 3 | 4.25% | 12.8% | 66.7% | 66.7% | 0.75% |
| strong_positive | 3 | 2.23% | 6.7% | 66.7% | 66.7% | -5.66% |
| weak_positive | 4 | 0.22% | 0.9% | 50.0% | 50.0% | -0.84% |

**Best regime:** `regime_shift` — 16 trades, 193.9% total return, 81.2% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction is correct because the correlation flip compensated.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 4 | -8.18% | -32.7% |
| ❌ | ✅ | 8 | 13.91% | 111.3% |
| ✅ | ❌ | 2 | -8.67% | -17.3% |
| ✅ | ✅ | 10 | 17.84% | 178.4% |

### Flip Trades (Signal Wrong → Direction Right)

**11 trades** where the UCC signal missed the earnings surprise but the correlation flip correctly identified the price move.

- Average return: **14.2%**
- Total return: **155.8%**
- Average alpha: **9.7%**

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| regime_shift | 5 | 14.15% |
| strong_negative | 2 | 7.08% |
| strong_positive | 2 | 11.84% |
| weak_positive | 1 | 20.87% |
| weak_negative | 1 | 26.39% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 17 | 11.98% | 203.6% | 82.4% | 82.4% |
| high | 12 | 3.94% | 47.3% | 58.3% | 58.3% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 22 | 9.33% | 205.3% | 72.7% | 72.7% |
| SHORT | 7 | 6.51% | 45.6% | 71.4% | 71.4% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2020 | 4 | 92.3% | 23.07% | 100.0% | 100.0% | 73.4% |
| 2021 | 4 | 31.4% | 7.86% | 75.0% | 75.0% | 18.6% |
| 2022 | 6 | 71.9% | 11.98% | 83.3% | 83.3% | 80.7% |
| 2023 | 6 | 19.5% | 3.25% | 50.0% | 50.0% | 13.0% |
| 2024 | 3 | 34.8% | 11.60% | 100.0% | 100.0% | 16.9% |
| 2025 | 5 | 18.0% | 3.60% | 60.0% | 60.0% | -5.6% |
| 2026 | 1 | -17.0% | -16.99% | 0.0% | 0.0% | -17.1% |

### Macro Context by Year

**2020** (Strong year: 92.3%, 4 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 31.4%, 4 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 71.9%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 19.5%, 6 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 34.8%, 3 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 18.0%, 5 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Losing year: -17.0%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -26.6% cumulative (trade 23 to trade 25)
**Period:** 2024-07-09 to 2025-02-14 (3 trades)
**Peak cumulative return:** 249.9% → **Trough:** 223.3%

**Macro context during drawdown:**
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2024-07-09 | 2025-01-23 | 1.0000 | 13.08% | strong_negative | ✅ |
| 2025-01-24 | 2025-02-13 | 1.0000 | -10.33% | weak_positive | ❌ |
| 2025-02-14 | 2025-04-03 | 1.0000 | -16.24% | weak_positive | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 1 | 1.07% | 1.1% | 100.0% |
| 16-30d | 8 | 8.92% | 71.4% | 75.0% |
| 31-50d | 12 | 7.03% | 84.3% | 58.3% |
| 50d+ | 4 | 13.73% | 54.9% | 100.0% |
| 6-15d | 4 | 9.81% | 39.2% | 75.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 2

## Conclusions & Observations

**Statistical robustness:** ⚠️ Only 29 trades — interpret cautiously.
**Diversification:** Excellent. HHI of 0.0443 is near the theoretical minimum of 0.0345. No single trade dominates returns.
**Edge:** Genuine structural edge: 72.4% win rate with 4.01× profit factor — wins are systematically larger than losses.
**Signal vs Direction:** Direction accuracy (75.0%) exceeds signal accuracy (50.0%), confirming the correlation flip adds value beyond raw signal prediction.

### Known Vulnerabilities

- **Worst year:** 2026 (-17.0%, 1 trades). Macro: No flagged events