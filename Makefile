.PHONY: install test lint clean

install:
	pip install -e ".[dev]"

test:
	python -m pytest --tb=short -q

lint:
	python -m ruff check src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache dist build *.egg-info
