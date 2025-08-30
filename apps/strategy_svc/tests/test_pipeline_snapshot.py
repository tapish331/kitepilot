from __future__ import annotations

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[3]))

from apps.strategy_svc.src import ensemble, loader


def _load_fixture() -> list[ensemble.Bar]:
    path = Path(__file__).parent / "fixtures" / "bars_fixture.jsonl"
    return ensemble.load_bars(path)


def test_pipeline_snapshot() -> None:
    bars = _load_fixture()
    strat = loader.load_strategy("sma_crossover", short_window=3, long_window=5)
    intents = ensemble.run(strat, bars)
    snapshot = [intent.model_dump(mode="json") for intent in intents]
    assert snapshot == [
        {
            "symbol": "AAPL",
            "side": "BUY",
            "qty": 1,
            "price": None,
            "ts": "2020-01-01T00:04:00Z",
            "reason": "strategy-svc",
        },
        {
            "symbol": "AAPL",
            "side": "SELL",
            "qty": 1,
            "price": None,
            "ts": "2020-01-01T00:06:00Z",
            "reason": "strategy-svc",
        },
    ]


def test_pipeline_emits_stdout(capsys) -> None:
    bars = _load_fixture()
    strat = loader.load_strategy("sma_crossover", short_window=3, long_window=5)
    ensemble.run(strat, bars)
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == [
        '{"symbol":"AAPL","side":"BUY","qty":1,"price":null,"ts":"2020-01-01T00:04:00Z","reason":"strategy-svc"}',
        '{"symbol":"AAPL","side":"SELL","qty":1,"price":null,"ts":"2020-01-01T00:06:00Z","reason":"strategy-svc"}',
    ]
