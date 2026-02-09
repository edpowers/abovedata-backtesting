# AboveData Backtesting Framework

An institutional-grade event study backtesting engine for alternative data, built with a paranoid focus on avoiding look-ahead bias.

**Core Principle:** *"Trade on what was known, not what is true now."*

## What This Is

This framework backtests trading strategies using **visible_revenue** and **visible_count** signals as leading indicators of corporate revenue trends. These signals are derived from UCC (Uniform Commercial Code) filings—cleaned and aggregated measures of secured lending activity. When companies finance equipment purchases or inventory, lenders file UCCs. These filings become public record and can signal revenue trends before earnings announcements.

The key insight: the relationship between visible signals and revenue isn't static. Sometimes higher signal values → more revenue (positive correlation), sometimes higher values → less revenue (negative correlation). The **correlation-aware** strategies in this framework use this dynamic relationship to determine trade direction:

```
trade_direction = sign(signal) × sign(historical_correlation)
```

## Quick Start

```bash
# Install dependencies
uv sync

# Run the full backtesting suite (benchmark + strategy grid search) for default ticker (DE)
make run-main

# Run only the correlation-aware strategy grid search
make run-corr TICKER=DE
```

Results are saved to `results/ticker=<TICKER>/time=latest/`.

## Project Structure

```
src/
├── abovedata_backtesting/
│   ├── benchmarks/         # Benchmark models and result handling
│   │   ├── benchmark_models.py    # Benchmark strategy definitions
│   │   └── benchmark_results.py   # Benchmark result aggregation
│   ├── data_loaders/       # Load signal and market data
│   │   ├── load_market_data.py    # yfinance market data retrieval
│   │   ├── load_signal_data.py    # visible_revenue/visible_count loading
│   │   └── utils.py               # Shared loader utilities
│   ├── entries/            # Entry signal generators
│   │   ├── correlation_aware_entry.py  # Core correlation-aware logic
│   │   ├── entry_context.py            # Entry context and state
│   │   └── entry_signals.py            # Momentum, threshold, divergence
│   ├── exits/              # Exit strategy implementations
│   │   └── exit_strategies.py          # SL/TP, trailing stop, signal change
│   ├── model/              # Data models and metrics
│   │   ├── metrics.py             # Performance metric calculations
│   │   └── strategy_models.py     # Strategy configuration models
│   ├── processors/         # Strategy execution engine
│   │   ├── benchmark_processor.py # Benchmark strategy execution
│   │   ├── signal_processor.py    # Signal preprocessing
│   │   └── strategy_processor.py  # Main strategy execution
│   └── trades/             # Trade analysis and reporting
│       ├── analysis_utils.py      # Trade analysis helpers
│       ├── report_generator.py    # Markdown report generation
│       ├── robustness_tests.py    # Strategy robustness validation
│       ├── trade_analyzer.py      # Trade-level analysis
│       ├── trade_log.py           # Trade logging utilities
│       └── trade_save_results.py  # Result persistence
└── notebooks/
    ├── benchmark_main.py                   # Benchmark analysis
    ├── correlation_aware_strategy_main.py  # Main strategy grid search
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
When entering before earnings (e.g., 20 trading days early), the full quarter's signal data isn't available yet.
- **Fix:** Estimate the signal as a fraction of the expected final value based on calendar position within the quarter
- **Constraint:** `entry_days_before` is measured in **trading days** (not calendar days). Max safe value is ~35-45 trading days (quarter start). Values beyond this would require trading on data that doesn't exist yet.
- **Example:** At 30 trading days (~6 weeks) before earnings, roughly 50% of the quarter has elapsed, so the signal is scaled accordingly.

## Strategy Types

### Correlation-Aware (Primary)
Uses signal direction × historical correlation to determine trade direction. Works especially well in "strong negative" correlation regimes where the relationship has flipped.

### Momentum Baseline
Price-only strategies for comparison. No fundamental input—pure technical momentum with z-score thresholds.

### Signal-Based
- **Threshold:** Enter when signal exceeds threshold
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
