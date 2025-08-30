from __future__ import annotations

from decimal import Decimal
from typing import Set

from pydantic import BaseModel, Field


class Limits(BaseModel):
    max_daily_loss: Decimal | None = None
    max_open_positions: int | None = None
    max_qty_per_order: Decimal | None = None
    max_qty_per_symbol_day: Decimal | None = None
    max_turnover_day: Decimal | None = None


class Throttle(BaseModel):
    min_seconds_between_orders: Decimal | None = None


class Toggles(BaseModel):
    kill_switch: bool = False
    opening_minutes_block: int | None = None


class Lists(BaseModel):
    instrument_banlist: Set[str] = Field(default_factory=set)


class Policy(BaseModel):
    limits: Limits = Field(default_factory=Limits)
    throttle: Throttle = Field(default_factory=Throttle)
    toggles: Toggles = Field(default_factory=Toggles)
    lists: Lists = Field(default_factory=Lists)

    def json_schema(self) -> dict[str, object]:
        """Return JSON schema for the policy."""
        return self.model_json_schema()
