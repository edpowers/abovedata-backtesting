# Strategy Analysis: momentum_lb10_z0.5_e10d × trailing_stop_5%

**Ticker:** CAT
**Entry:** `momentum_lb10_z0.5_e10d`
**Exit:** `trailing_stop_5%`
**Period:** 2018-10-09 to 2026-02-06
**Generated:** Auto-generated strategy analysis report

## Strategy Description

Entry type: **momentum**

### Entry Parameters

- **lookback_days:** `10`
- **zscore_threshold:** `0.5`
- **zscore_window:** `60`
- **entry_days_before:** `10` — Number of trading days before earnings to enter. Higher values capture the pre-earnings drift but increase exposure to non-earnings price moves

### Exit Parameters

- **Exit type:** `trailing_stop_5%`
  - 5% trailing stop from the high-water mark. Aims to let winners run while cutting losses, but can exit prematurely in volatile markets

## Headline Performance

| Metric | Value |
|---|---|
| **Total Return** | 358.7% |
| **Annualized Return** | 32.2% |
| **Sharpe Ratio** | 1.822 |
| **Max Drawdown** | -28.3% |
| **Total Trades** | 162 |
| **Win Rate** | 47.5% |
| **Signal Accuracy** | 44.3% |
| **Direction Accuracy** | 47.5% |
| **Skill Ratio** | 51.2% |
| **Profit Factor** | 1.65 |
| **Expectancy** | 0.0110 |
| **Tail Ratio** | 2.29 |

### vs Buy & Hold (same ticker)

| Metric | Buy & Hold | Strategy | Difference |
|---|---|---|---|
| Total Return | 954.1% | 358.7% | -595.4% |
| Annualized Return | 23.7% | 32.2% | — |

## Diversity & Concentration

Diversification: **Moderately diversified** — some concentration, generally acceptable (HHI ratio: 1.7×)

| Metric | Value | Notes |
|---|---|---|
| HHI | 0.0105 | Ideal for 162 trades: 0.0062 |
| Top-1 Trade | 4.5% of gross profit | Moderate concentration |
| Top-3 Trades | 12.6% of gross profit | Moderate concentration |
| Return ex-Top-1 | 280.8% | Positive without best trade |
| Return ex-Top-3 | 171.3% | Positive without top 3 |
| Max Single Trade | 20.5% | Largest individual trade return |

## Outcome Analysis

**No ambiguous outcomes observed in this sample:** Every trade with ground truth either got direction right and profited, or got direction wrong and lost. No cases of direction_right_loss or direction_wrong_profit appeared. This may suggest the exit mechanism is reasonably aligned with direction correctness, though the absence of edge cases could also reflect limited sample size or favorable market conditions during the test period.

| Outcome | Count | Avg Return | Total Return | Avg Alpha | Avg Holding |
|---|---|---|---|---|---|
| direction_right_profit | 65 | 6.05% | 393.1% | 5.02% | 11.05 |
| no_signal | 35 | -0.26% | -9.3% | -0.61% | 4.66 |
| direction_wrong_loss | 62 | -3.31% | -205.1% | -3.43% | 4.03 |

## Correlation Regime Performance

Performance by the correlation regime at entry time. Regimes are classified from the contemporaneous and leading correlation between UCC filings and revenue.

**Note on data availability:**
- `unknown` regime = correlation data unavailable at entry (early quarters)
- Signal accuracy excludes trades where consensus data is missing (delayed ~1 year)
- The strategy uses correlation for direction; consensus is only for post-hoc validation

| Correlation Regime | Count | Avg Return | Total Return | Direction Accuracy | Win Rate | Avg Alpha |
|---|---|---|---|---|---|---|
| unknown | 162 | 1.10% | 178.8% | 47.5% | 47.5% | 0.57% |

**Best-performing regime:** `unknown` — 162 trades, 178.8% total return, 47.5% win rate.

## The Correlation Flip Effect

For correlation-aware strategies, the trade direction includes a correlation-based flip: `direction = sign(signal) × sign(correlation)`. The signal can be 'wrong' about the earnings surprise while the trade direction ends up profitable because the correlation flip adjusted the position accordingly.

### Signal × Direction Cross-Tab

| Signal Correct | Trade Direction Correct | Count | Avg Return | Total Return |
|---|---|---|---|---|
| ❌ | ❌ | 48 | -3.37% | -161.6% |
| ❌ | ✅ | 44 | 5.75% | 252.8% |
| ✅ | ❌ | 14 | -3.10% | -43.5% |
| ✅ | ✅ | 21 | 6.68% | 140.3% |

### Flip Trades (Signal Wrong → Direction Right)

**56 trades** where the UCC signal missed the earnings surprise but the correlation flip resulted in a profitable direction.

- Average return: **5.6%**
- Total return: **314.3%**
- Average alpha: **4.9%**

Note: Whether these flips reflect a durable relationship or in-sample coincidence depends on the stability of the correlation regime across market conditions.

