# Start Payment Service Overview

This repository contains the scaffold for `start_payment_service`, a Python
service that will follow Ports and Adapters Architecture, also known as
Hexagonal Architecture.

The service belongs to a payment saga. It is the first step and should prepare a
payment intent before the saga continues to `debit_account_service`.

Use this document as the initial context when working with AI coding agents such
as Codex, Claude, or similar tools.

## Goal

The service will start a payment request.

Planned payment fields:

- `id`
- `payer_account_id`
- `merchant_id`
- `amount`
- `currency`
- `status`
- `idempotency_key`
- `created_at`
- `updated_at`

Planned operations for the driving port:

- start a payment;
- get a payment by ID;
- list payments by payer or merchant;
- mark the payment as ready for debit;
- reject invalid payment requests.

The initial business rules should include:

- amount must be greater than zero;
- payer and merchant identifiers are required;
- idempotency keys must prevent duplicate payment creation;
- a started payment must be persisted before any next saga step is triggered.

## Architecture

The project follows a hexagonal structure directly under `src`:

```text
src/
├── configurator.py
├── main.py
├── domain/
├── application/
│   ├── ports/
│   └── services/
└── adapters/
    ├── cli/
    ├── persistence/
    └── messaging/
```

### `domain`

Will contain pure payment entities and value objects. This package must not
depend on FastAPI, SQLite, messaging clients, or concrete adapters.

### `application/ports`

Will contain the application ports:

- driving ports for API, CLI, or message consumers that start payments;
- driven ports for persistence, idempotency lookup, and saga/event publishing.

Driving ports are called by adapters. Driven ports are implemented by adapters.

### `application/services`

Will contain use cases that implement the driving ports and enforce payment
start rules. Services may depend on the domain and interfaces, but not on
concrete adapters.

### `adapters`

Will contain concrete adapters around the hexagon:

- FastAPI HTTP routes as a driving adapter;
- SQLite persistence as a driven adapter;
- messaging producer adapter for the next saga step;
- CLI only as a development or demonstration adapter if still useful.

### `configurator.py`

Will build concrete dependencies. Expected direction:

```python
SQLitePaymentRepository -> StartPaymentService -> FastAPI routes or CLI
```

Adapters must not be instantiated directly inside application services.

## Dependencies

`requirements.txt` includes FastAPI for the future HTTP adapter and `aiosqlite`
for asynchronous SQLite access. Python also includes the standard library
`sqlite3` module, which can be used if the implementation stays synchronous.

## Tests

Tests live in `tests/`.

Current tests still reflect the template scaffold and should be replaced when
the payment domain is implemented. Future tests should cover:

- successful payment start;
- invalid amount rejection;
- required payer and merchant fields;
- idempotency behavior;
- persistence adapter behavior;
- API contract once FastAPI routes are added.

`pytest.ini` configures `pythonpath = src`, so imports start from `src`.

## Implementation Standards

When changing the project, follow these rules:

- keep the application hexagon directly under `src`;
- keep entities pure under `src/domain`;
- define driving and driven ports under `src/application/ports`;
- implement use cases under `src/application/services`;
- keep concrete adapters under `src/adapters`;
- do not import concrete adapters from domain or application services;
- wire concrete dependencies in `src/configurator.py`;
- use SQLite only through a persistence adapter;
- expose FastAPI only through an adapter layer;
- add or update tests under `tests/` when behavior changes.

## AI Agent Guidelines

- Before editing, check git status because local uncommitted changes may exist.
- Do not revert existing changes unless explicitly requested.
- Prefer small changes aligned with Ports and Adapters Architecture.
- If creating a new external dependency, define a driven port first.
- If creating a new entry point, call a driving port instead of a concrete
  service method that is not part of a port.
- Run `make test` after behavior changes.
- Run `make lint` or `make check` when changing imports, style, or structure.

## Main Commands

```bash
make run
make test
make lint
make docs
make check
```

See `specs/setup.md` for environment setup and project execution details.
