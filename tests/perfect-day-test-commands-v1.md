# Perfect Day Test Commands | add -> outbox-pattern

Comandos usados para validar o fluxo feliz ponta a ponta com Docker Compose,
RabbitMQ, consumers e outbox workers.

## 1. Subir Ambiente

```bash
docker compose up -d --build
```

## 2. Validar Containers

```bash
docker compose ps
```

## 3. Verificar Logs Iniciais

```bash
docker compose logs --no-color --since=30s debit_account_consumer confirm_payment_consumer reverse_payment_consumer notify_merchant_consumer notify_customer_consumer issue_receipt_consumer
```

## 4. Criar Conta Do Pagador

```bash
curl -sS -X POST http://localhost:8002/accounts \
  -H 'Content-Type: application/json' \
  -d '{
    "customer_id": "customer-outbox-1",
    "account_holder": "Customer Outbox One",
    "initial_deposit": "100.00"
  }'
```

Resposta obtida:

```json
{
  "account_id": "5d803135-2d59-423e-9b46-eb47585a0ecb",
  "customer_id": "customer-outbox-1",
  "status": "ACTIVE",
  "created_at": "2026-05-10T18:40:59.443398Z"
}
```

## 5. Criar Conta Do Recebedor

```bash
curl -sS -X POST http://localhost:8002/accounts \
  -H 'Content-Type: application/json' \
  -d '{
    "customer_id": "customer-outbox-2",
    "account_holder": "Customer Outbox Two",
    "initial_deposit": "50.00"
  }'
```

Resposta obtida:

```json
{
  "account_id": "33e9be17-9d46-4ce7-b97f-882dc6a37907",
  "customer_id": "customer-outbox-2",
  "status": "ACTIVE",
  "created_at": "2026-05-10T18:40:58.850933Z"
}
```

## 6. Preparar Conta No Debit Account Service

```bash
docker compose exec -T debit_account_service python -c "from decimal import Decimal; from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository; from domain.account import Account; repository = SQLiteAccountRepository('/data/debit_account.db'); account = repository.get_by_customer_id('customer-outbox-1') or Account.create(customer_id='customer-outbox-1', holder_name='Customer Outbox One', balance=Decimal('100.00')); repository.save(account); print(account.id, account.customer_id, account.balance)"
```

Saída obtida:

```text
dab6543a-3abd-418d-a8d1-0abd627e16ed customer-outbox-1 100.00
```

## 7. Iniciar Pagamento

```bash
curl -sS -X POST http://localhost:8000/payments/start \
  -H 'Content-Type: application/json' \
  -d '{
    "customer_id": "customer-outbox-1",
    "merchant_id": "customer-outbox-2",
    "amount": "20.00",
    "payment_method": "ACCOUNT_BALANCE"
  }'
```

Resposta obtida:

```json
{
  "transaction_id": "9244da16-03ff-490e-8b3b-4702512e6e50",
  "status": "STARTED",
  "created_at": "2026-05-10T18:41:15.526506Z"
}
```

## 8. Aguardar Consumers E Outbox Workers

```bash
sleep 6
```

## 9. Verificar Débito

```bash
docker compose exec -T debit_account_service python -c "from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository; tx='9244da16-03ff-490e-8b3b-4702512e6e50'; account = SQLiteAccountRepository('/data/debit_account.db').get_by_customer_id('customer-outbox-1'); print(account.balance); print([(entry.transaction_id, entry.amount, entry.entry_type) for entry in account.entries if entry.transaction_id == tx])"
```

Saída obtida:

```text
80.00
[('9244da16-03ff-490e-8b3b-4702512e6e50', Decimal('20.00'), 'DEBIT')]
```

## 10. Verificar Confirmação

```bash
docker compose exec -T confirm_payment_service python -c "from adapters.persistence.sqlite_transaction_repository import SQLiteTransactionRepository; tx = SQLiteTransactionRepository('/data/confirm_payment.db').get_by_id('9244da16-03ff-490e-8b3b-4702512e6e50'); print(None if tx is None else (tx.id, tx.merchant_id, tx.status.value))"
```

Saída obtida:

```text
('9244da16-03ff-490e-8b3b-4702512e6e50', 'customer-outbox-2', 'CONFIRMED')
```

## 11. Verificar Notificação Do Merchant