Regime distribution of flip trades:

| Correlation Regime | Count | Avg Return |
|---|---|---|
| unknown | 56 | 5.61% |

## Signal Quality Analysis

High = strong confidence + strong correlation; Medium = moderate; Low = weak signals; no_data = confidence unavailable at entry.

**Note:** Signal accuracy is computed against consensus data (beat/miss), which is delayed ~1 year. Trades with missing consensus are excluded from accuracy calculations but still count toward win rate and returns.

| Signal Quality | Count | Avg Return | Total Return | Direction Accuracy | Win Rate |
|---|---|---|---|---|---|
| medium | 66 | 1.30% | 85.7% | 48.5% | 48.5% |
| high | 24 | 2.51% | 60.1% | 50.0% | 50.0% |
| low | 70 | 0.29% | 20.6% | 44.3% | 44.3% |
| no_data | 2 | 6.15% | 12.3% | 100.0% | 100.0% |

## Long vs Short Performance

| Side | Count | Avg Return | Total Return | Win Rate | Direction Accuracy |
|---|---|---|---|---|---|
| LONG | 96 | 1.85% | 177.7% | 53.1% | 53.1% |
| SHORT | 66 | 0.02% | 1.0% | 39.4% | 39.4% |

## Annual Performance

| Year | Trades | Total Return | Avg Return | Win Rate | Direction Accuracy | Total Alpha |
|---|---|---|---|---|---|---|
| 2018 | 15 | 14.7% | 0.98% | 46.7% | 46.7% | 28.4% |
| 2019 | 14 | -16.7% | -1.19% | 42.9% | 42.9% | -42.5% |
| 2020 | 36 | 64.9% | 1.80% | 55.6% | 55.6% | 36.5% |
| 2021 | 21 | 48.0% | 2.29% | 57.1% | 57.1% | 27.8% |
| 2022 | 20 | 53.4% | 2.67% | 50.0% | 50.0% | 54.7% |
| 2023 | 7 | 2.3% | 0.33% | 42.9% | 42.9% | 6.6% |
| 2024 | 12 | 21.5% | 1.79% | 50.0% | 50.0% | 5.2% |
| 2025 | 33 | -29.0% | -0.88% | 27.3% | 27.3% | -43.0% |
| 2026 | 4 | 19.6% | 4.91% | 100.0% | 100.0% | 18.9% |

### Macro Context by Year

