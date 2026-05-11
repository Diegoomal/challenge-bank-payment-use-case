# Event Catalog

## Summary

An Event Catalog is a documented inventory of events used in an event-driven system.

It describes which events exist, who produces them, who consumes them, what data they carry, and when they are published.

It helps teams understand and govern communication between services.

## When to Use

Use an Event Catalog when you need to:

- Document events across services
- Understand producers and consumers
- Standardize event contracts
- Avoid duplicated or inconsistent events
- Improve governance in event-driven architecture
- Support onboarding of new developers
- Manage event versioning and evolution

## What to Document

For each event, document:

```text
Event name
Description
Producer
Consumers
Payload schema
Version
Topic, queue, or routing key
When it is published
Example payload
Owner team
```

## Example

```text
Event: PaymentConfirmed
Description: Published when a payment is successfully confirmed.
Producer: Payment Service
Consumers: Notification Service, Accounting Service
Routing Key: payment.confirmed
Version: v1
```

## Example Payload

```json
{
  "event_id": "evt-001",
  "event_type": "PaymentConfirmed",
  "version": "1.0",
  "occurred_at": "2026-05-11T10:00:00Z",
  "payload": {
    "payment_id": "pay-123",
    "account_id": "acc-456",
    "amount": 100.00,
    "currency": "BRL"
  }
}
```

## Benefits

- Better visibility of event flows
- Easier maintenance
- Better service integration
- Reduces coupling between teams
- Improves event governance
- Helps with debugging and impact analysis
- Supports backward compatibility

## Challenges

- Requires constant updates
- Can become outdated if not maintained
- Needs ownership per event
- Requires standard naming and schema rules
- Versioning must be managed carefully

## Related Concepts

```text
event-driven-architecture.md
domain-driven-design.md
api-versioning.md
backward-compatibility.md
rabbit-mq.md
outbox-pattern.md
```

## Simple Explanation

```text
An Event Catalog is like documentation for all events in the system.

It shows what events exist,
who sends them,
who consumes them,
and what data they contain.
```