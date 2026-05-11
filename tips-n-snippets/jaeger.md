# Jaeger

Jaeger recebe traces exportados pelo OpenTelemetry Collector.

## Acesso

```text
http://localhost:16686
```

## Verificar serviços instrumentados

```bash
curl -sS http://localhost:16686/api/services
```

Resultado esperado: lista de serviços instrumentados, por exemplo:

- `account_service`
- `start_payment_service`
- `debit_account_service`
- `debit_account_consumer`
- `debit_account_outbox`
- `confirm_payment_service`
- `confirm_payment_consumer`
- `confirm_payment_outbox`
- `notify_merchant_service`
- `notify_merchant_consumer`
- `notify_customer_service`
- `notify_customer_consumer`
- `issue_receipt_service`
- `issue_receipt_consumer`

## Buscar traces pela interface

1. Acesse `http://localhost:16686`.
2. No campo **Service**, selecione um serviço.
3. Ajuste o intervalo de tempo para o momento do teste.
4. Clique em **Find Traces**.

Serviços úteis para o teste do dia perfeito:

- `start_payment_service`: início do pagamento.
- `debit_account_consumer`: consumo de `payment.started`.
- `debit_account_outbox`: publicação de `debit.completed`.
- `confirm_payment_consumer`: consumo de `debit.completed`.
- `confirm_payment_outbox`: publicação de `payment.confirmed`.
- `notify_merchant_consumer`: notificação do merchant.
- `notify_customer_consumer`: notificação do customer.
- `issue_receipt_consumer`: emissão do recibo.

## Correlação com o teste do dia perfeito

Os eventos RabbitMQ e logs carregam `correlation_id`.

Exemplo usado no teste:

```text
perfect-day-20260510214815
```

Esse valor aparece nos logs JSON e nos atributos dos spans de mensageria.

Exemplo de logs relacionados:

```text
routing_key=debit.completed
transaction_id=4813d6cd-b7e1-4869-8b28-46fbacd8e8bd
correlation_id=perfect-day-20260510214815
```

```text
routing_key=payment.confirmed
transaction_id=4813d6cd-b7e1-4869-8b28-46fbacd8e8bd
correlation_id=perfect-day-20260510214815
```

## Fluxo esperado no Jaeger

Durante o teste do dia perfeito, devem existir traces para:

1. `POST /accounts`
2. `POST /payments/start`
3. consumo de `payment.started`
4. publicação de `debit.completed`
5. consumo de `debit.completed`
6. publicação de `payment.confirmed`
7. consumo de `payment.confirmed`
8. publicação de:
   - `merchant.notified`
   - `customer.notified`
   - `receipt.issued`
