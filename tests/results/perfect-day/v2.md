# Perfect Day Test Commands | add -> API-Gateway

Historico da execucao do teste do dia perfeito usando API Gateway, RabbitMQ,
consumers e outbox workers.

O ambiente ja estava iniciado com:

```bash
docker compose up -d --build
```

## Dados Do Teste

- Pagador: `customer-gateway-perfect-1`
- Recebedor / merchant: `customer-gateway-perfect-2`
- Valor: `20.00`
- TransactionId: `0dc36fe4-9a88-4cd7-829c-6e01a2e319db`

## 1. Verificar Containers

```bash
docker compose ps
```

## 2. Verificar API Gateway

```bash
curl -sS -i http://localhost:8080/health
```

Resposta:

```text
HTTP/1.1 200 OK

ok
```

## 3. Verificar Logs Recentes Antes Do Teste

```bash
docker compose logs --no-color --since=30s debit_account_consumer confirm_payment_consumer reverse_payment_consumer notify_merchant_consumer notify_customer_consumer issue_receipt_consumer account_outbox start_payment_outbox debit_account_outbox confirm_payment_outbox notify_merchant_outbox notify_customer_outbox issue_receipt_outbox
```

## 4. Criar Conta Do Pagador Pelo Gateway

```bash
curl -sS -X POST http://localhost:8080/api/v1/accounts \
  -H 'Content-Type: application/json' \
  -d '{
    "customer_id": "customer-gateway-perfect-1",
    "account_holder": "Customer Gateway Perfect One",
    "initial_deposit": "100.00"
  }'
```

Resposta:

```json
{
  "account_id": "4d9241ad-d8f6-4767-a30e-edd5689f936c",
  "customer_id": "customer-gateway-perfect-1",
  "status": "ACTIVE",
  "created_at": "2026-05-10T20:38:24.414525Z"
}
```

## 5. Criar Conta Do Recebedor Pelo Gateway

```bash
curl -sS -X POST http://localhost:8080/api/v1/accounts \
  -H 'Content-Type: application/json' \
  -d '{
    "customer_id": "customer-gateway-perfect-2",
    "account_holder": "Customer Gateway Perfect Two",
    "initial_deposit": "50.00"
  }'
```

Resposta:

```json
{
  "account_id": "0d4366c5-daee-4669-a045-1623ee2775ab",
  "customer_id": "customer-gateway-perfect-2",
  "status": "ACTIVE",
  "created_at": "2026-05-10T20:38:25.023493Z"
}
```

## 6. Preparar Conta No Debit Account Service

O `debit_account_service` usa banco proprio, entao a conta do pagador foi
semeada diretamente no SQLite dele.

```bash
docker compose exec -T debit_account_service python -c "from decimal import Decimal; from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository; from domain.account import Account; repository = SQLiteAccountRepository('/data/debit_account.db'); account = repository.get_by_customer_id('customer-gateway-perfect-1') or Account.create(customer_id='customer-gateway-perfect-1', holder_name='Customer Gateway Perfect One', balance=Decimal('100.00')); repository.save(account); print(account.id, account.customer_id, account.balance)"
```

Saida:

```text
f7829fe5-4f04-4ba8-91fc-366aca278a45 customer-gateway-perfect-1 100.00
```

## 7. Iniciar Pagamento Pelo Gateway

```bash
curl -sS -X POST http://localhost:8080/api/v1/payments/start \
  -H 'Content-Type: application/json' \
  -d '{
    "customer_id": "customer-gateway-perfect-1",
    "merchant_id": "customer-gateway-perfect-2",
    "amount": "20.00",
    "payment_method": "ACCOUNT_BALANCE"
  }'
```

Resposta:

```json
{
  "transaction_id": "0dc36fe4-9a88-4cd7-829c-6e01a2e319db",
  "status": "STARTED",
  "created_at": "2026-05-10T20:38:42.286218Z"
}
```

## 8. Aguardar Processamento Assincrono

```bash
sleep 6
```

## 9. Verificar Debito

```bash
docker compose exec -T debit_account_service python -c "from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository; tx='0dc36fe4-9a88-4cd7-829c-6e01a2e319db'; account = SQLiteAccountRepository('/data/debit_account.db').get_by_customer_id('customer-gateway-perfect-1'); print(account.id, account.customer_id, account.balance); print([(entry.transaction_id, entry.amount, entry.entry_type) for entry in account.entries if entry.transaction_id == tx])"
```

Saida:

```text
f7829fe5-4f04-4ba8-91fc-366aca278a45 customer-gateway-perfect-1 80.00
[('0dc36fe4-9a88-4cd7-829c-6e01a2e319db', Decimal('20.00'), 'DEBIT')]
```

## 10. Verificar Confirmacao

```bash
docker compose exec -T confirm_payment_service python -c "from adapters.persistence.sqlite_transaction_repository import SQLiteTransactionRepository; tx = SQLiteTransactionRepository('/data/confirm_payment.db').get_by_id('0dc36fe4-9a88-4cd7-829c-6e01a2e319db'); print(None if tx is None else (tx.id, tx.merchant_id, tx.status.value, tx.confirmed_at))"
```

Saida:

```text
('0dc36fe4-9a88-4cd7-829c-6e01a2e319db', 'customer-gateway-perfect-2', 'CONFIRMED', datetime.datetime(2026, 5, 10, 20, 38, 43, 876361, tzinfo=datetime.timezone.utc))
```

