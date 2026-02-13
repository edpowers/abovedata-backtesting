# Cross-Ticker Multi-Signal Analysis

## Overview

This analysis evaluates whether alternative (UCC) signals from one ticker can predict returns for other tickers, and identifies natural hedges where signals move in opposite directions. Unlike a single-signal approach that only uses the UCC residual, this framework evaluates **23 signal types** per ticker and builds cross-ticker predictive matrices for the statistically significant ones.

## Signal Types Evaluated

Each ticker's `processed_data.parquet` file contains multiple signal columns derived from STL decomposition of the UCC alternative data. The analysis evaluates all of them:

| Category | Signals | Description |
|----------|---------|-------------|
| **UCC Residual** | `resid` | STL residual of the visible column (core UCC surprise signal) |
| **Contemporaneous Correlations** | `contemp_corr_historical`, `contemp_corr_ma`, `filtered_contemp_corr` | How the UCC signal correlates with price at time T (raw, moving average, filtered) |
| **Leading Correlations** | `leading_corr_historical`, `leading_corr_ma`, `filtered_leading_corr` | How the UCC signal at T correlates with price at T+1 (raw, MA, filtered) |
| **Correlation Momentum** | `contemp_corr_momentum`, `leading_corr_momentum` | Rate of change in correlations (z-scored) |
| **Confidence Scores** | `contemp_confidence`, `leading_confidence` | Statistical confidence in the correlation estimates (0.0-0.77 range) |
| **Regime Shifts** | `contemp_regime_shift`, `leading_regime_shift` | Binary indicator (1 = regime shift detected, 0 = no shift) |
| **Cross-Correlations** | `ucc_consensus_corr_historical`, `consensus_revenue_corr_historical`, `ucc_surprise_corr_historical` | Relationships between UCC and consensus/revenue/surprise signals |
| **Beta Coefficients** | `ucc_to_rev_beta`, `ucc_to_surprise_beta` | Regression beta of UCC signal against revenue residual and surprise |
| **Prediction Signals** | `predicted_surprise_direction`, `predicted_surprise_magnitude`, `predicted_surprise_magnitude_v2`, `predicted_rev_resid_calibrated`, `predicted_surprise_calibrated` | Model-based predictions of earnings surprise direction/magnitude |

## Methodology

### Step 1: Signal Panel Construction

For each of the 61 tickers:
- Select the best `visible_col` variant (the one with the most non-null residual observations)
- Load the `processed_data.parquet` from `visible_col=X/` subdirectory
- Extract all 23 signal columns (regime shifts encoded as binary 0/1)
- Result: a panel with one row per (ticker, earnings_date) and all signal values

### Step 2: Per-Ticker Signal Screening

For every (ticker, signal_col) pair, compute:
- **IC (Information Coefficient)**: Spearman rank correlation between the signal value at each earnings date and the forward return over the horizon (default 30 trading days)
- **P-value**: Statistical significance of the IC
- **Direction Accuracy**: Percentage of times sign(signal) == sign(forward_return)
- **Long-Short Spread**: Mean return when signal > 0 minus mean return when signal < 0

A signal is considered **statistically significant** if |IC| >= 0.05 and p-value <= 0.20.

### Step 3: Cross-Ticker IC Matrix

For each signal type that is significant for 3+ tickers, build an NxN cross-signal IC matrix:

- `cross_ic[A][B]` = Spearman rank correlation between ticker A's signal value and ticker B's forward return, measured at ticker A's earnings dates
- This answers: "Does ticker A's leading correlation predict ticker B's stock price movement?"

Additionally, build an NxN signal-signal correlation matrix:
- Correlate ticker A's signal with ticker B's signal on overlapping (nearest within 30 days) earnings dates
- This identifies natural hedges where signals move in opposite directions

### Step 4: Portfolio Opportunities

Extract from the matrices:
- **Cross-predictive pairs**: Off-diagonal entries with |cross-IC| >= 0.10 (or 0.15)
- **Natural hedges**: Ticker pairs with negatively correlated signals (signal_corr < -0.2)

## Output Files

