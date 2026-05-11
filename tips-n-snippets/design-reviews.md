# Design Reviews

## Summary

Design Review is a technical evaluation of a proposed solution before implementation.

The goal is to validate architecture, trade-offs, risks, scalability, security, maintainability, and alignment with business requirements.

It helps teams avoid poor technical decisions before code is written.

## When to Use

Use Design Reviews when you need to:

- Validate a new architecture
- Review important technical decisions
- Identify risks early
- Align teams before implementation
- Evaluate scalability and reliability
- Review APIs, events, data models, or integrations
- Avoid rework and architectural problems

## What to Review

Common review points:

```text
Problem definition
Proposed solution
Architecture diagram
Data flow
APIs and contracts
Events and schemas
Security
Scalability
Observability
Failure scenarios
Trade-offs
Alternatives considered
```

## Practical Example

```text
1. Team proposes a new payment confirmation flow
2. The design document explains the architecture
3. Engineers review APIs, events, database changes, and failure scenarios
4. Risks are identified
5. Adjustments are made before implementation
6. The team starts development with more confidence
```

## Benefits

- Finds problems early
- Improves architecture quality
- Reduces rework
- Aligns teams
- Documents technical decisions
- Improves system reliability
- Encourages better engineering practices

## Challenges

- Can slow down delivery if too bureaucratic
- Requires clear documentation
- Needs experienced reviewers
- Discussions can become subjective
- Should focus on important decisions, not minor details

## Best Practices

- Keep the design document clear and objective
- Explain trade-offs
- Include diagrams when useful
- Review failure scenarios
- Document decisions
- Focus on business and technical impact
- Avoid turning it into a code review

## Related Concepts

```text
architecture-decision-record.md
domain-driven-design.md
event-driven-architecture.md
observability.md
api-versioning.md
backward-compatibility.md
```

## Simple Explanation

```text
Design Review is a technical review before implementation.

It checks if the proposed solution makes sense
before the team invests time writing code.
```