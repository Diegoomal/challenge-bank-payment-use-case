# Notify Merchant Service

## Business Description

The `notify_merchant_service` is responsible for notifying the recipient after a payment transaction is confirmed.

This service belongs to the Notification context and represents the communication step with the merchant in the payment saga.

It consumes the `payment.confirmed` event, creates a notification for the merchant, attempts delivery through the configured channel, and publishes the `merchant.notified` event.

## Bounded Context

Notification.

## Ubiquitous Language

- Notification: message sent to a recipient.
- NotificationId: the unique notification identifier.
- Merchant: the payment recipient.
- Recipient: the notification recipient.
- Channel: the notification delivery channel.
- DeliveryStatus: the current delivery state.
- PaymentConfirmed: event that reports that the payment was confirmed.

## Aggregate Root

### Notification

The `Notification` is the Aggregate Root of the Notification context.

It controls the notification lifecycle and ensures that delivery is recorded correctly.

## Notification States

- PENDING
- DELIVERED
- FAILED

## Invariants

- The merchant can only be notified after the payment is confirmed.
- A notification must have a valid recipient.
- A notification must have a valid channel.
- A notification must be associated with a `transaction_id`.
- The same merchant must not receive duplicate notifications for the same transaction.
- The operation must be idempotent by `transaction_id` and `merchant_id`.
- Notification failure must not reverse or cancel the payment.

## Main Use Case

### NotifyMerchant

Responsible for notifying the merchant after the payment is confirmed.

Expected input:

- transaction_id
- customer_id
- merchant_id
- amount
- confirmed_at

Expected output:

- notification_id
- transaction_id
- merchant_id
- status
- notified_at

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

### MerchantNotified

Published when the merchant notification is processed successfully.

Suggested payload:

- notification_id
- transaction_id
- merchant_id
- amount
- channel
- status
- notified_at

## Ports

### NotificationRepository

Responsible for saving and retrieving notifications.

### NotificationGateway

Responsible for delivering the notification through an external channel.

### EventPublisher

Responsible for publishing domain events.

## Responsibilities

This service must:

- Consume the `payment.confirmed` event.
- Create a notification for the merchant.
- Validate the recipient.
- Validate the delivery channel.
- Attempt to deliver the notification.
- Persist the notification result.
- Publish the `merchant.notified` event.

This service must not:

- Create transactions.
- Debit accounts.
- Credit accounts.
- Confirm payments.
- Reverse payments.
- Notify customers.
- Issue receipts.
