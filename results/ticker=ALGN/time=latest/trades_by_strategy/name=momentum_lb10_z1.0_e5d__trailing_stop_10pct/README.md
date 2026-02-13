# Strategy Analysis: momentum_lb10_z1.0_e5d × trailing_stop_10%

**Ticker:** ALGN
**Entry:** `momentum_lb10_z1.0_e5d`
**Exit:** `trailing_stop_10%`
**Period:** 2018-04-18 to 2025-07-23
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `10`
- **zscore_threshold:** `1.0`
- **zscore_window:** `60`
- **entry_days_before:** `5` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_10%`
  - 10% trailing stop. More room for normal volatility, targets larger trends

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 121.5% |
| **Annualized Return** | 13.6% |
| **Sharpe Ratio** | 1.081 |
| **Max Drawdown** | -11.0% |
| **Total Trades** | 20 |
| **Win Rate** | 45.0% |
| **Signal Accuracy** | 45.5% |
| **Direction Accuracy** | 45.0% |
| **Skill Ratio** | 47.1% |
| **Profit Factor** | 2.61 |
| **Expectancy** | 0.0488 |
| **Tail Ratio** | 3.23 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | -26.3% | 121.5% | 147.8% |
| Annualized Return | -4.1% | 13.6% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.7×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0870 | Ideal for 20 trades: 0.0500 |
| Top-1 Trade | 23.8% of gross profit | ⚠️ Notable concentration |
| Top-3 Trades | 58.0% of gross profit | ⚠️ Notable concentration |
| Return ex-Top-1 | 60.8% | Positive without best trade |
| Return ex-Top-3 | -0.4% | Negative without top 3 |
| Max Single Trade | 37.7% | Largest individual trade return |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 20 | 4.88% | 97.6% | 45.0% | 45.0% | 4.88% |

**Best-performing regime:** `unknown` — 20 trades, 97.6% total return, 45.0% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 6 | -5.52% | -33.1% |
| ❌ | ✅ | 6 | 19.74% | 118.5% |
| ✅ | ❌ | 3 | -6.58% | -19.7% |
| ✅ | ✅ | 2 | 10.80% | 21.6% |

### Flip Trades (Signal Wrong → Direction Right)

**7 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **19.5%**
- Total return: **136.7%**
- Average alpha: **19.5%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 7 | 19.53% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| no_data | 20 | 4.88% | 97.6% | 45.0% | 45.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 20 | 4.88% | 97.6% | 45.0% | 45.0% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 3 | 38.9% | 12.97% | 66.7% | 66.7% | 38.9% |
| 2019 | 4 | 58.0% | 14.49% | 75.0% | 75.0% | 58.0% |
| 2020 | 1 | -2.0% | -2.01% | 0.0% | 0.0% | -2.0% |
| 2021 | 3 | 6.9% | 2.30% | 33.3% | 33.3% | 6.9% |
| 2022 | 3 | -10.6% | -3.52% | 33.3% | 33.3% | -10.6% |
| 2024 | 3 | -4.0% | -1.34% | 33.3% | 33.3% | -4.0% |
| 2025 | 3 | 10.4% | 3.48% | 33.3% | 33.3% | 10.4% |

### Macro Context by Year

**2018** (Strong year: 38.9%, 3 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Strong year: 58.0%, 4 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Roughly flat: -2.0%, 1 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Modestly positive: 6.9%, 3 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Losing year: -10.6%, 3 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2024** (Roughly flat: -4.0%, 3 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Strong year: 10.4%, 3 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.


## Worst Drawdown Period

**Drawdown:** -24.0% cumulative (trade 13 to trade 16)
**Period:** 2022-07-26 to 2024-07-26 (4 trades)
**Peak cumulative return:** 102.2% → **Trough:** 78.3%

**Macro context during drawdown:**
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2022-07-26 | 2022-08-09 | 1.0000 | 8.65% | unknown | ✅ |
| 2022-08-10 | 2022-08-22 | 1.0000 | -11.04% | unknown | ❌ |
| 2024-07-17 | 2024-07-25 | 1.0000 | -9.79% | unknown | ❌ |
| 2024-07-26 | 2024-08-02 | 1.0000 | -3.16% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 5 | -4.52% | -22.6% | 0.0% |
| 16-30d | 3 | 9.87% | 29.6% | 66.7% |
| 31-50d | 3 | 22.98% | 68.9% | 100.0% |
| 50d+ | 1 | 29.56% | 29.6% | 100.0% |
| 6-15d | 8 | -0.98% | -7.9% | 37.5% |

## Win/Loss Streaks

- **Max consecutive wins:** 3
- **Max consecutive losses:** 3

## Observations & Caveats

**Sample size:** ⚠️ Only 20 trades — all metrics should be interpreted with caution. This is likely insufficient for reliable inference.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (-0.4%).
**Win/loss profile:** Profit factor of 2.61 with 45.0% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Signal accuracy (45.5%) and direction accuracy (45.0%) are similar, suggesting the correlation flip had limited net impact in this sample.

### Known Vulnerabilities

- **Worst year:** 2022 (-10.6%, 3 trades). Macro: Fed Tightening Cycle, 2022 Bear Market

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 18d, std 18d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.