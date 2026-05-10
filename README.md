# Bitbank Payment Saga

Study project for implementing payment use cases with hexagonal architecture,
event-driven communication, and local orchestration with Docker Compose.

The current implementation covers the first two steps of the flow:

1. `start_payment_service`: starts a payment transaction.
2. `debit_account_service`: debits the customer account after receiving the
   payment started event.

The next planned services are:

```text
confirm_payment_service
reverse_payment_service
notify_merchant_service
notify_customer_service
issue_receipt_service
```

## Architecture

Each service follows a basic hexagonal structure:

```text
service/
├── src/
│   ├── domain/
│   ├── application/
│   │   ├── ports/
│   │   └── services/
│   ├── adapters/
│   │   ├── api/
│   │   ├── messaging/
│   │   └── persistence/
│   ├── configurator.py
│   └── main.py
├── tests/
├── specs/
├── requirements.txt
└── dockerfile
```

Main rules:

- `domain` does not depend on frameworks, databases, or messaging.
- `application/ports` defines inbound and outbound contracts.
- `application/services` implements use cases.
- `adapters` contains FastAPI, RabbitMQ, and SQLite details.
- `configurator.py` wires concrete dependencies.

## Implemented Flow

```text
POST /payments/start
  -> start_payment_service creates a Transaction with STARTED status
  -> stores it in SQLite
  -> publishes payment.started to RabbitMQ

RabbitMQ exchange: payments
  routing key: payment.started

Debit account consumer
  -> consumes payment.started
  -> calls DebitAccountService
  -> finds Account by customer_id
  -> debits balance when possible
  -> publishes debit.completed or debit.failed
```

Events used:

```text
payment.started
DebitCompleted -> debit.completed
DebitFailed    -> debit.failed
```

## Services

| Service | Port | Responsibility |
| --- | --- | --- |
| `start_payment_service` | `8000` | Start payment and publish `PaymentStarted` |
| `debit_account_service` | `8001` | Debit account through the API |
| `debit_account_consumer` | - | Consume `payment.started` and execute debit |
| `rabbitmq` | `5672`, `15672` | Broker and management UI |

RabbitMQ Management:

```text
http://localhost:15672
user: bitbank
password: bitbank
```

## Start The Environment

```bash
docker compose up -d --build
```

Check containers:

```bash
docker compose ps
```

Follow logs:

```bash
docker compose logs -f start_payment_service
docker compose logs -f debit_account_service
docker compose logs -f debit_account_consumer
```

Stop the environment:

```bash
docker compose down
```

Remove volumes and container databases:

```bash
docker compose down -v
```

## Test Start Payment

```bash
curl -X POST http://localhost:8000/payments/start \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer-1",
    "merchant_id": "merchant-1",
    "amount": "50.00",
    "payment_method": "ACCOUNT_BALANCE"
  }'
```

Expected response:

```json
{
  "transaction_id": "...",
  "status": "STARTED",
  "created_at": "..."
}
```

This command also publishes `payment.started` to RabbitMQ.

## Create A Test Account

There is no public endpoint for account creation yet. To test the successful
debit case, create an account directly in the container SQLite database:

```bash
docker compose exec debit_account_service python - <<'PY'
from decimal import Decimal

from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository
from domain.account import Account

repository = SQLiteAccountRepository("/data/debit_account.db")
account = Account.create(
    customer_id="customer-1",
    holder_name="Customer One",
    balance=Decimal("100.00"),
)
repository.save(account)
print(account.id)
PY
```

## Test Debit Account Through The API

```bash
curl -X POST http://localhost:8001/accounts/debit \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "transaction-1",
    "customer_id": "customer-1",
    "amount": "50.00"
  }'
```

Expected response with an existing account:

```json
{
  "account_id": "...",
  "transaction_id": "transaction-1",
  "status": "COMPLETED",
  "reason": null
}
```

Expected response without an existing account:

```json
{
  "account_id": null,
  "transaction_id": "transaction-1",
  "status": "FAILED",
  "reason": "ACCOUNT_NOT_FOUND"
}
```

## Test The Saga Flow

1. Start the environment.
2. Create an account for `customer-1`.
3. Call `POST /payments/start`.
4. Check the consumer:

```bash
docker compose logs -f debit_account_consumer
```

With enough balance, the consumer should process the `payment.started` event,
debit the account, and publish `debit.completed`.

## Automated Tests

`start_payment_service`:

```bash
cd start_payment_service
make test
make lint
```

`debit_account_service`:

```bash
cd debit_account_service
make test
make lint
```

Or, inside each service:

```bash
make check
```

## Current Status

Implemented:

- `StartPayment` with FastAPI, SQLite, and RabbitMQ publisher.
- `DebitAccount` with FastAPI, SQLite, RabbitMQ publisher, and consumer.
- Unit and API tests for both services.
- Docker Compose with RabbitMQ and persistent volumes.

Pending:

- Public endpoint for account creation/administration.
- Outbox pattern for transactional event publishing.
- Next saga services: confirmation, reversal, notifications, and receipt.
