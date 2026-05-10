from datetime import datetime, timezone

import pytest

from domain.exceptions import InvalidTransactionStatus
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus


def test_started_transaction_can_be_reversed():
    transaction = Transaction.start("transaction-1")

    reversed_at = transaction.reverse("INSUFFICIENT_BALANCE")

    assert transaction.status == TransactionStatus.REVERSED
    assert transaction.reversed_at == reversed_at
    assert transaction.reversal_reason == "INSUFFICIENT_BALANCE"


def test_processing_transaction_can_be_reversed():
    now = datetime.now(timezone.utc)
    transaction = Transaction(
        id="transaction-1",
        status=TransactionStatus.PROCESSING,
        created_at=now,
        updated_at=now,
    )

    transaction.reverse("ACCOUNT_BLOCKED")

    assert transaction.status == TransactionStatus.REVERSED


def test_confirmed_transaction_cannot_be_reversed():
    now = datetime.now(timezone.utc)
    transaction = Transaction(
        id="transaction-1",
        status=TransactionStatus.CONFIRMED,
        created_at=now,
        updated_at=now,
    )

    with pytest.raises(InvalidTransactionStatus):
        transaction.reverse("INSUFFICIENT_BALANCE")


def test_reverse_requires_reason():
    transaction = Transaction.start("transaction-1")

    with pytest.raises(ValueError, match="reason is required"):
        transaction.reverse("")
