# Canary Deploy

## Summary

Canary Deploy is a deployment strategy where a new version is released to a small percentage of users before reaching everyone.

The goal is to validate the new version in production with limited risk.

If the new version works well, traffic is gradually increased.  
If problems appear, the deployment can be stopped or rolled back.

## When to Use

Use Canary Deploy when you need to:

- Reduce deployment risk
- Test a new version with real traffic
- Detect errors before full rollout
- Gradually release features
- Compare old and new versions
- Monitor impact before exposing all users
- Roll back safely if something fails

## How It Works

```text
Version 1 = stable version
Version 2 = new version
```

Deployment flow:

```text
1. 100% of users use Version 1
2. Deploy Version 2
3. Send 5% of traffic to Version 2
4. Monitor errors, latency, logs, and metrics
5. Increase traffic to 25%, 50%, then 100%
6. If something fails, rollback to Version 1
```

## Example Flow

```text
Users
  ↓
Load Balancer
  ├── 95% traffic → Version 1
  └── 5% traffic  → Version 2
```

After validation:

```text
Users
  ↓
Load Balancer
  ├── 50% traffic → Version 1
  └── 50% traffic → Version 2
```

Final state:

```text
Users
  ↓
Load Balancer
  └── 100% traffic → Version 2
```

## Benefits

- Safer production releases
- Early failure detection
- Gradual rollout
- Lower impact if the new version fails
- Works well with monitoring and observability
- Good fit for high-scale systems

## Challenges

- Requires traffic control
- Requires strong observability
- Rollback logic must be clear
- Database changes need backward compatibility
- Different users may experience different versions
- Can be more complex than a simple deployment

## Related Concepts

```text
blue-green-deploy.md
ci-cd.md
feature-flags.md
zero-downtime-migrations.md
backward-compatibility.md
observability.md
```

## Simple Explanation

```text
Canary Deploy means releasing a new version to a small group first.

If it works well, more users receive it.
If it fails, only a small group is affected.
```