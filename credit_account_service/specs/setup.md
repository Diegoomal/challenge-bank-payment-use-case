# Credit Account Service Setup

This guide runs `credit_account_service` locally as part of the Bitbank saga.

## Docker Compose

From the repository root:

```bash
docker compose up -d --build credit_account_service credit_account_consumer credit_account_outbox
```

The service listens on:

```text
http://localhost:8008/accounts/credit
```

## Seed A Merchant Account

```bash
docker compose exec credit_account_service python - <<'PY'
from decimal import Decimal

from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository
from domain.account import Account

repository = SQLiteAccountRepository('/data/credit_account.db')
account = Account.create(
    customer_id='merchant-1',
    holder_name='Merchant One',
    balance=Decimal('0.00'),
)
repository.save(account)
print(account.id)
PY
```

## Manual Credit Call

```bash
curl -X POST http://localhost:8008/accounts/credit \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "transaction-1",
    "customer_id": "customer-1",
    "merchant_id": "merchant-1",
    "amount": "50.00"
  }'
```

## Tests

```bash
pytest
```
