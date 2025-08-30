from __future__ import annotations

import io
import json
import runpy
from contextlib import redirect_stdout
from pathlib import Path

from strategy_kit.models import OrderSignal


def test_runner_smoke(tmp_path) -> None:
    script = (
        Path(__file__).parents[2] / "src" / "strategy_kit" / "examples" / "sma_crossover_runner.py"
    )
    buf = io.StringIO()
    with redirect_stdout(buf):
        # Execute the runner script in-process to avoid spawning a subprocess
        runpy.run_path(str(script), run_name="__main__")
    lines = [json.loads(line) for line in buf.getvalue().strip().splitlines() if line.strip()]
    assert lines  # at least one signal
    for line in lines:
        OrderSignal.model_validate(line)
