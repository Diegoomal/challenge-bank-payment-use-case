# Domain-Driven Design

## Summary

Domain-Driven Design, also known as DDD, is a software design approach focused on modeling the system around the business domain.

The main idea is to make the code reflect the business rules, language, processes, and concepts.

DDD is commonly used in complex systems where business logic is important and changes frequently.

## When to Use

Use Domain-Driven Design when you need to:

- Model complex business rules
- Align software design with business concepts
- Improve communication between developers and domain experts
- Organize code by business capabilities
- Avoid mixing technical concerns with business logic
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

### Ubiquitous Language

A shared language used by developers and business experts.

The same terms used by the business should appear in the code.

Example:

```text
PaymentConfirmed
DebitCompleted
AccountBlocked
OrderCreated
```

### Entity

An object with identity.

Example:

```text
Account
Customer
Payment
Order
```

Even if its data changes, the identity remains the same.

### Value Object

An object defined by its values, not by an identity.

Example:

```text
Money
Address
Email
CPF
DateRange
```

### Aggregate

A group of related objects treated as a consistency boundary.

Example:

```text
Order
 ├── OrderItem
 └── ShippingAddress
```

The aggregate root controls changes inside the aggregate.

### Aggregate Root

The main entity responsible for protecting business rules inside an aggregate.

Example:

```text
Order is the aggregate root.
OrderItem should not be changed directly from outside.
```

### Domain Event

An event that represents something important that happened in the domain.

Example:

```text
OrderCreated
PaymentConfirmed
DebitCompleted
AccountBlocked
```

### Repository

An abstraction used to persist and retrieve aggregates.

Example:

```text
PaymentRepository
AccountRepository
OrderRepository
```

### Domain Service

A service that contains business logic that does not naturally belong to a single entity or value object.

Example:

```text
TransferService
PaymentConfirmationService
FraudAnalysisService
```

## Practical Example

```text
1. Customer creates a payment
2. Payment is created with status Pending
3. Account is debited
4. DebitCompleted event is published
5. Payment is confirmed
6. PaymentConfirmed event is published
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
    interface/
      controllers/
```

## Benefits

- Business rules are clearer
- Code becomes closer to the real business
- Better separation of concerns
- Easier maintenance
- Better communication with business teams
- Good fit for microservices and bounded contexts

## Challenges

- Can be complex for simple CRUD systems
- Requires good understanding of the domain
- Needs strong collaboration with business experts
- Poor modeling can create unnecessary complexity

## Practical Use Cases

- Banking systems
- Payment platforms
- Insurance systems
- E-commerce
- Logistics
- Healthcare systems
- Complex enterprise applications

## Simple Explanation

```text
DDD means designing the software around the business,
not around the database or technical layers.
```