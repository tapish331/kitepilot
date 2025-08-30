from __future__ import annotations

from collections import deque
from typing import Deque, Dict, List

from ..interfaces import Strategy
from ..models import Bar, OrderSignal, Side
from ..registry import register_strategy


class SmaCrossoverStrategy(Strategy):
    """Simple moving-average crossover strategy.

    Emits a BUY signal when the short SMA crosses above the long SMA and a SELL
    signal when it crosses below.
    """

    def __init__(self, *, short_window: int, long_window: int) -> None:
        if short_window >= long_window:
            raise ValueError("short_window must be < long_window")
        self.short_window = short_window
        self.long_window = long_window
        self._short: Dict[str, Deque[float]] = {}
        self._long: Dict[str, Deque[float]] = {}
        self._last_rel: Dict[str, int] = {}

    def on_data(self, data: Bar | object) -> List[OrderSignal]:
        if not isinstance(data, Bar):
            return []
        short_q = self._short.setdefault(data.instrument, deque(maxlen=self.short_window))
        long_q = self._long.setdefault(data.instrument, deque(maxlen=self.long_window))
        last_rel = self._last_rel.get(data.instrument, 0)
        short_q.append(float(data.close))
        long_q.append(float(data.close))
        if len(long_q) < self.long_window:
            return []
        short_avg = sum(short_q) / len(short_q)
        long_avg = sum(long_q) / len(long_q)
        rel = 1 if short_avg > long_avg else (-1 if short_avg < long_avg else 0)
        signals: List[OrderSignal] = []
        if last_rel <= 0 and rel > 0:
            signals.append(
                OrderSignal(
                    instrument=data.instrument,
                    side=Side.BUY,
                    size=1,
                    ts=data.end,
                )
            )
        elif last_rel >= 0 and rel < 0:
            signals.append(
                OrderSignal(
                    instrument=data.instrument,
                    side=Side.SELL,
                    size=1,
                    ts=data.end,
                )
            )
        self._last_rel[data.instrument] = rel
        return signals


register_strategy("sma_crossover", "strategy_kit.strategies.sma_crossover.SmaCrossoverStrategy")
