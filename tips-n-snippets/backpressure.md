# Backpressure

## Summary

Backpressure is a technique used to control the flow of data or requests when a system is receiving more work than it can process.

It prevents overload by slowing down, rejecting, buffering, or limiting incoming traffic.

Backpressure is commonly used in distributed systems, queues, APIs, streaming systems, microservices, and event-driven architectures.

## When to Use

Use backpressure when you need to:

- Prevent service overload
- Control high traffic volume
- Protect downstream services
- Avoid memory exhaustion
- Handle slow consumers
- Stabilize queues and workers
- Improve system resilience

## The Problem

Without backpressure:

```text
Producer sends messages too fast
Consumer cannot process fast enough
Queue grows indefinitely
Memory or latency increases
System becomes unstable
```

## The Solution

With backpressure:

```text
System detects overload
Traffic is slowed, limited, buffered, or rejected
Consumers process work at a safe rate
System remains stable
```

## Common Strategies

### Rate Limiting

Limit how many requests are accepted in a period.

```text
Maximum 100 requests per second
```

### Queue Limits

Set a maximum queue size.

```text
If queue is full, reject or delay new messages
```

### Load Shedding

Reject low-priority requests when the system is overloaded.

```text
Return HTTP 429 or 503
```

### Retry Later

Ask clients or producers to try again later.

```text
Retry-After: 10 seconds
```

### Consumer Scaling

Add more consumers to process messages faster.

```text
Queue size increases → add more workers
```

## Practical Example

```text
1. Payment events arrive too fast
2. Queue size starts increasing
3. System detects high queue depth
4. Producers are rate limited
5. Consumers process events at a safe speed
6. System avoids overload
```

## Benefits

- Prevents system overload
- Protects downstream services
- Improves stability
- Reduces cascading failures
- Helps handle traffic spikes
- Keeps queues under control

## Challenges

- Requires good thresholds
- Can increase latency
- May reject valid requests
- Needs monitoring
- Requires coordination between producers and consumers
- Poor configuration can hide capacity problems

## Related Concepts

```text
circuit-breaker.md
retry-with-jitter.md
dead-letter-queue.md
fault-tolerance.md
event-driven-architecture.md
rabbit-mq.md
observability.md
```

## Simple Explanation

```text
Backpressure means telling the system to slow down
when it is receiving more work than it can handle.
```