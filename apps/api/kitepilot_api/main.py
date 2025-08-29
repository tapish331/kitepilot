import logging

from fastapi import FastAPI

from .config import PACKAGE_VERSION, get_settings
from .routers import health

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    s = get_settings()
    docs_url = "/docs" if s.DOCS_ENABLED else None
    redoc_url = "/redoc" if s.DOCS_ENABLED else None
    openapi_url = "/openapi.json" if s.DOCS_ENABLED else None

    app = FastAPI(
        title=s.APP_NAME,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
    )
    app.include_router(health.router)

    logger.info("Starting %s v%s [env=%s]", s.APP_NAME, PACKAGE_VERSION, s.ENV)

    return app


app = create_app()
