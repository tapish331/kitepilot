from __future__ import annotations
from kitepilot_broker.base import PlaceOrderRequest
from kitepilot_broker.zerodha import ZerodhaClient

def test_mapping_idempotency_roundtrip():
    c = ZerodhaClient()
    req = PlaceOrderRequest(client_order_id="abc-123", symbol="INFY", side="BUY", order_type="LIMIT", quantity=5, price=100.5)
    r1 = c.place_order(req)
    r2 = c.place_order(req)
    assert r1.client_order_id == "abc-123"
    assert r1.broker_order_id == r2.broker_order_id
    assert r2.status == "duplicate"
