from __future__ import annotations

import os
from threading import Lock
from typing import Optional

from kitepilot_risk import Policy


class PolicyStore:
    """In-memory policy store with optional mutation protection."""

    def __init__(self, initial: Optional[Policy] = None) -> None:
        self._policy = initial or Policy()
        self._lock = Lock()
        self.allow_mutations = os.getenv("RISK_ALLOW_POLICY_MUTATIONS", "0") == "1"

    def get(self) -> Policy:
        with self._lock:
            return self._policy

    def set(self, new_policy: Policy) -> None:
        if not self.allow_mutations:
            raise PermissionError("policy mutations disabled")
        with self._lock:
            self._policy = new_policy
