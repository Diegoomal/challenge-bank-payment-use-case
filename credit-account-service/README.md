<!-- AI context: use specs/overview.md as the primary project overview before making code changes. -->
# Credit Account Service

Python service responsible for crediting the merchant account after the customer
account has been successfully debited.

The service belongs to the Account bounded context and implements the second
financial movement of the transfer flow with Hexagonal Architecture, FastAPI,
SQLite persistence, RabbitMQ event consumption, and outbox-based event
publishing.

## Responsibilities

- Consume `debit.completed`.
- Locate the merchant account by `merchant_id`.
- Credit the payment amount to the merchant account.
- Keep the credit idempotent by `transaction_id`.
- Persist a `CREDIT` accounting entry for every successful credit.
- Publish `CreditCompleted` as `credit.completed`.
- Publish `CreditFailed` as `credit.failed` when the merchant account cannot be credited.

## HTTP API

```text
POST /accounts/credit
```
