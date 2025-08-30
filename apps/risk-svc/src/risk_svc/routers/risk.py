from __future__ import annotations

from fastapi import APIRouter, HTTPException

from kitepilot_risk import OrderIntent, Policy, evaluate_order

from ..policy_store import PolicyStore
from ..state_provider import StateProvider


def get_router(store: PolicyStore, state: StateProvider) -> APIRouter:
    router = APIRouter()

    @router.post("/evaluate")
    def evaluate(intent: OrderIntent):
        policy = store.get()
        snapshot = state.snapshot()
        decision = evaluate_order(policy, snapshot, intent)
        if decision.allowed:
            state.record(intent)
        return decision

    @router.get("/policy")
    def get_policy() -> Policy:
        return store.get()

    @router.post("/policy")
    def set_policy(policy: Policy):
        try:
            store.set(policy)
        except PermissionError as exc:
            raise HTTPException(status_code=403, detail=str(exc))
        return {"status": "ok"}

    @router.post("/kill")
    def toggle_kill(active: bool):
        policy = store.get()
        policy.toggles.kill_switch = active
        return {"kill_switch": policy.toggles.kill_switch}

    @router.get("/status")
    def status():
        return state.snapshot()

    return router
