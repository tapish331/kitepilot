from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Protocol

from .models import Bar, OrderSignal, Position, Tick


class DataSource(Protocol):
    """Produces market data events for strategies."""

    def stream(self) -> Iterable[Bar | Tick]:  # pragma: no cover - protocol method
        """Return an iterable of market data events."""


class Strategy(ABC):
    """Base strategy interface."""

    @abstractmethod
    def on_data(self, data: Bar | Tick) -> list[OrderSignal]:
        """Consume a bar or tick and optionally emit order signals."""


class PositionSizer(Protocol):
    """Determines order quantities based on strategy signals and current positions."""

    def size_order(
        self, signal: OrderSignal, position: Position
    ) -> OrderSignal:  # pragma: no cover
        """Return a sized order signal."""


class RiskManager(Protocol):
    """Approves or rejects signals based on risk constraints."""

    def approve(self, signal: OrderSignal, position: Position) -> bool:  # pragma: no cover
        """Return True if the order may proceed."""
