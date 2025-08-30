import pandas as pd
from kitepilot_features.price import rolling_returns, vwap_zscore


def test_rolling_returns_parity():
    df = pd.DataFrame({"close": [1.0, 1.1, 1.21, 1.331]})
    res = rolling_returns(df, [1, 2])
    expected1 = df["close"].pct_change(1)
    expected2 = df["close"].pct_change(2)
    assert res["feat.ret_1s"].equals(expected1)
    assert res["feat.ret_2s"].equals(expected2)


def test_vwap_zscore():
    df = pd.DataFrame(
        {
            "close": [10, 11, 12, 13, 14],
            "vwap": [10, 10.5, 11.5, 12.5, 13.5],
        }
    )
    res = vwap_zscore(df, window=3)
    diff = df["close"] - df["vwap"]
    mean = diff.rolling(3).mean()
    std = diff.rolling(3).std(ddof=0)
    expected = (diff - mean) / std
    assert res["feat.vwap_z"].equals(expected)
