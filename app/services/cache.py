from typing import Any, Dict, Optional
from app.utils.hashing import stable_hash


class InMemoryCache:
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def make_key(self, template_id: str, user_input: str, parameters: Dict[str, Any]) -> str:
        return stable_hash(
            {
                "template_id": template_id,
                "input": user_input,
                "parameters": parameters or {},
            }
        )

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        return self._store.get(key)

    def set(self, key: str, value: Dict[str, Any]) -> None:
        self._store[key] = value

    def size(self) -> int:
        return len(self._store)


cache = InMemoryCache()
