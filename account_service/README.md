<!-- AI context: use specs/overview.md as the primary project overview before making code changes. -->
# Debit Account Service

Python service scaffolded with a basic Ports and Adapters, also known as
Hexagonal Architecture, structure.

This service is responsible for the account debit step of the payment saga:
receiving a debit request from the started payment flow, validating account
availability, recording the debit attempt, and returning or publishing the debit
result. The business implementation is intentionally pending.

## Architecture

- `src`: application hexagon.
- `domain`: future account debit entities and value objects.
- `application/ports`: operations offered to external actors and resources
  required by the application.
- `application/services`: future application services that implement driving
  ports.
- `adapters`: concrete adapters for API, CLI, persistence, and messaging.
- `configurator.py`: dependency wiring.
- `main.py`: executable entry point.

The application core must depend only on its domain and interfaces. Adapters
depend inward on the application core.

## Planned Responsibilities

- Receive debit requests for a started payment.
- Validate account identity, balance, currency, and idempotency data.
- Persist debit attempts and their status in SQLite.
- Expose an HTTP API with FastAPI.
- Publish success for payment confirmation or failure for reversal.

## Project Structure

```text
root/
├── src/
│   ├── configurator.py
│   ├── main.py
│   ├── domain/
│   ├── application/
│   │   ├── ports/
│   │   └── services/
│   └── adapters/
│       ├── cli/
│       ├── persistence/
│       └── messaging/
├── specs/
├── tests/
└── requirements.txt
```

## Environment

Create the Conda environment:

```bash
conda env create -n debit-account-env -f env.yml
```

Activate the environment:

```bash
conda activate debit-account-env
```

Or use `venv`:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Commands

- `make run`: runs the current scaffold entry point with `python3`.
- `make test`: runs the test suite.
- `make lint`: checks code style.
- `make docs`: generates the `docs/` directory.
- `make check`: runs lint and tests.

## Current Status

This service currently has a basic hexagonal scaffold copied from the template.
Domain, ports, services, adapters, and tests still need to be renamed and
implemented for account debit behavior.

[author](https://github.com/Diegoomal)
