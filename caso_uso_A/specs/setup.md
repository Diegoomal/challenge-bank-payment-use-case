# Project Setup

This document explains how to prepare the local environment, install
dependencies, run the example application, and execute checks.

## Requirements

The project uses Python 3.10. The recommended environment is described in
`env.yml` and installs the dependencies listed in `requirements.txt`.

Expected tools:

- Conda or Mamba, recommended;
- Python 3.10, if using a virtual environment without Conda;
- `make`, for the `Makefile` shortcuts.

## Option 1: Conda Environment

Create the environment from `env.yml`:

```bash
conda env create -f env.yml
```

The name defined in `env.yml` is `project-env`. Activate it:

```bash
conda activate project-env
```

If you prefer another name, use:

```bash
conda env create -n ports-adapters-env -f env.yml
conda activate ports-adapters-env
```

## Option 2: `venv` Environment

If you do not want to use Conda, create a virtual environment with Python 3.10:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On some systems, the binary may be named `python`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run The Project

Use the `Makefile` target:

```bash
make run
```

This command runs:

```bash
PYTHONPATH=src python3 src/main.py
```

The script runs a demonstrative in-memory CRUD flow.

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

## Expected Structure After Setup

```text
.
├── env.yml
├── requirements.txt
├── Makefile
├── pytest.ini
├── specs/
│   ├── overview.md
│   └── setup.md
├── src/
│   ├── configurator.py
│   ├── main.py
│   ├── adapters/
│   ├── application/
│   └── domain/
└── tests/
    ├── test_for_managing_users.py
    └── test_in_memory_user_repository.py
```

## Common Issues

### `ModuleNotFoundError` When Running Manually

If you execute Python files without `make`, include `src` in `PYTHONPATH`:

```bash
PYTHONPATH=src python3 src/main.py
```

### Conda Environment Created With An Unexpected Name

The `env.yml` file defines the name `project-env`. If any command mentions a
different environment name, confirm which name was used:

```bash
conda env list
```

### Missing Dependencies

Reinstall dependencies in the active environment:

```bash
pip install -r requirements.txt
```

## Recommended Development Flow

1. Activate the environment.
2. Make small changes aligned with Ports and Adapters Architecture.
3. Run `make test`.
4. Run `make lint` when changing imports, formatting, or adding files.
5. Use `make check` before finishing a delivery.
