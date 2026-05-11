# Credit Account Service Overview

This repository contains `credit_account_service`, a Python service that follows
Ports and Adapters Architecture, also known as Hexagonal Architecture.

The service belongs to the Account bounded context. It credits the merchant
account after the customer account debit succeeds.

## Goal

The service performs the receiving side of the transfer flow.

Consumed event:

```text
debit.completed
```

Published events:

```text
credit.completed
credit.failed
```

## Business Rules

- The merchant account must exist.
- The credit amount must be greater than zero.
- The credit must be associated with a `transaction_id`.
- The same transaction must not be credited more than once.
- The operation is idempotent by `transaction_id`.
- Every successful credit generates a `CREDIT` accounting entry.
- A failed credit publishes `credit.failed`; it is not silently ignored.

## Main Commands

```bash
make run
make test
make lint
make docs
make check
```
