# strategy-kit

Reusable strategy interfaces, models, and utilities for Kitepilot.

## Quickstart

```bash
pip install -e packages/strategy-kit
```

```python
from strategy_kit.strategies.sma_crossover import SmaCrossoverStrategy
from strategy_kit.examples.sma_crossover_runner import generate_bars

strategy = SmaCrossoverStrategy(short_window=3, long_window=5)
for bar in generate_bars():
    for signal in strategy.on_bar(bar):
        print(signal)
```
