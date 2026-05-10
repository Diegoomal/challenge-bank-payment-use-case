# Perfect Day Test Commands

Executed against the local Docker Compose environment.

## Scenario

- payer: `customer-perfect-5`
- receiver / merchant: `customer-perfect-6`
- amount: `20.00`
- transaction_id: `a01486be-9e9d-49d3-9f78-8530bb03f17e`

## 1. Check Containers

```bash
docker compose ps
```

```bash
docker compose logs --no-color --since=30s debit_account_consumer confirm_payment_consumer reverse_payment_consumer notify_merchant_consumer notify_customer_consumer issue_receipt_consumer
```

## 2. Create Payer Account

```bash
curl -sS -X POST http://localhost:8002/accounts \
  -H 'Content-Type: application/json' \
  -d '{
    "customer_id": "customer-perfect-5",
    "account_holder": "Customer Perfect Five",
    "initial_deposit": "100.00"
  }'
```

Response:

```json
{
  "account_id": "9df02386-be32-4b6b-880d-cb755b4de069",
  "customer_id": "customer-perfect-5",
  "status": "ACTIVE",
  "created_at": "2026-05-10T18:27:27.726855Z"
}
```

## 3. Create Receiver Account

```bash
curl -sS -X POST http://localhost:8002/accounts \
  -H 'Content-Type: application/json' \
  -d '{
    "customer_id": "customer-perfect-6",
    "account_holder": "Customer Perfect Six",
    "initial_deposit": "50.00"
  }'
```

Response:

```json
{
  "account_id": "a3328c51-6180-4e05-a8d1-046c5dec7f01",
  "customer_id": "customer-perfect-6",
  "status": "ACTIVE",
  "created_at": "2026-05-10T18:27:27.275745Z"
}
```

## 4. Seed Debit Account Database

The debit service has its own SQLite database, so the payer account was seeded
directly there.

```bash
docker compose exec -T debit_account_service python -c "from decimal import Decimal; from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository; from domain.account import Account; repository = SQLiteAccountRepository('/data/debit_account.db'); account = repository.get_by_customer_id('customer-perfect-5') or Account.create(customer_id='customer-perfect-5', holder_name='Customer Perfect Five', balance=Decimal('100.00')); repository.save(account); print(account.id, account.customer_id, account.balance)"
```

Output:

```text
ca3d3b78-16af-40fb-9eb1-db2c890e33c2 customer-perfect-5 100.00
```

## 5. Start Payment

```bash
curl -sS -X POST http://localhost:8000/payments/start \
  -H 'Content-Type: application/json' \
  -d '{
    "customer_id": "customer-perfect-5",
    "merchant_id": "customer-perfect-6",
    "amount": "20.00",
    "payment_method": "ACCOUNT_BALANCE"
  }'
```

Response:

```json
{
  "transaction_id": "a01486be-9e9d-49d3-9f78-8530bb03f17e",
  "status": "STARTED",
  "created_at": "2026-05-10T18:27:42.793672Z"
}
```

## 6. Wait For Consumers

```bash
sleep 4
```

## 7. Verify Debit

```bash
docker compose exec -T debit_account_service python -c "from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository; tx='a01486be-9e9d-49d3-9f78-8530bb03f17e'; account = SQLiteAccountRepository('/data/debit_account.db').get_by_customer_id('customer-perfect-5'); print(account.id, account.customer_id, account.balance); print([(entry.transaction_id, entry.amount, entry.entry_type) for entry in account.entries if entry.transaction_id == tx])"
```

Output:

```text
ca3d3b78-16af-40fb-9eb1-db2c890e33c2 customer-perfect-5 80.00
[('a01486be-9e9d-49d3-9f78-8530bb03f17e', Decimal('20.00'), 'DEBIT')]
```

## 8. Verify Payment Confirmation

