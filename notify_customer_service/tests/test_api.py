from datetime import datetime, timezone

from fastapi.testclient import TestClient

from configurator import create_app


def test_notify_customer_endpoint_delivers_notification(tmp_path):
    database_path = str(tmp_path / "notify.db")
    app = create_app(database_path)
    client = TestClient(app)

    response = client.post(
        "/notifications/customer",
        json={
            "transaction_id": "transaction-1",
            "merchant_id": "merchant-1",
            "customer_id": "customer-1",
            "amount": "50.00",
            "confirmed_at": datetime.now(timezone.utc).isoformat(),
            "recipient": "customer@example.com",
            "channel": "EMAIL",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["notification_id"]
    assert body["transaction_id"] == "transaction-1"
    assert body["customer_id"] == "customer-1"
    assert body["status"] == "DELIVERED"
    assert body["notified_at"]


def test_notify_customer_endpoint_rejects_invalid_payload(tmp_path):
    app = create_app(str(tmp_path / "notify.db"))
    client = TestClient(app)

    response = client.post(
        "/notifications/customer",
        json={
            "transaction_id": "",
            "merchant_id": "merchant-1",
            "customer_id": "customer-1",
            "amount": "50.00",
            "confirmed_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 422
