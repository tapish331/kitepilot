from __future__ import annotations

from importlib import import_module
from typing import Dict, Type

from .interfaces import Strategy

_REGISTRY: Dict[str, Type[Strategy] | str] = {}


def register_strategy(slug: str, target: Type[Strategy] | str) -> None:
    """Register a strategy class or import path under *slug*."""

    _REGISTRY[slug] = target


def get_strategy(slug: str) -> Type[Strategy]:
    """Return the strategy class registered under *slug*.

    Supports lazy loading when an import path string was registered.
    """

    target = _REGISTRY.get(slug)
    if target is None:
        raise KeyError(f"strategy '{slug}' not found")
    if isinstance(target, str):
        module_name, class_name = target.rsplit(".", 1)
        module = import_module(module_name)
        cls = getattr(module, class_name)
        if not issubclass(cls, Strategy):  # pragma: no cover - defensive programming
            raise TypeError(f"{cls!r} is not a Strategy")
        _REGISTRY[slug] = cls
        return cls
    return target
