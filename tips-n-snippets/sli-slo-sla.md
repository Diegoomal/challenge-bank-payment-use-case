# SLI, SLO and SLA

## Summary

SLI, SLO and SLA are reliability concepts used to measure, define, and communicate service quality.

They are commonly used in observability, SRE, cloud systems, APIs, microservices, and production platforms.

## SLI

SLI means Service Level Indicator.

It is a metric that measures how a service is performing.

Examples:

```text
Availability
Latency
Error rate
Request success rate
Throughput
```

Example:

```text
99.95% of requests succeeded in the last 30 days.
```

## SLO

SLO means Service Level Objective.

It is the target defined for an SLI.

Example:

```text
99.9% of requests must succeed every month.
```

Another example:

```text
95% of requests must respond in less than 300ms.
```

## SLA

SLA means Service Level Agreement.

It is a formal agreement with customers or users.

If the SLA is not met, there may be business consequences, such as credits, refunds, or contractual penalties.

Example:

```text
The service guarantees 99.9% monthly availability.
If not met, the customer receives service credits.
```

## Difference

```text
SLI = what you measure
SLO = the target you want to achieve
SLA = the formal agreement with the customer
```

## Practical Example

```text
SLI:
Request success rate

SLO:
99.9% of requests must succeed per month

SLA:
If monthly availability is below 99.9%, the customer receives credits
```

## Simple Explanation

```text
SLI measures reliability.
SLO defines the reliability goal.
SLA defines the business promise.
```

## Related Concepts

```text
observability.md
grafana.md
prometheus.md
opentelemetry-collector.md
jaeger.md
```