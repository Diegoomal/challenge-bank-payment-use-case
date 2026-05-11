# API Gateway

## Business Description

The `api_gateway` is responsible for exposing a single entry point for external clients to access the platform services.

This component does not belong to a specific Bounded Context. It acts as the application's entry layer, routing HTTP requests to the correct internal services.

It centralizes external access, simplifies client communication, and protects internal services from direct exposure.

## Bounded Context

It does not have its own Bounded Context.

The `api_gateway` is an infrastructure/application component that connects external clients to the internal Bounded Contexts.

## Ubiquitous Language

- API Gateway: the application's single entry point.
- Route: HTTP path exposed to the client.
- Upstream Service: internal service that receives the request.
- Request: request made by the client.
- Response: response returned to the client.
- CorrelationId: identifier used to trace a request across services.
- Authentication: validation of the client's identity.
- Authorization: validation of access permission.

## Main Responsibility

The `api_gateway` must receive external requests and forward them to the responsible internal service.

Examples:

- `/api/v1/accounts` forwards to `account_service`
- `/api/v1/payments/start` forwards to `start_payment_service`

## Main Use Cases

### RouteAccountRequests

Responsible for forwarding account requests to the `account_service`.

### RoutePaymentRequests

Responsible for forwarding payment requests to the `start_payment_service`.

## Rules

- The gateway must expose a simple and consistent public API.
- The gateway must hide the internal service addresses.
- The gateway must forward relevant headers, such as `correlation_id`.
- The gateway must return standardized responses to the client.
- The gateway must not contain domain business rules.
- The gateway must not directly access service databases.
- The gateway must not publish domain events.
- The gateway must not execute payment, account, notification, or receipt logic.

## Ports / Integrations

### HTTP Client

Responsible for calling internal services.

### Request Router

Responsible for mapping external routes to internal services.

### Error Handler

Responsible for standardizing error responses.

## Responsibilities

This component must:

- Expose public HTTP routes.
- Forward requests to internal services.
- Propagate `correlation_id`.
- Standardize error responses.
- Centralize the application's entry point.
- Make future authentication and authorization easier.
- Avoid direct exposure of internal services.

This component must not:

- Create accounts directly.
- Start payments directly in the domain.
- Debit accounts.
- Credit accounts.
- Confirm payments.
- Reverse payments.
- Notify customers or merchants.
- Issue receipts.
- Access internal service databases.
- Publish domain events.
