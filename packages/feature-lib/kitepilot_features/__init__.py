"""Feature computation library for Kitepilot.

Public API exposes :func:`compute_features` and :class:`FeatureConfig`.
"""

from .config import FeatureConfig
from .compute import compute_features

__all__ = ["compute_features", "FeatureConfig"]
