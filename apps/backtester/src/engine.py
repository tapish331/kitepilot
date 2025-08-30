from __future__ import annotations

from kitepilot_risk import AccountState, OrderIntent, Policy, Decision, evaluate_order


def simulate_order(policy: Policy, state: AccountState, intent: OrderIntent) -> Decision:
    """Evaluate an order before simulation."""
    decision = evaluate_order(policy, state, intent)
    if not decision.allowed:
        return decision
    # In a full implementation, fills would be simulated here.
    return decision
