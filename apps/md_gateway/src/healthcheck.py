from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def write_health(path: Path, *, version: str) -> None:
    data = {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": version,
    }
    path.write_text(json.dumps(data))