| File | Description |
|------|-------------|
| `signal_screening_all.csv` | Full screening results: one row per (ticker, signal_col) with IC, p-value, accuracy, long-short spread |
| `significant_signals.csv` | Subset of screening where |IC| >= 0.05 and p-value <= 0.20 |
| `best_signal_per_ticker.csv` | For each ticker, the single signal type with the highest |IC| |
| `signal_type_summary.csv` | Aggregated statistics per signal type across all tickers (mean IC, # significant, mean accuracy) |
| `cross_predictive_pairs.csv` | Ticker pairs where one ticker's signal predicts another's returns (|cross-IC| >= 0.10), across all significant signal types |
| `natural_hedges.csv` | Ticker pairs with negatively correlated signals (potential offsetting exposure) |

## How to Read the Results

### `signal_screening_all.csv`

| Column | Meaning |
|--------|---------|
| `ticker` | Stock ticker |
| `visible_col` | Which UCC visible column was used (e.g., `total_universe`, `visible_count`) |
| `signal_col` | Which signal type (e.g., `leading_corr_historical`, `contemp_confidence`) |
| `n_obs` | Total earnings date observations for this ticker |
| `n_paired` | Observations with both a valid signal value and a computable forward return |
| `ic` | Information Coefficient (Spearman rank correlation with forward returns). Positive = signal predicts positive returns; negative = signal predicts negative returns |
| `pval` | P-value for the IC. Lower = more statistically significant |
| `accuracy` | % of times sign(signal) matches sign(forward_return) |
| `ls_spread` | Long-short spread: mean return when signal > 0 minus mean return when signal < 0 |
| `abs_ic` | Absolute value of IC (for ranking) |

### `cross_predictive_pairs.csv`

| Column | Meaning |
|--------|---------|
| `signal_ticker` | Ticker whose signal is being used as the predictor |
| `target_ticker` | Ticker whose returns are being predicted |
| `signal_col` | Which signal type drives the cross-prediction |
| `cross_ic` | Spearman IC between signal_ticker's signal and target_ticker's forward returns |
| `abs_ic` | Absolute cross-IC |
| `direction` | "positive" = signal and returns move together; "negative" = opposite |

### `natural_hedges.csv`

| Column | Meaning |
|--------|---------|
| `ticker_a`, `ticker_b` | The two tickers in the pair |
| `signal_col` | Which signal type has the negative correlation |
| `signal_corr` | Spearman correlation between the two tickers' signals on overlapping dates. Negative = opposite signals = potential natural hedge |

## Usage

```bash
# Default: 30-day horizon, p-value <= 0.20, |IC| >= 0.05
python src/notebooks/cross_ticker_signal_analysis.py

# Custom horizon and thresholds
python src/notebooks/cross_ticker_signal_analysis.py --horizon 60 --pval 0.10 --min-ic 0.10

# All options
python src/notebooks/cross_ticker_signal_analysis.py \
    --horizon 30 \
    --min-obs 8 \
    --start-date 2018-01-01 \
    --pval 0.20 \
    --min-ic 0.05
```

## Lookahead Bias Protection

Since different tickers report earnings on different dates (staggered by weeks within the same fiscal quarter), cross-ticker analysis is vulnerable to lookahead bias. Three protections are in place:

### 1. Signal computation (upstream, in signal pipeline)

All correlation signals (`contemp_corr_historical`, `leading_corr_historical`, etc.) are computed with `shift(1)` internally — the signal at quarter N only uses data through quarter N-1. The first ~8 quarters are burn-in and produce null signals.

### 2. Cross-ticker IC matrix — no lookahead

The cross-IC computation uses **ticker A's `earnings_date`** as the reference point. This is the date A's earnings were publicly reported (typically 25-35 days after quarter end). Ticker B's forward returns are measured from that same public date forward:

```
Timeline:
  A reports Q1 (Apr 25)  →  measure B's returns from Apr 25 forward
```

The signal existed on A's earnings_date. We only look at B's *future* price movement from that date. No future information is used.

### 3. Signal-signal correlation — backward join only

When correlating A's signal with B's signal (for natural hedge detection), we use `join_asof(strategy="backward")`: for each of A's earnings dates, we only match B's **most recent prior** earnings date (within 60 days). This prevents matching a B signal that hasn't been publicly released yet:

```
A reports Q1 (Apr 25): matches B's most recent earnings BEFORE Apr 25
B reports Q1 (May 15): matches A's most recent earnings BEFORE May 15
Both directions computed, then averaged for the symmetric matrix.
```

### What is NOT protected (known limitations)

- **Fiscal quarter alignment**: Tickers may use different fiscal calendars. A ticker with a January fiscal year end reports "Q1" at a different calendar time than one with a March year end. The signals are aligned by `earnings_date` (calendar date), not by fiscal quarter.
- **Stale signals**: With `strategy="backward"` and 60-day tolerance, a match may use a signal that is 1-2 months old. This is conservative (no lookahead) but means the signal-signal correlation reflects lagged, not contemporaneous, relationships.

## Interpretation Notes

- **Small sample sizes**: Many tickers have only 5-15 earnings dates with valid signals. High IC values from small samples (n < 10) should be treated with caution.
- **Multiple testing**: With 23 signal types x 61 tickers = 1,403 tests, some significant results are expected by chance. Focus on signals that are significant across multiple tickers.
- **Regime shifts are sparse**: The `contemp_regime_shift` and `leading_regime_shift` columns are mostly null (encoded as 0), so their IC values reflect whether the presence/absence of a regime shift predicts returns.
- **Cross-IC matrix is not symmetric**: `cross_ic[A][B] != cross_ic[B][A]` because A's signal dates differ from B's.
- **Signal-signal correlation uses backward `join_asof`**: For each of A's earnings dates, we match B's most recent prior earnings date within 60 days. This avoids lookahead but means the correlation captures lagged relationships.
