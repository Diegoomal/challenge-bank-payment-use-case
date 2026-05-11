# Zero-Downtime Migrations

## Summary

Zero-Downtime Migration is a strategy used to change databases, schemas, or infrastructure without stopping the application.

The goal is to deploy changes while the system continues serving users normally.

It is commonly used in production systems, microservices, APIs, databases, and high-availability platforms.

## When to Use

Use Zero-Downtime Migrations when you need to:

- Change database schemas safely
- Deploy without interrupting users
- Support high availability
- Avoid breaking old application versions
- Run rolling deployments
- Evolve APIs and databases gradually
- Reduce production release risk

## The Problem

Without zero-downtime migration:

```text
1. Application uses old database schema
2. New schema is deployed
3. Old application version breaks
4. Users experience errors or downtime
```

## The Solution

Make changes in small backward-compatible steps.

```text
1. Add new schema without removing old fields
2. Deploy application that supports both old and new schema
3. Migrate data gradually
4. Switch reads and writes to the new schema
5. Remove old schema only after everything is migrated
```

## Common Strategy

### Expand

Add new fields, tables, or columns without removing old ones.

```sql
ALTER TABLE payments ADD COLUMN confirmed_at TIMESTAMP NULL;
```

### Migrate

Move or backfill data gradually.

```text
Copy data from old column to new column
```

### Contract

Remove old fields only after no application version depends on them.

```sql
ALTER TABLE payments DROP COLUMN old_status;
```

## Practical Example

```text
1. Add new column payment_status_v2
2. Application writes to both payment_status and payment_status_v2
3. Backfill old records
4. Application reads from payment_status_v2
5. Stop using payment_status
6. Remove payment_status in a later release
```

## Benefits

- Avoids downtime
- Reduces deployment risk
- Supports rolling deployments
- Keeps old and new versions compatible
- Improves reliability in production
- Works well with CI/CD

## Challenges

- Requires multiple deployment steps
- Needs backward compatibility
- Data backfill can be slow
- Rollback must be planned
- Requires monitoring
- Old fields must be cleaned up later

## Related Concepts

```text
backward-compatibility.md
blue-green-deploy.md
canary-deploy.md
ci-cd.md
feature-flags.md
observability.md
```

## Simple Explanation

```text
Zero-Downtime Migration means changing the database or system
without stopping the application.

The change is done gradually so old and new versions can work together.
```