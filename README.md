# AboveData Backtesting Framework

An institutional-grade event study backtesting engine for alternative data, built with a paranoid focus on avoiding look-ahead bias.

**Core Principle:** *"Trade on what was known, not what is true now."*

## What This Is

This framework backtests trading strategies using **UCC (Uniform Commercial Code) filing data** as a leading indicator of corporate revenue trends. UCC filings capture secured lending activity—when companies finance equipment purchases or inventory, lenders file UCCs. These filings become public record and can signal revenue trends before earnings announcements.

The key insight: the relationship between UCC filings and revenue isn't static. Sometimes more filings → more revenue (positive correlation), sometimes more filings → less revenue (negative correlation). The **correlation-aware** strategies in this framework use this dynamic relationship to determine trade direction:

```
trade_direction = sign(UCC_signal) × sign(historical_correlation)
```

## Quick Start

```bash
# Install dependencies
uv sync

# Run the full backtesting suite (benchmark + strategy grid search) for default ticker (DE)
make run-main

# Run for a specific ticker
make run-main TICKER=AGCO

# Run only the correlation-aware strategy grid search
make run-corr TICKER=DE
```

Results are saved to `results/ticker=<TICKER>/time=<TIMESTAMP>/`.

## Example Results

See the [DE (Deere & Co) top strategy analysis](results/ticker=DE/time=20260208_145945/top_strategy/) for a complete breakdown of the best-performing strategy, including:

- **641.6% total return** over 84 trades (2018-2026)
- **0.66 Sharpe ratio** with -24.8% max drawdown
- **57.1% win rate** with 2.16× profit factor
- Detailed correlation regime analysis
- Macro context for each trading year
- Full trade-by-trade breakdown

## Project Structure

```
src/
├── abovedata_backtesting/
│   ├── data_loaders/       # Load signal and market data
│   ├── entries/            # Entry signal generators
│   │   ├── correlation_aware_entry.py  # Core correlation-aware logic
│   │   └── entry_signals.py            # Momentum, threshold, divergence
│   ├── exits/              # Exit strategy implementations
│   │   └── exit_strategies.py          # SL/TP, trailing stop, signal change
│   ├── processors/         # Strategy execution engine
│   ├── trades/             # Trade analysis and reporting
│   └── model/              # Data models and metrics
└── notebooks/
    ├── benchmark_main.py       # Benchmark analysis
    └── gated_strategy_main.py  # Main strategy grid search
```

## The Iron Rules

This framework enforces strict anti-look-ahead bias measures:

### Rule 1: AMC Gap Defense
Earnings are often released After Market Close. You cannot buy at the closing price of the report day.
- **Fix:** `Trade_Date = Signal_Date + 1 Day`
- **Validation:** If 1D Sharpe > 3.0, you're likely capturing the overnight gap (a bug)

### Rule 2: Three-Date Timestamping
Every data point has:
1. **Period End:** Fiscal quarter end
2. **Report Date:** UTC timestamp of public release
3. **Trade Date:** Execution timestamp (Report Date + 1)

### Rule 3: Expanding Window Z-Scores
Never use global quantiles—they leak future volatility.
- **Fix:** Use `rolling(min_periods=N).mean()` on **shifted** (t-1) data
- **Constraint:** Never include observation t in the distribution used to score observation t

### Rule 4: Intra-Quarter Signal Estimation
When entering before earnings (e.g., 30 trading days early), the full quarter's UCC data isn't available yet.
- **Fix:** Estimate the signal as a fraction of the expected final value based on calendar position within the quarter
- **Constraint:** `entry_days_before` is measured in **trading days** (not calendar days). Max safe value is ~35-45 trading days (quarter start). Values beyond this would require trading on data that doesn't exist yet.
- **Example:** At 30 trading days (~6 weeks) before earnings, roughly 50% of the quarter has elapsed, so the signal is scaled accordingly.

## Strategy Types

### Correlation-Aware (Primary)
Uses UCC signal direction × historical correlation to determine trade direction. Works especially well in "strong negative" correlation regimes where the relationship has flipped.

### Momentum Baseline
Price-only strategies for comparison. No fundamental input—pure technical momentum with z-score thresholds.

### Signal-Based
- **Threshold:** Enter when UCC signal exceeds threshold
- **Confirmation:** Signal + momentum alignment
- **Divergence:** Signal and price moving in opposite directions

## Exit Strategies

- **Stop-Loss / Take-Profit:** Asymmetric exits (e.g., -5% SL, +10% TP)
- **Trailing Stop:** Lock in gains as price moves favorably
- **Fixed Holding:** Exit after N days or at next signal date
- **Signal Change:** Exit when signal reverses

## Return Calculations

### Total Return
**Compounded return** across all round-trip trades:

```
total_return = ∏(1 + r_i) - 1
```

Where `r_i` is the return of trade `i`, calculated as:
```
trade_return = (exit_price / entry_price - 1) × direction
```

This measures the actual P&L from executing the strategy, compounding each trade's gains/losses sequentially.

### Annualized Return
Converts the total return to an **equivalent annual rate** using the CAGR formula:

```
annualized_return = (1 + total_return)^(1/n_years) - 1
```

Where `n_years = n_trading_days / 252` (assuming 252 trading days per year).

**Example:** A strategy with 641.6% total return over ~7.6 years (2018-2026) yields:
```
annualized = (1 + 6.416)^(1/7.6) - 1 ≈ 13.7%
```

This allows fair comparison between strategies with different holding periods.

## Key Dependencies

- **polars** (≥1.37): Fast DataFrame operations
- **yfinance** (≥1.0): Market data retrieval
- **altair** (≥6.0): Visualization
- **pydantic** (≥2.12): Data validation
- **statsmodels** (≥0.14): Statistical analysis

## Output Format

Each backtest run creates:
```
results/ticker=<TICKER>/time=<TIMESTAMP>/
├── metadata.json           # Run configuration
├── top_strategy/
│   ├── README.md           # Detailed strategy analysis
│   ├── metadata.json       # Strategy parameters and metrics
│   └── trades.csv          # Individual trade records
└── trades_by_strategy/
    └── name=<STRATEGY>/
        ├── README.md
        └── <strategy>.csv
```

## License

Proprietary. Contact [ed@abovedata.io](mailto:ed@abovedata.io) for licensing inquiries.
