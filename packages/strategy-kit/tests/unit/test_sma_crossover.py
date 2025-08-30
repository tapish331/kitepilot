from __future__ import annotations

import json
from pathlib import Path

from strategy_kit.examples.sma_crossover_runner import generate_bars
from strategy_kit.models import OrderSignal
from strategy_kit.strategies.sma_crossover import SmaCrossoverStrategy


def test_sma_crossover_golden() -> None:
    strategy = SmaCrossoverStrategy(short_window=3, long_window=5)
    signals: list[OrderSignal] = []
    for bar in generate_bars():
        signals.extend(strategy.on_data(bar))
    expected_path = Path(__file__).parents[1] / "data" / "sma_crossover_expected.json"
    expected_raw = json.loads(expected_path.read_text())
    expected = [OrderSignal.model_validate(e) for e in expected_raw]
    assert [s.model_dump() for s in signals] == [s.model_dump() for s in expected]
