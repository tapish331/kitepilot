"""Strategy loader utilities."""
from __future__ import annotations

import importlib

from strategy_kit.interfaces import Strategy  # type: ignore[import-untyped]
from strategy_kit.registry import get_strategy  # type: ignore[import-untyped]


def load_strategy(slug: str, **kwargs) -> Strategy:
    """Instantiate a strategy registered under *slug* with given kwargs."""
    try:
        cls = get_strategy(slug)
    except KeyError:
        importlib.import_module(f"strategy_kit.strategies.{slug}")
        cls = get_strategy(slug)
    return cls(**kwargs)
