from __future__ import annotations

from fastapi import FastAPI

from .policy_store import PolicyStore
from .state_provider import StateProvider
from .routers.risk import get_router


def create_app() -> FastAPI:
    store = PolicyStore()
    state = StateProvider()
    app = FastAPI()
    app.include_router(get_router(store, state), prefix="/risk")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
