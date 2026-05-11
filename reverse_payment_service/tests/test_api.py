from datetime import datetime, timezone

from fastapi.testclient import TestClient

from adapters.persistence.sqlite_transaction_repository import (
    SQLiteTransactionRepository,
)
from configurator import create_app
from domain.transaction import Transaction


def test_reverse_payment_endpoint_reverses_transaction(tmp_path):
    database_path = str(tmp_path / "reverse.db")
    repository = SQLiteTransactionRepository(database_path)
    repository.save(Transaction.start("transaction-1"))
    app = create_app(database_path)
    client = TestClient(app)

    response = client.post(
        "/payments/reverse",
        json={
            "transaction_id": "transaction-1",
            "customer_id": "customer-1",
            "merchant_id": "merchant-1",
            "amount": "50.00",
            "reason": "INSUFFICIENT_BALANCE",
            "occurred_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["transaction_id"] == "transaction-1"
    assert body["status"] == "REVERSED"
    assert body["reason"] == "INSUFFICIENT_BALANCE"
    assert body["reversed_at"]


def test_reverse_payment_endpoint_returns_400_when_transaction_missing(tmp_path):
    app = create_app(str(tmp_path / "reverse.db"))
    client = TestClient(app)

    response = client.post(
        "/payments/reverse",
        json={
            "transaction_id": "missing",
            "customer_id": "customer-1",
            "amount": "50.00",
            "reason": "ACCOUNT_NOT_FOUND",
            "occurred_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "transaction not found"
