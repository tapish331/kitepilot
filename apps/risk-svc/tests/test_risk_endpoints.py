from __future__ import annotations

import json
import os
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from fastapi.testclient import TestClient
from freezegun import freeze_time
from kitepilot_risk import OrderIntent, Policy
from kitepilot_risk.policy import Lists, Throttle
from risk_svc.main import create_app


def test_allow_and_banlist():
    os.environ["RISK_ALLOW_POLICY_MUTATIONS"] = "1"
    c = TestClient(create_app())
    intent = OrderIntent(symbol="AAPL", side="BUY", qty=Decimal("1"), account="acc")
    resp = c.post("/risk/evaluate", json=json.loads(intent.model_dump_json()))
    assert resp.json()["allowed"] is True
    # banlist update
    pol = Policy(lists=Lists(instrument_banlist={"AAPL"}))
    c.post("/risk/policy", json=json.loads(pol.model_dump_json()))
    resp = c.post("/risk/evaluate", json=json.loads(intent.model_dump_json()))
    assert resp.json()["allowed"] is False


def test_kill_switch():
    os.environ["RISK_ALLOW_POLICY_MUTATIONS"] = "1"
    c = TestClient(create_app())
    c.post("/risk/kill", params={"active": True})
    intent = OrderIntent(symbol="AAPL", side="BUY", qty=Decimal("1"), account="acc")
    resp = c.post("/risk/evaluate", json=json.loads(intent.model_dump_json()))
    assert resp.json()["reason"] == "KILL_SWITCH"


def test_throttle_endpoint():
    os.environ["RISK_ALLOW_POLICY_MUTATIONS"] = "1"
    app = create_app()
    c = TestClient(app)
    now = datetime(2024, 1, 1, 12, 0, tzinfo=UTC)
    pol = Policy(throttle=Throttle(min_seconds_between_orders=Decimal("5")))
    c.post("/risk/policy", json=json.loads(pol.model_dump_json()))
    intent = OrderIntent(symbol="AAPL", side="BUY", qty=Decimal("1"), account="acc")
    with freeze_time(now):
        c.post("/risk/evaluate", json=json.loads(intent.model_dump_json()))
    with freeze_time(now + timedelta(seconds=2)):
        resp = c.post("/risk/evaluate", json=json.loads(intent.model_dump_json()))
        assert resp.json()["reason"] == "THROTTLED"
    with freeze_time(now + timedelta(seconds=6)):
        resp = c.post("/risk/evaluate", json=json.loads(intent.model_dump_json()))
        assert resp.json()["allowed"] is True
