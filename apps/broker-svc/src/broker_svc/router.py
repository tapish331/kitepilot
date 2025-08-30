from __future__ import annotations
from fastapi import APIRouter, Header, HTTPException
from kitepilot_broker.base import PlaceOrderRequest, PlaceOrderResponse, ModifyOrderRequest, CancelOrderRequest
from kitepilot_broker.zerodha import ZerodhaClient
from .idempotency import MemoryIdempotencyStore

router = APIRouter()
_client = ZerodhaClient()
_store = MemoryIdempotencyStore()

@router.post("/orders", response_model=PlaceOrderResponse)
def place_order(req: PlaceOrderRequest, Idempotency_Key: str | None = Header(default=None, alias="Idempotency-Key")):
    key = Idempotency_Key or req.client_order_id
    if not key:
        raise HTTPException(status_code=400, detail="Missing Idempotency-Key or client_order_id")
    cached = _store.get(key)
    if cached:
        return cached
    resp = _client.place_order(req)
    _store.set(key, resp)
    return resp

@router.patch("/orders/{client_order_id}")
def modify_order(client_order_id: str, req: ModifyOrderRequest):
    if client_order_id != req.client_order_id:
        raise HTTPException(status_code=400, detail="client_order_id mismatch")
    _client.modify_order(req)
    return {"status": "ok"}

@router.delete("/orders/{client_order_id}")
def cancel_order(client_order_id: str):
    _client.cancel_order(CancelOrderRequest(client_order_id=client_order_id))
    return {"status": "ok"}
