from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
from kitepilot_common import (
    Side,
    OrderType,
    Signal,
    OrderIntent,
    OrderState,
    Fees,
    Limits,
)


def test_signal_roundtrip():
    now = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    s = Signal(symbol="BTCUSDT", side=Side.BUY, strength=0.8, ts_ist=now, ts_utc=now)
    payload = s.model_dump_json()
    again = Signal.model_validate_json(payload)
    assert again == s


def test_order_and_fees_limits():
    oi = OrderIntent(symbol="AAPL", side=Side.SELL, qty=10, order_type=OrderType.MARKET)
    st = OrderState(client_order_id="c1")
    fees = Fees(commission=Decimal("1.25"), taxes=Decimal("0.75"))
    lim = Limits(
        max_notional=Decimal("100000"), max_positions=10, max_risk_per_symbol=Decimal("2500")
    )
    assert fees.total == Decimal("2.00")
    assert st.status.value == "NEW"
    assert oi.qty == 10 and lim.max_positions == 10
