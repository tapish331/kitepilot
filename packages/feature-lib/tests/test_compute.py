import pandas as pd
from kitepilot_features import FeatureConfig, compute_features


def _sample_bars():
    ts = pd.date_range("2024-01-01", periods=5, freq="S", tz="UTC")
    return pd.DataFrame(
        {
            "ts": ts,
            "symbol": ["A"] * 5,
            "open": [10, 10.1, 10.2, 10.3, 10.4],
            "high": [10, 10.2, 10.3, 10.4, 10.5],
            "low": [10, 10.0, 10.1, 10.2, 10.3],
            "close": [10, 10.1, 10.2, 10.3, 10.4],
            "volume": [100] * 5,
            "vwap": [10, 10.05, 10.15, 10.25, 10.35],
        }
    )


def _sample_quotes():
    ts = pd.date_range("2024-01-01", periods=5, freq="S", tz="UTC")
    return pd.DataFrame(
        {
            "ts": ts,
            "symbol": ["A"] * 5,
            "bid_size": [100, 110, 120, 130, 140],
            "ask_size": [90, 95, 100, 105, 110],
        }
    )


def test_compute_features_columns():
    bars = _sample_bars()
    quotes = _sample_quotes()
    cfg = FeatureConfig(return_horizons=(1,))
    res = compute_features(bars, quotes_df=quotes, config=cfg)
    expected_cols = {
        "feat.ret_1s",
        "feat.vwap_z",
        "feat.vol_rolling",
        "feat.vol_ewm",
        "feat.dow_sin",
        "feat.dow_cos",
        "feat.tod_sin",
        "feat.tod_cos",
        "feat.ob_imbalance",
    }
    assert set(res.columns) == expected_cols


def test_compute_features_perf():
    bars = pd.concat([_sample_bars() for _ in range(2000)], ignore_index=True)
    bars["symbol"] = ["A"] * len(bars)
    quotes = pd.concat([_sample_quotes() for _ in range(2000)], ignore_index=True)
    quotes["symbol"] = ["A"] * len(quotes)
    start = pd.Timestamp.utcnow()
    res = compute_features(bars, quotes_df=quotes)
    duration = (pd.Timestamp.utcnow() - start).total_seconds()
    per_bar = duration / len(bars)
    assert per_bar < 0.01
    assert not res.isna().all().any()
