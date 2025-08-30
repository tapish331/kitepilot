"""Microstructure features derived from quotes/order book."""

from __future__ import annotations

import pandas as pd


def quote_imbalance(df: pd.DataFrame) -> pd.DataFrame:
    """Compute simple bid/ask size imbalance.

    Args:
        df: DataFrame with ``bid_size`` and ``ask_size`` columns.

    Returns:
        DataFrame with ``feat.ob_imbalance`` column.
    """

    required = {"bid_size", "ask_size"}
    if missing := required - set(df.columns):
        raise ValueError(f"missing columns for quote imbalance: {missing}")
    denom = df["ask_size"] + df["bid_size"]
    imbalance = (df["ask_size"] - df["bid_size"]) / denom.replace(0, pd.NA)
    return pd.DataFrame({"feat.ob_imbalance": imbalance})
