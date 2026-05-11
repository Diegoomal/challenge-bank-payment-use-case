# Dead Letter Queue

## Summary

Dead Letter Queue, also known as DLQ, is a queue used to store messages that could not be processed successfully.

When a message fails many times, instead of being retried forever, it is moved to a DLQ for later analysis or manual recovery.

DLQ is commonly used in event-driven architecture, queues, microservices, and distributed systems.

## When to Use

Use Dead Letter Queue when you need to:

- Handle messages that fail repeatedly
- Avoid infinite retry loops
- Investigate processing errors
- Protect consumers from bad messages
- Keep the main queue healthy
- Recover failed events later
- Improve system resilience

## The Problem

Without DLQ:

```text
Consumer receives message
Processing fails
Message is retried
Processing fails again
Message keeps returning to the queue
System wastes resources
Other messages may be delayed
```

## The Solution

With DLQ:

```text
Consumer receives message
Processing fails multiple times
Retry limit is reached
Message is moved to Dead Letter Queue
Main queue continues processing other messages
```

## Practical Example

```text
1. PaymentConfirmed event is published
2. Notification Service consumes the event
3. Email sending fails
4. The message is retried 3 times
5. After repeated failures, the message goes to DLQ
6. Team analyzes the failed message later
```

## Common Causes

```text
Invalid message format
Missing required fields
Consumer bug
External API unavailable
Database error
Timeout
Unexpected business rule failure
```

## Benefits

- Prevents infinite retries
- Keeps queues healthy
- Improves fault tolerance
- Helps debug failed messages
- Allows manual or automated recovery
- Protects the system from poison messages

## Challenges

- DLQ must be monitored
- Failed messages need investigation
- Reprocessing requires care
- Messages can become outdated
- Consumers must still be idempotent
- Too many messages in DLQ may indicate a bigger problem

## Related Concepts

```text
event-driven-architecture.md
rabbit-mq.md
retry-with-jitter.md
backpressure.md
circuit-breaker.md
idempotency.md
observability.md
```

## Simple Explanation

```text
Dead Letter Queue is where failed messages go
when the system cannot process them after multiple attempts.
```