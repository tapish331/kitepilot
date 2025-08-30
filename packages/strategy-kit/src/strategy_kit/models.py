from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Side(str, Enum):
    """Order side."""

    BUY = "BUY"
    SELL = "SELL"


class Tick(BaseModel):
    """Market data tick."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    instrument: str
    price: Decimal
    bid: Decimal | None = None
    ask: Decimal | None = None
    qty: int = 0

    @field_validator("ts")
    @classmethod
    def ensure_aware(cls, v: datetime) -> datetime:
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)


class Bar(BaseModel):
    """OHLCV bar."""

    model_config = ConfigDict(extra="forbid")

    instrument: str
    start: datetime
    end: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int = 0

    @field_validator("start", "end")
    @classmethod
    def ensure_aware(cls, v: datetime) -> datetime:
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)


class OrderSignal(BaseModel):
    """Signal emitted by a strategy to express trading intent."""

    model_config = ConfigDict(extra="forbid")

    instrument: str
    side: Side
    size: int = Field(gt=0)
    ts: datetime

    @field_validator("ts")
    @classmethod
    def ensure_aware(cls, v: datetime) -> datetime:
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)


class Position(BaseModel):
    """Current position for an instrument."""

    model_config = ConfigDict(extra="forbid")

    instrument: str
    qty: int = 0
    avg_price: Decimal = Decimal("0")
