# SDK Versioning

## Summary

SDK Versioning is the practice of controlling and documenting changes in a Software Development Kit.

An SDK is used by other applications to interact with an API, service, or platform.

Good versioning helps developers upgrade safely without breaking existing integrations.

## When to Use

Use SDK versioning when you need to:

- Release new SDK features
- Fix bugs safely
- Maintain backward compatibility
- Support multiple client applications
- Avoid breaking consumers
- Communicate changes clearly
- Manage API evolution

## Semantic Versioning

A common strategy is Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
1.4.2
```

### MAJOR

Used when there are breaking changes.

```text
1.0.0 → 2.0.0
```

Example:

```text
A method is removed
A parameter becomes required
A response structure changes
```

### MINOR

Used when new features are added without breaking existing code.

```text
1.0.0 → 1.1.0
```

Example:

```text
New method added
New optional parameter added
New helper function added
```

### PATCH

Used for bug fixes and small improvements.

```text
1.0.0 → 1.0.1
```

Example:

```text
Bug fix
Documentation correction
Internal improvement
```

## Best Practices

- Avoid breaking changes when possible
- Keep backward compatibility
- Use clear changelogs
- Deprecate before removing
- Support older versions for a defined period
- Version the SDK independently from the API when needed
- Document migration steps between major versions

## Deprecation

Deprecation means a feature still works, but should no longer be used.

Example:

```text
getUser() is deprecated.
Use getCustomer() instead.
```

This gives developers time to migrate before removal.

## Practical Example

```text
v1.0.0
Initial SDK release

v1.1.0
Adds createPayment()

v1.1.1
Fixes timeout handling

v2.0.0
Removes deprecated confirmPaymentOld()
```

## Simple Explanation

```text
SDK versioning tells developers what changed,
whether the update is safe,
and whether they need to change their code.
```