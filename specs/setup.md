# Bitbank Setup

This guide starts the full local payment saga environment with Docker Compose.

## Requirements

- Docker
- Docker Compose plugin
- Python 3.10, only needed when running service tests outside containers

## Start The Environment

From the repository root:

```bash
docker compose up -d --build
```

Check container status:

```bash
docker compose ps
```

Open RabbitMQ Management:

```text
http://localhost:15672
user: bitbank
password: bitbank
```

## Services And Ports

| Service | URL |
| --- | --- |
| `api_gateway` | `http://localhost:8080` |
| `start_payment_service` | `http://localhost:8000` |
| `debit_account_service` | `http://localhost:8001` |
| `account_service` | `http://localhost:8002` |
| `confirm_payment_service` | `http://localhost:8003` |
| `reverse_payment_service` | `http://localhost:8004` |
| `notify_merchant_service` | `http://localhost:8005` |
| `notify_customer_service` | `http://localhost:8006` |
| `issue_receipt_service` | `http://localhost:8007` |
| RabbitMQ AMQP | `localhost:5672` |
| RabbitMQ Management | `http://localhost:15672` |

## Create An Account

```bash
curl -X POST http://localhost:8080/api/v1/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer-1",
    "account_holder": "Customer One",
    "initial_deposit": "100.00"
  }'
```

The debit service keeps its own SQLite database. Until account projection is
implemented, seed the debit service database directly for full saga tests:

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

## Start A Payment

```bash
curl -X POST http://localhost:8080/api/v1/payments/start \
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

This publishes `payment.started`. The saga consumers then continue the flow.

## Follow Logs

Useful logs:

```bash
docker compose logs -f start_payment_service
docker compose logs -f debit_account_consumer
docker compose logs -f confirm_payment_consumer
docker compose logs -f reverse_payment_consumer
docker compose logs -f notify_merchant_consumer
docker compose logs -f notify_customer_consumer
docker compose logs -f issue_receipt_consumer
```

## Manual Service Calls

The saga should normally drive these services through RabbitMQ events, but the
APIs can be called directly for local testing.

Notify merchant:

```bash
curl -X POST http://localhost:8080/api/v1/notifications/merchant \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "transaction-1",
    "merchant_id": "merchant-1",
    "customer_id": "customer-1",
    "amount": "50.00",
    "confirmed_at": "2026-05-10T12:00:00+00:00",
    "recipient": "merchant@example.com",
    "channel": "EMAIL"
  }'
```

Notify customer:

```bash
curl -X POST http://localhost:8080/api/v1/notifications/customer \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "transaction-1",
    "customer_id": "customer-1",
    "merchant_id": "merchant-1",
    "amount": "50.00",
    "confirmed_at": "2026-05-10T12:00:00+00:00",
    "recipient": "customer@example.com",
    "channel": "EMAIL"
  }'
```

Issue receipt:

```bash
curl -X POST http://localhost:8080/api/v1/receipts \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "transaction-1",
    "customer_id": "customer-1",
    "merchant_id": "merchant-1",
    "amount": "50.00",
    "confirmed_at": "2026-05-10T12:00:00+00:00"
  }'
```

## Run Tests

Run all service test suites:

```bash
for service in \
  account_service \
  start_payment_service \
  debit_account_service \
  confirm_payment_service \
  reverse_payment_service \
  notify_merchant_service \
  notify_customer_service \
  issue_receipt_service
do
  (cd "$service" && pytest)
done
```

Or run one service:

```bash
cd notify_customer_service
pytest
```

## Stop The Environment

Stop containers:

```bash
docker compose down
```

Stop containers and remove persistent volumes:

```bash
docker compose down -v
```
