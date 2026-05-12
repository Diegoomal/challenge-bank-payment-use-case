from decimal import Decimal

import pytest

from domain.account import Account
from domain.exceptions import InsufficientBalance


def test_account_debit_subtracts_balance_and_creates_entry():
    account = Account.create(
        customer_id="customer-1",
        holder_name="Customer One",
        balance=Decimal("100.00"),
    )

    entry = account.debit("transaction-1", Decimal("25.50"))

    assert account.balance == Decimal("74.50")
    assert entry.account_id == account.id
    assert entry.transaction_id == "transaction-1"
    assert entry.amount == Decimal("25.50")
    assert entry.entry_type == "DEBIT"
    assert account.entries == [entry]


def test_account_debit_rejects_insufficient_balance():
    account = Account.create(
        customer_id="customer-1",
        holder_name="Customer One",
        balance=Decimal("10.00"),
    )

    with pytest.raises(InsufficientBalance, match="insufficient balance"):
        account.debit("transaction-1", Decimal("20.00"))

    assert account.balance == Decimal("10.00")
    assert account.entries == []


def test_account_cannot_start_with_negative_balance():
    with pytest.raises(ValueError, match="balance cannot be negative"):
        Account.create(
            customer_id="customer-1",
            holder_name="Customer One",
            balance=Decimal("-1.00"),
        )
