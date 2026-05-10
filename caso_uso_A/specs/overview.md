# Project Overview

This repository is a small Python service that demonstrates Ports and Adapters
Architecture, also known as Hexagonal Architecture.

It implements user CRUD operations using in-memory persistence. The
the `src` package layout is the application hexagon. CLI and persistence are
adapters around that hexagon.

Use this document as the initial context when working with AI coding agents such
as Codex, Claude, or similar tools.

## Goal

The service manages users with these fields:

- `id`
- `name`
- `email`
- `birthdate`
- `created_at`
- `updated_at`

The main operations are exposed by the `ForManagingUsers` driving port:

- create a user;
- list users;
- get a user by ID;
- update a user;
- delete a user.

The most important business rule is preventing two users from using the same
email address. This validation exists in both creation and update flows.

## Architecture

The project follows a hexagonal structure directly under `src`:

```text
src/
├── configurator.py
├── main.py
├── domain/
│   └── user.py
├── application/
│   ├── ports/
│   │   ├── for_managing_users.py
│   │   └── user_repository.py
│   └── services/
│       ├── user_management_service.py
│       └── user_validations.py
└── adapters/
    ├── cli/
    │   └── main.py
    ├── persistence/
    │   └── in_memory_user_repository.py
    └── messaging/
```

### `domain`

Contains pure business entities.

- `src/domain/user.py`
  - defines `User`, a `dataclass` entity;
  - defines `IEntity`, a `Protocol` with common entity fields;
  - contains the entity string representation.

This package must not depend on adapters, frameworks, or external details.

### `application/ports`

Contains the ports of the application hexagon.

- `driving_ports/for_managing_users.py`
  - defines the operations external actors can call.
- `driven_ports/user_repository.py`
  - defines the persistence operations required by the application.

Driving ports are called by adapters. Driven ports are implemented by adapters.

### `application/services`

Contains application services.

- `user_management_service.py`
  - implements `ForManagingUsers`;
  - coordinates persistence through `UserRepository`;
  - enforces duplicate email and not-found rules.
- `user_validations.py`
  - validates email format and minimum age.

Services may depend on the domain and interfaces, but not on concrete adapters.

### `adapters`

Contains concrete adapters around the hexagon.

- `cli/main.py`
  - driving adapter that receives `ForManagingUsers` and runs the demo flow.
- `persistence/in_memory_user_repository.py`
  - driven adapter that implements `UserRepository` using an in-memory list.
- `messaging/`
  - reserved for future messaging adapters.

### `configurator.py`

Builds concrete dependencies:

```python
InMemoryUserRepository -> UserManagementService
```

The CLI does not instantiate concrete persistence directly.

## Tests

Tests live in `tests/`.

- `tests/test_for_managing_users.py` tests the application through the driving
  port behavior.
- `tests/test_in_memory_user_repository.py` tests the persistence adapter.

`pytest.ini` configures `pythonpath = src`, so imports start from `src`, for
example:

```python
from application.services.user_management_service import UserManagementService
from adapters.persistence.in_memory_user_repository import (
    InMemoryUserRepository,
)
```

## Implementation Standards

When changing the project, follow these rules:

- keep the application hexagon directly under `src`;
- keep entities pure under `src/domain`;
- define driving ports under `src/application/ports`;
- define driven ports under `src/application/ports`;
- implement application behavior under `src/application/services`;
- keep concrete adapters under `src/adapters`;
- do not import concrete adapters from `domain`, `interfaces`, or `services`;
- wire concrete dependencies in `src/configurator.py`;
- raise `ValueError` for business rule errors or missing resources, following
  the current style;
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
