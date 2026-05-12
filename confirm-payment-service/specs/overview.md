# Confirm Payment Service

## Business Description

The `confirm_payment_service` is responsible for confirming a payment transaction after the recipient account has been credited successfully.

This service belongs to the Payment context and represents the step where the payment stops being only started and becomes confirmed.

It consumes the `credit.completed` event, validates whether the transaction can be confirmed, changes the status to `CONFIRMED`, and publishes the `payment.confirmed` event.

## Bounded Context

Payment.

## Ubiquitous Language

- Payment: a payment requested by a customer.
- Transaction: the main payment record.
- TransactionId: the unique transaction identifier.
- TransactionStatus: the current transaction state.
- Confirmation: confirmation that the payment was completed.
- CreditCompleted: event that reports that the recipient credit was completed successfully.

## Aggregate Root

### Transaction

The `Transaction` is the Aggregate Root of the Payment context.

It controls the payment lifecycle and ensures that a transaction is only confirmed in a valid state.

## Transaction States

- STARTED
- CONFIRMED
- REVERSED
- FAILED

## Invariants

- A transaction can only be confirmed if it has `STARTED` status.
- An already confirmed transaction cannot be confirmed again.
- A reversed transaction cannot be confirmed.
- A failed transaction cannot be confirmed.
- The confirmation must be associated with a `transaction_id`.
- The confirmation can only occur after the recipient credit is completed successfully.
- The confirmation must be idempotent by `transaction_id`.

## Main Use Case

### ConfirmPayment

Responsible for confirming a transaction after the credit is completed.

Expected input:

- transaction_id
- customer_id
- merchant_id
- account_id
- amount
- credited_at

Expected output:

- transaction_id
- status
- confirmed_at

## Consumed Domain Events

### CreditCompleted

Consumed when the recipient account credit was completed successfully.

Expected payload:

- transaction_id
- customer_id
- merchant_id
- account_id
- amount
- credited_at

## Published Domain Events

### PaymentConfirmed

Published when the payment is confirmed successfully.

Suggested payload:

- transaction_id
- customer_id
- merchant_id
- amount
- confirmed_at

## Ports

### TransactionRepository

Responsible for retrieving and saving transactions.

### EventPublisher

Responsible for publishing domain events.

## Responsibilities

This service must:

- Consume the `credit.completed` event.
- Find the transaction by `transaction_id`.
- Validate whether the transaction can be confirmed.
- Change the transaction status to `CONFIRMED`.
- Persist the change.
- Publish the `payment.confirmed` event.

This service must not:

- Create transactions.
- Debit accounts.
- Credit accounts.
- Reverse payments.
- Notify customers or merchants.
- Issue receipts.
