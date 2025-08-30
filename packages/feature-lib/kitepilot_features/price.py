"""Price based features such as returns and VWAP z-score."""

from __future__ import annotations

from typing import Sequence

import pandas as pd


def rolling_returns(df: pd.DataFrame, horizons: Sequence[int]) -> pd.DataFrame:
    """Compute rolling returns for given horizons.

    Args:
        df: DataFrame with column ``close``.
        horizons: Iterable of horizon lengths in rows.

    Returns:
        DataFrame with columns ``feat.ret_{h}s`` for each horizon ``h``.
    """

    if "close" not in df:
        raise ValueError("close column required for returns computation")
    out = pd.DataFrame(index=df.index)
    close = df["close"]
    for h in horizons:
        out[f"feat.ret_{h}s"] = close.pct_change(h)
    return out


def vwap_zscore(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Compute VWAP z-score of close relative to VWAP."""

    if {"close", "vwap"} - set(df.columns):
        raise ValueError("close and vwap columns required for vwap_zscore")
    diff = df["close"] - df["vwap"]
    mean = diff.rolling(window).mean()
    std = diff.rolling(window).std(ddof=0)
    z = (diff - mean) / std
    return pd.DataFrame({"feat.vwap_z": z})
