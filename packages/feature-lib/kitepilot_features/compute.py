"""Top-level feature computation entrypoint."""

from __future__ import annotations

from typing import Optional

import pandas as pd

from .config import FeatureConfig
from .microstructure import quote_imbalance
from .price import rolling_returns, vwap_zscore
from .seasonality import seasonality
from .volatility import ewm_volatility, realized_volatility


BAR_REQUIRED = {"ts", "symbol", "close"}


def _validate_columns(df: pd.DataFrame, required: set[str]) -> None:
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {missing}")


def compute_features(
    bars_df: pd.DataFrame,
    *,
    quotes_df: Optional[pd.DataFrame] = None,
    config: FeatureConfig = FeatureConfig(),
) -> pd.DataFrame:
    """Compute feature set for given bars and optional quotes.

    Args:
        bars_df: DataFrame with columns ``ts``, ``symbol``, ``close`` and optional ``vwap``.
        quotes_df: Optional DataFrame with ``ts``, ``symbol``, ``bid_size``, ``ask_size``.
        config: Feature configuration.

    Returns:
        DataFrame indexed by ``ts`` and ``symbol`` with ``feat.*`` columns.
    """

    _validate_columns(bars_df, BAR_REQUIRED)
    bars_df = bars_df.sort_values("ts")

    features: list[pd.DataFrame] = []
    for symbol, grp in bars_df.groupby("symbol"):
        grp = grp.reset_index(drop=True)
        feats = pd.concat(
            [
                rolling_returns(grp, config.return_horizons),
                (
                    vwap_zscore(grp, config.vwap_window)
                    if "vwap" in grp
                    else pd.DataFrame(index=grp.index)
                ),
                realized_volatility(grp, config.vol_window),
                ewm_volatility(grp, config.vol_ewm_span),
                seasonality(grp),
            ],
            axis=1,
        )
        feats.index = pd.MultiIndex.from_arrays(
            [grp["ts"], [symbol] * len(grp)], names=["ts", "symbol"]
        )
        features.append(feats)
    result = pd.concat(features).sort_index()

    if quotes_df is not None and not quotes_df.empty:
        _validate_columns(quotes_df, {"ts", "symbol", "bid_size", "ask_size"})
        q_features: list[pd.DataFrame] = []
        for symbol, qgrp in quotes_df.groupby("symbol"):
            qgrp = qgrp.sort_values("ts").reset_index(drop=True)
            q_feats = quote_imbalance(qgrp)
            q_feats.index = pd.MultiIndex.from_arrays(
                [qgrp["ts"], [symbol] * len(qgrp)], names=["ts", "symbol"]
            )
            q_features.append(q_feats)
        qdf = pd.concat(q_features).sort_index()
        result = result.join(qdf, how="left")
    return result
