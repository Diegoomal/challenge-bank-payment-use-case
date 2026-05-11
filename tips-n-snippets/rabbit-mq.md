# RabbitMQ

## Summary

RabbitMQ is a message broker used to send messages between systems, services, or applications.

It helps services communicate asynchronously, without requiring them to be online or directly connected at the same time.

RabbitMQ is commonly used in microservices, event-driven architecture, background jobs, queues, retries, and distributed systems.

## When to Use

Use RabbitMQ when you need to:

- Process tasks asynchronously
- Decouple services
- Use queues between applications
- Retry failed operations
- Distribute work between workers
- Handle background processing
- Build event-driven systems
- Avoid direct service-to-service dependencies

## Core Concepts

### Producer

The application that sends a message.

```text
Payment Service publishes PaymentConfirmed
```

### Queue

A storage buffer where messages wait until they are consumed.

```text
payment-confirmed-queue
```

### Consumer

The application that receives and processes messages from a queue.

```text
Notification Service consumes PaymentConfirmed
```

### Exchange

Receives messages from producers and routes them to queues.

```text
Producer → Exchange → Queue → Consumer
```

### Binding

Connects an exchange to a queue using routing rules.

```text
Exchange is bound to Queue
```

### Routing Key

A key used by RabbitMQ to decide where to route the message.

```text
payment.confirmed
```

## Exchange Types

### Direct Exchange

Routes messages using an exact routing key.

```text
routing_key = payment.confirmed
```

### Fanout Exchange

Broadcasts the message to all bound queues.

```text
One message → many queues
```

### Topic Exchange

Routes messages using patterns.

```text
payment.*
order.created
```

### Headers Exchange

Routes messages based on message headers instead of routing keys.

## Example Flow

```text
Payment Service
    ↓ publishes PaymentConfirmed
Exchange
    ↓ routes by routing key
Queue
    ↓ stores message
Notification Service
    ↓ consumes message
```

## Example Message

```json
{
  "event_id": "evt-001",
  "event_type": "PaymentConfirmed",
  "routing_key": "payment.confirmed",
  "payload": {
    "payment_id": "pay-123",
    "account_id": "acc-456",
    "amount": 100.00
  }
}
```

## Useful Commands

Run RabbitMQ with Docker:

```bash
docker run -d \
  --name rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:3-management
```

Access management UI:

```text
http://localhost:15672
```

Default credentials:

```text
user: guest
password: guest
```

## Benefits

- Asynchronous communication
- Decouples services
- Supports retries
- Supports work queues
- Supports routing patterns
- Good for background jobs
- Good fit for event-driven systems

## Challenges

- Requires monitoring
- Consumers must be idempotent
- Message ordering can be complex
- Failed messages need retry or DLQ
- Queue growth can indicate problems
- Requires careful exchange and queue design

## Important Concepts

### Acknowledgement

A consumer confirms that a message was processed successfully.

```text
Message processed → ACK
```

If the consumer fails, the message can be requeued.

### Dead Letter Queue

A queue used to store messages that failed after retries.

```text
failed messages → DLQ
```

### Retry

Failed messages can be processed again later.

### Durability

Queues and messages can be configured to survive broker restarts.

## Practical Use Cases

- Payment events
- Notification systems
- Email sending
- Background jobs
- Order processing
- Webhook processing
- Distributed task processing
- Microservices communication

## Simple Explanation

```text
RabbitMQ is like a post office for systems.

One service sends a message,
RabbitMQ stores and routes it,
and another service receives it when ready.
```