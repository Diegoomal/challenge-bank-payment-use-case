# Account Service Setup

This document explains how to prepare the local environment, install
dependencies, run the service, and execute checks.

## Requirements

The project uses Python 3.10. The recommended environment is described in
`env.yml` and installs the dependencies listed in `requirements.txt`.

Expected tools:

- Conda or Mamba, recommended;
- Python 3.10, if using a virtual environment without Conda;
- `make`, for the `Makefile` shortcuts;
- Docker and Docker Compose, when running the full stack.

Runtime dependencies include:

- FastAPI, used by the HTTP driving adapter;
- Uvicorn, used to run the FastAPI application;
- Pika, used by the RabbitMQ messaging adapter;
- a SQLite dependency through `aiosqlite` for future async adapters, plus
  Python's built-in `sqlite3` module used by the current synchronous adapter.

## Conda Environment

Create environment using `env.yml`:

```bash
conda env create -n account-service-env -f env.yml
conda activate account-service-env
```

## Run The Service

Use the `Makefile` target:

```bash
make run
```

This command runs the FastAPI application on port `8002`:

```bash
PYTHONPATH=src uvicorn main:app --host 0.0.0.0 --port 8002
```

You can also run it manually:

```bash
PYTHONPATH=src uvicorn main:app --reload --port 8002
```

## Environment Variables

Supported variables:

- `DATABASE_PATH`: SQLite database path. Default: `account.db`.
- `RABBITMQ_URL`: RabbitMQ connection URL. When unset, the service uses the
  in-memory event publisher.

Docker Compose sets:

```text
DATABASE_PATH=/data/account.db
RABBITMQ_URL=amqp://bitbank:bitbank@rabbitmq:5672/%2F
```

## HTTP API

Create an account:

```bash
curl -X POST http://localhost:8002/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer-1",
    "account_holder": "Customer One",
    "initial_deposit": "100.00"
  }'
```

Expected response:

```json
{
  "account_id": "...",
  "customer_id": "customer-1",
  "status": "ACTIVE",
  "created_at": "..."
}
```

If the customer already has an active account, the endpoint returns `400` with:

```json
{
  "detail": "customer already has an active account"
}
```

## Docker

From the repository root, run:

```bash
docker compose up -d --build account_service
```

The root `docker-compose.yml` runs this service on port `8002` and stores the
SQLite database in the `account_data` volume.

RabbitMQ Management is available at:

```text
http://localhost:15672
user: bitbank
password: bitbank
```

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
2. Define or update ports before concrete adapters.
3. Keep account lifecycle rules in the domain or application service.
4. Implement SQLite persistence behind `AccountRepository`.
5. Publish domain events through `EventPublisher`.
6. Expose HTTP behavior through FastAPI adapters.
7. Run `make test`.
8. Run `make lint` when changing imports, formatting, or adding files.
