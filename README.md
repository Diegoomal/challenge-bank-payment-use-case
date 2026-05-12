<!-- AI context: use specs/overview.md as the primary project overview before making code changes. -->
# Bank - Payment Use Case

Bitbank is a study project for a payment flow built as an event-driven saga.
The goal is to show how a payment can move through independent services while
keeping each service focused on its own business boundary, data model, and
infrastructure adapters.

This README is the project presentation. For the detailed service map, ports,
routing keys, API endpoints, and idempotency rules, see
[specs/overview.md](specs/overview.md).

## What This Project Demonstrates

- A distributed payment saga from payment start to debit, credit, confirmation,
  compensation, notifications, and receipt issuing.
- Event-driven communication between services with RabbitMQ topic routing.
- Hexagonal Architecture, also known as Ports and Adapters, applied consistently
  across the services.
- Service-owned persistence, where each service keeps its own SQLite database
  instead of sharing domain tables.
- Idempotent consumers for projections, notifications, and receipt issuing.
- Transactional outbox workers for asynchronous broker publishing from service
  databases.
- Structured JSON logs with correlation IDs, trace IDs, span IDs, business
  event names, routing keys, and transaction IDs.
- Distributed tracing across FastAPI requests and RabbitMQ saga messages with
  OpenTelemetry and Jaeger.
- Local orchestration with Docker Compose and Kubernetes for services, broker,
  gateway, and observability tools.
- Automated tests focused on domain behavior, application use cases, adapters,
  and HTTP APIs.

## Techniques Applied

| Technique | How it appears in the project |
| --- | --- |
| Saga pattern | The payment is processed through ordered steps and compensation is triggered when debit fails. |
| Event-driven architecture | Services publish and consume RabbitMQ events instead of calling each other directly for saga progression. |
| Ports and Adapters | Domain and application code stay independent from FastAPI, RabbitMQ, and SQLite details. |
| Domain-driven boundaries | Each service models one business capability, such as account debit, payment confirmation, notification, or receipt issuing. |
| Idempotency | Consumers use business keys such as `transaction_id`, `transaction_id + merchant_id`, and `transaction_id + customer_id + notification_type`. |
| Outbox pattern | Services persist outgoing events in `outbox_events`; worker containers publish pending events to RabbitMQ. |
| Local projections | Services that need payment context store their own projection from `payment.started`. |
| Container orchestration | Docker Compose runs the full local environment, and Kubernetes manifests support local cluster execution. |
| Structured logs | Services write JSON logs to stdout with `correlation_id`, `trace_id`, `span_id`, `event`, `routing_key`, and `transaction_id`. |
| Distributed tracing | OpenTelemetry instruments FastAPI and RabbitMQ publish/consume operations; Jaeger displays traces locally. |
| Metrics | Prometheus scrapes service `/metrics` endpoints and Grafana is available for dashboards. |

## Technologies

| Area | Stack |
| --- | --- |
| Language | Python |
| HTTP APIs | FastAPI |
| Messaging | RabbitMQ topic exchange |
| Persistence | SQLite per service |
| Containers | Docker, Docker Compose, Kubernetes, Minikube, Kompose |
| Gateway | Nginx API gateway |
| Tests | pytest |
| Quality commands | Make, flake8 configuration |
| Observability | Structured JSON logs, OpenTelemetry, Jaeger, Prometheus, Grafana |

## Payment Flow

The main flow follows these steps:

```text
1. Account is created
   -> account_service publishes account.created

2. Payment is started
   -> start_payment_service stores the transaction
   -> publishes payment.started

3. Customer account is debited
   -> debit_account_consumer consumes payment.started
   -> debit_account_service debits the account
   -> publishes debit.completed or debit.failed

4. Merchant account is credited
   -> credit_account_consumer consumes debit.completed
   -> credit_account_service credits the merchant account
   -> publishes credit.completed or credit.failed

5. Payment is confirmed or reversed
   -> confirm_payment_consumer consumes credit.completed
   -> publishes payment.confirmed

   -> reverse_payment_consumer consumes debit.failed
   -> publishes payment.reversed

   -> reverse_payment_consumer consumes credit.failed
   -> publishes payment.reversed

   -> notify_customer_consumer consumes payment.reversed
   -> publishes customer.notified

6. Post-confirmation actions run independently
   -> notify_merchant_consumer publishes merchant.notified
   -> notify_customer_consumer publishes customer.notified
   -> issue_receipt_consumer publishes receipt.issued
```

Customer notifications also run after payment reversal, so the customer is
informed about failed or compensated payments. Merchant notifications and
receipt issuing remain post-confirmation side effects.

## Services At A Glance

| Service | Responsibility |
| --- | --- |
| `account_service` | Creates customer financial accounts. |
| `start_payment_service` | Starts payment transactions. |
| `debit_account_service` | Debits customer account balance. |
| `credit_account_service` | Credits merchant account balance after successful debit. |
| `confirm_payment_service` | Confirms payments after successful credit. |
| `reverse_payment_service` | Reverses payments after failed debit or credit. |
| `notify_merchant_service` | Notifies merchants after payment confirmation. |
| `notify_customer_service` | Notifies customers after payment confirmation or reversal. |
| `issue_receipt_service` | Issues receipts after payment confirmation. |
| `api_gateway` | Exposes a single local HTTP entry point. |
| `rabbitmq` | Handles saga events and consumer delivery. |

