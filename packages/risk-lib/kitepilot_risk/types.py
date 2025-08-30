from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Dict

from pydantic import BaseModel, Field


class OrderIntent(BaseModel):
    symbol: str
    side: str
    qty: Decimal
    price: Decimal | None = None
    account: str


class AccountState(BaseModel):
    pnl: Decimal = Decimal("0")
    open_positions: int = 0
    turnover_by_symbol: Dict[str, Decimal] = Field(default_factory=dict)
    qty_by_symbol: Dict[str, Decimal] = Field(default_factory=dict)
    last_order_ts_by_symbol: Dict[str, datetime] = Field(default_factory=dict)
