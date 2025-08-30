"""Configuration for feature computation."""

from dataclasses import dataclass, field
from typing import Sequence


@dataclass(slots=True)
class FeatureConfig:
    """Configuration for :func:`compute_features`.

    Attributes:
        return_horizons: Sequence of horizons (in rows) for simple returns.
        vol_window: Rolling window for standard deviation of returns.
        vol_ewm_span: Span for exponentially weighted volatility.
        vwap_window: Rolling window for VWAP z-score.
    """

    return_horizons: Sequence[int] = field(default_factory=lambda: (1,))
    vol_window: int = 30
    vol_ewm_span: int = 30
    vwap_window: int = 30
