"""FastAPI entrypoint for strategy service."""
from __future__ import annotations

import logging
import os

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from .loader import load_strategy

logger = logging.getLogger(__name__)

app = FastAPI()
strategy = None


@app.on_event("startup")
def startup() -> None:
    """Load strategy on service startup."""
    global strategy
    slug = os.getenv("STRATEGY_ID", "sma_crossover")
    short_window = int(os.getenv("SHORT_WINDOW", "3"))
    long_window = int(os.getenv("LONG_WINDOW", "5"))
    strategy = load_strategy(slug, short_window=short_window, long_window=long_window)
    logger.info("loaded strategy %s", slug)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    """Basic health check."""
    return {"status": "ok"}


@app.get("/metrics")
async def metrics() -> PlainTextResponse:
    """Expose Prometheus metrics."""
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
