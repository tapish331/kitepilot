"""Seasonality encodings for time of day and day of week."""

from __future__ import annotations

import numpy as np
import pandas as pd


SECONDS_PER_DAY = 24 * 60 * 60


def seasonality(df: pd.DataFrame) -> pd.DataFrame:
    """Compute sine/cosine encodings for day-of-week and time-of-day."""

    if "ts" not in df:
        raise ValueError("ts column required for seasonality features")
    ts = pd.to_datetime(df["ts"], utc=True)
    dow = ts.dt.dayofweek
    tod_seconds = ts.dt.hour * 3600 + ts.dt.minute * 60 + ts.dt.second
    dow_rad = 2 * np.pi * dow / 7
    tod_rad = 2 * np.pi * tod_seconds / SECONDS_PER_DAY
    return pd.DataFrame(
        {
            "feat.dow_sin": np.sin(dow_rad),
            "feat.dow_cos": np.cos(dow_rad),
            "feat.tod_sin": np.sin(tod_rad),
            "feat.tod_cos": np.cos(tod_rad),
        }
    )
