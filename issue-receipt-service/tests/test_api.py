from datetime import datetime, timezone

from fastapi.testclient import TestClient

from configurator import create_app


def test_issue_receipt_endpoint_issues_receipt(tmp_path):
    app = create_app(str(tmp_path / "receipts.db"))
    client = TestClient(app)

    response = client.post(
        "/receipts",
        json={
            "transaction_id": "transaction-1",
            "customer_id": "customer-1",
            "merchant_id": "merchant-1",
            "amount": "15.75",
            "confirmed_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["receipt_id"]
    assert body["transaction_id"]
    assert body["status"] == "ISSUED"
    assert body["issued_at"]


def test_issue_receipt_endpoint_rejects_invalid_amount(tmp_path):
    app = create_app(str(tmp_path / "receipts.db"))
    client = TestClient(app)

    response = client.post(
        "/receipts",
        json={
            "transaction_id": "transaction-1",
            "customer_id": "customer-1",
            "merchant_id": "merchant-1",
            "amount": "0",
            "confirmed_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 422
