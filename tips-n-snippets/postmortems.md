# Postmortems

## Summary

Postmortem is a document created after an incident to understand what happened, why it happened, and how to prevent similar problems in the future.

The goal is not to blame people, but to improve the system, process, monitoring, and response.

Postmortems are commonly used in production systems, SRE, DevOps, observability, cloud platforms, APIs, and distributed systems.

## When to Use

Use postmortems when you need to:

- Analyze production incidents
- Understand root causes
- Improve reliability
- Document failures and decisions
- Identify gaps in monitoring
- Improve incident response
- Prevent repeated problems

## What to Include

```text
Incident summary
Impact
Timeline
Root cause
Detection method
What worked well
What did not work well
Action items
Owners
Deadlines
```

## Practical Example

```text
1. Payment API latency increased
2. Users started receiving timeout errors
3. Alert was triggered by high p95 latency
4. Team investigated logs, metrics, and traces
5. Root cause was a slow database query
6. Query was optimized
7. New alerts and dashboards were created
8. Action items were assigned
```

## Benefits

- Improves system reliability
- Reduces repeated incidents
- Documents technical learnings
- Improves observability
- Improves team response
- Creates clear action items
- Helps build a learning culture

## Challenges

- Requires honest analysis
- Can become useless if action items are not completed
- Needs good incident data
- Should avoid blame
- Requires discipline after stressful incidents

## Best Practices

- Keep it blameless
- Focus on facts and timeline
- Identify technical and process gaps
- Define clear action items
- Assign owners and deadlines
- Review whether actions were completed
- Use logs, metrics, and traces as evidence

## Related Concepts

```text
observability.md
sli-slo-sla.md
structured-logs.md
distributed-tracing.md
fault-tolerance.md
incident-response.md
```

## Simple Explanation

```text
Postmortem is a review after an incident.

It explains what happened,
why it happened,
and what will be improved.
```