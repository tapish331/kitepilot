"""Signal pipeline turning bars into order intents."""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Iterable, List
import logging

from pydantic import BaseModel, ConfigDict, Field, field_validator

from strategy_kit import models as kit_models  # type: ignore[import-untyped]
from strategy_kit.interfaces import Strategy  # type: ignore[import-untyped]

from .position_sizing import OrderIntent, Signal, size_signal

logger = logging.getLogger(__name__)


class Bar(BaseModel):
    """Input bar data."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    o: Decimal
    h: Decimal
    l_: Decimal = Field(alias="l")
    c: Decimal
    v: int
    symbol: str

    @field_validator("ts")
    @classmethod
    def ensure_aware(cls, v: datetime) -> datetime:
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)


def load_bars(path: Path) -> List[Bar]:
    """Load bars from a JSONL *path*."""
    with path.open("r", encoding="utf-8") as f:
        return [Bar.model_validate_json(line) for line in f if line.strip()]


def run(strategy: Strategy, bars: Iterable[Bar]) -> List[OrderIntent]:
    """Run *bars* through *strategy* and return order intents."""
    intents: List[OrderIntent] = []
    for bar in bars:
        kit_bar = kit_models.Bar(
            instrument=bar.symbol,
            start=bar.ts,
            end=bar.ts,
            open=bar.o,
            high=bar.h,
            low=bar.l_,
            close=bar.c,
            volume=bar.v,
        )
        for os in strategy.on_data(kit_bar):
            signal = Signal(
                symbol=os.instrument,
                side=os.side.value,
                confidence=1.0,
                ts=os.ts,
            )
            intent = size_signal(signal)
            logger.info(intent.model_dump_json())
            print(intent.model_dump_json())
            intents.append(intent)
    return intents
