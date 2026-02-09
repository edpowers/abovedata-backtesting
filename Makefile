# Run correlation-aware strategy for a specific ticker
# Usage: make run-corr TICKER=DE
TICKER ?= DE

run-corr:
	uv run python -m src.notebooks.correlation_aware_strategy_main --ticker $(TICKER)

install-hooks:
	uv run pre-commit install --install-hooks

run-all:
	uv run pre-commit run --all