**2018** (Strong year: 14.7%, 15 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.

**2019** (Losing year: -16.7%, 14 trades)
- *US-China Trade War Escalation* (volatile): Tariff escalation between US and China created uncertainty for industrial exporters. Deere particularly exposed due to agricultural equipment demand tied to commodity prices and trade flows.
- *Fed Rate Cuts (2019)* (bullish): Three 'insurance' rate cuts as growth slowed. Supportive for capital-intensive industrials but uncertainty remained elevated.

**2020** (Strong year: 64.9%, 36 trades)
- *COVID-19 Crash & Recovery* (bearish): S&P 500 fell ~34% in 23 trading days. Industrial stocks hit harder due to supply chain disruption and demand collapse. DE fell from $180 to $115 before recovering.
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2021** (Strong year: 48.0%, 21 trades)
- *Post-COVID Stimulus Rally* (bullish): Unprecedented fiscal and monetary stimulus drove a broad equity rally. Agricultural commodity boom and infrastructure spending expectations boosted DE from ~$130 to ~$390. Strong negative UCC-price correlation period — falling UCC filings while revenues surged.

**2022** (Strong year: 53.4%, 20 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2022 Bear Market* (bearish): S&P 500 peak-to-trough decline of ~25%. Industrials sold off on recession fears. Weak correlation signals during this period — macro dominated micro.

**2023** (Modestly positive: 2.3%, 7 trades)
- *Fed Tightening Cycle* (volatile): Aggressive rate hikes from 0% to 5.25-5.50%. Growth-sensitive industrials whipsawed as markets repriced duration risk. DE traded in a wide $280-$450 range with sharp reversals.
- *2023 Soft Landing Rally* (bullish): Growing confidence in a soft landing. DE benefited from strong ag cycle and precision agriculture demand. Correlation regimes began shifting as rate expectations stabilized.

**2024** (Strong year: 21.5%, 12 trades)
- *2024 Election Year Uncertainty* (volatile): Policy uncertainty around tariffs, trade, and fiscal direction created headwinds for export-oriented industrials. DE faced ag cycle downturn concerns.

**2025** (Losing year: -29.0%, 33 trades)
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**2026** (Strong year: 19.6%, 4 trades)
- No major macro events flagged.


## Worst Drawdown Period

**Drawdown:** -43.4% cumulative (trade 126 to trade 149)
**Period:** 2025-01-15 to 2025-10-15 (24 trades)
**Peak cumulative return:** 192.6% → **Trough:** 149.2%

**Macro context during drawdown:**
- *2025 Tariff Escalation* (volatile): New tariff announcements on steel, aluminum, and reciprocal tariffs created fresh uncertainty for industrial supply chains. Regime shifts in correlation structure as market repriced trade exposure.
- *2025 H2 Recovery* (bullish): Trade deal optimism and rate cut expectations drove industrial recovery. DE recovered on strong order book and precision ag technology demand.

**Trades during drawdown:**

| Entry Date | Exit Date | Direction | Trade Return | Correlation Regime | Trade Direction Correct |
|---|---|---|---|---|---|
| 2025-01-15 | 2025-01-28 | 1.0000 | 4.49% | unknown | ✅ |
| 2025-01-29 | 2025-01-30 | 1.0000 | -4.64% | unknown | ❌ |
| 2025-01-31 | 2025-02-05 | 1.0000 | -3.39% | unknown | ❌ |
| 2025-02-06 | 2025-02-13 | 1.0000 | -3.22% | unknown | ❌ |
| 2025-02-14 | 2025-02-21 | 1.0000 | -3.76% | unknown | ❌ |
| 2025-02-24 | 2025-03-03 | 1.0000 | -2.03% | unknown | ❌ |
| 2025-03-04 | 2025-03-13 | 1.0000 | 2.01% | unknown | ✅ |
| 2025-03-14 | 2025-03-28 | 1.0000 | -2.93% | unknown | ❌ |
| 2025-03-31 | 2025-04-03 | 1.0000 | -7.29% | unknown | ❌ |
| 2025-04-04 | 2025-04-07 | 1.0000 | -2.78% | unknown | ❌ |
| 2025-04-08 | 2025-04-09 | 1.0000 | 9.88% | unknown | ✅ |
| 2025-04-10 | 2025-04-15 | 1.0000 | 1.48% | unknown | ✅ |
| 2025-04-15 | 2025-04-21 | -1.0000 | 2.49% | unknown | ✅ |
| 2025-04-22 | 2025-04-23 | -1.0000 | -1.58% | unknown | ❌ |
| 2025-04-24 | 2025-04-30 | -1.0000 | -0.79% | unknown | ❌ |
| 2025-05-01 | 2025-05-08 | -1.0000 | -3.28% | unknown | ❌ |
| 2025-05-09 | 2025-05-12 | -1.0000 | -5.20% | unknown | ❌ |
| 2025-05-13 | 2025-05-27 | -1.0000 | 0.29% | unknown | ✅ |
| 2025-05-28 | 2025-06-06 | -1.0000 | -1.10% | unknown | ❌ |
| 2025-06-09 | 2025-06-24 | -1.0000 | -4.18% | unknown | ❌ |
| 2025-06-25 | 2025-06-30 | -1.0000 | -4.48% | unknown | ❌ |
| 2025-07-01 | 2025-07-09 | -1.0000 | -2.88% | unknown | ❌ |
| 2025-07-10 | 2025-07-22 | -1.0000 | -2.54% | unknown | ❌ |
| 2025-10-15 | 2025-10-22 | 1.0000 | -3.49% | unknown | ❌ |

## Holding Period Analysis

| Bucket | Count | Avg Return | Total Return | Win Rate |
|---|---|---|---|---|
| 1-5d | 96 | -1.00% | -95.8% | 32.3% |
| 16-30d | 17 | 7.34% | 124.7% | 100.0% |
| 31-50d | 2 | 9.76% | 19.5% | 100.0% |
| 6-15d | 47 | 2.77% | 130.3% | 57.4% |

## Win/Loss Streaks

- **Max consecutive wins:** 6
- **Max consecutive losses:** 6

## Observations & Caveats

**Sample size:** 162 trades provides a reasonable sample for most metrics, though tail statistics (max drawdown, streaks) remain noisy.
**Diversification:** Moderate concentration. Returns remain positive excluding top 3 trades (171.3%).
**Win/loss profile:** Profit factor of 1.65 with 47.5% win rate. Positive in-sample but the margin is thin enough that transaction cost assumptions and execution slippage matter.
**Signal vs Direction:** Direction accuracy (47.5%) exceeded signal accuracy (44.3%) in this sample, suggesting the correlation flip may have contributed positively. This relationship should be tested across different market regimes.

### Known Vulnerabilities

- **Worst year:** 2025 (-29.0%, 33 trades). Macro: 2025 Tariff Escalation, 2025 H2 Recovery

### ⚠️ Robustness Red Flags

- **VARIABLE_HOLDING:** Holding period varies widely (mean 7d, std 7d). Combined with high win rate, this suggests the strategy holds losing positions longer until they recover — a form of survivorship bias in exits.

### General Caveats

- All metrics are in-sample. Out-of-sample and cross-asset validation is necessary before drawing conclusions about edge durability.
- Transaction costs are modeled but execution slippage, market impact, and liquidity constraints are not.
- Correlation regimes are estimated from historical data and may shift unpredictably.