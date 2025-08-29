from __future__ import annotations

import asyncio

from apps.md_gateway.src.ws_client import simulated_ticks


async def collect_ticks(seed: int):
    ticks = []
    async for t in simulated_ticks(["TCS"], seed=seed, seconds=None, realtime=False):
        ticks.append((t.instrument, float(t.last_price), t.qty))
        if len(ticks) >= 5:
            break
    return ticks


def test_simulated_ticks_deterministic():
    t1 = asyncio.run(collect_ticks(42))
    t2 = asyncio.run(collect_ticks(42))
    assert t1 == t2
