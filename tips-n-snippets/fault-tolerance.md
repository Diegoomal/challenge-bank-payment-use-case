# Fault Tolerance

## Summary

Fault Tolerance is the ability of a system to continue operating even when part of it fails.

The goal is not to avoid all failures, but to make the system handle failures safely without stopping completely.

Fault tolerance is commonly used in distributed systems, microservices, APIs, queues, cloud platforms, and event-driven architectures.

## When to Use

Use Fault Tolerance when you need to:

- Keep systems available during failures
- Prevent one failure from stopping the whole system
- Handle network errors
- Handle service outages
- Recover from temporary failures
- Protect critical business flows
- Improve reliability in production

## Common Failures

```text
Service unavailable
Database timeout
Message broker failure
Network instability
High latency
Consumer failure
External API outage
Node or pod crash
```

## Common Strategies

### Retry with Jitter

Retry temporary failures with random delays.

```text
Request fails → wait random time → retry
```

### Circuit Breaker

Stop calling a failing dependency temporarily.

```text
Dependency failing → circuit opens → fail fast
```

### Backpressure

Slow down or reject traffic when the system is overloaded.

```text
Too many requests → limit traffic
```

### Dead Letter Queue

Store messages that failed multiple times.

```text
Message fails repeatedly → move to DLQ
```

### Redundancy

Run multiple instances of a service.

```text
Service replica 1 fails
Service replica 2 continues running
```

### Graceful Degradation

Keep part of the system working even if some features fail.

```text
Recommendation service fails
Main checkout flow still works
```

## Practical Example

```text
1. Payment Service calls Fraud Service
2. Fraud Service is unavailable
3. Circuit breaker opens
4. Payment Service uses fallback behavior
5. Failed events are retried later
6. Messages that keep failing go to DLQ
7. System continues operating without full outage
```

## Benefits

- Improves system reliability
- Reduces downtime
- Prevents cascading failures
- Handles temporary failures safely
- Protects critical flows
- Improves user experience during incidents

## Challenges

- Adds architectural complexity
- Requires good monitoring
- Requires clear fallback behavior
- Retries must be controlled
- Some failures need manual recovery
- Poor configuration can hide real problems

## Related Concepts

```text
retry-with-jitter.md
circuit-breaker.md
backpressure.md
dead-letter-queue.md
high-availability.md
observability.md
```

## Simple Explanation

```text
Fault Tolerance means the system can keep working
even when some parts fail.
```