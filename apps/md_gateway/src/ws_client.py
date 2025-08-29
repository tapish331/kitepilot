from __future__ import annotations

import asyncio
import random
from datetime import datetime, timezone
from decimal import Decimal
from typing import AsyncIterator, Iterable, List

from kitepilot_common import Tick


async def simulated_ticks(
    symbols: Iterable[str], *, seed: int, seconds: int | None = None, realtime: bool = True
) -> AsyncIterator[Tick]:
    """Deterministic synthetic tick stream."""
    rng = random.Random(seed)  # nosec B311 - non-crypto PRNG used for deterministic simulation
    prices = {s: Decimal(100 + i * 10) for i, s in enumerate(symbols)}
    start = asyncio.get_event_loop().time()
    symbols_list: List[str] = list(symbols)
    while True:
        if seconds is not None and asyncio.get_event_loop().time() - start > seconds:
            return
        symbol = rng.choice(symbols_list)
        price = prices[symbol] + Decimal(rng.normalvariate(0, 0.5))
        prices[symbol] = price
        qty = rng.randint(1, 10)
        yield Tick(
            ts_utc=datetime.now(timezone.utc),
            instrument=symbol,
            last_price=price,
            bid=None,
            ask=None,
            qty=qty,
        )
        if realtime:
            await asyncio.sleep(1 / rng.uniform(5, 20))
