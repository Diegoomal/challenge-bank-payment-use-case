# Confirm Payment Service Overview

This repository contains `confirm_payment_service`, a Python service that
follows Ports and Adapters Architecture, also known as Hexagonal Architecture.

The service belongs to the Payment bounded context. It confirms a payment after
receiving a successful debit event and publishes `PaymentConfirmed`.

## Goal

The service confirms transactions after account debit succeeds.

Transaction fields:

- `id`
- `status`
- `confirmed_at`
- `created_at`
- `updated_at`

The main operation is exposed by `ForConfirmingPayment`:

- confirm a payment from a `DebitCompleted` event.

Business rules:

- only `STARTED` transactions can be confirmed;
- already confirmed transactions cannot be confirmed again;
- reversed transactions cannot be confirmed;
- failed transactions cannot be confirmed;
- confirmation requires a `transaction_id`;
- confirmation happens only after a successful debit.

## Architecture

```text
src/
├── configurator.py
├── consumer.py
├── main.py
├── domain/
├── application/
│   ├── ports/
│   └── services/
└── adapters/
    ├── api/
    ├── messaging/
    └── persistence/
```

## Messaging

Consumed events:

```text
payment.started
debit.completed
```

Published event:

```text
payment.confirmed
```

## Main Commands

```bash
make run
make test
make lint
make docs
make check
```
