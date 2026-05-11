<!-- AI context: use specs/overview.md as the primary project overview before making code changes. -->
# Bitbank Payment Saga

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
- Local orchestration with Docker Compose for services, broker, gateway, and
  observability tools.
- Automated tests focused on domain behavior, application use cases, adapters,
  and HTTP APIs.

## Techniques Applied

| Technique | How it appears in the project |
| --- | --- |
| Saga pattern | The payment is processed through ordered steps and compensation is triggered when debit fails. |
| Event-driven architecture | Services publish and consume RabbitMQ events instead of calling each other directly for saga progression. |
| Ports and Adapters | Domain and application code stay independent from FastAPI, RabbitMQ, and SQLite details. |
| Domain-driven boundaries | Each service models one business capability, such as account debit, payment confirmation, notification, or receipt issuing. |
| Idempotency | Consumers use business keys such as `transaction_id`, `transaction_id + merchant_id`, and `transaction_id + customer_id`. |
| Outbox pattern | Services persist outgoing events in `outbox_events`; worker containers publish pending events to RabbitMQ. |
| Local projections | Services that need payment context store their own projection from `payment.started`. |
| Container orchestration | Docker Compose runs the full local environment with isolated services. |
| Observability | The repository includes Prometheus, Grafana, and Jaeger configuration and notes. |

## Technologies

| Area | Stack |
| --- | --- |
| Language | Python |
| HTTP APIs | FastAPI |
| Messaging | RabbitMQ topic exchange |
| Persistence | SQLite per service |
| Containers | Docker and Docker Compose |
| Gateway | Nginx API gateway |
| Tests | pytest |
| Quality commands | Make, flake8 configuration |
| Observability | Prometheus, Grafana, Jaeger, OpenTelemetry configuration |

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

6. Post-confirmation actions run independently
   -> notify_merchant_consumer publishes merchant.notified
   -> notify_customer_consumer publishes customer.notified
   -> issue_receipt_consumer publishes receipt.issued
```

Notification and receipt failures do not cancel a confirmed payment. They are
post-confirmation side effects and have their own idempotency rules.

## Services At A Glance

| Service | Responsibility |
| --- | --- |
| `account_service` | Creates customer financial accounts. |
| `start_payment_service` | Starts payment transactions. |
| `debit_account_service` | Debits customer account balance. |
| `credit_account_service` | Credits merchant account balance after successful debit. |
| `confirm_payment_service` | Confirms payments after successful credit. |
| `reverse_payment_service` | Reverses payments after failed debit. |
| `notify_merchant_service` | Notifies merchants after payment confirmation. |
| `notify_customer_service` | Notifies customers after payment confirmation. |
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
