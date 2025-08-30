from __future__ import annotations
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_place_order_idempotent():
    payload = {
        "client_order_id": "abc-123",
        "symbol": "INFY",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 1,
        "price": 100.0
    }
    r1 = client.post("/orders", json=payload, headers={"Idempotency-Key": "abc-123"})
    r2 = client.post("/orders", json=payload, headers={"Idempotency-Key": "abc-123"})
    assert r1.status_code == 200
    assert r1.json()["broker_order_id"] == r2.json()["broker_order_id"]
