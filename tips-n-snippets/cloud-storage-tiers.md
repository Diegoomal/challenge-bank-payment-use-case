# Cloud Storage Tiers

## Summary

Cloud Storage Tiers are different storage classes used to balance cost, access frequency, and performance.

The main idea is to store frequently accessed data in faster, more expensive tiers, and rarely accessed data in cheaper, slower tiers.

Cloud storage tiers are commonly used for backups, logs, data lakes, archives, media files, and long-term retention.

## When to Use

Use cloud storage tiers when you need to:

- Reduce storage costs
- Store large amounts of data
- Separate hot and cold data
- Archive old data
- Keep backups for long periods
- Optimize data lake storage
- Manage compliance and retention requirements

## Common Tiers

### Hot Tier

Used for frequently accessed data.

```text
Fast access
Higher cost
Good for active data
```

Examples:

```text
Application files
Recent logs
Active datasets
User uploads
```

### Cool Tier

Used for data accessed less frequently.

```text
Lower cost
Slower or more expensive access
Good for older data
```

Examples:

```text
Monthly reports
Old logs
Backup copies
Historical datasets
```

### Archive Tier

Used for rarely accessed long-term data.

```text
Very low storage cost
Slow retrieval
May have restore delay
```

Examples:

```text
Compliance records
Long-term backups
Audit logs
Old media files
```

## Practical Example

```text
1. Recent application logs stay in Hot Storage for 30 days
2. Logs older than 30 days move to Cool Storage
3. Logs older than 1 year move to Archive Storage
4. Old logs are restored only when needed
```

## Lifecycle Policies

Lifecycle policies automatically move data between tiers.

Example:

```text
After 30 days → move to Cool
After 365 days → move to Archive
After 7 years → delete
```

## Benefits

- Reduces cloud storage cost
- Improves data lifecycle management
- Supports long-term retention
- Good for backups and archives
- Helps with compliance
- Works well for data lakes and logs

## Challenges

- Archive retrieval can be slow
- Accessing cold data may cost more
- Wrong tier selection can increase cost
- Requires lifecycle planning
- Data recovery time must be considered

## Related Concepts

```text
cloud-right-sizing.md
cloud-savings-plans.md
finops.md
data-lake.md
backup-strategy.md
```

## Simple Explanation

```text
Cloud Storage Tiers let you store data in different cost levels.

Frequently used data stays in fast storage.
Rarely used data moves to cheaper storage.
```