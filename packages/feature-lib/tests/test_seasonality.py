import numpy as np
import pandas as pd
from kitepilot_features.seasonality import seasonality


def test_seasonality_encodings():
    ts = pd.to_datetime(["2024-01-01 00:00:00", "2024-01-02 12:00:00"], utc=True)
    df = pd.DataFrame({"ts": ts})
    res = seasonality(df)
    dow = ts.dayofweek
    tod_sec = ts.hour * 3600 + ts.minute * 60 + ts.second
    dow_rad = 2 * np.pi * dow / 7
    tod_rad = 2 * np.pi * tod_sec / (24 * 3600)
    expected = pd.DataFrame(
        {
            "feat.dow_sin": np.sin(dow_rad),
            "feat.dow_cos": np.cos(dow_rad),
            "feat.tod_sin": np.sin(tod_rad),
            "feat.tod_cos": np.cos(tod_rad),
        }
    )
    pd.testing.assert_frame_equal(res, expected)
