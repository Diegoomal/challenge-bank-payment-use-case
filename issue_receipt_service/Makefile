.PHONY: run test lint docs check

run:
	PYTHONPATH=src:.. python3 src/main.py

test:
	pytest

lint:
	flake8 src tests

docs:
	PYTHONPATH=src:.. pdoc configurator domain application adapters -o docs

check: lint test
