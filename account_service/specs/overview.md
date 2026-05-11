# Account Service

## Business Description

The `account_service` is responsible for creating financial accounts for customers.

This service belongs to the Account context and represents the administrative entry point for opening accounts that can participate in the payment flow.

It receives an HTTP request, creates a new `Account` with `ACTIVE` status, persists the account, and publishes the `account.created` event.

## Bounded Context

Account.

## Ubiquitous Language

- Account: a customer's financial account.
- AccountId: the unique account identifier.
- Customer: the customer who owns the account.
- AccountHolder: the account holder.
- Balance: the available account balance.
- AccountStatus: the current account state.
- InitialDeposit: the initial amount deposited into the account.
- AccountCreated: event that reports that an account was created.

## Aggregate Root

### Account

The `Account` is the Aggregate Root of the Account context.

It controls the account's core data and ensures that an account is created in a valid state.

## Account States

- ACTIVE
- INACTIVE
- CLOSED

## Invariants

- An account must have a unique `account_id`.
- An account must have a `customer_id`.
- An account must have a valid account holder.
- A newly created account must start with `ACTIVE` status.
- The initial deposit cannot be negative.
- A customer must not have more than one active account.
- An account must not start with a negative balance.

## Main Use Case

### CreateAccount

Responsible for creating a new financial account for a customer.

Expected input:

- customer_id
- account_holder
- initial_deposit

Expected output:

- account_id
- customer_id
- status
- created_at

## Consumed Domain Events

This service does not consume domain events.

It is started by an external HTTP call.

## Published Domain Events

### AccountCreated

Published when an account is created successfully.

Suggested payload:

- account_id
- customer_id
- account_holder
- initial_deposit
- status
- created_at

## Ports

### AccountRepository

Responsible for saving and retrieving accounts.

### EventPublisher

Responsible for publishing domain events.

## Responsibilities

This service must:

- Receive an account creation request.
- Validate the account data.
- Check whether the customer already has an active account.
- Create a new account with `ACTIVE` status.
- Persist the account.
- Publish the `account.created` event.

This service must not:

- Start payments.
- Debit accounts.
- Credit accounts.
- Confirm payments.
- Reverse payments.
- Notify customers or merchants.
- Issue receipts.
