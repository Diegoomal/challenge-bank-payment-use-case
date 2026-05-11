# Reverse Payment Service

## Business Description

The `reverse_payment_service` is responsible for reversing a payment transaction when any financial step of the saga fails.

This service belongs to the Payment context and represents the saga compensation step.

It consumes the `debit.failed` or `credit.failed` events, validates whether the transaction can be reversed, changes the status to `REVERSED`, and publishes the `payment.reversed` event.

## Bounded Context

Payment.

## Ubiquitous Language

- Payment: a payment requested by a customer.
- Transaction: the main payment record.
- TransactionId: the unique transaction identifier.
- TransactionStatus: the current transaction state.
- Reversal: compensation action applied when the payment cannot be completed.
- ReversalReason: the reversal reason.
- DebitFailed: event that reports that the debit failed.
- CreditFailed: event that reports that the credit failed.

## Aggregate Root

### Transaction

The `Transaction` is the Aggregate Root of the Payment context.

It controls the payment lifecycle and ensures that a transaction is only reversed in a valid state.

## Transaction States

- STARTED
- CONFIRMED
- REVERSED
- FAILED

## Invariants

- A transaction can only be reversed if it has `STARTED` or `PROCESSING` status.
- An already confirmed transaction must not be reversed because of a debit or credit failure.
- An already reversed transaction must not be reversed again.
- A failed transaction must not be confirmed.
- The reversal must be associated with a `transaction_id`.
- The reversal must record the failure reason.
- The reversal must be idempotent by `transaction_id`.

## Main Use Case

### ReversePayment

Responsible for reversing a transaction after a debit or credit failure.

Expected input:

- transaction_id
- customer_id
- merchant_id
- amount
- reason
- occurred_at

Expected output:

- transaction_id
- status
- reversal_reason
- reversed_at

## Consumed Domain Events

### DebitFailed

Consumed when the customer's account debit fails.

Expected payload:

- transaction_id
- customer_id
- merchant_id
- amount
- reason
- failed_at

### CreditFailed

Consumed when the recipient account credit fails.

Expected payload:

- transaction_id
- customer_id
- merchant_id
- amount
- reason
- failed_at

## Published Domain Events

### PaymentReversed

Published when the payment transaction is reversed successfully.

Suggested payload:

- transaction_id
- customer_id
- merchant_id
- amount
- reason
- reversed_at

## Ports

### TransactionRepository

Responsible for retrieving and saving transactions.

### EventPublisher

Responsible for publishing domain events.

## Responsibilities

This service must:

- Consume the `debit.failed` and `credit.failed` events.
- Find the transaction by `transaction_id`.
- Validate whether the transaction can be reversed.
- Change the transaction status to `REVERSED`.
- Record the reversal reason.
- Persist the change.
- Publish the `payment.reversed` event.

This service must not:

- Create transactions.
- Debit accounts.
- Credit accounts.
- Confirm payments.
- Notify customers or merchants.
- Issue receipts.
