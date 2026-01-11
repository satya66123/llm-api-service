import hashlib
import json
from typing import Any, Dict


def stable_hash(payload: Dict[str, Any]) -> str:
    """
    Stable hashing for cache keys.
    Ensures dict ordering is consistent.
    """
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
