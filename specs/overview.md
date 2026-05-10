# Bitbank Payment Saga Overview

Bitbank is a study project for a payment saga implemented with Ports and
Adapters Architecture, RabbitMQ topic events, FastAPI APIs, SQLite persistence,
and Docker Compose orchestration.

The system is split into small services around bounded contexts. Each service
owns its data model and communicates with other services through events instead
of direct domain-entity sharing.

## Architecture

Each service follows the same structure:

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

Main rules:

- `domain` contains aggregate roots, value objects, enums, and domain events.
- `application/ports` defines the contracts required by the use cases.
- `application/services` orchestrates domain behavior and port calls.
- `adapters` contains FastAPI, RabbitMQ, SQLite, and other infrastructure code.
- `configurator.py` wires concrete adapters into application services.
- Consumers must be idempotent by the business key of their bounded context.

## Services

| Service | Host Port | Responsibility |
| --- | ---: | --- |
| `account_service` | `8002` | Create accounts and publish account events |
| `start_payment_service` | `8000` | Start payment transactions and publish `payment.started` |
| `debit_account_service` | `8001` | Debit accounts through the API |
| `debit_account_consumer` | - | Consume `payment.started` and publish debit outcome events |
| `confirm_payment_service` | `8003` | Confirm payments through the API |
| `confirm_payment_consumer` | - | Consume debit success events and publish `payment.confirmed` |
| `reverse_payment_service` | `8004` | Reverse payments through the API |
| `reverse_payment_consumer` | - | Consume debit failure events and publish `payment.reversed` |
| `notify_merchant_service` | `8005` | Notify merchants after payment confirmation |
| `notify_merchant_consumer` | - | Consume `payment.confirmed` and publish `merchant.notified` |
| `notify_customer_service` | `8006` | Notify customers after payment confirmation |
| `notify_customer_consumer` | - | Consume `payment.confirmed` and publish `customer.notified` |
| `issue_receipt_service` | `8007` | Issue receipts after payment confirmation |
| `issue_receipt_consumer` | - | Consume `payment.confirmed` and publish `receipt.issued` |
| `rabbitmq` | `5672`, `15672` | Message broker and management UI |

## Saga Flow

```text
POST /payments/start
  -> start_payment_service creates a payment transaction
  -> publishes payment.started

debit_account_consumer
  -> consumes payment.started
  -> debits customer account
  -> publishes debit.completed or debit.failed

confirm_payment_consumer
  -> consumes payment.started for a local transaction projection
  -> consumes debit.completed
  -> confirms the payment
  -> publishes payment.confirmed

reverse_payment_consumer
  -> consumes payment.started for a local transaction projection
  -> consumes debit.failed
  -> reverses the payment
  -> publishes payment.reversed

notify_merchant_consumer
  -> consumes payment.confirmed
  -> notifies merchant
  -> publishes merchant.notified

notify_customer_consumer
  -> consumes payment.confirmed
  -> notifies customer
  -> publishes customer.notified

issue_receipt_consumer
  -> consumes payment.confirmed
  -> issues receipt
  -> publishes receipt.issued
```

## Events

The RabbitMQ topic exchange is named `payments`.

Main routing keys:

- `payment.started`
- `debit.completed`
- `debit.failed`
- `payment.confirmed`
- `payment.reversed`
- `merchant.notified`
- `customer.notified`
- `receipt.issued`

## Idempotency Rules

- Payment projections are idempotent by `transaction_id`.
- Merchant notifications are idempotent by `transaction_id + merchant_id`.
- Customer notifications are idempotent by `transaction_id + customer_id`.
- Receipts are idempotent by `transaction_id`.

Notification and receipt failures must not reverse or cancel a confirmed
payment.

## API Entry Points

Common local endpoints:

- `POST http://localhost:8002/accounts`
- `POST http://localhost:8000/payments/start`
- `POST http://localhost:8001/accounts/debit`
- `POST http://localhost:8003/payments/confirm`
- `POST http://localhost:8004/payments/reverse`
- `POST http://localhost:8005/notifications/merchant`
- `POST http://localhost:8006/notifications/customer`
- `POST http://localhost:8007/receipts`

RabbitMQ Management:

```text
http://localhost:15672
user: bitbank
password: bitbank
```
