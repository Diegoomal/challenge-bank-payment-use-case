# Start Payment Service

## Business Description

The `start_payment_service` is responsible for starting a payment transaction.

This service belongs to the Payment context and represents the first step of the payment saga.

It receives a payment request, creates a new `Transaction` with `STARTED` status, persists the transaction, and publishes the `payment.started` event.

## Bounded Context

Payment.

## Ubiquitous Language

- Payment: a payment requested by a customer.
- Transaction: the main payment record.
- TransactionId: the unique transaction identifier.
- TransactionStatus: the current transaction state.
- PaymentMethod: the method used to perform the payment.
- Amount: the monetary amount of the transaction.
- Customer: the paying customer.
- Merchant: the payment recipient.
- PaymentStarted: event that reports that a payment transaction was started.

## Aggregate Root

### Transaction

The `Transaction` is the Aggregate Root of the Payment context.

It controls the start of the payment lifecycle and ensures that a transaction is created in a valid state.

## Transaction States

- STARTED
- CONFIRMED
- REVERSED
- FAILED

## Invariants

- A transaction must have a unique `transaction_id`.
- A transaction must have a `customer_id`.
- A transaction must have a `merchant_id`.
- A transaction amount must be greater than zero.
- A transaction must have a valid payment method.
- A newly created transaction must start with `STARTED` status.
- A transaction must not be confirmed at creation time.
- A transaction must not be reversed at creation time.

## Main Use Case

### StartPayment

Responsible for starting a new payment transaction.

Expected input:

- customer_id
- merchant_id
- amount
- payment_method

Expected output:

- transaction_id
- status
- created_at

## Consumed Domain Events

This service does not consume domain events.

It is started by an external HTTP call.

## Published Domain Events

### PaymentStarted

Published when a payment transaction is created successfully.

Suggested payload:

- transaction_id
- customer_id
- merchant_id
- amount
- payment_method
- occurred_at

## Ports

### TransactionRepository

Responsible for saving and retrieving transactions.

### EventPublisher

Responsible for publishing domain events.

## Responsibilities

This service must:

- Receive a payment start request.
- Create a new transaction.
- Validate the initial payment data.
- Persist the transaction with `STARTED` status.
- Publish the `payment.started` event.

This service must not:

- Debit accounts.
- Credit accounts.
- Confirm payments.
- Reverse payments.
- Notify customers or merchants.
- Issue receipts.