```bash
docker compose exec -T notify_merchant_service python -c "from adapters.persistence.sqlite_notification_repository import SQLiteNotificationRepository; n = SQLiteNotificationRepository('/data/notify_merchant.db').get_by_transaction_and_merchant('9244da16-03ff-490e-8b3b-4702512e6e50','customer-outbox-2'); print(None if n is None else (n.status.value, n.notified_at))"
```

Saída obtida:

```text
('DELIVERED', datetime.datetime(2026, 5, 10, 18, 41, 16, 574665, tzinfo=datetime.timezone.utc))
```

## 12. Verificar Notificação Do Customer

```bash
docker compose exec -T notify_customer_service python -c "from adapters.persistence.sqlite_notification_repository import SQLiteNotificationRepository; n = SQLiteNotificationRepository('/data/notify_customer.db').get_by_transaction_and_customer('9244da16-03ff-490e-8b3b-4702512e6e50','customer-outbox-1'); print(None if n is None else (n.status.value, n.notified_at))"
```

Saída obtida:

```text
('DELIVERED', datetime.datetime(2026, 5, 10, 18, 41, 16, 575230, tzinfo=datetime.timezone.utc))
```

## 13. Verificar Recibo

```bash
docker compose exec -T issue_receipt_service python -c "from adapters.persistence.sqlite_receipt_repository import SQLiteReceiptRepository; r = SQLiteReceiptRepository('/data/issue_receipt.db').get_by_transaction_id('9244da16-03ff-490e-8b3b-4702512e6e50'); print(None if r is None else (r.status.value, bool(r.document_data)))"
```

Saída obtida:

```text
('ISSUED', True)
```

## 14. Verificar Outbox Events

```bash
docker compose exec -T account_service python -c "import sqlite3; c=sqlite3.connect('/data/account.db'); print(c.execute('select routing_key,status,count(*) from outbox_events group by routing_key,status order by routing_key,status').fetchall())"
```

```bash
docker compose exec -T start_payment_service python -c "import sqlite3; c=sqlite3.connect('/data/start_payment.db'); print(c.execute('select routing_key,status,count(*) from outbox_events group by routing_key,status order by routing_key,status').fetchall())"
```

```bash
docker compose exec -T debit_account_service python -c "import sqlite3; c=sqlite3.connect('/data/debit_account.db'); print(c.execute('select routing_key,status,count(*) from outbox_events group by routing_key,status order by routing_key,status').fetchall())"
```

```bash
docker compose exec -T confirm_payment_service python -c "import sqlite3; c=sqlite3.connect('/data/confirm_payment.db'); print(c.execute('select routing_key,status,count(*) from outbox_events group by routing_key,status order by routing_key,status').fetchall())"
```

```bash
docker compose exec -T notify_merchant_service python -c "import sqlite3; c=sqlite3.connect('/data/notify_merchant.db'); print(c.execute('select routing_key,status,count(*) from outbox_events group by routing_key,status order by routing_key,status').fetchall())"
```

```bash
docker compose exec -T notify_customer_service python -c "import sqlite3; c=sqlite3.connect('/data/notify_customer.db'); print(c.execute('select routing_key,status,count(*) from outbox_events group by routing_key,status order by routing_key,status').fetchall())"
```

```bash
docker compose exec -T issue_receipt_service python -c "import sqlite3; c=sqlite3.connect('/data/issue_receipt.db'); print(c.execute('select routing_key,status,count(*) from outbox_events group by routing_key,status order by routing_key,status').fetchall())"
```

Saídas esperadas/obtidas:

```text
[('account.created', 'PUBLISHED', 2)]
[('payment.started', 'PUBLISHED', 1)]
[('debit.completed', 'PUBLISHED', 1)]
[('payment.confirmed', 'PUBLISHED', 1)]
[('merchant.notified', 'PUBLISHED', 1)]
[('customer.notified', 'PUBLISHED', 1)]
[('receipt.issued', 'PUBLISHED', 1)]
```

## 15. Verificar Logs Dos Workers De Outbox

```bash
docker compose logs --no-color --since=2m account_outbox start_payment_outbox debit_account_outbox confirm_payment_outbox reverse_payment_outbox notify_merchant_outbox notify_customer_outbox issue_receipt_outbox
```

## 16. Verificar Containers Ao Final

```bash
docker compose ps
```
