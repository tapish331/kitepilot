from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

import pytest

from strategy_kit.models import Bar, OrderSignal, Position, Side, Tick


def test_tick_validation_and_schema() -> None:
    t = Tick(ts=datetime(2024, 1, 1, 12, 0), instrument="X", price=Decimal("1"))
    assert t.ts.tzinfo is not None
    schema = Tick.model_json_schema()
    assert "instrument" in schema["properties"]


def test_order_signal() -> None:
    sig = OrderSignal(
        instrument="X",
        side=Side.BUY,
        size=1,
        ts=datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc),
    )
    assert sig.size == 1


def test_position() -> None:
    pos = Position(instrument="X", qty=2, avg_price=Decimal("3"))
    assert pos.qty == 2 and pos.avg_price == Decimal("3")


def test_bar_validation() -> None:
    b = Bar(
        instrument="X",
        start=datetime(2024, 1, 1, tzinfo=timezone.utc),
        end=datetime(2024, 1, 1, 0, 1, tzinfo=timezone.utc),
        open=Decimal("1"),
        high=Decimal("2"),
        low=Decimal("0.5"),
        close=Decimal("1.5"),
        volume=100,
    )
    assert b.end > b.start
    with pytest.raises(ValueError):
        OrderSignal(
            instrument="X",
            side=Side.BUY,
            size=0,
            ts=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
