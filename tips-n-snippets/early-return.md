# Early Return

## Summary

Early Return is a coding practice where a function returns as soon as a condition is met.

Instead of using many nested `if` statements, the function handles invalid cases first and exits early.

This makes the code simpler, flatter, and easier to read.

## When to Use

Use Early Return when you need to:

- Avoid deeply nested conditions
- Validate inputs at the beginning of a function
- Handle error cases first
- Make business logic easier to read
- Improve code clarity
- Reduce unnecessary `else` blocks

## Without Early Return

```python
def process_payment(payment):
    if payment is not None:
        if payment.status == "pending":
            if payment.amount > 0:
                return "Payment processed"
            else:
                return "Invalid amount"
        else:
            return "Invalid status"
    else:
        return "Payment not found"
```

## With Early Return

```python
def process_payment(payment):
    if payment is None:
        return "Payment not found"

    if payment.status != "pending":
        return "Invalid status"

    if payment.amount <= 0:
        return "Invalid amount"

    return "Payment processed"
```

## Benefits

- Reduces nested code
- Makes validation clearer
- Improves readability
- Keeps the main logic at the end
- Makes functions easier to maintain
- Helps avoid complex `if/else` chains

## Practical Use Cases

- Input validation
- API request validation
- Business rule validation
- Error handling
- Guard clauses
- Service methods
- Use cases in Clean Architecture
- Domain services

## Simple Explanation

```text
Early Return means checking invalid cases first
and leaving the function immediately.

This keeps the main logic clean and easy to follow.
```