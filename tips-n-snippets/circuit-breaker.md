# Circuit Breaker

## Summary

Circuit Breaker is a resilience pattern used to prevent repeated calls to a failing service.

When a dependency is unhealthy, the circuit breaker stops sending requests for a period of time.

This helps avoid cascading failures and protects the system from wasting resources on calls that are likely to fail.

## When to Use

Use Circuit Breaker when you need to:

- Protect services from failing dependencies
- Avoid cascading failures
- Handle unstable external APIs
- Prevent repeated timeouts
- Improve system resilience
- Fail fast when a service is unavailable
- Give dependencies time to recover

## The Problem

Without Circuit Breaker:

```text
Service A calls Service B
Service B is failing
Service A keeps retrying
Requests pile up
Threads, memory, and connections are exhausted
Failure spreads to other services
```

## The Solution

With Circuit Breaker:

```text
Service B starts failing
Circuit Breaker opens
Service A stops calling Service B temporarily
System fails fast or uses fallback
After some time, the circuit tests recovery
```

## Circuit States

### Closed

Normal state.

Requests are allowed.

```text
Service is healthy → requests pass through
```

### Open

Failure threshold was reached.

Requests are blocked temporarily.

```text
Service is failing → requests fail fast
```

### Half-Open

The system sends a small number of test requests.

```text
If test succeeds → circuit closes
If test fails → circuit opens again
```

## Example Flow

```text
1. Payment Service calls Fraud Service
2. Fraud Service starts timing out
3. Circuit Breaker detects repeated failures
4. Circuit opens
5. Payment Service stops calling Fraud Service temporarily
6. System returns fallback response or fails fast
7. After timeout, circuit becomes half-open
8. If Fraud Service recovers, circuit closes
```

## Benefits

- Prevents cascading failures
- Reduces pressure on unhealthy services
- Improves fault tolerance
- Makes failures faster and controlled
- Protects system resources
- Gives dependencies time to recover

## Challenges

- Requires good thresholds
- Fallback behavior must be designed carefully
- Can hide real problems if poorly monitored
- Incorrect settings can block healthy traffic
- Needs observability to track open circuits

## Related Concepts

```text
backpressure.md
retry-with-jitter.md
fault-tolerance.md
observability.md
distributed-architecture.md
microservices.md
```

## Simple Explanation

```text
Circuit Breaker stops calling a failing service
before the failure spreads to the rest of the system.
```