"""Position sizing and intent models."""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Signal(BaseModel):
    """Trading signal produced by a strategy."""

    model_config = ConfigDict(extra="forbid")

    symbol: str
    side: Literal["BUY", "SELL", "FLAT"]
    confidence: float
    ts: datetime

    @field_validator("ts")
    @classmethod
    def ensure_aware(cls, v: datetime) -> datetime:
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)


class OrderIntent(BaseModel):
    """Paper trade order intent."""

    model_config = ConfigDict(extra="forbid")

    symbol: str
    side: Literal["BUY", "SELL"]
    qty: int = Field(gt=0)
    price: Decimal | None = None
    ts: datetime
    reason: str

    @field_validator("ts")
    @classmethod
    def ensure_aware(cls, v: datetime) -> datetime:
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)


def size_signal(signal: Signal) -> OrderIntent:
    """Map a *signal* to a sized :class:`OrderIntent`."""
    if signal.side == "FLAT":
        raise ValueError("cannot size FLAT signal")
    return OrderIntent(
        symbol=signal.symbol,
        side=signal.side,
        qty=1,
        price=None,
        ts=signal.ts,
        reason="strategy-svc",
    )
