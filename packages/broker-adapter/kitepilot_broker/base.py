from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel

class PlaceOrderRequest(BaseModel):
    client_order_id: str
    symbol: str
    side: str  # "BUY" | "SELL"
    order_type: str  # "LIMIT" | "MARKET"
    quantity: int
    price: Optional[float] = None
    product: str = "MIS"  # placeholder
    validity: str = "DAY"

class PlaceOrderResponse(BaseModel):
    client_order_id: str
    broker_order_id: str
    status: str  # "accepted" | "duplicate" | "rejected"

class ModifyOrderRequest(BaseModel):
    client_order_id: str
    price: Optional[float] = None
    quantity: Optional[int] = None

class CancelOrderRequest(BaseModel):
    client_order_id: str

class BrokerClient(ABC):
    @abstractmethod
    def place_order(self, req: PlaceOrderRequest) -> PlaceOrderResponse: ...
    @abstractmethod
    def modify_order(self, req: ModifyOrderRequest) -> None: ...
    @abstractmethod
    def cancel_order(self, req: CancelOrderRequest) -> None: ...
