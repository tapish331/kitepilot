from __future__ import annotations
from datetime import datetime, timezone
from kitepilot_common import ist_utc_pair


def test_ist_utc_pair_converts_and_is_aware():
    naive = datetime(2024, 1, 1, 0, 0, 0)  # assume UTC if naive
    ist, utc = ist_utc_pair(naive)
    assert ist.tzinfo is not None and utc.tzinfo is not None
    assert utc.tzinfo is timezone.utc