```bash
docker compose exec -T confirm_payment_service python -c "from adapters.persistence.sqlite_transaction_repository import SQLiteTransactionRepository; tx = SQLiteTransactionRepository('/data/confirm_payment.db').get_by_id('a01486be-9e9d-49d3-9f78-8530bb03f17e'); print(None if tx is None else (tx.id, tx.merchant_id, tx.status.value, tx.confirmed_at))"
```

Output:

```text
('a01486be-9e9d-49d3-9f78-8530bb03f17e', 'customer-perfect-6', 'CONFIRMED', datetime.datetime(2026, 5, 10, 18, 27, 42, 854264, tzinfo=datetime.timezone.utc))
```

## 9. Verify No Reversal

```bash
docker compose exec -T reverse_payment_service python -c "from adapters.persistence.sqlite_transaction_repository import SQLiteTransactionRepository; tx = SQLiteTransactionRepository('/data/reverse_payment.db').get_by_id('a01486be-9e9d-49d3-9f78-8530bb03f17e'); print(None if tx is None else (tx.id, tx.status.value, tx.reversed_at))"
```

Output:

```text
('a01486be-9e9d-49d3-9f78-8530bb03f17e', 'STARTED', None)
```

## 10. Verify Merchant Notification

```bash
docker compose exec -T notify_merchant_service python -c "from adapters.persistence.sqlite_notification_repository import SQLiteNotificationRepository; n = SQLiteNotificationRepository('/data/notify_merchant.db').get_by_transaction_and_merchant('a01486be-9e9d-49d3-9f78-8530bb03f17e','customer-perfect-6'); print(None if n is None else (n.id, n.transaction_id, n.merchant_id, n.status.value, n.notified_at))"
```

Output:

```text
('2cc3c293-d05c-4ca8-a802-30f3868f5b4e', 'a01486be-9e9d-49d3-9f78-8530bb03f17e', 'customer-perfect-6', 'DELIVERED', datetime.datetime(2026, 5, 10, 18, 27, 42, 879985, tzinfo=datetime.timezone.utc))
```

## 11. Verify Customer Notification

```bash
docker compose exec -T notify_customer_service python -c "from adapters.persistence.sqlite_notification_repository import SQLiteNotificationRepository; n = SQLiteNotificationRepository('/data/notify_customer.db').get_by_transaction_and_customer('a01486be-9e9d-49d3-9f78-8530bb03f17e','customer-perfect-5'); print(None if n is None else (n.id, n.transaction_id, n.customer_id, n.status.value, n.notified_at))"
```

Output:

```text
('c4960249-2fdc-48b7-aa7b-fdd0e543774d', 'a01486be-9e9d-49d3-9f78-8530bb03f17e', 'customer-perfect-5', 'DELIVERED', datetime.datetime(2026, 5, 10, 18, 27, 42, 879294, tzinfo=datetime.timezone.utc))
```

## 12. Verify Receipt

```bash
docker compose exec -T issue_receipt_service python -c "from adapters.persistence.sqlite_receipt_repository import SQLiteReceiptRepository; r = SQLiteReceiptRepository('/data/issue_receipt.db').get_by_transaction_id('a01486be-9e9d-49d3-9f78-8530bb03f17e'); print(None if r is None else (r.id, r.transaction_id, r.customer_id, r.merchant_id, r.status.value, r.issued_at, bool(r.document_data)))"
```

Output:

```text
('0791be0b-143e-43f4-97bb-bcb2a467c556', 'a01486be-9e9d-49d3-9f78-8530bb03f17e', 'customer-perfect-5', 'customer-perfect-6', 'ISSUED', datetime.datetime(2026, 5, 10, 18, 27, 42, 879018, tzinfo=datetime.timezone.utc), True)
```

## 13. Check Consumer Logs

```bash
docker compose logs --no-color --since=2m debit_account_consumer confirm_payment_consumer reverse_payment_consumer notify_merchant_consumer notify_customer_consumer issue_receipt_consumer
```

No recent consumer errors were returned.

## 14. Check Containers Again

```bash
docker compose ps
```
