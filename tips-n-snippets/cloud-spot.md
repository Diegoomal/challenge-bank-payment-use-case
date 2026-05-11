# Cloud Spot

## Summary

Cloud Spot is a pricing model where cloud providers offer unused compute capacity at a lower cost.

Spot instances are cheaper than regular on-demand instances, but they can be interrupted when the cloud provider needs the capacity back.

They are commonly used for batch jobs, data processing, CI/CD runners, machine learning training, workers, and fault-tolerant workloads.

## When to Use

Use Cloud Spot when you need to:

- Reduce cloud costs
- Run temporary workloads
- Process batch jobs
- Run background workers
- Execute ML or AI training jobs
- Run workloads that can be restarted
- Scale non-critical processing cheaply

## The Problem

On-demand instances can be expensive for large workloads.

```text
Long-running compute job
High number of instances
High cloud cost
```

## The Solution

Use spot capacity for workloads that tolerate interruption.

```text
Use cheaper unused cloud capacity
Checkpoint progress when possible
Restart jobs if interrupted
Reduce total compute cost
```

## Common Use Cases

```text
Batch processing
Data pipelines
Machine learning training
CI/CD jobs
Image processing
Video processing
Queue consumers
Kubernetes worker nodes
Non-critical workloads
```

## Important Risk

Spot instances can be interrupted.

```text
Cloud provider needs capacity back
    ↓
Spot instance is terminated
    ↓
Workload must restart or continue elsewhere
```

## Best Practices

- Use spot only for fault-tolerant workloads
- Save progress with checkpoints
- Combine spot with on-demand instances
- Use autoscaling groups
- Use retries for failed jobs
- Avoid spot for critical stateful services
- Monitor interruption rates

## Benefits

- Lower compute cost
- Good for scalable workloads
- Useful for batch and async processing
- Works well with autoscaling
- Good fit for AI and data workloads

## Challenges

- Can be interrupted
- Not ideal for critical services
- Requires retry logic
- Requires fault-tolerant design
- Availability depends on cloud capacity
- Stateful workloads need extra care

## Related Concepts

```text
cloud-autoscaling.md
cloud-right-sizing.md
fault-tolerance.md
retry-with-jitter.md
backpressure.md
kubernetes.md
```

## Simple Explanation

```text
Cloud Spot means using cheaper unused cloud capacity.

It costs less,
but the cloud provider can take it back at any time.
```