import pandas as pd
from kitepilot_features.volatility import ewm_volatility, realized_volatility


def test_realized_volatility():
    df = pd.DataFrame({"close": [1, 1.1, 1.2, 1.3, 1.4]})
    res = realized_volatility(df, window=3)
    returns = df["close"].pct_change()
    expected = returns.rolling(3).std(ddof=0)
    assert res["feat.vol_rolling"].equals(expected)


def test_ewm_volatility():
    df = pd.DataFrame({"close": [1, 1.1, 1.2, 1.3, 1.4]})
    res = ewm_volatility(df, span=2)
    returns = df["close"].pct_change()
    expected = returns.ewm(span=2, adjust=False).std(bias=False)
    assert res["feat.vol_ewm"].equals(expected)
