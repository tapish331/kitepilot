from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field

from .policy import Policy
from .reasons import (
    INSTRUMENT_BANNED,
    KILL_SWITCH,
    MAX_DAILY_LOSS,
    MAX_OPEN_POS,
    MAX_QTY_DAY,
    MAX_QTY_ORDER,
    MAX_TURNOVER_DAY,
    OPENING_BLOCK,
    THROTTLED,
)
from .types import AccountState, OrderIntent


class Decision(BaseModel):
    allowed: bool
    reason: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


# rule helpers

def _ok() -> tuple[bool, str | None, dict[str, Any]]:
    return True, None, {}


def rule_kill_switch(policy: Policy, state: AccountState, intent: OrderIntent):
    if policy.toggles.kill_switch:
        return False, KILL_SWITCH, {}
    return _ok()


def rule_banlist(policy: Policy, state: AccountState, intent: OrderIntent):
    if intent.symbol in policy.lists.instrument_banlist:
        return False, INSTRUMENT_BANNED, {"symbol": intent.symbol}
    return _ok()


def rule_opening_block(policy: Policy, state: AccountState, intent: OrderIntent):
    block = policy.toggles.opening_minutes_block
    if not block:
        return _ok()
    now = datetime.now(UTC)
    market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
    if now < market_open + timedelta(minutes=block):
        return False, OPENING_BLOCK, {"minutes": block}
    return _ok()


def rule_max_daily_loss(policy: Policy, state: AccountState, intent: OrderIntent):
    cap = policy.limits.max_daily_loss
    if cap is not None and state.pnl <= -cap:
        return False, MAX_DAILY_LOSS, {"pnl": str(state.pnl)}
    return _ok()


def rule_max_open_positions(policy: Policy, state: AccountState, intent: OrderIntent):
    cap = policy.limits.max_open_positions
    if cap is not None and state.open_positions >= cap:
        return False, MAX_OPEN_POS, {"open_positions": state.open_positions}
    return _ok()


def rule_max_qty_order(policy: Policy, state: AccountState, intent: OrderIntent):
    cap = policy.limits.max_qty_per_order
    if cap is not None and intent.qty > cap:
        return False, MAX_QTY_ORDER, {"qty": str(intent.qty), "cap": str(cap)}
    return _ok()


def rule_max_qty_day(policy: Policy, state: AccountState, intent: OrderIntent):
    cap = policy.limits.max_qty_per_symbol_day
    if cap is None:
        return _ok()
    current = state.qty_by_symbol.get(intent.symbol, Decimal("0"))
    if current + intent.qty > cap:
        return False, MAX_QTY_DAY, {"qty": str(current + intent.qty), "cap": str(cap)}
    return _ok()


def rule_max_turnover(policy: Policy, state: AccountState, intent: OrderIntent):
    cap = policy.limits.max_turnover_day
    if cap is None or intent.price is None:
        return _ok()
    turnover = state.turnover_by_symbol.get(intent.symbol, Decimal("0")) + intent.qty * intent.price
    if turnover > cap:
        return False, MAX_TURNOVER_DAY, {"turnover": str(turnover), "cap": str(cap)}
    return _ok()


def rule_throttle(policy: Policy, state: AccountState, intent: OrderIntent):
    window = policy.throttle.min_seconds_between_orders
    if window is None:
        return _ok()
    last = state.last_order_ts_by_symbol.get(intent.symbol)
    now = datetime.now(UTC)
    if last and (now - last).total_seconds() < float(window):
        return False, THROTTLED, {"wait": str(window)}
    return _ok()


RULES: list[
    Callable[[Policy, AccountState, OrderIntent], tuple[bool, str | None, dict[str, Any]]]
] = [
    rule_kill_switch,
    rule_banlist,
    rule_opening_block,
    rule_max_daily_loss,
    rule_max_open_positions,
    rule_max_qty_order,
    rule_max_qty_day,
    rule_max_turnover,
    rule_throttle,
]


def evaluate_order(policy: Policy, state: AccountState, intent: OrderIntent) -> Decision:
    for rule in RULES:
        ok, reason, details = rule(policy, state, intent)
        if not ok:
            return Decision(allowed=False, reason=reason, details=details)
    return Decision(allowed=True)