## Architecture Shape

Each service follows the same internal layout:

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
│   ├── consumer.py
│   └── main.py
├── tests/
├── specs/
├── requirements.txt
└── dockerfile
```

The `domain` layer contains business concepts and events. The `application`
layer defines ports and use cases. The `adapters` layer contains framework,
broker, and database integrations.

## Run Locally

The project can be executed locally in two ways:

- Docker Compose, for the simplest local setup.
- Kubernetes with Minikube, for a local cluster setup generated from the Compose
  stack.

### Docker Compose

Start the full environment:

```bash
docker compose up -d --build
```

Check the containers:

```bash
docker compose ps
```

Follow service logs:

```bash
docker compose logs -f start_payment_service
docker compose logs -f debit_account_consumer
docker compose logs -f confirm_payment_consumer
```

Stop everything:

```bash
docker compose down
```

Remove local volumes and service databases:

```bash
docker compose down -v
```

RabbitMQ Management UI:

```text
http://localhost:15672
user: bitbank
password: bitbank
```

### Kubernetes

The project also includes Kubernetes support for running the same local stack in
Minikube. The manifests in `k8s/generated/` are generated from
`docker-compose.yml` with Kompose, and the helper script builds the images
inside Minikube's Docker environment before applying the manifests.

Prerequisites:

```text
Docker
Minikube
kubectl
Kompose
```

Start the Kubernetes environment:

```bash
./scripts/k8s-local-up.sh
```

The script runs these steps:

```text
1. starts Minikube with the Docker driver
2. points Docker commands to Minikube's Docker daemon
3. builds the Docker Compose images
4. regenerates manifests under k8s/generated/
5. applies the manifests with kubectl
6. lists pods, services, and deployments
```

Check the workload state:

```bash
kubectl get pods
kubectl get services
kubectl get deployments
```

Follow logs for a service or worker:

```bash
kubectl logs -f deployment/start-payment-service
kubectl logs -f deployment/debit-account-consumer
kubectl logs -f deployment/confirm-payment-consumer
```

Expose local UIs or API services with port-forwarding when needed:

```bash
kubectl port-forward service/api-gateway 8080:8080
kubectl port-forward service/rabbitmq 15672:15672
kubectl port-forward service/jaeger 16686:16686
kubectl port-forward service/prometheus 9090:9090
kubectl port-forward service/grafana 3000:3000
```

Stop and remove the Kubernetes resources:

```bash
./scripts/k8s-local-down.sh
```

## Observability

The local environment includes structured logs, distributed tracing, and
metrics.

### Structured Logs

Each service writes JSON logs to stdout. Logs include operational context and
business identifiers so a saga can be followed across containers.

Common fields:

```json
{
  "timestamp": "2026-05-11T19:41:52.021240+00:00",
  "level": "INFO",
  "service": "confirm_payment_outbox",
  "logger": "shared.observability.messaging",
  "message": "message published",
  "correlation_id": "perfect-day-20260511164110",
  "trace_id": "321c7d489fd5d7c995c55807ea5db724",
  "span_id": "fe8e7ae59bbbbc52",
  "event": "message.published",
  "routing_key": "payment.confirmed",
  "transaction_id": "1dbb08cf-0d12-4666-a282-087d1368884b"
}
```

Useful log commands:

```bash
docker compose logs -f start_payment_service
docker compose logs -f debit_account_consumer credit_account_consumer
docker compose logs -f confirm_payment_consumer notify_customer_consumer
```

### Distributed Tracing

FastAPI requests and RabbitMQ publish/consume operations are instrumented with
OpenTelemetry. Message publishers inject trace context into RabbitMQ headers,
and consumers extract it so saga steps remain connected in Jaeger.

Jaeger UI:

```text
http://localhost:16686
```

The OpenTelemetry Collector receives OTLP traffic on:

```text
http://localhost:4318
grpc://localhost:4317
```

Services are configured through environment variables in `docker-compose.yml`:

```text
OTEL_SERVICE_NAME=<service_name>
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel_collector:4318
LOG_LEVEL=INFO
```

### Metrics

Each FastAPI service exposes Prometheus metrics at `/metrics`. Prometheus and
Grafana are available locally:

```text
Prometheus: http://localhost:9090
Grafana:    http://localhost:3000
```

## Useful Documentation

- [specs/overview.md](specs/overview.md): detailed architecture, services,
  ports, events, idempotency rules, and API entry points.
- [specs/setup.md](specs/setup.md): local setup and test commands.
- [tips-n-snippets/ports-and-adapters-architecture.md](tips-n-snippets/ports-and-adapters-architecture.md): architecture notes.
- [tips-n-snippets/jaeger.md](tips-n-snippets/jaeger.md): tracing notes.
- [tips-n-snippets/prometheus.md](tips-n-snippets/prometheus.md): metrics notes.
- [tips-n-snippets/grafana.md](tips-n-snippets/grafana.md): dashboard notes.

## Current Notes

The project already implements the main payment saga path, including payment
start, debit, confirmation, reversal, merchant notification, customer
notification, and receipt issuing.

Known next improvements:

- Project `account.created` into `debit_account_service` automatically.
- Expand account administration endpoints beyond account creation.
