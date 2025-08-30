from __future__ import annotations
import uuid
from pydantic import BaseModel
from ..base import BrokerClient, PlaceOrderRequest, PlaceOrderResponse, ModifyOrderRequest, CancelOrderRequest
from .models import ZerodhaOrder

class _MemoryBrokerState(BaseModel):
    orders: dict[str, str] = {}

_state = _MemoryBrokerState()

class ZerodhaClient(BrokerClient):
    """Stubbed client that maps to Zerodha payloads without real HTTP."""
    def _map_place(self, req: PlaceOrderRequest) -> ZerodhaOrder:
        return ZerodhaOrder(
            tradingsymbol=req.symbol,
            transaction_type=req.side,
            order_type=req.order_type,
            product=req.product,
            quantity=req.quantity,
            price=req.price,
            tag=req.client_order_id,
        )

    def place_order(self, req: PlaceOrderRequest) -> PlaceOrderResponse:
        # Simulate id assignment
        existing = _state.orders.get(req.client_order_id)
        if existing:
            return PlaceOrderResponse(client_order_id=req.client_order_id, broker_order_id=existing, status="duplicate")
        payload = self._map_place(req)
        _ = payload  # would be used for real HTTP
        broker_id = str(uuid.uuid4())
        _state.orders[req.client_order_id] = broker_id
        return PlaceOrderResponse(client_order_id=req.client_order_id, broker_order_id=broker_id, status="accepted")

    def modify_order(self, req: ModifyOrderRequest) -> None:
        if req.client_order_id not in _state.orders:
            return  # no-op in stub
        return

    def cancel_order(self, req: CancelOrderRequest) -> None:
        _state.orders.pop(req.client_order_id, None)
        return
