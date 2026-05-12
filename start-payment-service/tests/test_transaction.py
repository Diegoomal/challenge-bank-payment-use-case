from decimal import Decimal

import pytest

from domain.payment_method import PaymentMethod
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus


def test_transaction_starts_with_started_status():
    transaction = Transaction.start(
        customer_id="customer-1",
        merchant_id="merchant-1",
        amount=Decimal("10.50"),
        payment_method=PaymentMethod.ACCOUNT_BALANCE,
    )

    assert transaction.id
    assert transaction.status == TransactionStatus.STARTED
    assert transaction.amount == Decimal("10.50")


def test_transaction_rejects_non_positive_amount():
    with pytest.raises(ValueError, match="amount must be greater than zero"):
        Transaction.start(
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("0"),
            payment_method=PaymentMethod.ACCOUNT_BALANCE,
        )


def test_transaction_requires_customer_id():
    with pytest.raises(ValueError, match="customer_id is required"):
        Transaction.start(
            customer_id="",
            merchant_id="merchant-1",
            amount=Decimal("10.00"),
            payment_method=PaymentMethod.ACCOUNT_BALANCE,
        )
