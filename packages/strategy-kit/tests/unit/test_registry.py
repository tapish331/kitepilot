from __future__ import annotations

import pytest

from strategy_kit.interfaces import Strategy
from strategy_kit.registry import get_strategy, register_strategy


class DummyStrategy(Strategy):
    def on_data(self, data):  # pragma: no cover - trivial
        return []


def test_register_and_get() -> None:
    register_strategy("dummy", DummyStrategy)
    assert get_strategy("dummy") is DummyStrategy


def test_lazy_import() -> None:
    register_strategy("lazy", "strategy_kit.strategies.sma_crossover.SmaCrossoverStrategy")
    cls = get_strategy("lazy")
    assert cls.__name__ == "SmaCrossoverStrategy"

    with pytest.raises(KeyError):
        get_strategy("missing")
