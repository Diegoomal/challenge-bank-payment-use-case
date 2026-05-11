# Structured Logs

## Summary

Structured Logs are logs written in a consistent format, usually JSON.

Instead of plain text messages, structured logs use fields such as service name, level, timestamp, request ID, user ID, and error details.

They make logs easier to search, filter, aggregate, and analyze in observability tools.

## When to Use

Use structured logs when you need to:

- Debug production issues
- Search logs efficiently
- Track requests across services
- Correlate logs with traces
- Analyze errors by service or domain
- Improve observability
- Support distributed systems

## Example

Unstructured log:

```text
Payment failed for payment pay-123
```

Structured log:

```json
{
  "timestamp": "2026-05-11T10:00:00Z",
  "level": "error",
  "service": "payment-service",
  "message": "Payment confirmation failed",
  "payment_id": "pay-123",
  "trace_id": "abc-123",
  "error": "Account balance is insufficient"
}
```

## Common Fields

```text
timestamp
level
service
message
trace_id
request_id
user_id
event_name
error_code
domain_context
```

## Benefits

- Easier searching
- Better filtering
- Better debugging
- Better correlation with traces
- Useful for alerts and dashboards
- Improves production investigation
- Works well with observability platforms

## Challenges

- Requires consistent log format
- Needs standard field names
- Can increase log volume
- Sensitive data must be protected
- Poor logging can create noise

## Best Practices

- Use JSON format
- Keep field names consistent
- Include trace_id and request_id
- Avoid logging sensitive data
- Use clear log levels
- Log business identifiers when useful
- Keep messages objective and searchable

## Related Concepts

```text
observability.md
distributed-tracing.md
domain-observability.md
sli-slo-sla.md
postmortems.md
```

## Simple Explanation

```text
Structured Logs are logs organized as fields.

They are easier to search, filter, and connect with traces and metrics.
```