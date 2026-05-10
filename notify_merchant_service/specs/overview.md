# Reverse Payment Service Overview

This repository contains `reverse_payment_service`, a Python service that
follows Ports and Adapters Architecture, also known as Hexagonal Architecture.

The service belongs to the Payment bounded context. It compensates the payment
saga by reversing a transaction after account debit fails.

## Goal

The service reverses transactions after account debit failure.

Consumed events:

```text
payment.started
debit.failed
```

Published event:

```text
payment.reversed
```

Business rules:

- only `STARTED` or `PROCESSING` transactions can be reversed;
- `CONFIRMED`, `REVERSED`, and `FAILED` transactions cannot be reversed again;
- reversal requires `transaction_id` and reason;
- service-level reversal is idempotent for already reversed transactions.

## Main Commands

```bash
make run
make test
make lint
make docs
make check
```
