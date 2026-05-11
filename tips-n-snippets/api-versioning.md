# API Versioning

## Summary

API Versioning is the practice of managing changes in an API without breaking existing consumers.

It allows an API to evolve while keeping older clients working safely.

API versioning is commonly used in REST APIs, public APIs, microservices, SDKs, and distributed systems.

## When to Use

Use API versioning when you need to:

- Change request or response contracts
- Add new features safely
- Maintain backward compatibility
- Support old and new clients at the same time
- Avoid breaking integrations
- Manage API evolution over time

## Common Versioning Strategies

### URL Versioning

The version appears in the URL.

```http
GET /v1/payments
GET /v2/payments
```

Simple and easy to understand.

### Header Versioning

The version is sent in the request header.

```http
GET /payments
API-Version: 1
```

Keeps URLs cleaner, but is less visible.

### Query Parameter Versioning

The version is sent as a query parameter.

```http
GET /payments?version=1
```

Easy to test, but less common for production APIs.

### Media Type Versioning

The version is sent in the `Accept` header.

```http
Accept: application/vnd.company.payments.v1+json
```

More formal, but more complex.

## Semantic Versioning

APIs can also follow semantic versioning:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
v1.2.3
```

### MAJOR

Used for breaking changes.

```text
v1 → v2
```

Example:

```text
Remove field
Rename field
Change response structure
Change required parameters
```

### MINOR

Used for backward-compatible features.

```text
v1.1 → v1.2
```

Example:

```text
Add optional field
Add optional parameter
Add new endpoint
```

### PATCH

Used for fixes that do not change the contract.

```text
v1.1.0 → v1.1.1
```

Example:

```text
Bug fix
Performance improvement
Documentation correction
```

## Breaking Changes

Breaking changes require a new major version.

Examples:

```text
Removing a field
Renaming a field
Changing field type
Changing authentication rules
Removing an endpoint
Changing error format
Making an optional field required
```

## Non-Breaking Changes

Non-breaking changes usually do not require a new major version.

Examples:

```text
Adding a new optional field
Adding a new endpoint
Adding a new optional query parameter
Improving performance
Fixing a bug without changing the contract
```

## Deprecation

Deprecation means an old API version still works, but should no longer be used.

Example:

```text
/v1/payments is deprecated.
Use /v2/payments instead.
```

A good deprecation process includes:

```text
1. Announce deprecation
2. Keep old version working for a defined period
3. Provide migration guide
4. Monitor usage
5. Remove only after migration window
```

## Practical Example

```text
v1 response:
{
  "payment_id": "pay-123",
  "status": "confirmed"
}

v2 response:
{
  "id": "pay-123",
  "status": "confirmed",
  "confirmed_at": "2026-05-11T10:00:00Z"
}
```

Because `payment_id` changed to `id`, this is a breaking change.

## Best Practices

- Prefer backward-compatible changes
- Avoid removing fields without deprecation
- Keep contracts stable
- Document all changes
- Use changelogs
- Provide migration guides
- Monitor usage by version
- Keep old versions only for a defined support period

## Simple Explanation

```text
API versioning allows an API to change over time
without breaking applications that already use it.
```