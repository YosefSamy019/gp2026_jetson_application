import threading
from collections import deque
from typing import Deque, Dict, Any, List, Optional


class ItemsQueue:
    def __init__(self, name: str, max_n_items: Optional[int] = 50):
        self._name = name
        self._lock = threading.Lock()
        self._items_queue: Deque[Dict[str, Any]] = deque(maxlen=max_n_items)

    def get_name(self) -> str:
        return self._name

    def put(self, item: Dict[str, Any]):
        with self._lock:
            self._items_queue.append(item)

    def get_last(self) -> Optional[Dict[str, Any]]:
        with self._lock:
            if self._items_queue:
                return self._items_queue[-1]
            return None

    def pop_all(self) -> List[Dict[str, Any]]:
        with self._lock:
            if not self._items_queue:
                return []
            items = list(self._items_queue)
            self._items_queue.clear()
            return items

    def get_attributes(self, *keys):
        with self._lock:
            if not self._items_queue:
                return [None] * len(keys)

            last_val = self._items_queue[-1]
            return [last_val.get(k) for k in keys]

    def __len__(self):
        with self._lock:
            return len(self._items_queue)
