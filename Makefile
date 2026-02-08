

# Run correlation-aware strategy for a specific ticker
# Usage: make run-corr TICKER=DE
TICKER ?= DE

run-main:
	uv run python -m src.notebooks.benchmark_main
	uv run python -m src.notebooks.correlation_aware_strategy_main --ticker $(TICKER)

run-corr:
	uv run python -m src.notebooks.correlation_aware_strategy_main --ticker $(TICKER)

