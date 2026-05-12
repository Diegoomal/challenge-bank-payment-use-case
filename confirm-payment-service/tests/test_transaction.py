from datetime import datetime, timezone

import pytest

from domain.exceptions import InvalidTransactionStatus
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus


def test_started_transaction_can_be_confirmed():
    transaction = Transaction.start("transaction-1")

    confirmed_at = transaction.confirm()

    assert transaction.status == TransactionStatus.CONFIRMED
    assert transaction.confirmed_at == confirmed_at


def test_confirm_rejects_already_confirmed_transaction():
    transaction = Transaction.start("transaction-1")
    transaction.confirm()

    with pytest.raises(InvalidTransactionStatus):
        transaction.confirm()


def test_confirm_rejects_reversed_transaction():
    now = datetime.now(timezone.utc)
    transaction = Transaction(
        id="transaction-1",
        merchant_id="merchant-1",
        status=TransactionStatus.REVERSED,
        created_at=now,
        updated_at=now,
    )

    with pytest.raises(InvalidTransactionStatus):
        transaction.confirm()


def test_transaction_requires_id():
    with pytest.raises(ValueError, match="transaction_id is required"):
        Transaction.start("")
