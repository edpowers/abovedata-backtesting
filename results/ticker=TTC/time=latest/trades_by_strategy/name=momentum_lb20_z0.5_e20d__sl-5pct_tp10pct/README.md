# Strategy Analysis: momentum_lb20_z0.5_e20d × sl-5%_tp10%

**Ticker:** TTC
**Entry:** `momentum_lb20_z0.5_e20d`
**Exit:** `sl-5%_tp10%`
**Period:** 2016-07-21 to 2026-02-09
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `20`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `20` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `sl-5%_tp10%`
  - Stop-loss at -5%, take-profit at +10%. Asymmetric exit targets a 2:1 reward/risk ratio

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 339.3% |
| **Annualized Return** | 10.7% |
| **Sharpe Ratio** | 0.618 |
| **Max Drawdown** | -28.3% |
| **Total Trades** | 97 |
| **Win Rate** | 51.5% |
| **Signal Accuracy** | 64.2% |
| **Direction Accuracy** | 52.1% |
| **Skill Ratio** | 50.7% |
| **Profit Factor** | 1.80 |
| **Expectancy** | 0.0178 |
| **Tail Ratio** | 1.51 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 259.6% | 339.3% | 79.8% |
| Annualized Return | 12.2% | 10.7% | — |

## Diversity & Concentration

Diversification: **Well-diversified** — close to evenly distributed across trades (HHI ratio: 1.3×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0139 | Ideal for 97 trades: 0.0103 |
| Top-1 Trade | 4.2% of gross profit | Moderate concentration |
| Top-3 Trades | 11.9% of gross profit | Moderate concentration |
| Return ex-Top-1 | 278.3% | Positive without best trade |
| Return ex-Top-3 | 186.1% | Positive without top 3 |
| Max Single Trade | 16.1% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 37 | 7.62% | 281.9% | 7.10% | 17.30 |
| no_signal | 24 | 1.79% | 43.0% | 0.50% | 17.88 |
| direction_wrong_loss | 36 | -4.24% | -152.5% | -4.79% | 15.33 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 97 | 1.78% | 172.4% | 51.5% | 51.5% | 1.06% |

**Best-performing regime:** `unknown` — 97 trades, 172.4% total return, 51.5% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 15 | -4.30% | -64.5% |
| ❌ | ✅ | 15 | 8.02% | 120.3% |
| ✅ | ❌ | 21 | -4.19% | -87.9% |
| ✅ | ✅ | 22 | 7.35% | 161.6% |

### Flip Trades (Signal Wrong → Direction Right)

**28 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **8.1%**
- Total return: **226.4%**
- Average alpha: **5.6%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 28 | 8.09% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 97 | 1.78% | 172.4% | 51.5% | 51.5% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 66 | 2.02% | 133.1% | 51.5% | 51.5% |
| SHORT | 31 | 1.27% | 39.3% | 51.6% | 51.6% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 5 | 31.9% | 6.39% | 80.0% | 80.0% | 24.7% |
| 2017 | 7 | 21.8% | 3.11% | 71.4% | 71.4% | 4.7% |
| 2018 | 3 | 2.0% | 0.68% | 33.3% | 33.3% | -1.3% |
| 2019 | 5 | 34.1% | 6.82% | 80.0% | 80.0% | 15.7% |
| 2020 | 15 | 65.7% | 4.38% | 66.7% | 66.7% | 100.6% |
| 2021 | 11 | -45.1% | -4.10% | 9.1% | 9.1% | -57.7% |
| 2022 | 13 | 45.4% | 3.50% | 61.5% | 61.5% | 40.7% |
| 2023 | 14 | 19.5% | 1.39% | 57.1% | 57.1% | 6.9% |
| 2024 | 11 | 7.5% | 0.68% | 36.4% | 36.4% | -5.4% |
| 2025 | 10 | -15.5% | -1.55% | 40.0% | 40.0% | -32.2% |
| 2026 | 3 | 5.1% | 1.68% | 33.3% | 33.3% | 5.9% |

### Macro Context by Year

**2016** (Strong year: 31.9%, 5 trades)
- No major macro events flagged.

**2017** (Strong year: 21.8%, 7 trades)
- No major macro events flagged.

**2018** (Modestly positive: 2.0%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 34.1%, 5 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 65.7%, 15 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Losing year: -45.1%, 11 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 45.4%, 13 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Strong year: 19.5%, 14 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 7.5%, 11 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -15.5%, 10 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Modestly positive: 5.1%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -45.1% cumulative (trade 35 to trade 46)
**Period:** 2020-09-22 to 2021-12-21 (12 trades)
**Peak cumulative return:** 155.6% → **Trough:** 110.5%

**Macro context during drawdown:**
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2020-09-22 | 2020-11-17 | 1.0000 | 7.40% | unknown | ✅ |
| 2021-02-03 | 2021-02-10 | -1.0000 | -3.97% | unknown | ❌ |
| 2021-02-11 | 2021-04-01 | -1.0000 | -5.07% | unknown | ❌ |
| 2021-04-05 | 2021-04-16 | -1.0000 | -7.08% | unknown | ❌ |
| 2021-04-19 | 2021-05-05 | -1.0000 | -2.76% | unknown | ❌ |
| 2021-05-05 | 2021-09-20 | 1.0000 | -12.38% | unknown | ❌ |
| 2021-09-21 | 2021-10-12 | 1.0000 | -5.05% | unknown | ❌ |
| 2021-10-13 | 2021-11-16 | 1.0000 | 9.89% | unknown | ✅ |
| 2021-11-17 | 2021-12-03 | 1.0000 | -4.73% | unknown | ❌ |
| 2021-12-06 | 2021-12-15 | 1.0000 | -4.51% | unknown | ❌ |
| 2021-12-16 | 2021-12-20 | 1.0000 | -5.82% | unknown | ❌ |
| 2021-12-21 | 2022-01-21 | 1.0000 | -3.59% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 24 | 2.08% | 49.9% | 45.8% |
| 16-30d | 23 | 4.15% | 95.5% | 69.6% |
| 31-50d | 12 | 3.91% | 47.0% | 75.0% |
| 50d+ | 3 | -1.80% | -5.4% | 33.3% |
| 6-15d | 35 | -0.42% | -14.5% | 37.1% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 97 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Well-distributed. HHI of 0.0139 is near the theoretical minimum of 0.0103 for 97 trades.
**Win/loss profile:** 51.5% win rate with 1.80× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (64.2%) exceeded direction accuracy (52.1%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2021 (-45.1%, 11 trades). Macro: Post-COVID Stimulus Rally

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 17d, std 16d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.