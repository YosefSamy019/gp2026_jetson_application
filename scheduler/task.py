import math
import time
from abc import ABC, abstractmethod
from collections import deque

from mcal import logs


class Task(ABC):
    def __init__(self, name: str, periodicity: float):
        self.name = name
        self.periodicity = periodicity

        self._engine_last_call_time = None
        self._engine_deltas_calls = deque(
            maxlen=math.ceil(5 / self.periodicity))  # Store statistics over last 5 seconds

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError

    def engine(self):
        try:
            self.start()
        except Exception as e:
            logs.add_log(f"Task: {self.name}, Error: {e}", logs.LogLevel.ERROR)

        while True:
            self._engine_ticker()

            try:
                self.update()
            except Exception as e:
                logs.add_log(f"Task: {self.name}, Error: {e}", logs.LogLevel.ERROR)

            # time.sleep(self.periodicity)
            time.sleep(
                max(
                    0,
                    self.periodicity - (time.time() - self._engine_last_call_time)
                )
            )

    def _engine_ticker(self):
        if self._engine_last_call_time is None:
            self._engine_last_call_time = time.time()
        else:
            _cur_delta = time.time() - self._engine_last_call_time
            self._engine_last_call_time = time.time()
            self._engine_deltas_calls.append(_cur_delta)

    def get_avg_periodicity(self) -> float:
        if len(self._engine_deltas_calls) > 0:
            return sum(self._engine_deltas_calls) / len(self._engine_deltas_calls)
        else:
            return 0
