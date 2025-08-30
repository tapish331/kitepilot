# kitepilot-features

Reusable feature computation library for Kitepilot.

## Usage

```python
import pandas as pd
from kitepilot_features import compute_features, FeatureConfig

bars = pd.DataFrame({
    "ts": pd.date_range("2024-01-01", periods=5, freq="S", tz="UTC"),
    "symbol": ["A"] * 5,
    "open": [1,2,3,4,5],
    "high": [1,2,3,4,5],
    "low": [1,2,3,4,5],
    "close": [1,2,3,4,5],
    "volume": [100]*5,
    "vwap": [1,2,3,4,5],
})

features = compute_features(bars, config=FeatureConfig(return_horizons=(1,)))
print(features.head())
```
