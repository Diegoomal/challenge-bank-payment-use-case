from decimal import Decimal

from adapters.persistence.sqlite_transaction_repository import (
    SQLiteTransactionRepository,
)
from domain.payment_method import PaymentMethod
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus


def test_sqlite_transaction_repository_saves_and_gets_transaction(tmp_path):
    repository = SQLiteTransactionRepository(str(tmp_path / "payments.db"))
    transaction = Transaction.start(
        customer_id="customer-1",
        merchant_id="merchant-1",
        amount=Decimal("99.99"),
        payment_method=PaymentMethod.CREDIT_CARD,
    )

    repository.save(transaction)

    saved = repository.get_by_id(transaction.id)
    assert saved is not None
    assert saved.id == transaction.id
    assert saved.amount == Decimal("99.99")
    assert saved.payment_method == PaymentMethod.CREDIT_CARD
    assert saved.status == TransactionStatus.STARTED


def test_sqlite_transaction_repository_returns_none_when_not_found(tmp_path):
    repository = SQLiteTransactionRepository(str(tmp_path / "payments.db"))

    assert repository.get_by_id("missing") is None
