# Strategy Analysis: momentum_lb20_z0.5_e0d × signal_change

**Ticker:** AGCO
**Entry:** `momentum_lb20_z0.5_e0d`
**Exit:** `signal_change`
**Period:** 2016-10-26 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `0` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `signal_change`
  - Exit when the UCC signal reverses direction. Fundamentally-driven exit that stays in the trade as long as the thesis holds

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 819.2% |
| **Annualized Return** | 19.8% |
| **Sharpe Ratio** | 0.681 |
| **Max Drawdown** | -41.9% |
| **Total Trades** | 20 |
| **Win Rate** | 75.0% |
| **Signal Accuracy** | 73.3% |
| **Direction Accuracy** | 75.0% |
| **Skill Ratio** | 73.3% |
| **Profit Factor** | 6.33 |
| **Expectancy** | 0.1510 |
| **Tail Ratio** | 5.72 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 222.5% | 819.2% | 596.7% |
| Annualized Return | 13.5% | 19.8% | — |

## Diversity & Concentration

Diversification: **Somewhat concentrated** — noticeable dependence on top trades (HHI ratio: 3.1×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.1573 | Ideal for 20 trades: 0.0500 |
| Top-1 Trade | 41.5% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 58.2% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 269.4% | Positive without best trade |
| Return ex-Top-3 | 119.0% | Positive without top 3 |
| Max Single Trade | 148.8% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 11 | 27.31% | 300.4% | 27.31% | 89.91 |
| no_signal | 5 | 9.60% | 48.0% | 9.60% | 90.40 |
| direction_wrong_loss | 4 | -11.60% | -46.4% | -11.60% | 65.00 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 20 | 15.10% | 302.0% | 75.0% | 75.0% | 15.10% |

**Best-performing regime:** `unknown` — 20 trades, 302.0% total return, 75.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ✅ | 4 | 10.58% | 42.3% |
| ✅ | ❌ | 4 | -11.60% | -46.4% |
| ✅ | ✅ | 7 | 36.86% | 258.0% |

### Flip Trades (Signal Wrong → Direction Right)

**8 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **12.6%**
- Total return: **100.6%**
- Average alpha: **12.6%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 8 | 12.57% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 20 | 15.10% | 302.0% | 75.0% | 75.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 11 | 22.67% | 249.3% | 81.8% | 81.8% |
| SHORT | 9 | 5.85% | 52.6% | 66.7% | 66.7% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 1 | 26.3% | 26.26% | 100.0% | 100.0% | 26.3% |
| 2017 | 2 | 15.1% | 7.55% | 100.0% | 100.0% | 15.1% |
| 2018 | 2 | -31.4% | -15.72% | 0.0% | 0.0% | -31.4% |
| 2019 | 1 | 7.3% | 7.29% | 100.0% | 100.0% | 7.3% |
| 2020 | 2 | 177.7% | 88.83% | 100.0% | 100.0% | 177.7% |
| 2021 | 1 | 11.7% | 11.68% | 100.0% | 100.0% | 11.7% |
| 2022 | 3 | 52.1% | 17.37% | 100.0% | 100.0% | 52.1% |
| 2023 | 2 | 11.6% | 5.81% | 100.0% | 100.0% | 11.6% |
| 2024 | 3 | 4.1% | 1.36% | 33.3% | 33.3% | 4.1% |
| 2025 | 2 | 10.7% | 5.37% | 50.0% | 50.0% | 10.7% |
| 2026 | 1 | 16.9% | 16.89% | 100.0% | 100.0% | 16.9% |

### Macro Context by Year

**2016** (Strong year: 26.3%, 1 trades)
- No major macro events flagged.

**2017** (Strong year: 15.1%, 2 trades)
- No major macro events flagged.

**2018** (Losing year: -31.4%, 2 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 7.3%, 1 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 177.7%, 2 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 11.7%, 1 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 52.1%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 11.6%, 2 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 4.1%, 3 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 10.7%, 2 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 16.9%, 1 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -31.4% cumulative (trade 3 to trade 5)
**Period:** 2017-10-31 to 2018-10-30 (3 trades)
**Peak cumulative return:** 41.4% → **Trough:** 9.9%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2017-10-31 | 2018-07-31 | -1.0000 | 7.48% | unknown | ✅ |
| 2018-07-31 | 2018-10-30 | 1.0000 | -13.87% | unknown | ❌ |
| 2018-10-30 | 2019-02-05 | -1.0000 | -17.58% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 1 | 16.89% | 16.9% | 100.0% |
| 50d+ | 19 | 15.00% | 285.1% | 73.7% |

## Win/Loss Streaks

- **Max consecutive wins:** 10
- **Max consecutive losses:** 2

## Observations & Caveats

**Sample size:** ⚠️ Only 20 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** ⚠️ Concentrated. HHI of 0.1573 is 3.1× the ideal, suggesting meaningful dependence on a small number of trades.
**Win/loss profile:** 75.0% win rate with 6.33× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (73.3%) and direction accuracy (75.0%) are similar, suggesting the correlation flip had limited net impact in this sample.

### Known Vulnerabilities

- **Worst year:** 2018 (-31.4%, 2 trades). Macro: US-China Trade War Escalation

### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 222.5% buy-and-hold return (aligned to strategy period: None to None), yet 9 short trades returned 52.6% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.