## 11. Verificar Que Nao Houve Reversao

```bash
docker compose exec -T reverse_payment_service python -c "from adapters.persistence.sqlite_transaction_repository import SQLiteTransactionRepository; tx = SQLiteTransactionRepository('/data/reverse_payment.db').get_by_id('0dc36fe4-9a88-4cd7-829c-6e01a2e319db'); print(None if tx is None else (tx.id, tx.status.value, tx.reversed_at))"
```

Saida:

```text
('0dc36fe4-9a88-4cd7-829c-6e01a2e319db', 'STARTED', None)
```

## 12. Verificar Notificacao Do Merchant

```bash
docker compose exec -T notify_merchant_service python -c "from adapters.persistence.sqlite_notification_repository import SQLiteNotificationRepository; n = SQLiteNotificationRepository('/data/notify_merchant.db').get_by_transaction_and_merchant('0dc36fe4-9a88-4cd7-829c-6e01a2e319db','customer-gateway-perfect-2'); print(None if n is None else (n.id, n.transaction_id, n.merchant_id, n.status.value, n.notified_at))"
```

Saida:

```text
('b72f1306-da94-4611-ac80-c61fc139ef3d', '0dc36fe4-9a88-4cd7-829c-6e01a2e319db', 'customer-gateway-perfect-2', 'DELIVERED', datetime.datetime(2026, 5, 10, 20, 38, 44, 405500, tzinfo=datetime.timezone.utc))
```

## 13. Verificar Notificacao Do Customer

```bash
docker compose exec -T notify_customer_service python -c "from adapters.persistence.sqlite_notification_repository import SQLiteNotificationRepository; n = SQLiteNotificationRepository('/data/notify_customer.db').get_by_transaction_and_customer('0dc36fe4-9a88-4cd7-829c-6e01a2e319db','customer-gateway-perfect-1'); print(None if n is None else (n.id, n.transaction_id, n.customer_id, n.status.value, n.notified_at))"
```

Saida:

```text
('2afb9bcd-dc48-4481-b7be-9b0c8b2a85a8', '0dc36fe4-9a88-4cd7-829c-6e01a2e319db', 'customer-gateway-perfect-1', 'DELIVERED', datetime.datetime(2026, 5, 10, 20, 38, 44, 403404, tzinfo=datetime.timezone.utc))
```

## 14. Verificar Recibo

```bash
docker compose exec -T issue_receipt_service python -c "from adapters.persistence.sqlite_receipt_repository import SQLiteReceiptRepository; r = SQLiteReceiptRepository('/data/issue_receipt.db').get_by_transaction_id('0dc36fe4-9a88-4cd7-829c-6e01a2e319db'); print(None if r is None else (r.id, r.transaction_id, r.customer_id, r.merchant_id, r.status.value, r.issued_at, bool(r.document_data)))"
```

Saida:

```text
('c38b0d06-9627-49f6-9a13-303c00eee8bf', '0dc36fe4-9a88-4cd7-829c-6e01a2e319db', 'customer-gateway-perfect-1', 'customer-gateway-perfect-2', 'ISSUED', datetime.datetime(2026, 5, 10, 20, 38, 44, 402892, tzinfo=datetime.timezone.utc), True)
```

## 15. Verificar Logs Recentes Do Fluxo

```bash
docker compose logs --no-color --since=2m debit_account_consumer confirm_payment_consumer reverse_payment_consumer notify_merchant_consumer notify_customer_consumer issue_receipt_consumer account_outbox start_payment_outbox debit_account_outbox confirm_payment_outbox notify_merchant_outbox notify_customer_outbox issue_receipt_outbox
```

Observacao: apareceu uma mensagem isolada em `notify_customer_consumer`:

```text
RabbitMQ consumer failed: . Retrying in 5 seconds.
```

Mesmo assim, os dados persistidos e as outboxes confirmaram que o fluxo foi
concluido corretamente.

## 16. Verificar Outbox Events

```bash
for svc_db in account_service:/data/account.db start_payment_service:/data/start_payment.db debit_account_service:/data/debit_account.db confirm_payment_service:/data/confirm_payment.db notify_merchant_service:/data/notify_merchant.db notify_customer_service:/data/notify_customer.db issue_receipt_service:/data/issue_receipt.db reverse_payment_service:/data/reverse_payment.db; do svc=${svc_db%%:*}; db=${svc_db#*:}; echo $svc; docker compose exec -T $svc python -c "import sqlite3; c=sqlite3.connect('$db'); print(c.execute('select routing_key,status,count(*) from outbox_events group by routing_key,status order by routing_key,status').fetchall())"; done
```

Saida:

```text
account_service
[('account.created', 'PUBLISHED', 2)]
start_payment_service
[('payment.started', 'PUBLISHED', 1)]
debit_account_service
[('debit.completed', 'PUBLISHED', 1)]
confirm_payment_service
[('payment.confirmed', 'PUBLISHED', 1)]
notify_merchant_service
[('merchant.notified', 'PUBLISHED', 1)]
notify_customer_service
[('customer.notified', 'PUBLISHED', 1)]
issue_receipt_service
[('receipt.issued', 'PUBLISHED', 1)]
reverse_payment_service
[]
```
