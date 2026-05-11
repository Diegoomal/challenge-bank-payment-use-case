# Backward Compatibility

## Summary

Backward Compatibility means that a system can evolve without breaking existing clients, integrations, or consumers.

A new version of an API, SDK, event, or service should continue to support the behavior expected by older versions.

It is commonly used in APIs, SDKs, microservices, event-driven systems, databases, and distributed architectures.

## When to Use

Use backward compatibility when you need to:

- Evolve systems safely
- Avoid breaking existing clients
- Support multiple versions during migration
- Deploy services independently
- Change APIs, events, or SDKs with less risk
- Maintain stable contracts between systems

## Examples

### API

Adding an optional field is usually backward compatible:

```json
{
  "payment_id": "pay-123",
  "status": "confirmed",
  "confirmed_at": "2026-05-11T10:00:00Z"
}
```

Older clients can ignore `confirmed_at`.

### Event

Adding a new optional field to an event is usually safe:

```json
{
  "event_type": "PaymentConfirmed",
  "payment_id": "pay-123",
  "amount": 100.00,
  "currency": "BRL"
}
```

Older consumers can keep using only the fields they know.

### SDK

Adding a new method is backward compatible:

```text
confirmPayment()
refundPayment()
```

Existing applications using `confirmPayment()` continue working.

## Breaking Changes

These changes are usually not backward compatible:

```text
Remove a field
Rename a field
Change a field type
Remove an endpoint
Change response structure
Make an optional field required
Change event payload format
Remove SDK methods
Change method behavior unexpectedly
```

## Non-Breaking Changes

These changes are usually backward compatible:

```text
Add optional fields
Add optional parameters
Add new endpoints
Add new event types
Add new SDK methods
Improve performance
Fix bugs without changing the contract
```

## Best Practices

- Prefer additive changes
- Do not remove fields suddenly
- Do not rename fields without versioning
- Keep old contracts working during migration
- Use deprecation before removal
- Document changes clearly
- Monitor old version usage
- Provide migration guides

## Practical Example

Backward compatible change:

```text
v1:
GET /payments/{id}

v2:
GET /payments/{id}
Response adds optional field confirmed_at
```

Breaking change:

```text
v1:
payment_id

v2:
id
```

Changing `payment_id` to `id` can break clients that depend on the old field.

## Simple Explanation

```text
Backward compatibility means new changes do not break old clients.
```