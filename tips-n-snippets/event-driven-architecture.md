# Event-Driven Architecture

## Summary

Event-Driven Architecture is an architectural pattern where systems communicate through events.

An event represents something that already happened in the system, such as `OrderCreated`, `PaymentConfirmed`, or `UserRegistered`.

Instead of one service calling another directly, services publish events and other services react to them asynchronously.

This helps build systems that are decoupled, scalable, and easier to evolve.

## When to Use

Use Event-Driven Architecture when you need to:

- Decouple services
- Process tasks asynchronously
- Integrate multiple systems
- Build scalable microservices
- React to business events
- Reduce direct dependencies between services
- Improve resilience in distributed systems

## Common Components

### Event

A message that represents something that happened.

Example:

```json
{
  "event": "PaymentConfirmed",
  "payment_id": "123",
  "status": "confirmed"
}
```

### Producer

The service that publishes the event.

Example:

```text
Payment Service publishes PaymentConfirmed
```

### Consumer

The service that receives and processes the event.

Example:

```text
Notification Service consumes PaymentConfirmed
```

### Broker

The infrastructure responsible for transporting events.

Examples:

```text
RabbitMQ
Kafka
AWS SNS
AWS SQS
Google Pub/Sub
Azure Event Grid
```

## Event Flow

```text
Order Service
    ↓ publishes OrderCreated
Message Broker
    ↓ delivers event
Payment Service
    ↓ processes payment
    ↓ publishes PaymentConfirmed
Notification Service
    ↓ sends confirmation email
```

## Benefits

- Low coupling between services
- Better scalability
- Asynchronous processing
- Easier integration between systems
- Better support for distributed systems
- Services can evolve independently

## Challenges

- Harder debugging
- Event ordering issues
- Duplicate message handling
- Requires idempotency
- More complex observability
- Event versioning needs care

## Important Concepts

### Idempotency

Consumers must be able to process the same event more than once without causing duplicated side effects.

### Retry

If event processing fails, the system can retry later.

### Dead Letter Queue

A queue used to store messages that failed after multiple retries.

### Event Versioning

Events may evolve over time, so producers and consumers must remain compatible.

## Practical Example

```text
1. Customer creates an order
2. Order Service publishes OrderCreated
3. Payment Service consumes OrderCreated
4. Payment Service processes payment
5. Payment Service publishes PaymentConfirmed
6. Notification Service consumes PaymentConfirmed
7. Notification Service sends an email
```

## Example Event

```json
{
  "event_id": "evt-001",
  "event_type": "OrderCreated",
  "occurred_at": "2026-05-11T10:00:00Z",
  "payload": {
    "order_id": "ord-123",
    "customer_id": "cus-456",
    "total": 150.00
  }
}
```

## Practical Use Cases

- Payment processing
- Order management
- Notification systems
- Audit logs
- Data synchronization
- Microservices communication
- AI workflows and agent orchestration

## Simple Explanation

```text
In a traditional system, one service directly calls another.

In an event-driven system, one service announces that something happened,
and other services decide what to do with that information.
```