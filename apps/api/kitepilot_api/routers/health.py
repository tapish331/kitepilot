from fastapi import APIRouter

from ..config import PACKAGE_VERSION, get_settings

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/status")
def status() -> dict[str, str]:
    s = get_settings()
    return {"env": s.ENV, "app": s.APP_NAME, "version": PACKAGE_VERSION}
