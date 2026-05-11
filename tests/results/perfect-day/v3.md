# Perfect Day Test Commands | add -> Observability

Executado em: 2026-05-10

IDs usados neste teste:

- `CORRELATION_ID=perfect-day-20260510213126`
- `CUSTOMER_1=customer-1-20260510213126`
- `CUSTOMER_2=customer-2-20260510213126`
- `ACCOUNT_1=6f437975-c32f-4cc9-9162-3dd14b3bfab8`
- `ACCOUNT_2=499c3541-d12f-4dd7-9124-a8a4cc1965f5`
- `TRANSACTION_ID=8bdd186a-cd08-4acc-9750-00e17820aecb`

## 1. Verificar containers

```bash
docker compose ps
```

## 2. Verificar rotas do API Gateway

```bash
sed -n '1,220p' api_gateway/nginx.conf
```

## 3. Verificar endpoints disponíveis

```bash
rg -n "@.*post|@.*get|payments|accounts|notifications|receipts" */src -g '*.py'
```

## 4. Verificar health do API Gateway

```bash
curl -sS -i http://localhost:8080/health
```

## 5. Verificar RabbitMQ

```bash
curl -sS http://localhost:15672/api/overview -u bitbank:bitbank
```

## 6. Criar usuário 1

```bash
curl -sS -X POST http://localhost:8080/api/v1/accounts \
  -H 'Content-Type: application/json' \
  -H 'X-Correlation-ID: perfect-day-20260510213126' \
  -d '{"customer_id":"customer-1-20260510213126","account_holder":"Customer One Perfect Day","initial_deposit":"100.00"}'
```

Resultado:

```json
{"account_id":"6f437975-c32f-4cc9-9162-3dd14b3bfab8","customer_id":"customer-1-20260510213126","status":"ACTIVE","created_at":"2026-05-10T21:31:43.320536Z"}
```

## 7. Criar usuário 2

```bash
curl -sS -X POST http://localhost:8080/api/v1/accounts \
  -H 'Content-Type: application/json' \
  -H 'X-Correlation-ID: perfect-day-20260510213126' \
  -d '{"customer_id":"customer-2-20260510213126","account_holder":"Customer Two Perfect Day","initial_deposit":"50.00"}'
```

Resultado:

```json
{"account_id":"499c3541-d12f-4dd7-9124-a8a4cc1965f5","customer_id":"customer-2-20260510213126","status":"ACTIVE","created_at":"2026-05-10T21:31:48.671286Z"}
```

## 8. Aguardar processamento assíncrono inicial

```bash
sleep 3
```

## 9. Preparar contas no debit_account_service

```bash
docker compose exec -T debit_account_service python -c "import sqlite3, datetime; now=datetime.datetime.now(datetime.timezone.utc).isoformat(); c=sqlite3.connect('/data/debit_account.db'); c.execute('insert or replace into accounts (id, customer_id, holder_name, balance, created_at, updated_at) values (?, ?, ?, ?, ?, ?)', ('6f437975-c32f-4cc9-9162-3dd14b3bfab8','customer-1-20260510213126','Customer One Perfect Day','100.00',now,now)); c.execute('insert or replace into accounts (id, customer_id, holder_name, balance, created_at, updated_at) values (?, ?, ?, ?, ?, ?)', ('499c3541-d12f-4dd7-9124-a8a4cc1965f5','customer-2-20260510213126','Customer Two Perfect Day','50.00',now,now)); c.commit(); print(c.execute('select id, customer_id, balance from accounts where customer_id in (?, ?) order by customer_id', ('customer-1-20260510213126','customer-2-20260510213126')).fetchall())"
```

Resultado:

```text
[('6f437975-c32f-4cc9-9162-3dd14b3bfab8', 'customer-1-20260510213126', '100.00'), ('499c3541-d12f-4dd7-9124-a8a4cc1965f5', 'customer-2-20260510213126', '50.00')]
```

## 10. Iniciar pagamento

```bash
curl -sS -X POST http://localhost:8080/api/v1/payments/start \
  -H 'Content-Type: application/json' \
  -H 'X-Correlation-ID: perfect-day-20260510213126' \
  -d '{"customer_id":"customer-1-20260510213126","merchant_id":"customer-2-20260510213126","amount":"20.00","payment_method":"ACCOUNT_BALANCE"}'
```

Resultado:

```json
{"transaction_id":"8bdd186a-cd08-4acc-9750-00e17820aecb","status":"STARTED","created_at":"2026-05-10T21:32:53.419466Z"}
```

## 11. Aguardar saga

```bash
sleep 6
```

## 12. Validar débito

```bash
docker compose exec -T debit_account_service python -c "import sqlite3; c=sqlite3.connect('/data/debit_account.db'); print('accounts=', c.execute('select customer_id, balance from accounts where customer_id in (?, ?) order by customer_id', ('customer-1-20260510213126','customer-2-20260510213126')).fetchall()); print('entries=', c.execute('select transaction_id, account_id, amount, entry_type from accounting_entries where transaction_id=?', ('8bdd186a-cd08-4acc-9750-00e17820aecb',)).fetchall()); print('outbox=', c.execute('select event_name, routing_key, status from outbox_events where aggregate_id=? order by created_at', ('8bdd186a-cd08-4acc-9750-00e17820aecb',)).fetchall())"
```

Resultado:

```text
accounts= [('customer-1-20260510213126', '80.00'), ('customer-2-20260510213126', '50.00')]
entries= [('8bdd186a-cd08-4acc-9750-00e17820aecb', '6f437975-c32f-4cc9-9162-3dd14b3bfab8', '20.00', 'DEBIT')]
outbox= [('DebitCompleted', 'debit.completed', 'PUBLISHED')]
```

