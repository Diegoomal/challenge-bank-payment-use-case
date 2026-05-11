# Cloud Savings Plans

## Summary

Cloud Savings Plans are cloud pricing models where you commit to a certain amount of usage for a period of time in exchange for lower prices.

They are commonly used to reduce costs for predictable workloads.

Savings Plans are often used with compute services, containers, serverless workloads, and long-running applications.

## When to Use

Use Cloud Savings Plans when you need to:

- Reduce cloud costs
- Optimize predictable workloads
- Commit to long-term cloud usage
- Lower compute pricing
- Improve FinOps practices
- Save money compared to on-demand pricing

## How It Works

```text
You commit to spend a fixed amount per hour
    ↓
Cloud provider gives discounted pricing
    ↓
Usage covered by the plan costs less
    ↓
Extra usage is charged as on-demand
```

## Practical Example

```text
A company always uses around $10/hour of compute.

It buys a Savings Plan for $10/hour for 1 or 3 years.

That committed usage receives a discount.
Any usage above $10/hour is charged normally.
```

## Benefits

- Reduces cloud cost
- Good for predictable workloads
- Easier cost planning
- Works well with long-running services
- Can be more flexible than reserved instances
- Useful for FinOps optimization

## Challenges

- Requires usage commitment
- Bad estimates can waste money
- Less useful for unpredictable workloads
- Commitment usually lasts 1 or 3 years
- Needs continuous cost monitoring

## Best Practices

- Analyze historical usage before committing
- Start with conservative commitments
- Use for stable baseline workloads
- Combine with autoscaling and spot instances
- Review usage regularly
- Avoid covering highly variable workloads first

## Related Concepts

```text
cloud-right-sizing.md
cloud-autoscaling.md
cloud-spot.md
finops.md
scalability.md
```

## Simple Explanation

```text
Cloud Savings Plans give discounts
when you commit to using a minimum amount of cloud resources
for a long period.
```