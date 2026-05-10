from datetime import datetime, timezone

from fastapi.testclient import TestClient

from adapters.persistence.sqlite_transaction_repository import (
    SQLiteTransactionRepository,
)
from configurator import create_app
from domain.transaction import Transaction


def test_confirm_payment_endpoint_confirms_transaction(tmp_path):
    database_path = str(tmp_path / "confirm.db")
    repository = SQLiteTransactionRepository(database_path)
    repository.save(Transaction.start("transaction-1"))
    app = create_app(database_path)
    client = TestClient(app)

    response = client.post(
        "/payments/confirm",
        json={
            "transaction_id": "transaction-1",
            "account_id": "account-1",
            "customer_id": "customer-1",
            "amount": "50.00",
            "occurred_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["transaction_id"] == "transaction-1"
    assert body["status"] == "CONFIRMED"
    assert body["confirmed_at"]


def test_confirm_payment_endpoint_returns_400_when_transaction_missing(tmp_path):
    app = create_app(str(tmp_path / "confirm.db"))
    client = TestClient(app)

    response = client.post(
        "/payments/confirm",
        json={
            "transaction_id": "missing",
            "account_id": "account-1",
            "customer_id": "customer-1",
            "amount": "50.00",
            "occurred_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "transaction not found"
