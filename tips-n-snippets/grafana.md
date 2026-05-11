# Grafana

Grafana é usado para explorar métricas do Prometheus e traces do Jaeger.

## Acesso

```text
http://localhost:3000
```

Credenciais:

```text
user: bitbank
password: bitbank
```

## Verificar saúde

```bash
curl -sS http://localhost:3000/api/health
```

Resultado esperado:

```json
{
  "database": "ok"
}
```

## Datasources

As datasources são provisionadas automaticamente pelo Docker Compose:

- `Prometheus`
- `Jaeger`

## Consultar métricas

1. Acesse `http://localhost:3000`.
2. Faça login com `bitbank / bitbank`.
3. Abra **Explore**.
4. Selecione a datasource `Prometheus`.
5. Execute uma query PromQL.

Exemplos:

```promql
http_requests_total
```

```promql
rate(http_requests_total[5m])
```

```promql
http_requests_total{service="start_payment_service", method="POST", path="/payments/start"}
```

## Consultar traces

1. Acesse **Explore**.
2. Selecione a datasource `Jaeger`.
3. Escolha um serviço da saga.
4. Busque traces no intervalo de tempo do teste.

Serviços úteis para investigar o teste do dia perfeito:

- `account_service`
- `start_payment_service`
- `debit_account_consumer`
- `debit_account_outbox`
- `confirm_payment_consumer`
- `confirm_payment_outbox`
- `notify_merchant_consumer`
- `notify_customer_consumer`
- `issue_receipt_consumer`

## Correlação com logs

Os requests e eventos carregam `correlation_id`.

Exemplo usado no teste do dia perfeito:

```text
perfect-day-20260510214815
```

Use esse valor para comparar:

- logs JSON dos containers;
- eventos publicados por outbox;
- traces no Jaeger;
- métricas HTTP no Prometheus.
