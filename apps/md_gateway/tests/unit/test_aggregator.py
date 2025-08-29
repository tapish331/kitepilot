from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal

from kitepilot_common import Bar1M, Bar1S, Tick

from apps.md_gateway.src.aggregator import Aggregator


UTC = timezone.utc


def tick(ts: datetime, price: float, symbol: str = "TCS", qty: int = 1) -> Tick:
    return Tick(
        ts_utc=ts,
        instrument=symbol,
        last_price=Decimal(str(price)),
        bid=None,
        ask=None,
        qty=qty,
    )


def test_single_symbol_bar():
    out: list[Bar1S] = []
    agg = Aggregator(on_bar_1s=out.append)
    t0 = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)
    agg.ingest(tick(t0, 100))
    agg.ingest(tick(t0 + timedelta(milliseconds=200), 101))
    agg.ingest(tick(t0 + timedelta(milliseconds=800), 99))
    agg.flush()
    assert len(out) == 1
    bar = out[0]
    assert bar.open == Decimal("100")
    assert bar.high == Decimal("101")
    assert bar.low == Decimal("99")
    assert bar.close == Decimal("99")
    assert bar.volume == 3
    assert bar.trades == 3


def test_gap_filling():
    out: list[Bar1S] = []
    agg = Aggregator(on_bar_1s=out.append)
    t0 = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)
    agg.ingest(tick(t0, 100))
    agg.ingest(tick(t0 + timedelta(seconds=3), 102))
    agg.flush()
    assert len(out) == 4
    assert [b.start_utc.second for b in out[:3]] == [0, 1, 2]
    assert out[1].volume == 0 and out[1].open == out[1].close == Decimal("100")


def test_multi_symbol_interleave():
    out: list[tuple[str, Bar1S]] = []

    def sink(bar: Bar1S) -> None:
        out.append((bar.instrument, bar))

    agg = Aggregator(on_bar_1s=sink)
    t0 = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)
    agg.ingest(tick(t0, 100, symbol="TCS"))
    agg.ingest(tick(t0 + timedelta(milliseconds=100), 200, symbol="INFY"))
    agg.ingest(tick(t0 + timedelta(seconds=1), 101, symbol="TCS"))
    agg.ingest(tick(t0 + timedelta(seconds=1, milliseconds=100), 201, symbol="INFY"))
    agg.flush()
    symbols = [s for s, _ in out]
    assert symbols == ["TCS", "INFY", "TCS", "INFY"]


def test_minute_rollup():
    bars_1m: list[Bar1M] = []
    agg = Aggregator(on_bar_1m=bars_1m.append)
    t = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)
    for i in range(60):
        agg.ingest(tick(t + timedelta(seconds=i), 100 + i * 0.1))
    agg.flush()
    assert len(bars_1m) == 1
    mbar = bars_1m[0]
    assert mbar.open == Decimal("100")
    assert mbar.close == Decimal(str(100 + 59 * 0.1))
    assert mbar.trades == 60

