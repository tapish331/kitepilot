from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from kitepilot_common import __version__

from .aggregator import Aggregator
from .ws_client import simulated_ticks
from .healthcheck import write_health


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="md-gateway simulated runner")
    p.add_argument("--mode", choices=["sim"], default="sim")
    p.add_argument("--symbols", type=str, required=True)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--seconds", type=int, default=60)
    return p


async def run_sim(symbols: list[str], seed: int, seconds: int) -> None:
    artifacts = Path(".artifacts/md-gateway")
    artifacts.mkdir(parents=True, exist_ok=True)
    out_file = artifacts / "bars.ndjson"
    f = out_file.open("w")

    def sink(bar) -> None:
        line = bar.model_dump_json()
        print(line)
        f.write(line + "\n")

    agg = Aggregator(on_bar_1s=sink, on_bar_1m=None)
    async for tick in simulated_ticks(symbols, seed=seed, seconds=seconds):
        agg.ingest(tick)
    agg.flush()
    f.close()
    write_health(artifacts / "health.json", version=__version__)


def main() -> None:
    args = build_arg_parser().parse_args()
    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    asyncio.run(run_sim(symbols, seed=args.seed, seconds=args.seconds))


if __name__ == "__main__":
    main()
