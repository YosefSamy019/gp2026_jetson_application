import threading
import time


class SingleItemQueue:
    def __init__(self, is_volatile: bool = True):
        self._lock = threading.Lock()
        self._item = None
        self._has_item = False
        self._is_volatile = is_volatile

    def put(self, item):
        with self._lock:
            self._item = item
            self._has_item = True

    def get(self):
        """Return current item, or Wait if nothing yet."""
        while True:
            with self._lock:
                if self._has_item:
                    item = self._item
                    if self._is_volatile:
                        self._has_item = False
                        self._item = None
                    return item

            time.sleep(1 / 30)

    def get_immediate(self, fallback_value=None):
        with self._lock:
            if self._has_item:
                if self._is_volatile:
                    self._has_item = False
                    self._item = None

                return self._item
            else:
                return fallback_value

    def len(self):
        with self._lock:
            return 1 if self._has_item else 0
