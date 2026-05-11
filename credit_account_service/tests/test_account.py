from decimal import Decimal

import pytest

from domain.account import Account


def test_account_credit_adds_balance_and_creates_entry():
    account = Account.create(
        customer_id="customer-1",
        holder_name="Customer One",
        balance=Decimal("100.00"),
    )

    entry = account.credit("transaction-1", Decimal("25.50"))

    assert account.balance == Decimal("125.50")
    assert entry.account_id == account.id
    assert entry.transaction_id == "transaction-1"
    assert entry.amount == Decimal("25.50")
    assert entry.entry_type == "CREDIT"
    assert account.entries == [entry]


def test_account_credit_is_idempotent_by_transaction_id():
    account = Account.create(
        customer_id="customer-1",
        holder_name="Customer One",
        balance=Decimal("10.00"),
    )

    first = account.credit("transaction-1", Decimal("20.00"))
    second = account.credit("transaction-1", Decimal("20.00"))

    assert first == second
    assert account.balance == Decimal("30.00")
    assert account.entries == [first]


def test_account_cannot_start_with_negative_balance():
    with pytest.raises(ValueError, match="balance cannot be negative"):
        Account.create(
            customer_id="customer-1",
            holder_name="Customer One",
            balance=Decimal("-1.00"),
        )
