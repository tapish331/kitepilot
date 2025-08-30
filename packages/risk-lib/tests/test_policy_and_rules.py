from __future__ import annotations

from datetime import datetime, timezone, timedelta
from decimal import Decimal

from freezegun import freeze_time

from kitepilot_risk import (
    AccountState,
    OrderIntent,
    Policy,
    THROTTLED,
    KILL_SWITCH,
    INSTRUMENT_BANNED,
    MAX_QTY_ORDER,
    evaluate_order,
)
from kitepilot_risk.policy import Limits, Lists, Toggles, Throttle


def test_policy_roundtrip():
    pol = Policy()
    payload = pol.model_dump_json()
    again = Policy.model_validate_json(payload)
    assert again == pol
    assert "limits" in pol.json_schema()["properties"]


def test_kill_switch_rejects():
    pol = Policy(toggles=Toggles(kill_switch=True))
    st = AccountState()
    intent = OrderIntent(symbol="AAPL", side="BUY", qty=Decimal("1"), account="acc")
    dec = evaluate_order(pol, st, intent)
    assert not dec.allowed and dec.reason == KILL_SWITCH


def test_banlist():
    pol = Policy(lists=Lists(instrument_banlist={"IBM"}))
    st = AccountState()
    intent = OrderIntent(symbol="IBM", side="BUY", qty=Decimal("1"), account="acc")
    dec = evaluate_order(pol, st, intent)
    assert not dec.allowed and dec.reason == INSTRUMENT_BANNED


def test_max_qty_per_order():
    pol = Policy(limits=Limits(max_qty_per_order=Decimal("5")))
    st = AccountState()
    intent = OrderIntent(symbol="AAPL", side="BUY", qty=Decimal("10"), account="acc")
    dec = evaluate_order(pol, st, intent)
    assert not dec.allowed and dec.reason == MAX_QTY_ORDER


def test_throttle():
    pol = Policy(throttle=Throttle(min_seconds_between_orders=Decimal("5")))
    now = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    st = AccountState(last_order_ts_by_symbol={"AAPL": now})
    intent = OrderIntent(symbol="AAPL", side="BUY", qty=Decimal("1"), account="acc")
    with freeze_time(now + timedelta(seconds=3)):
        dec = evaluate_order(pol, st, intent)
        assert not dec.allowed and dec.reason == THROTTLED
    with freeze_time(now + timedelta(seconds=6)):
        dec = evaluate_order(pol, st, intent)
        assert dec.allowed
