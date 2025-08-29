from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Callable, Dict, List

from kitepilot_common import Bar1M, Bar1S, Tick


@dataclass
class _SecondState:
    bar: Bar1S


class Aggregator:
    """Aggregate ticks into 1-second and 1-minute bars."""

    def __init__(
        self,
        on_bar_1s: Callable[[Bar1S], None] | None = None,
        on_bar_1m: Callable[[Bar1M], None] | None = None,
    ) -> None:
        self.on_bar_1s = on_bar_1s
        self.on_bar_1m = on_bar_1m
        self._seconds: Dict[str, _SecondState] = {}
        self._pending_minutes: Dict[str, List[Bar1S]] = {}
        self._last_close: Dict[str, Decimal] = {}

    def ingest(self, tick: Tick) -> None:
        symbol = tick.instrument
        second = tick.ts_utc.replace(microsecond=0)
        state = self._seconds.get(symbol)
        if state is None:
            self._start_new_second(symbol, second, tick)
            return
        if second == state.bar.start_utc:
            self._update_second(state.bar, tick)
            return
        # new second arrived
        self._close_second(symbol, state.bar, second)
        self._start_new_second(symbol, second, tick)

    def flush(self) -> None:
        for symbol, state in list(self._seconds.items()):
            self._close_second(
                symbol, state.bar, state.bar.start_utc + timedelta(seconds=1)
            )
        self._seconds.clear()
        for symbol, bars in list(self._pending_minutes.items()):
            if bars:
                self._emit_minute(symbol, bars)
            self._pending_minutes[symbol] = []

    # internal helpers
    def _start_new_second(self, symbol: str, second: datetime, tick: Tick) -> None:
        price = tick.last_price
        bar = Bar1S(
            instrument=symbol,
            start_utc=second,
            end_utc=second + timedelta(seconds=1),
            open=price,
            high=price,
            low=price,
            close=price,
            volume=tick.qty,
            trades=1 if tick.qty else 0,
            last_ts_utc=tick.ts_utc,
        )
        self._seconds[symbol] = _SecondState(bar=bar)
        self._last_close.setdefault(symbol, price)

    def _update_second(self, bar: Bar1S, tick: Tick) -> None:
        price = tick.last_price
        bar.high = max(bar.high, price)
        bar.low = min(bar.low, price)
        bar.close = price
        bar.volume += tick.qty
        bar.trades += 1
        bar.last_ts_utc = tick.ts_utc

    def _close_second(self, symbol: str, bar: Bar1S, next_second: datetime) -> None:
        # finalise current bar
        self._last_close[symbol] = bar.close
        self._emit_second(symbol, bar)
        # fill gaps if any
        start = bar.start_utc + timedelta(seconds=1)
        while start < next_second:
            gap_bar = Bar1S(
                instrument=symbol,
                start_utc=start,
                end_utc=start + timedelta(seconds=1),
                open=self._last_close[symbol],
                high=self._last_close[symbol],
                low=self._last_close[symbol],
                close=self._last_close[symbol],
                volume=0,
                trades=0,
                last_ts_utc=start,
            )
            self._emit_second(symbol, gap_bar)
            start += timedelta(seconds=1)

    def _emit_second(self, symbol: str, bar: Bar1S) -> None:
        if self.on_bar_1s:
            self.on_bar_1s(bar)
        pending = self._pending_minutes.setdefault(symbol, [])
        pending.append(bar)
        if len(pending) == 60:
            self._emit_minute(symbol, pending)
            self._pending_minutes[symbol] = []

    def _emit_minute(self, symbol: str, seconds: List[Bar1S]) -> None:
        start = seconds[0].start_utc
        end = start + timedelta(minutes=1)
        bar = Bar1M(
            instrument=symbol,
            start_utc=start,
            end_utc=end,
            open=seconds[0].open,
            high=max(b.high for b in seconds),
            low=min(b.low for b in seconds),
            close=seconds[-1].close,
            volume=sum(b.volume for b in seconds),
            trades=sum(b.trades for b in seconds),
            last_ts_utc=seconds[-1].last_ts_utc,
        )
        if self.on_bar_1m:
            self.on_bar_1m(bar)
