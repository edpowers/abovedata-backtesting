# Strategy Analysis: momentum_lb20_z0.5_e30d × fixed_holding_30d

**Ticker:** ALGN
**Entry:** `momentum_lb20_z0.5_e30d`
**Exit:** `fixed_holding_30d`
**Period:** 2017-12-14 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `30` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `fixed_holding_30d`
  - Fixed 30-day holding period after entry

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 1117.7% |
| **Annualized Return** | 27.3% |
| **Sharpe Ratio** | 0.771 |
| **Max Drawdown** | -62.0% |
| **Total Trades** | 47 |
| **Win Rate** | 59.6% |
| **Signal Accuracy** | 58.3% |
| **Direction Accuracy** | 59.6% |
| **Skill Ratio** | 61.4% |
| **Profit Factor** | 3.20 |
| **Expectancy** | 0.0670 |
| **Tail Ratio** | 1.78 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -19.8% | 1117.7% | 1137.4% |
| Annualized Return | -2.7% | 27.3% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.9×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0397 | Ideal for 47 trades: 0.0213 |
| Top-1 Trade | 9.3% of gross profit | Moderate concentration |
| Top-3 Trades | 25.5% of gross profit | Moderate concentration |
| Return ex-Top-1 | 753.5% | Positive without best trade |
| Return ex-Top-3 | 354.4% | Positive without top 3 |
| Max Single Trade | 42.7% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 47 | 6.70% | 315.1% | 59.6% | 59.6% | 6.70% |

**Best-performing regime:** `unknown` — 47 trades, 315.1% total return, 59.6% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 9 | -4.88% | -43.9% |
| ❌ | ✅ | 14 | 15.72% | 220.1% |
| ✅ | ❌ | 8 | -10.74% | -86.0% |
| ✅ | ✅ | 13 | 17.22% | 223.9% |

### Flip Trades (Signal Wrong → Direction Right)

**15 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **15.6%**
- Total return: **234.1%**
- Average alpha: **15.6%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 15 | 15.61% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 47 | 6.70% | 315.1% | 59.6% | 59.6% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 22 | 8.90% | 195.9% | 77.3% | 77.3% |
| SHORT | 25 | 4.77% | 119.2% | 44.0% | 44.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2017 | 1 | -15.4% | -15.36% | 0.0% | 0.0% | -15.4% |
| 2018 | 6 | 52.8% | 8.81% | 83.3% | 83.3% | 52.8% |
| 2019 | 6 | 81.2% | 13.53% | 50.0% | 50.0% | 81.2% |
| 2020 | 6 | 12.9% | 2.14% | 50.0% | 50.0% | 12.9% |
| 2021 | 3 | 17.4% | 5.80% | 66.7% | 66.7% | 17.4% |
| 2022 | 5 | 90.8% | 18.16% | 80.0% | 80.0% | 90.8% |
| 2023 | 11 | 46.7% | 4.25% | 63.6% | 63.6% | 46.7% |
| 2024 | 6 | 27.7% | 4.61% | 50.0% | 50.0% | 27.7% |
| 2025 | 3 | 0.9% | 0.31% | 33.3% | 33.3% | 0.9% |

### Macro Context by Year

**2017** (Losing year: -15.4%, 1 trades)
- No major macro events flagged.

**2018** (Strong year: 52.8%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 81.2%, 6 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 12.9%, 6 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 17.4%, 3 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 90.8%, 5 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 46.7%, 11 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 27.7%, 6 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 0.9%, 3 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -52.7% cumulative (trade 14 to trade 17)
**Period:** 2020-01-23 to 2020-06-09 (4 trades)
**Peak cumulative return:** 152.1% → **Trough:** 99.5%

**Macro context during drawdown:**
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-01-23 | 2020-03-12 | -1.0000 | 33.48% | unknown | ✅ |
| 2020-03-13 | 2020-04-27 | -1.0000 | -0.40% | unknown | ❌ |
| 2020-04-28 | 2020-06-09 | -1.0000 | -37.44% | unknown | ❌ |
| 2020-06-09 | 2020-06-11 | 1.0000 | -14.81% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 16 | -2.40% | -38.4% | 31.2% |
| 16-30d | 10 | 3.63% | 36.3% | 70.0% |
| 31-50d | 7 | 19.53% | 136.7% | 85.7% |
| 50d+ | 13 | 14.50% | 188.5% | 76.9% |
| 6-15d | 1 | -8.08% | -8.1% | 0.0% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 3

## Observations & Caveats

**Sample size:** 47 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (354.4%).
**Win/loss profile:** 59.6% win rate with 3.20× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (58.3%) and direction accuracy (59.6%) are similar, suggesting the correlation flip had limited net impact in this sample.

### Known Vulnerabilities

- **Worst year:** 2017 (-15.4%, 1 trades). Macro: No flagged events

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 28d, std 23d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.