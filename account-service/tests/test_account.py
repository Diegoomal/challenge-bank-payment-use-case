from decimal import Decimal

import pytest

from domain.account import Account
from domain.account_status import AccountStatus


def test_account_is_created_active_with_initial_deposit():
    account = Account.create("customer-1", "Customer One", Decimal("100.00"))

    assert account.id
    assert account.customer_id == "customer-1"
    assert account.account_holder == "Customer One"
    assert account.balance == Decimal("100.00")
    assert account.status == AccountStatus.ACTIVE


def test_account_rejects_negative_initial_deposit():
    with pytest.raises(ValueError, match="initial deposit cannot be negative"):
        Account.create("customer-1", "Customer One", Decimal("-1.00"))


def test_account_requires_holder():
    with pytest.raises(ValueError, match="account_holder is required"):
        Account.create("customer-1", "", Decimal("0"))
