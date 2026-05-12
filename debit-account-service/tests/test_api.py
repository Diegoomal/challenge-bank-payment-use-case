from decimal import Decimal

from fastapi.testclient import TestClient

from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository
from configurator import create_app
from domain.account import Account


def test_debit_account_endpoint_completes_debit(tmp_path):
    database_path = str(tmp_path / "accounts.db")
    repository = SQLiteAccountRepository(database_path)
    repository.save(Account.create("customer-1", "Customer One", Decimal("100.00")))
    app = create_app(database_path)
    client = TestClient(app)

    response = client.post(
        "/accounts/debit",
        json={
            "transaction_id": "transaction-1",
            "customer_id": "customer-1",
            "merchant_id": "merchant-1",
            "amount": "40.00",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["account_id"]
    assert body["transaction_id"] == "transaction-1"
    assert body["status"] == "COMPLETED"
    assert body["reason"] is None


def test_debit_account_endpoint_returns_failed_when_account_not_found(tmp_path):
    app = create_app(str(tmp_path / "accounts.db"))
    client = TestClient(app)

    response = client.post(
        "/accounts/debit",
        json={
            "transaction_id": "transaction-1",
            "customer_id": "customer-1",
            "merchant_id": "merchant-1",
            "amount": "40.00",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["account_id"] is None
    assert body["status"] == "FAILED"
    assert body["reason"] == "ACCOUNT_NOT_FOUND"
