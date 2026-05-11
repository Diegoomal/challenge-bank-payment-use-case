# Graceful Degradation

## Summary

Graceful Degradation is a resilience strategy where a system continues working partially when one component or dependency fails.

Instead of stopping the entire system, only the affected feature is disabled, reduced, or replaced by a fallback behavior.

It is commonly used in distributed systems, microservices, APIs, cloud platforms, and fault-tolerant architectures.

## When to Use

Use Graceful Degradation when you need to:

- Keep critical flows working during failures
- Avoid full system outages
- Handle dependency failures safely
- Provide fallback behavior
- Reduce business impact during incidents
- Improve user experience during partial failures
- Build fault-tolerant systems

## The Problem

Without graceful degradation:

```text
Recommendation Service fails
    ↓
Checkout page fails
    ↓
User cannot complete purchase
```

## The Solution

With graceful degradation:

```text
Recommendation Service fails
    ↓
Recommendations are hidden
    ↓
Checkout continues working
```

## Practical Example

```text
1. User opens checkout
2. Checkout calls Recommendation Service
3. Recommendation Service is unavailable
4. Checkout ignores recommendations
5. User can still complete the purchase
```

## Common Fallbacks

```text
Hide optional feature
Return cached data
Use default values
Send request to manual review
Show simplified response
Disable non-critical integrations
```

## Benefits

- Prevents full outages
- Protects critical business flows
- Improves fault tolerance
- Reduces user impact
- Helps systems survive partial failures
- Works well with circuit breaker and fallback logic

## Challenges

- Requires clear definition of critical and optional features
- Fallback behavior must be designed carefully
- Can hide failures if not monitored
- Users may receive reduced experience
- Requires good observability

## Related Concepts

```text
fault-tolerance.md
circuit-breaker.md
retry-with-jitter.md
backpressure.md
observability.md
distributed-architecture.md
```

## Simple Explanation

```text
Graceful Degradation means the system loses part of its functionality,
but does not stop completely.

It keeps the most important flows working.
```