# Issue Receipt Service

## Business Description

The `issue_receipt_service` is responsible for issuing the receipt after a payment transaction is confirmed.

This service belongs to the Receipt context and represents the document generation step of the payment saga.

It consumes the `payment.confirmed` event, creates a receipt with a snapshot of the confirmed transaction data, persists the receipt, and publishes the `receipt.issued` event.

## Bounded Context

Receipt.

## Ubiquitous Language

- Receipt: document that proves a confirmed payment.
- ReceiptId: the unique receipt identifier.
- TransactionData: snapshot of the confirmed transaction data.
- IssuingStatus: the current receipt issuing state.
- PaymentConfirmed: event that reports that the payment was confirmed.

## Aggregate Root

### Receipt

The `Receipt` is the Aggregate Root of the Receipt context.

It controls the issuing lifecycle and ensures that only one valid receipt is issued for each transaction.

## Receipt States

- PENDING
- ISSUED
- FAILED

## Invariants

- A receipt can only be issued after the payment is confirmed.
- A receipt must be associated with a `transaction_id`.
- A transaction must have at most one valid receipt.
- The receipt must contain a snapshot of the transaction data.
- The receipt must not directly depend on the `Transaction` entity from another service.
- Issuing must be idempotent by `transaction_id`.
- If a receipt already exists for the transaction, the service must return the existing one or ignore the duplicate event.

## Main Use Case

### IssueReceipt

Responsible for issuing the receipt after the payment is confirmed.

Expected input:

- transaction_id
- customer_id
- merchant_id
- amount
- confirmed_at

Expected output:

- receipt_id
- transaction_id
- status
- issued_at

## Consumed Domain Events

### PaymentConfirmed

Consumed when the payment transaction is confirmed.

Expected payload:

- transaction_id
- customer_id
- merchant_id
- amount
- confirmed_at

## Published Domain Events

### ReceiptIssued

Published when the receipt is issued successfully.

Suggested payload:

- receipt_id
- transaction_id
- customer_id
- merchant_id
- amount
- issued_at

## Ports

### ReceiptRepository

Responsible for saving and retrieving receipts.

### ReceiptGenerator

Responsible for generating the receipt data or document.

### EventPublisher

Responsible for publishing domain events.

## Responsibilities

This service must:

- Consume the `payment.confirmed` event.
- Create a receipt for the confirmed transaction.
- Store a snapshot of the transaction data.
- Ensure idempotency by `transaction_id`.
- Persist the receipt.
- Publish the `receipt.issued` event.

This service must not:

- Create transactions.
- Debit accounts.
- Credit accounts.
- Confirm payments.
- Reverse payments.
- Notify customers or merchants.
