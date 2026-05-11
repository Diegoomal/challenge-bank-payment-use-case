# Retry with Jitter

## Summary

Retry with Jitter is a resilience technique used to retry failed operations with random delay between attempts.

Instead of all clients retrying at the same time, jitter adds randomness to the retry interval.

This helps avoid traffic spikes and reduces pressure on unhealthy services.

## When to Use

Use Retry with Jitter when you need to:

- Retry temporary failures
- Handle network instability
- Reduce retry storms
- Protect overloaded services
- Improve fault tolerance
- Work with APIs, queues, databases, or external services
- Avoid many clients retrying at the same time

## The Problem

Without jitter:

```text
Many clients call a service
The service fails
All clients retry after 1 second
The service receives another traffic spike
The failure becomes worse
```

## The Solution

With jitter:

```text
Many clients call a service
The service fails
Each client retries after a slightly different random delay
Traffic is spread over time
The service has a better chance to recover
```

## Common Strategy

### Exponential Backoff

Increase the delay after each failed attempt.

```text
Attempt 1 → wait 1 second
Attempt 2 → wait 2 seconds
Attempt 3 → wait 4 seconds
Attempt 4 → wait 8 seconds
```

### Jitter

Add randomness to the delay.

```text
Attempt 1 → wait 0.8 seconds
Attempt 2 → wait 2.3 seconds
Attempt 3 → wait 3.6 seconds
Attempt 4 → wait 7.2 seconds
```

## Practical Example

```text
1. Payment Service calls Fraud Service
2. Fraud Service times out
3. Payment Service waits a random delay
4. Payment Service retries
5. If it fails again, the delay increases
6. After max attempts, the request fails or goes to fallback
```

## Benefits

- Reduces retry storms
- Protects unstable services
- Improves resilience
- Handles temporary failures safely
- Spreads retry traffic over time
- Works well with distributed systems

## Challenges

- Requires max retry limit
- Can increase latency
- Not suitable for all operations
- Must be combined with idempotency
- Bad retry configuration can overload dependencies
- Needs monitoring

## Best Practices

- Use exponential backoff
- Add jitter to retry delays
- Define maximum retry attempts
- Define timeout per request
- Retry only temporary failures
- Avoid retrying validation errors
- Combine with circuit breaker
- Ensure operations are idempotent

## Related Concepts

```text
backpressure.md
circuit-breaker.md
dead-letter-queue.md
fault-tolerance.md
idempotency.md
observability.md
```

## Simple Explanation

```text
Retry with Jitter means retrying failed operations,
but with random waiting time between attempts.

This avoids many systems retrying together at the same time.
```