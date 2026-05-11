# Idempotency

## Summary

Idempotency is the ability to execute the same operation multiple times and always produce the same final result.

In distributed systems, the same request or event can be processed more than once because of retries, network failures, timeouts, or duplicated messages.

An idempotent operation prevents duplicated side effects, such as charging a customer twice or creating the same order multiple times.

## When to Use

Use idempotency when you need to:

- Handle retries safely
- Process events from queues
- Avoid duplicate payments
- Avoid duplicate database records
- Protect APIs from repeated requests
- Build reliable distributed systems
- Work with event-driven architecture

## Common Scenarios

### Payment Processing

```text
The customer sends a payment request.
The API times out.
The client retries the same request.
The system must not charge the customer twice.
```

### Event Consumers

```text
A consumer receives the same event more than once.
The event must be processed only once.
```

### API Requests

```text
POST /payments
Idempotency-Key: abc-123
```

If the same key is sent again, the system returns the previous result instead of creating a new payment.

## Idempotency Key

An idempotency key is a unique identifier used to recognize repeated requests.

Example:

```http
POST /payments
Idempotency-Key: payment-123
```

The system stores the result of the first request and reuses it when the same key appears again.

## Practical Flow

```text
1. Client sends a request with an idempotency key
2. System checks if the key already exists
3. If it exists, return the previous result
4. If it does not exist, process the request
5. Store the result linked to the key
6. Return the response
```

## Example

```text
Request 1:
Idempotency-Key: payment-123
Result: Payment created

Request 2:
Idempotency-Key: payment-123
Result: Same payment returned, no duplicate charge
```

## Benefits

- Prevents duplicated side effects
- Makes retries safe
- Improves reliability
- Reduces risk in distributed systems
- Helps consumers handle duplicated messages
- Protects critical operations like payments and orders

## Challenges

- Requires storing processed keys or events
- Requires deciding expiration time for keys
- Needs careful handling of concurrent requests
- Must define what makes an operation unique
- Requires consistency between request, key, and result

## Practical Use Cases

- Payment APIs
- Order creation
- Account debit operations
- Event consumers
- Queue processing
- Webhook handlers
- Distributed transactions
- Saga steps

## Simple Explanation

```text
Idempotency means that repeating the same action does not repeat the side effect.
```