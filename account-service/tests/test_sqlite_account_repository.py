from decimal import Decimal

from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository
from domain.account import Account


def test_sqlite_account_repository_saves_and_gets_account(tmp_path):
    repository = SQLiteAccountRepository(str(tmp_path / "accounts.db"))
    account = Account.create("customer-1", "Customer One", Decimal("100.00"))

    repository.save(account)

    saved = repository.get_by_customer_id("customer-1")
    assert saved is not None
    assert saved.id == account.id
    assert saved.balance == Decimal("100.00")
    assert repository.has_active_account("customer-1") is True


def test_sqlite_account_repository_returns_none_when_not_found(tmp_path):
    repository = SQLiteAccountRepository(str(tmp_path / "accounts.db"))

    assert repository.get_by_customer_id("missing") is None
    assert repository.has_active_account("missing") is False
