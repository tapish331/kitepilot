from __future__ import annotations
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from .enums import Side, OrderType, TimeInForce, OrderStatus

IST = timezone(timedelta(hours=5, minutes=30))


def ist_utc_pair(dt: datetime) -> tuple[datetime, datetime]:
    """Return (ist, utc) aware datetimes for input dt.
    If dt is naive, assume UTC.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(IST), dt.astimezone(timezone.utc)


class Signal(BaseModel):
    symbol: str
    side: Side
    strength: float = Field(ge=0.0, le=1.0)
    ts_ist: datetime
    ts_utc: datetime

    @field_validator("ts_utc")
    @classmethod
    def ensure_aware(cls, v: datetime) -> datetime:
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)


class OrderIntent(BaseModel):
    symbol: str
    side: Side
    qty: int = Field(gt=0)
    order_type: OrderType = OrderType.MARKET
    limit_price: Optional[Decimal] = None
    tif: TimeInForce = TimeInForce.DAY

    @field_validator("limit_price")
    @classmethod
    def price_required_for_limit(
        cls, v: Optional[Decimal], info: ValidationInfo
    ) -> Optional[Decimal]:
        order_type = info.data.get("order_type")
        if order_type == OrderType.LIMIT and v is None:
            raise ValueError("limit_price required for LIMIT orders")
        return v


class Fees(BaseModel):
    commission: Decimal = Decimal("0")
    taxes: Decimal = Decimal("0")

    @property
    def total(self) -> Decimal:
        return self.commission + self.taxes


class Limits(BaseModel):
    max_notional: Decimal = Field(gt=0)
    max_positions: int = Field(gt=0)
    max_risk_per_symbol: Decimal = Field(gt=0)


class OrderState(BaseModel):
    client_order_id: str
    status: OrderStatus = OrderStatus.NEW
    filled_qty: int = 0
    avg_price: Optional[Decimal] = None


class Tick(BaseModel):
    """Market data tick."""

    ts_utc: datetime
    instrument: str
    last_price: Decimal
    bid: Optional[Decimal] = None
    ask: Optional[Decimal] = None
    qty: int = 0

    @field_validator("ts_utc")
    @classmethod
    def ensure_aware(cls, v: datetime) -> datetime:
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)


class BarBase(BaseModel):
    """Common OHLCV bar fields."""

    instrument: str
    start_utc: datetime
    end_utc: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int = 0
    trades: int = 0
    last_ts_utc: datetime

    @field_validator("start_utc", "end_utc", "last_ts_utc")
    @classmethod
    def ensure_aware(cls, v: datetime) -> datetime:
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)


class Bar1S(BarBase):
    """One-second OHLCV bar."""


class Bar1M(BarBase):
    """One-minute OHLCV bar."""

