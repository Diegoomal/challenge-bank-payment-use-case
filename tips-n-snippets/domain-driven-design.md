# Domain-Driven Design

## Summary

Domain-Driven Design, also known as DDD, is a software design approach focused on modeling the system around the business domain.

The main idea is to make the code reflect the business rules, language, processes, and concepts.

DDD is commonly used in complex systems where business logic is important, changes frequently, and needs to scale with low coupling between teams and services.

## When to Use

Use Domain-Driven Design when you need to:

- Model complex business rules
- Align software design with business concepts
- Improve communication between developers and domain experts
- Organize code by business capabilities
- Create reusable business capabilities
- Reduce coupling between services
- Support high-scale systems
- Build systems that are easier to evolve

## Core Concepts

### Domain

The business area the system is built for.

Example:

```text
Payments
Orders
Accounts
Loans
Insurance
Logistics
```

### Bounded Context

A Bounded Context defines a clear boundary where a specific business model, language, and rules are valid.

Example:

```text
Payment Context
Account Context
Notification Context
Fraud Analysis Context
```

The same word can have different meanings in different contexts.

Example:

```text
Customer in Billing Context
Customer in Support Context
```

## Ubiquitous Language

Ubiquitous Language is a shared language used by developers and business experts.

The same terms used by the business should appear in the code.

Example:

```text
PaymentConfirmed
DebitCompleted
AccountBlocked
OrderCreated
```

## Entity

An object with identity.

Example:

```text
Account
Customer
Payment
Order
```

Even if its data changes, the identity remains the same.

## Value Object

An object defined by its values, not by an identity.

Example:

```text
Money
Address
Email
CPF
DateRange
```

## Aggregate

An Aggregate is a group of related objects treated as a consistency boundary.

Example:

```text
Order
 ├── OrderItem
 └── ShippingAddress
```

The aggregate protects business rules and controls changes inside its boundary.

## Aggregate Root

The Aggregate Root is the main entity responsible for protecting business rules inside an aggregate.

Example:

```text
Order is the aggregate root.
OrderItem should not be changed directly from outside.
```

## Domain Event

A Domain Event represents something important that happened in the business domain.

Example:

```text
OrderCreated
PaymentConfirmed
DebitCompleted
AccountBlocked
```

Domain Events help decouple services and allow other parts of the system to react asynchronously.

## Repository

A Repository is an abstraction used to persist and retrieve aggregates.

Example:

```text
PaymentRepository
AccountRepository
OrderRepository
```

## Domain Service

A Domain Service contains business logic that does not naturally belong to a single entity or value object.

Example:

```text
TransferService
PaymentConfirmationService
FraudAnalysisService
```

## Anti-Corruption Layer

An Anti-Corruption Layer protects one domain model from being polluted by another system or external model.

It translates data and concepts between systems.

Example:

```text
External Banking API
    ↓
Anti-Corruption Layer
    ↓
Internal Payment Domain
```

Use it when integrating with legacy systems, third-party APIs, or services with different domain models.

## Reusable Capabilities

DDD helps organize software around business capabilities that can be reused across products, services, or workflows.

Example:

```text
Payment Confirmation
Account Debit
Fraud Analysis
Notification Sending
```

These capabilities can be exposed through APIs, events, SDKs, or internal services.

## Low Coupling

DDD encourages low coupling by separating business contexts and avoiding direct dependency between unrelated models.

Example:

```text
Payment Context does not need to know internal rules from Account Context.
```

Services communicate through contracts, APIs, or domain events.

## High Scale

DDD supports high-scale systems by dividing the business into independent bounded contexts.

Each context can evolve, scale, and be deployed independently.

Example:

```text
Payment Service scales separately from Notification Service.
```

## Reuse

DDD improves reuse by making business capabilities explicit and isolated.

Example:

```text
The same FraudAnalysisService can be reused by payments, loans, and account operations.
```

## Aggregation

In DDD, aggregation usually refers to Aggregates.

An Aggregate groups related domain objects and protects consistency rules.

Example:

```text
Payment
 ├── PaymentMethod
 ├── Money
 └── PaymentStatus
```

If aggregation means combining data from multiple services, that is usually an application, API, or data architecture concern, not the main meaning of Aggregate in DDD.

## Practical Example

```text
1. Customer creates a payment
2. Payment is created with status Pending
3. Account is debited
4. DebitCompleted event is published
5. Payment is confirmed
6. PaymentConfirmed event is published
7. Notification Service reacts to PaymentConfirmed
```

## Example Structure

```text
src/
  payment/
    domain/
      entities/
        payment.py
      value_objects/
        money.py
      events/
        payment_confirmed.py
      repositories/
        payment_repository.py
      services/
        confirm_payment_service.py
    application/
      use_cases/
        confirm_payment.py
    infrastructure/
      database/
      messaging/
      anti_corruption/
    interface/
      controllers/
```

## Benefits

- Business rules are clearer
- Code becomes closer to the real business
- Better separation of concerns
- Lower coupling between services
- Better reuse of business capabilities
- Easier maintenance
- Better scalability
- Better communication with business teams
- Good fit for microservices and bounded contexts

## Challenges

- Can be complex for simple CRUD systems
- Requires good understanding of the domain
- Needs strong collaboration with business experts
- Poor modeling can create unnecessary complexity
- Requires discipline to keep bounded contexts clean
- Requires careful integration between contexts

## Practical Use Cases

- Banking systems
- Payment platforms
- Insurance systems
- E-commerce
- Logistics
- Healthcare systems
- Complex enterprise applications
- Microservices platforms
- High-scale distributed systems

## Simple Explanation

```text
DDD means designing the software around the business,
not around the database or technical layers.

It separates the system into clear business contexts,
uses the same language as the business,
and keeps business rules explicit in the code.
```