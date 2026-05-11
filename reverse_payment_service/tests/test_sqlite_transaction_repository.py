from adapters.persistence.sqlite_transaction_repository import (
    SQLiteTransactionRepository,
)
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus


def test_sqlite_transaction_repository_saves_and_gets_transaction(tmp_path):
    repository = SQLiteTransactionRepository(str(tmp_path / "reverse.db"))
    transaction = Transaction.start("transaction-1", "customer-1", "merchant-1")
    transaction.reverse("INSUFFICIENT_BALANCE")

    repository.save(transaction)

    saved = repository.get_by_id("transaction-1")
    assert saved is not None
    assert saved.id == "transaction-1"
    assert saved.customer_id == "customer-1"
    assert saved.merchant_id == "merchant-1"
    assert saved.status == TransactionStatus.REVERSED
    assert saved.reversal_reason == "INSUFFICIENT_BALANCE"
    assert saved.reversed_at is not None


def test_sqlite_transaction_repository_returns_none_when_not_found(tmp_path):
    repository = SQLiteTransactionRepository(str(tmp_path / "reverse.db"))

    assert repository.get_by_id("missing") is None
