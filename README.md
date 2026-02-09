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
