import threading
import time
from collections import deque
from typing import Deque, Generic, TypeVar, List, Optional, Any, Tuple

from scheduler.attribute_monitor import AttributeMonitor

T = TypeVar("T")


class ItemsQueue(Generic[T]):
    def __init__(self,
                 name: str,
                 max_n_items: Optional[int] = 100,
                 attribute_monitors: List[AttributeMonitor[T]] = None
                 ):

        self._name = name
        self._lock = threading.Lock()
        self._items_queue: Deque[T] = deque(maxlen=max_n_items)
        self.max_n_items = max_n_items

        self._attribute_monitors_dict = {x.attribute_name: x for x in
                                         attribute_monitors} if attribute_monitors else {}

    def get_name(self) -> str:
        return self._name

    def put(self, item: T) -> None:
        with self._lock:
            for k, v in self._attribute_monitors_dict.items():
                v.update(item)

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

    def monitor_attribute(self, attribute_name: str) -> Tuple[Optional[float], Any]:
        if attribute_name not in self._attribute_monitors_dict:
            raise AttributeError(f"Attribute {attribute_name} not found in {T}.")

        with self._lock:
            get_seconds = self._attribute_monitors_dict[attribute_name].get_seconds()
            get_last_val = self._attribute_monitors_dict[attribute_name].get_last_value()
            return get_seconds, get_last_val
