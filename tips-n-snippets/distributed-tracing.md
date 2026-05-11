# Distributed Tracing

## Summary

Distributed Tracing is an observability technique used to track a request as it moves across multiple services.

It helps understand where a request passed, how long each step took, and where errors or bottlenecks happened.

Distributed tracing is commonly used in microservices, APIs, event-driven systems, Kubernetes, and cloud-native applications.

## When to Use

Use distributed tracing when you need to:

- Debug requests across multiple services
- Analyze latency between services
- Find performance bottlenecks
- Investigate production errors
- Understand service dependencies
- Correlate logs, metrics, and traces
- Improve observability in distributed systems

## Core Concepts

### Trace

A trace represents the full journey of a request.

```text
API Gateway → Payment Service → Account Service → RabbitMQ → Notification Service
```

### Span

A span represents one operation inside a trace.

```text
HTTP request
Database query
Message publish
External API call
```

### Trace ID

A unique ID shared across all spans of the same request.

```text
trace_id = abc-123
```

### Span ID

A unique ID for a specific operation inside the trace.

```text
span_id = span-456
```

## Practical Example

```text
1. User calls POST /payments
2. API Gateway receives the request
3. Payment Service validates payment
4. Account Service debits account
5. Payment Service publishes PaymentConfirmed
6. Notification Service sends email
7. Trace shows the full request path and duration
```

## Benefits

- Easier debugging
- Better root cause analysis
- Shows service dependencies
- Helps find slow operations
- Improves incident investigation
- Works well with structured logs and metrics

## Challenges

- Requires instrumentation
- Can generate high data volume
- Needs trace context propagation
- Sampling strategy must be configured
- Async flows can be harder to trace
- Requires good observability tooling

## Common Tools

```text
OpenTelemetry
Jaeger
Grafana Tempo
Datadog APM
New Relic
Zipkin
```

## Related Concepts

```text
observability.md
structured-logs.md
opentelemetry-collector.md
jaeger.md
domain-observability.md
postmortems.md
```

## Simple Explanation

```text
Distributed Tracing shows the path of a request
across multiple services.

It helps identify where the system is slow,
where it failed,
and which services were involved.
```