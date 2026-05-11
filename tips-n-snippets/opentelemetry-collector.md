# OpenTelemetry Collector

## Summary

OpenTelemetry Collector is a service used to receive, process, and export observability data.

It works as a central pipeline for telemetry data such as logs, metrics, and traces.

Instead of each application sending data directly to tools like Jaeger, Prometheus, Grafana, or Datadog, the application sends data to the collector, and the collector forwards it to the correct destination.

## When to Use

Use OpenTelemetry Collector when you need to:

- Collect logs, metrics, and traces
- Centralize observability pipelines
- Export telemetry data to different tools
- Avoid vendor lock-in
- Process or enrich telemetry before sending it
- Standardize observability in microservices
- Reduce direct dependency between applications and monitoring tools

## Core Concepts

### Receiver

Receives telemetry data from applications or agents.

Example:

```text
Application sends traces to OpenTelemetry Collector
```

Common receivers:

```text
otlp
prometheus
jaeger
zipkin
```

### Processor

Processes telemetry data before exporting it.

Examples:

```text
batch
memory_limiter
attributes
resource
filter
```

### Exporter

Sends telemetry data to an external destination.

Examples:

```text
jaeger
prometheus
otlp
logging
datadog
grafana tempo
```

### Pipeline

Connects receivers, processors, and exporters.

```text
Receiver → Processor → Exporter
```

## Example Flow

```text
Application
    ↓ sends traces, logs, and metrics
OpenTelemetry Collector
    ↓ processes telemetry
Jaeger / Prometheus / Grafana / Datadog
```

## Example Configuration

```yaml
receivers:
  otlp:
    protocols:
      grpc:
      http:

processors:
  batch:

exporters:
  logging:
  otlp:
    endpoint: tempo:4317
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [logging, otlp]
```

## Benefits

- Centralized telemetry management
- Supports logs, metrics, and traces
- Reduces vendor lock-in
- Works well with microservices
- Can filter, batch, and enrich data
- Makes observability architecture more flexible
- Supports multiple backends

## Challenges

- Requires configuration
- Can become a critical infrastructure component
- Needs monitoring itself
- Incorrect pipelines can drop telemetry data
- Requires understanding of logs, metrics, and traces

## Practical Use Cases

- Distributed tracing
- Microservices observability
- Kubernetes monitoring
- Sending traces to Jaeger or Tempo
- Sending metrics to Prometheus
- Sending logs to centralized logging tools
- Standardizing telemetry across services

## Simple Explanation

```text
OpenTelemetry Collector is like a router for observability data.

Applications send telemetry to it,
and it decides where that data should go.
```