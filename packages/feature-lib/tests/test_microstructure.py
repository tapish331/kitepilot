import pandas as pd
from kitepilot_features.microstructure import quote_imbalance


def test_quote_imbalance():
    df = pd.DataFrame(
        {
            "bid_size": [100, 200, 150],
            "ask_size": [200, 100, 150],
        }
    )
    res = quote_imbalance(df)
    expected = (df["ask_size"] - df["bid_size"]) / (df["ask_size"] + df["bid_size"])
    assert res["feat.ob_imbalance"].equals(expected)
