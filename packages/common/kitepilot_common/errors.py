class KitepilotError(Exception):
    """Base exception for Kitepilot libraries."""


class ConfigError(KitepilotError):
    """Configuration-related errors."""
