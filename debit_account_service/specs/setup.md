# Debit Account Service Setup

This document explains how to prepare the local environment, install
dependencies, run the current scaffold, and execute checks.

## Requirements

The project uses Python 3.10. The recommended environment is described in
`env.yml` and installs the dependencies listed in `requirements.txt`.

Expected tools:

- Conda or Mamba, recommended;
- Python 3.10, if using a virtual environment without Conda;
- `make`, for the `Makefile` shortcuts.

Runtime dependencies include:

- FastAPI, planned for the HTTP driving adapter;
- a SQLite dependency through `aiosqlite`, plus Python's built-in `sqlite3`
  module when synchronous access is enough.

## Conda Environment

```bash
conda env create -n debit-account-service-env -f env.yml
conda activate debit-account-service-env
```

## Run The Current Scaffold

Use the `Makefile` target:

```bash
make run
```

This command runs:

```bash
PYTHONPATH=src python3 src/main.py
```

The current script still runs the template example. It should be replaced by the
account debit entry point when the service is implemented.

## Future FastAPI Execution

When the HTTP adapter is implemented, the expected local command is:

```bash
uvicorn src.main:app --reload
```

Add `uvicorn` to `requirements.txt` when the FastAPI application object is
introduced.

## Run Tests

Execute:

```bash
make test
```

Or run `pytest` directly:

```bash
pytest
```

The `pytest.ini` file configures `pythonpath = src`, so manually exporting
`PYTHONPATH` is not necessary for tests.

## Run Lint

Execute:

```bash
make lint
```

This command runs:

```bash
flake8 src tests
```

## Run All Checks

Execute:

```bash
make check
```

This target runs lint and tests:

```bash
make lint
make test
```

## Generate Documentation

Execute:

```bash
make docs
```

This command uses `pdoc` to generate documentation in `docs/`:

```bash
PYTHONPATH=src pdoc configurator domain application adapters -o docs
```

## Recommended Development Flow

1. Activate the environment.
2. Replace template user code with account debit domain code.
3. Define ports before concrete adapters.
4. Implement SQLite persistence behind driven ports.
5. Add FastAPI routes as a driving adapter.
6. Run `make test`.
7. Run `make lint` when changing imports, formatting, or adding files.
