# Saga Pattern

## Summary

Saga Pattern is a pattern used to manage distributed transactions across multiple services.

Instead of using one large database transaction, a saga breaks the process into several smaller local transactions.

Each step executes a business action and, if something fails, the saga runs compensating actions to undo previous steps.

Saga Pattern is commonly used in microservices, event-driven architecture, payment flows, order processing, and distributed systems.

## When to Use

Use Saga Pattern when you need to:

- Coordinate a business process across multiple services
- Avoid distributed database transactions
- Handle failures in long-running processes
- Keep services loosely coupled
- Manage workflows in microservices
- Execute compensation when a step fails
- Build reliable distributed systems

## The Problem

Without Saga Pattern:

```text
1. Order is created
2. Payment is processed
3. Inventory is reserved
4. Shipping is created
5. One step fails
6. The system does not know how to rollback previous steps
```

## The Solution

With Saga Pattern:

```text
1. Execute one local transaction
2. Publish an event or call the next step
3. Continue the process
4. If a step fails, execute compensating actions
5. Keep the business process consistent
```

## Example Flow

```text
Create Order
    ↓
Debit Account
    ↓
Reserve Inventory
    ↓
Confirm Payment
    ↓
Create Shipment
```

If `Reserve Inventory` fails:

```text
Reserve Inventory failed
    ↓
Refund Payment
    ↓
Cancel Order
```

## Types of Saga

### Choreography

Each service reacts to events and publishes the next event.

```text
OrderCreated
    ↓
Payment Service consumes event
    ↓
PaymentCompleted
    ↓
Inventory Service consumes event
    ↓
InventoryReserved
```

Use choreography when the flow is simple and services can react independently.

### Orchestration

A central orchestrator controls the workflow and tells each service what to do.

```text
Saga Orchestrator
    ↓
Create Order
    ↓
Debit Account
    ↓
Reserve Inventory
    ↓
Confirm Payment
```

Use orchestration when the flow is complex and needs centralized control.

## Compensation

A compensating action is the opposite operation used to undo a previous step.

Examples:

```text
Debit Account → Refund Account
Create Order → Cancel Order
Reserve Inventory → Release Inventory
Confirm Payment → Cancel Payment
```

## Practical Example

```text
1. Customer creates an order
2. Order Service creates the order
3. Payment Service debits the account
4. Inventory Service reserves the product
5. Payment Service confirms payment
6. Notification Service sends confirmation
```

If inventory reservation fails:

```text
1. Inventory reservation fails
2. Payment is refunded
3. Order is cancelled
4. Customer receives failure notification
```

## Benefits

- Avoids distributed transactions
- Works well with microservices
- Supports long-running business processes
- Improves resilience
- Keeps services independent
- Allows failure recovery through compensation

## Challenges

- More complex than a local transaction
- Requires careful compensation logic
- Debugging can be harder
- Event ordering matters
- Services must be idempotent
- Requires good observability

## Important Concepts

### Local Transaction

Each service updates only its own database.

```text
Payment Service updates payment database
```

### Compensation Transaction

A business action used to undo a previous local transaction.

```text
Refund payment
Cancel order
Release inventory
```

### Saga State

The current progress of the distributed workflow.

```text
OrderCreated → PaymentCompleted → InventoryReserved
```

### Idempotency

Each saga step must safely handle retries and duplicated messages.

## Simple Explanation

```text
Saga Pattern coordinates a business process across multiple services.

If one step fails, the system executes compensating actions
instead of trying to rollback everything with one database transaction.
```