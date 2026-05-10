from fastapi.testclient import TestClient

from configurator import create_app


def test_create_account_endpoint_creates_account(tmp_path):
    app = create_app(str(tmp_path / "accounts.db"))
    client = TestClient(app)

    response = client.post(
        "/accounts",
        json={
            "customer_id": "customer-1",
            "account_holder": "Customer One",
            "initial_deposit": "100.00",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["account_id"]
    assert body["customer_id"] == "customer-1"
    assert body["status"] == "ACTIVE"
    assert body["created_at"]


def test_create_account_endpoint_rejects_duplicate_active_account(tmp_path):
    app = create_app(str(tmp_path / "accounts.db"))
    client = TestClient(app)
    payload = {
        "customer_id": "customer-1",
        "account_holder": "Customer One",
        "initial_deposit": "100.00",
    }

    assert client.post("/accounts", json=payload).status_code == 201
    response = client.post("/accounts", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "customer already has an active account"
