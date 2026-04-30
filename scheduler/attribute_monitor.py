import threading
import time
from collections import deque
from typing import Deque, Generic, TypeVar, List, Optional

T = TypeVar("T")


class AttributeMonitor(Generic[T]):
    def __init__(
            self,
            attribute_name: str,
    ):
        self.attribute_name = attribute_name
        self._time_for_repeat = time.time()
        self._last_value = None

    def update(self, item: T):
        if self.attribute_name in item.__dict__:
            cur_value = getattr(item, self.attribute_name)
            if self._last_value != cur_value:
                self._last_value = cur_value
                self._time_for_repeat = time.time()
        else:
            self._last_value = None
            self._time_for_repeat = None

    def get_seconds(self) -> Optional[float]:
        if self._time_for_repeat:
            return time.time() - self._time_for_repeat
        return None

    def get_last_value(self) -> Optional[T]:
        return self._last_value
