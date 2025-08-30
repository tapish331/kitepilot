from __future__ import annotations
from fastapi import FastAPI
from broker_svc.router import router

app = FastAPI(title="Kitepilot Broker Service")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router)
