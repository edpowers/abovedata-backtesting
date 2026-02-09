# Strategy Analysis: momentum_lb20_z0.5_e0d × trailing_stop_10%

**Ticker:** AGCO
**Entry:** `momentum_lb20_z0.5_e0d`
**Exit:** `trailing_stop_10%`
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

- **Exit type:** `trailing_stop_10%`
  - 10% trailing stop. More room for normal volatility, targets larger trends

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 404.7% |
| **Annualized Return** | 27.3% |
| **Sharpe Ratio** | 1.182 |
| **Max Drawdown** | -30.0% |
| **Total Trades** | 64 |
| **Win Rate** | 54.7% |
| **Signal Accuracy** | 61.2% |
| **Direction Accuracy** | 54.7% |
| **Skill Ratio** | 51.0% |
| **Profit Factor** | 2.35 |
| **Expectancy** | 0.0293 |
| **Tail Ratio** | 2.43 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 222.5% | 404.7% | 182.2% |
| Annualized Return | 13.5% | 27.3% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.6×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0257 | Ideal for 64 trades: 0.0156 |
| Top-1 Trade | 8.0% of gross profit | Moderate concentration |
| Top-3 Trades | 21.6% of gross profit | Moderate concentration |
| Return ex-Top-1 | 299.7% | Positive without best trade |
| Return ex-Top-3 | 168.0% | Positive without top 3 |
| Max Single Trade | 26.3% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 26 | 9.49% | 246.6% | 9.49% | 27.88 |
| no_signal | 13 | 4.04% | 52.5% | 4.04% | 26.31 |
| direction_wrong_loss | 25 | -4.46% | -111.5% | -4.46% | 14.20 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 64 | 2.93% | 187.6% | 54.7% | 54.7% | 2.93% |

**Best-performing regime:** `unknown` — 64 trades, 187.6% total return, 54.7% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 9 | -3.73% | -33.6% |
| ❌ | ✅ | 12 | 8.30% | 99.6% |
| ✅ | ❌ | 16 | -4.87% | -77.9% |
| ✅ | ✅ | 14 | 10.50% | 147.1% |

### Flip Trades (Signal Wrong → Direction Right)

**21 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **8.5%**
- Total return: **179.5%**
- Average alpha: **8.5%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 21 | 8.55% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 64 | 2.93% | 187.6% | 54.7% | 54.7% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 33 | 4.64% | 153.1% | 60.6% | 60.6% |
| SHORT | 31 | 1.11% | 34.5% | 48.4% | 48.4% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2016 | 1 | 26.3% | 26.26% | 100.0% | 100.0% | 26.3% |
| 2017 | 5 | 14.8% | 2.95% | 80.0% | 80.0% | 14.8% |
| 2018 | 7 | -24.8% | -3.54% | 14.3% | 14.3% | -24.8% |
| 2019 | 3 | 2.7% | 0.91% | 33.3% | 33.3% | 2.7% |
| 2020 | 10 | 106.9% | 10.69% | 80.0% | 80.0% | 106.9% |
| 2021 | 4 | 15.5% | 3.87% | 75.0% | 75.0% | 15.5% |
| 2022 | 10 | 20.9% | 2.09% | 40.0% | 40.0% | 20.9% |
| 2023 | 4 | 0.7% | 0.17% | 50.0% | 50.0% | 0.7% |
| 2024 | 9 | 9.8% | 1.09% | 55.6% | 55.6% | 9.8% |
| 2025 | 8 | 2.3% | 0.29% | 50.0% | 50.0% | 2.3% |
| 2026 | 3 | 12.6% | 4.19% | 66.7% | 66.7% | 12.6% |

### Macro Context by Year

**2016** (Strong year: 26.3%, 1 trades)
- No major macro events flagged.

**2017** (Strong year: 14.8%, 5 trades)
- No major macro events flagged.

**2018** (Losing year: -24.8%, 7 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Modestly positive: 2.7%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 106.9%, 10 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 15.5%, 4 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 20.9%, 10 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 0.7%, 4 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Modestly positive: 9.8%, 9 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Modestly positive: 2.3%, 8 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 12.6%, 3 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -43.4% cumulative (trade 6 to trade 15)
**Period:** 2017-11-30 to 2019-05-02 (10 trades)
**Peak cumulative return:** 41.0% → **Trough:** -2.4%

**Macro context during drawdown:**
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2017-11-30 | 2018-05-08 | -1.0000 | 10.77% | unknown | ✅ |
| 2018-05-09 | 2018-05-21 | -1.0000 | -7.50% | unknown | ❌ |
| 2018-05-22 | 2018-07-31 | -1.0000 | 6.02% | unknown | ✅ |
| 2018-08-01 | 2018-08-13 | 1.0000 | -4.98% | unknown | ❌ |
| 2018-08-14 | 2018-10-11 | 1.0000 | -3.95% | unknown | ❌ |
| 2018-10-12 | 2018-10-23 | 1.0000 | -5.19% | unknown | ❌ |
| 2018-10-30 | 2018-12-06 | -1.0000 | -7.76% | unknown | ❌ |
| 2018-12-07 | 2019-01-04 | -1.0000 | -1.39% | unknown | ❌ |
| 2019-01-07 | 2019-01-18 | -1.0000 | -8.79% | unknown | ❌ |
| 2019-05-02 | 2019-05-17 | 1.0000 | -9.83% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 10 | 6.15% | 61.5% | 80.0% |
| 16-30d | 13 | 3.25% | 42.2% | 61.5% |
| 31-50d | 12 | 5.37% | 64.4% | 66.7% |
| 50d+ | 6 | 13.23% | 79.4% | 100.0% |
| 6-15d | 23 | -2.61% | -60.0% | 21.7% |

## Win/Loss Streaks

- **Max consecutive wins:** 5
- **Max consecutive losses:** 7

## Observations & Caveats

**Sample size:** 64 trades is a moderate sample. Point estimates may have wide confidence intervals, particularly for Sharpe and drawdown.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (168.0%).
**Win/loss profile:** 54.7% win rate with 2.35× profit factor — in this sample, winning trades tended to be larger than losing trades. Whether this reflects a durable edge or favorable conditions during the test period warrants further investigation (e.g., out-of-sample testing, different tickers).
**Signal vs Direction:** Signal accuracy (61.2%) exceeded direction accuracy (54.7%), suggesting the correlation flip occasionally inverted a correct signal. Net impact on returns depends on the magnitude of flip-induced losses vs. flip-induced gains.

### Known Vulnerabilities

- **Worst year:** 2018 (-24.8%, 7 trades). Macro: US-China Trade War Escalation

### ⚠️ Robustness Red Flags

- **BETA_DISGUISED:** Stock had 222.5% buy-and-hold return (aligned to strategy period: None to None), yet 31 short trades returned 34.5% total. Winning shorts in an uptrending stock suggests mean-reversion capture within the trend, not directional prediction from signal data.
- **VARIABLE_HOLDING:** Holding period varies widely (mean 22d, std 22d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.