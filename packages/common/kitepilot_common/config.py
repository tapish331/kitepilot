from __future__ import annotations
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field
from .errors import ConfigError


class Settings(BaseModel):
    env: Literal["dev", "staging", "prod"] = "dev"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    timezone: str = "UTC"
    app_name: str = "kitepilot"
    version: str = "0.1.0"
    database_url: Optional[str] = Field(default=None, description="Optional DB URL for consumers")


def schema_json() -> dict[str, Any]:
    """Return the JSON Schema dict that should be published for config."""
    return Settings.model_json_schema()


def load_settings(data: dict[str, Any] | None = None) -> Settings:
    try:
        return Settings(**(data or {}))
    except Exception as exc:  # pragma: no cover
        raise ConfigError(str(exc))
