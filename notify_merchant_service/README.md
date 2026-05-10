<!-- AI context: use specs/overview.md as the primary project overview before making code changes. -->
# Reverse Payment Service

Python service responsible for reversing payment transactions when account debit
fails.

The service implements the `ReversePayment` use case with Hexagonal
Architecture, FastAPI, SQLite persistence, RabbitMQ event publishing, and a
RabbitMQ consumer for saga events.

## Responsibilities

- Consume `payment.started` to keep a local transaction projection.
- Consume `debit.failed`.
- Reverse transactions that are `STARTED` or `PROCESSING`.
- Persist the reversal state and reason.
- Publish `PaymentReversed` as `payment.reversed`.

## HTTP API

```text
POST /payments/reverse
```
