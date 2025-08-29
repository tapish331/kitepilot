from __future__ import annotations

import json
import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from apps.md_gateway.src.aggregator import Aggregator
from kitepilot_common import Tick

UTC = timezone.utc


def tick(ts: datetime, price: float) -> Tick:
    return Tick(
        ts_utc=ts,
        instrument="TCS",
        last_price=Decimal(str(price)),
        bid=None,
        ask=None,
        qty=1,
    )


def test_minute_snapshot():
    bars = []
    agg = Aggregator(on_bar_1m=bars.append)
    start = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)
    price = 100.0
    r = random.Random(42)
    for i in range(60):
        price += r.uniform(-1, 1)
        agg.ingest(tick(start + timedelta(seconds=i), price))
    agg.flush()
    expected = json.loads(Path("apps/md_gateway/tests/data/golden_1m.json").read_text())
    assert json.loads(bars[0].model_dump_json()) == expected
