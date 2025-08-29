from functools import lru_cache
from importlib import metadata

from pydantic_settings import BaseSettings, SettingsConfigDict

try:
    PACKAGE_VERSION = metadata.version("kitepilot-api")
except metadata.PackageNotFoundError:  # pragma: no cover - version not installed
    PACKAGE_VERSION = "0.0.0"


class Settings(BaseSettings):
    ENV: str = "dev"
    APP_NAME: str = "KitePilot API"
    DOCS_ENABLED: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
