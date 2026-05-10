from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus
from adapters.persistence.sqlite_transaction_repository import (
    SQLiteTransactionRepository,
)


def test_sqlite_transaction_repository_saves_and_gets_transaction(tmp_path):
    repository = SQLiteTransactionRepository(str(tmp_path / "confirm.db"))
    transaction = Transaction.start("transaction-1")
    transaction.confirm()

    repository.save(transaction)

    saved = repository.get_by_id("transaction-1")
    assert saved is not None
    assert saved.id == "transaction-1"
    assert saved.status == TransactionStatus.CONFIRMED
    assert saved.confirmed_at is not None


def test_sqlite_transaction_repository_returns_none_when_not_found(tmp_path):
    repository = SQLiteTransactionRepository(str(tmp_path / "confirm.db"))

    assert repository.get_by_id("missing") is None
