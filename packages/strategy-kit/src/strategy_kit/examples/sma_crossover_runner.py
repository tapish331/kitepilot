from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Iterator

from strategy_kit.models import Bar
from strategy_kit.strategies.sma_crossover import SmaCrossoverStrategy


PRICES = [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3]


def generate_bars() -> Iterator[Bar]:
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    for i, price in enumerate(PRICES):
        ts = start + timedelta(minutes=i)
        yield Bar(
            instrument="TEST",
            start=ts,
            end=ts + timedelta(minutes=1),
            open=Decimal(price),
            high=Decimal(price),
            low=Decimal(price),
            close=Decimal(price),
            volume=100,
        )


def main() -> None:
    strategy = SmaCrossoverStrategy(short_window=3, long_window=5)
    for bar in generate_bars():
        for signal in strategy.on_data(bar):
            print(signal.model_dump_json())


if __name__ == "__main__":  # pragma: no cover - manual run
    main()
