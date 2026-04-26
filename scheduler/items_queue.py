import threading
from collections import deque
from typing import Deque, Generic, TypeVar, List, Optional

T = TypeVar("T")


class ItemsQueue(Generic[T]):
    def __init__(self, name: str, max_n_items: Optional[int] = 100):
        self._name = name
        self._lock = threading.Lock()
        self._items_queue: Deque[T] = deque(maxlen=max_n_items)

    def get_name(self) -> str:
        return self._name

    def put(self, item: T) -> None:
        with self._lock:
            self._items_queue.append(item)

    def get_last(self) -> Optional[T]:
        with self._lock:
            if self._items_queue:
                return self._items_queue[-1]
            return None

    def pop_all(self) -> List[T]:
        with self._lock:
            if not self._items_queue:
                return []
            items = list(self._items_queue)
            self._items_queue.clear()
            return items

    def __len__(self) -> int:
        with self._lock:
            return len(self._items_queue)
