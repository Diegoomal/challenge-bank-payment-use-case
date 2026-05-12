<!-- AI context: use specs/overview.md as the primary project overview before making code changes. -->
# Account Service

Python service responsible for creating and maintaining customer financial
accounts in the Account bounded context.

The service implements the `CreateAccount` use case with Hexagonal
Architecture, FastAPI, SQLite persistence, and RabbitMQ event publishing.

## Responsibilities

- Create financial accounts.
- Validate initial account data.
- Prevent creating a second active account for the same customer.
- Persist accounts in SQLite.
- Publish `AccountCreated`.

This service does not debit balances, execute payments, notify users, issue
receipts, or authenticate customers.

## HTTP API

```text
POST /accounts
```

Request:

```json
{
  "customer_id": "customer-1",
  "account_holder": "Customer One",
  "initial_deposit": "100.00"
}
```

Response:

```json
{
  "account_id": "...",
  "customer_id": "customer-1",
  "status": "ACTIVE",
  "created_at": "..."
}
```

## Commands

```bash
make run
make test
make lint
make check
```
