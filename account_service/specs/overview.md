# Account Service Overview

This repository contains `account_service`, a Python service that follows Ports
and Adapters Architecture, also known as Hexagonal Architecture.

The service belongs to the Account bounded context. It manages the lifecycle of
customer financial accounts and publishes account creation events for other
services to consume without coupling to this service internals.

Use this document as the initial context when working with AI coding agents such
as Codex, Claude, or similar tools.

## Goal

The service creates customer financial accounts.

Account fields:

- `id`
- `customer_id`
- `account_holder`
- `balance`
- `status`
- `created_at`
- `updated_at`

The main operations are exposed by the `ForCreatingAccount` driving port:

- create an account;
- reject invalid account creation requests;
- prevent a customer from having more than one active account.

The initial business rules are:

- an account must have a unique identifier;
- `customer_id` is required;
- `account_holder` is required;
- initial deposit cannot be negative;
- newly created accounts start with status `ACTIVE`;
- a customer cannot have more than one active account.

## Architecture

The project follows a hexagonal structure directly under `src`:

```text
src/
├── configurator.py
├── main.py
├── domain/
│   ├── account.py
│   ├── account_status.py
│   └── events.py
├── application/
│   ├── schemas.py
│   ├── ports/
│   │   ├── account_repository.py
│   │   ├── event_publisher.py
│   │   └── for_creating_account.py
│   └── services/
│       └── create_account_service.py
└── adapters/
    ├── api/
    │   ├── routes.py
    │   └── schemas.py
    ├── messaging/
    │   ├── in_memory_event_publisher.py
    │   └── rabbitmq_event_publisher.py
    └── persistence/
        └── sqlite_account_repository.py
```

### `domain`

Contains pure account entities, enums, and domain events.

- `src/domain/account.py`
  - defines `Account`, the aggregate root;
  - validates required customer and holder data;
  - validates non-negative initial deposit;
  - creates accounts with `ACTIVE` status.
- `src/domain/account_status.py`
  - defines `ACTIVE`, `BLOCKED`, and `CLOSED` statuses.
- `src/domain/events.py`
  - defines `AccountCreated` and its serializable payload.

This package must not depend on FastAPI, SQLite, RabbitMQ, messaging clients,
or concrete adapters.

### `application/ports`

Contains the ports of the application hexagon.

- `for_creating_account.py`
  - driving port for the `CreateAccount` use case.
- `account_repository.py`
  - driven persistence port used by the application.
- `event_publisher.py`
  - driven messaging port used to publish domain events.

Driving ports are called by adapters. Driven ports are implemented by adapters.

### `application/services`

Contains application services.

- `create_account_service.py`
  - implements `ForCreatingAccount`;
  - checks whether the customer already has an active account;
  - creates and persists the `Account` aggregate;
  - publishes `AccountCreated`.

Services may depend on the domain and interfaces, but not on concrete adapters.

### `adapters`

Contains concrete adapters around the hexagon.

- `api/routes.py`
  - FastAPI driving adapter exposing `POST /accounts`.
- `api/schemas.py`
  - HTTP request and response schemas.
- `persistence/sqlite_account_repository.py`
  - SQLite driven adapter implementing `AccountRepository`.
- `messaging/in_memory_event_publisher.py`
  - test and local fallback publisher.
- `messaging/rabbitmq_event_publisher.py`
  - RabbitMQ driven adapter that publishes `account.created`.

### `configurator.py`

Builds concrete dependencies. Expected direction:

```python
SQLiteAccountRepository -> CreateAccountService -> FastAPI routes
RabbitMQEventPublisher  -> CreateAccountService
```

If `RABBITMQ_URL` is present, the service uses RabbitMQ. Otherwise, it falls
back to the in-memory publisher.

Adapters must not be instantiated directly inside application services.

## Messaging

Published event:

```text
AccountCreated
```

RabbitMQ mapping:

```text
exchange: accounts
routing_key: account.created
```

Payload:

```json
{
  "event_name": "AccountCreated",
  "account_id": "...",
  "customer_id": "customer-1",
  "account_holder": "Customer One",
  "initial_deposit": "100.00",
  "occurred_at": "..."
}
```

## Dependencies

`requirements.txt` includes FastAPI for the HTTP adapter, `pika` for RabbitMQ,
and `aiosqlite` for future asynchronous SQLite access. The current persistence
adapter uses Python's built-in `sqlite3` module.

## Tests

Tests live in `tests/`.

Current tests cover:

- account creation with `ACTIVE` status;
- negative initial deposit rejection;
- missing account holder rejection;
- duplicate active account rejection;
- `AccountCreated` publication;
- SQLite persistence behavior;
- FastAPI `POST /accounts` contract;
- RabbitMQ publisher exchange and routing key behavior.

`pytest.ini` configures `pythonpath = src`, so imports start from `src`.

## Implementation Standards

When changing the project, follow these rules:

- keep the application hexagon directly under `src`;
- keep entities and domain events pure under `src/domain`;
- define driving and driven ports under `src/application/ports`;
- implement use cases under `src/application/services`;
- keep concrete adapters under `src/adapters`;
- do not import concrete adapters from domain or application services;
- wire concrete dependencies in `src/configurator.py`;
- use SQLite only through persistence adapters;
- expose FastAPI only through adapter layers;
- publish events only through `EventPublisher`;
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
