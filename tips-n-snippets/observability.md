# Observability

## Summary

Observability is the ability to understand what is happening inside a system using external signals.

The main signals are:

```text
Logs
Metrics
Traces
```

It helps developers monitor systems, detect failures, investigate errors, and understand performance problems.

## When to Use

Use observability when you need to:

- Monitor applications in production
- Debug distributed systems
- Investigate errors
- Analyze latency
- Track requests across services
- Create alerts
- Understand system health

## Core Signals

### Logs

Logs describe what happened in the application.

Example:

```text
Payment confirmation failed
```

### Metrics

Metrics are numerical measurements over time.

Examples:

```text
request_count
error_rate
latency_p95
cpu_usage
memory_usage
```

### Traces

Traces show the path of a request through multiple services.

Example:

```text
API Gateway → Payment Service → Account Service → RabbitMQ
```

## Related Tools

For more details, see:

```text
grafana.md
opentelemetry-collector.md
prometheus.md
jaeger.md
```

## Simple Explanation

```text
Observability helps you understand what is happening inside the system.

Logs show what happened.
Metrics show how the system is performing.
Traces show where the request passed.
```