## 13. Validar confirmação de pagamento

```bash
docker compose exec -T confirm_payment_service python -c "import sqlite3; c=sqlite3.connect('/data/confirm_payment.db'); print('transactions=', c.execute('select id, merchant_id, status, confirmed_at from transactions where id=?', ('8bdd186a-cd08-4acc-9750-00e17820aecb',)).fetchall()); print('outbox=', c.execute('select event_name, routing_key, status from outbox_events where aggregate_id=? order by created_at', ('8bdd186a-cd08-4acc-9750-00e17820aecb',)).fetchall())"
```

Resultado:

```text
transactions= [('8bdd186a-cd08-4acc-9750-00e17820aecb', 'customer-2-20260510213126', 'CONFIRMED', '2026-05-10T21:32:55.648138+00:00')]
outbox= [('PaymentConfirmed', 'payment.confirmed', 'PUBLISHED')]
```

## 14. Validar ausência de reversão

```bash
docker compose exec -T reverse_payment_service python -c "import sqlite3; c=sqlite3.connect('/data/reverse_payment.db'); print(c.execute('select id, status, reversal_reason from transactions where id=?', ('8bdd186a-cd08-4acc-9750-00e17820aecb',)).fetchall())"
```

Resultado:

```text
[('8bdd186a-cd08-4acc-9750-00e17820aecb', 'STARTED', None)]
```

## 15. Validar notificação do merchant

```bash
docker compose exec -T notify_merchant_service python -c "import sqlite3; c=sqlite3.connect('/data/notify_merchant.db'); print('notifications=', c.execute('select transaction_id, merchant_id, channel, status from notifications where transaction_id=?', ('8bdd186a-cd08-4acc-9750-00e17820aecb',)).fetchall())"
```

Resultado:

```text
notifications= [('8bdd186a-cd08-4acc-9750-00e17820aecb', 'customer-2-20260510213126', 'WEBHOOK', 'DELIVERED')]
```

## 16. Validar notificação do customer

```bash
docker compose exec -T notify_customer_service python -c "import sqlite3; c=sqlite3.connect('/data/notify_customer.db'); print('notifications=', c.execute('select transaction_id, customer_id, channel, status from notifications where transaction_id=?', ('8bdd186a-cd08-4acc-9750-00e17820aecb',)).fetchall())"
```

Resultado:

```text
notifications= [('8bdd186a-cd08-4acc-9750-00e17820aecb', 'customer-1-20260510213126', 'PUSH', 'DELIVERED')]
```

## 17. Validar recibo

```bash
docker compose exec -T issue_receipt_service python -c "import sqlite3; c=sqlite3.connect('/data/issue_receipt.db'); print('receipts=', c.execute('select transaction_id, status, issued_at from receipts where transaction_id=?', ('8bdd186a-cd08-4acc-9750-00e17820aecb',)).fetchall())"
```

Resultado:

```text
receipts= [('8bdd186a-cd08-4acc-9750-00e17820aecb', 'ISSUED', '2026-05-10T21:32:56.952271+00:00')]
```

## 18. Validar eventos finais publicados

```bash
docker compose exec -T notify_merchant_service python -c "import sqlite3; c=sqlite3.connect('/data/notify_merchant.db'); print(c.execute('select event_name, routing_key, status, payload from outbox_events order by created_at desc limit 3').fetchall())"
docker compose exec -T notify_customer_service python -c "import sqlite3; c=sqlite3.connect('/data/notify_customer.db'); print(c.execute('select event_name, routing_key, status, payload from outbox_events order by created_at desc limit 3').fetchall())"
docker compose exec -T issue_receipt_service python -c "import sqlite3; c=sqlite3.connect('/data/issue_receipt.db'); print(c.execute('select event_name, routing_key, status, payload from outbox_events order by created_at desc limit 3').fetchall())"
```

Resultados esperados observados:

- `MerchantNotified`, `merchant.notified`, `PUBLISHED`
- `CustomerNotified`, `customer.notified`, `PUBLISHED`
- `ReceiptIssued`, `receipt.issued`, `PUBLISHED`

## 19. Verificar logs da saga

```bash
docker compose logs --no-color --tail=80 debit_account_outbox
docker compose logs --no-color --tail=80 confirm_payment_outbox
docker compose logs --no-color --tail=80 debit_account_consumer
docker compose logs --no-color --tail=80 confirm_payment_consumer
docker compose logs --no-color --tail=80 notify_customer_consumer
docker compose logs --no-color --tail=80 issue_receipt_consumer
```

Logs relevantes observados:

```text
debit_account_outbox: routing_key=debit.completed, transaction_id=8bdd186a-cd08-4acc-9750-00e17820aecb, correlation_id=perfect-day-20260510213126
confirm_payment_outbox: routing_key=payment.confirmed, transaction_id=8bdd186a-cd08-4acc-9750-00e17820aecb, correlation_id=perfect-day-20260510213126
```

## 20. Verificar observabilidade

```bash
curl -sS http://localhost:9090/-/ready
curl -sS http://localhost:3000/api/health
curl -sS http://localhost:16686/api/services
curl -sS 'http://localhost:9090/api/v1/query?query=http_requests_total'
```

Resultados observados:

- Prometheus: `Prometheus Server is Ready.`
- Grafana: `database=ok`
- Jaeger: serviços da saga visíveis, incluindo consumers e outbox workers.
- Prometheus: métricas `http_requests_total` disponíveis para os serviços.

