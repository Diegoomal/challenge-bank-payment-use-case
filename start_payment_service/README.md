<!-- AI context: use specs/overview.md as the primary project overview before making code changes. -->
# Start Payment Service

Python service scaffolded with a basic Ports and Adapters, also known as
Hexagonal Architecture, structure.

This service is responsible for the first step of the payment saga: receiving a
payment request, validating the minimum required data, creating the payment
intent, and publishing or exposing the next step for account debit. The business
implementation is intentionally pending.

## Architecture

- `src`: application hexagon.
- `domain`: future payment entities and value objects.
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

- Receive payment start requests.
- Validate payer, merchant, amount, currency, and idempotency data.
- Create a payment record with an initial status.
- Persist payment state in SQLite through a driven persistence port.
- Expose an HTTP API with FastAPI.
- Trigger the next saga step handled by `debit_account_service`.

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
conda env create -n start-payment-env -f env.yml
```

Activate the environment:

```bash
conda activate start-payment-env
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
implemented for payment start behavior.

[author](https://github.com/Diegoomal)
