from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from strategy_kit.models import OrderSignal


def test_runner_smoke(tmp_path) -> None:
    script = (
        Path(__file__).parents[2] / "src" / "strategy_kit" / "examples" / "sma_crossover_runner.py"
    )
    proc = subprocess.run([sys.executable, str(script)], capture_output=True, check=True, text=True)
    lines = [json.loads(line) for line in proc.stdout.strip().splitlines() if line.strip()]
    assert lines  # at least one signal
    for line in lines:
        OrderSignal.model_validate(line)
