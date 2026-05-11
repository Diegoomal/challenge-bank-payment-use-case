# Blue-Green Deploy

## Summary

Blue-Green Deploy is a deployment strategy that uses two production environments.

One environment is active and receives real traffic.  
The other environment is idle and receives the new version.

After validation, traffic is switched from the old environment to the new one.

## When to Use

Use Blue-Green Deploy when you need to:

- Deploy with minimal downtime
- Reduce release risk
- Roll back quickly
- Validate a new version before exposing users
- Keep two production-ready environments
- Improve deployment safety

## How It Works

```text
Blue environment = current production version
Green environment = new version
```

Deployment flow:

```text
1. Blue is serving users
2. New version is deployed to Green
3. Green is tested
4. Traffic is switched from Blue to Green
5. Green becomes production
6. Blue remains available for rollback
```

## Example Flow

```text
Users
  ↓
Load Balancer
  ↓
Blue Environment

Deploy new version:
Green Environment

After validation:
Users
  ↓
Load Balancer
  ↓
Green Environment
```

## Rollback

If the new version fails, traffic can be switched back quickly.

```text
Green has problem
    ↓
Switch traffic back to Blue
```

## Benefits

- Minimal downtime
- Fast rollback
- Safer production releases
- Easier validation before traffic switch
- Reduces deployment risk
- Good fit for critical systems

## Challenges

- Requires two environments
- Higher infrastructure cost
- Database migrations need care
- State and sessions must be handled correctly
- Both environments must be kept consistent

## Related Concepts

```text
canary-deploy.md
ci-cd.md
feature-flags.md
zero-downtime-migrations.md
backward-compatibility.md
observability.md
```

## Simple Explanation

```text
Blue-Green Deploy means running two environments.

The old version handles traffic,
the new version is prepared separately,
and traffic is switched when the new version is ready.
```