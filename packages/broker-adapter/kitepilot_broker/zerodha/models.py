from __future__ import annotations
from pydantic import BaseModel

class ZerodhaOrder(BaseModel):
    variety: str = "regular"
    exchange: str = "NSE"
    tradingsymbol: str
    transaction_type: str  # BUY/SELL
    order_type: str  # LIMIT/MARKET
    product: str  # MIS/CNC/NRML
    quantity: int
    price: float | None = None
    validity: str = "DAY"
    tag: str | None = None
