from fastapi.testclient import TestClient

from configurator import create_app


def test_start_payment_endpoint_creates_payment(tmp_path):
    app = create_app(str(tmp_path / "payments.db"))
    client = TestClient(app)

    response = client.post(
        "/payments/start",
        json={
            "customer_id": "customer-1",
            "merchant_id": "merchant-1",
            "amount": "15.75",
            "payment_method": "ACCOUNT_BALANCE",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["transaction_id"]
    assert body["status"] == "STARTED"
    assert body["created_at"]


def test_start_payment_endpoint_rejects_invalid_amount(tmp_path):
    app = create_app(str(tmp_path / "payments.db"))
    client = TestClient(app)

    response = client.post(
        "/payments/start",
        json={
            "customer_id": "customer-1",
            "merchant_id": "merchant-1",
            "amount": "0",
            "payment_method": "ACCOUNT_BALANCE",
        },
    )

    assert response.status_code == 422
