"""Volatility features."""

from __future__ import annotations

import pandas as pd


def realized_volatility(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Rolling standard deviation of simple returns."""

    if "close" not in df:
        raise ValueError("close column required for volatility")
    returns = df["close"].pct_change()
    vol = returns.rolling(window).std(ddof=0)
    return pd.DataFrame({"feat.vol_rolling": vol})


def ewm_volatility(df: pd.DataFrame, span: int) -> pd.DataFrame:
    """Exponentially weighted volatility of returns."""

    if "close" not in df:
        raise ValueError("close column required for volatility")
    returns = df["close"].pct_change()
    vol = returns.ewm(span=span, adjust=False).std(bias=False)
    return pd.DataFrame({"feat.vol_ewm": vol})
