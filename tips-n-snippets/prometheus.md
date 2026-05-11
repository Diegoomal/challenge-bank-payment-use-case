# Prometheus

Prometheus coleta as métricas HTTP expostas pelos serviços FastAPI no endpoint
`/metrics`.

## Acesso

```text
http://localhost:9090
```

## Verificar saúde

```bash
curl -sS http://localhost:9090/-/ready
```

Resultado esperado:

```text
Prometheus Server is Ready.
```

## Verificar targets

Acesse:

```text
http://localhost:9090/targets
```

Todos os serviços devem aparecer como `UP`, incluindo:

- `account_service`
- `start_payment_service`
- `debit_account_service`
- `confirm_payment_service`
- `reverse_payment_service`
- `notify_merchant_service`
- `notify_customer_service`
- `issue_receipt_service`

## Consultas úteis

Total de requests HTTP:

```promql
http_requests_total
```

Taxa de requests nos últimos 5 minutos:

```promql
rate(http_requests_total[5m])
```

Quantidade de medições de duração por endpoint:

```promql
http_request_duration_seconds_count
```

Soma total das durações por endpoint:

```promql
http_request_duration_seconds_sum
```

Exemplo filtrando chamadas de criação de conta:

```promql
http_requests_total{service="account_service", method="POST", path="/accounts"}
```

Exemplo filtrando início de pagamento:

```promql
http_requests_total{service="start_payment_service", method="POST", path="/payments/start"}
```

## Validação via API

```bash
curl -sS 'http://localhost:9090/api/v1/query?query=http_requests_total'
```

Durante o teste do dia perfeito, devem aparecer métricas para:

- `POST /accounts`
- `POST /payments/start`
- `GET /metrics`
