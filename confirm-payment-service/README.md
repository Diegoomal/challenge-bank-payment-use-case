<!-- AI context: use specs/overview.md as the primary project overview before making code changes. -->
# Confirm Payment Service

Python service responsible for confirming payment transactions after account
debit succeeds.

The service implements the `ConfirmPayment` use case with Hexagonal
Architecture, FastAPI, SQLite persistence, RabbitMQ event publishing, and a
RabbitMQ consumer for payment saga events.

## Responsibilities

- Consume `payment.started` to keep a local transaction projection.
- Consume `debit.completed`.
- Confirm transactions that are still `STARTED`.
- Persist the confirmed transaction state.
- Publish `PaymentConfirmed` as `payment.confirmed`.

## HTTP API

```text
POST /payments/confirm
```

## Commands

```bash
make run
make test
make lint
make check
```
