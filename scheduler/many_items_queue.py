import threading


class ManyItemsQueue:
    def __init__(self):
        self._lock = threading.Lock()
        self._items = list()

    def put(self, item):
        with self._lock:
            self._items.append(item)

    def get_all(self):
        with self._lock:
            if len(self._items) > 0:
                ret_val = self._items
                self._items = list()
                return ret_val
            else:
                return []

    def len(self):
        with self._lock:
            return len(self._items)
