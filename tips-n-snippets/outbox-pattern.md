# Outbox Pattern

## Summary

Outbox Pattern is a reliability pattern used to guarantee that a database change and an event publication happen consistently.

Instead of saving data in the database and publishing an event directly to a broker, the application saves both the business data and the event in the same database transaction.

Later, a separate process reads the outbox table and publishes the event to the message broker.

This avoids losing events when the database operation succeeds but the message broker publication fails.

## When to Use

Use Outbox Pattern when you need to:

- Publish events reliably
- Avoid losing domain events
- Keep database changes and event publication consistent
- Work with microservices
- Work with event-driven architecture
- Avoid distributed transactions
- Support retries when publishing events fails

## The Problem

Without Outbox Pattern:

```text
1. Payment is confirmed in the database
2. System tries to publish PaymentConfirmed event
3. Message broker is unavailable
4. Event is lost
5. Other services never know the payment was confirmed
```

## The Solution

With Outbox Pattern:

```text
1. Payment is confirmed in the database
2. PaymentConfirmed event is saved in the outbox table
3. Both happen in the same database transaction
4. A worker reads the outbox table
5. The worker publishes the event to the message broker
6. The event is marked as published
```

## Event Flow

```text
Application Service
    ↓ saves business data
Database
    ↓ saves event in outbox table
Outbox Worker
    ↓ reads pending events
Message Broker
    ↓ delivers event
Consumer Service
```

## Example Outbox Table

```sql
CREATE TABLE outbox_events (
    id UUID PRIMARY KEY,
    event_type VARCHAR(255) NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    published_at TIMESTAMP NULL
);
```

## Example Event

```json
{
  "id": "evt-001",
  "event_type": "PaymentConfirmed",
  "payload": {
    "payment_id": "pay-123",
    "account_id": "acc-456",
    "amount": 100.00
  },
  "status": "pending",
  "created_at": "2026-05-11T10:00:00Z"
}
```

## Practical Example

```text
1. ConfirmPaymentService confirms the payment
2. Payment status changes to Confirmed
3. PaymentConfirmed event is saved in the outbox table
4. Transaction is committed
5. Outbox worker finds the pending event
6. Worker publishes PaymentConfirmed to RabbitMQ, Kafka, SNS, or SQS
7. Event status changes to Published
```

## Benefits

- Prevents lost events
- Makes event publishing reliable
- Avoids distributed transactions
- Supports retries
- Improves consistency between database and messaging
- Works well with Domain Events and Event-Driven Architecture

## Challenges

- Requires an outbox table
- Requires a background worker
- Events may be published more than once
- Consumers must be idempotent
- Requires cleanup strategy for old events
- Adds operational complexity

## Important Concepts

### Atomic Transaction

The business change and the outbox event are saved together.

```text
Update payment + insert event = same transaction
```

### Outbox Worker

A background process responsible for publishing pending events.

```text
pending → published
```

### Retry

If publishing fails, the worker can try again later.

### Idempotency

Consumers must handle duplicate events safely.

## Simple Explanation

```text
Outbox Pattern means saving the event in the database first,
then publishing it later in a reliable way.
```