from __future__ import annotations
from broker_svc.idempotency import MemoryIdempotencyStore

def test_idempotency_store_roundtrip():
    s = MemoryIdempotencyStore(ttl_seconds=60)
    assert s.get("k") is None
    s.set("k", {"x": 1})
    assert s.get("k") == {"x": 1}
