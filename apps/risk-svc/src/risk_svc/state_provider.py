from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from decimal import Decimal

from kitepilot_risk import AccountState, OrderIntent


class StateProvider:
    """Thread-safe in-memory state for risk evaluation."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._state = AccountState()

    def snapshot(self) -> AccountState:
        with self._lock:
            return self._state

    def record(self, intent: OrderIntent) -> None:
        now = datetime.now(timezone.utc)
        with self._lock:
            st = self._state
            st.qty_by_symbol[intent.symbol] = st.qty_by_symbol.get(intent.symbol, Decimal("0")) + intent.qty
            if intent.price is not None:
                st.turnover_by_symbol[intent.symbol] = st.turnover_by_symbol.get(intent.symbol, Decimal("0")) + intent.qty * intent.price
            st.last_order_ts_by_symbol[intent.symbol] = now
