from enum import Enum
from typing import List, Optional


class LogLevel(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3

    def to_str(self):
        return ["None", "Info", "WARNING", "ERROR"][int(self.value)]


class LogDataClass:
    def __init__(self, msg: str, level: LogLevel):
        self.msg = msg
        self.level = level
        self.repeat = 1

    def __str__(self):
        return f"{self.repeat:03d} * {self.level.to_str().center(10)}: {self.msg}"


_runtime_logs: List[LogDataClass] = []


def add_log(msg: str, level: LogLevel):
    new_log = LogDataClass(msg, level)

    for log_i in _runtime_logs:
        if log_i.level.value == level.value and str(log_i.msg).strip().lower() == str(msg).strip().lower():
            log_i.repeat = log_i.repeat + 1
            return

    _runtime_logs.append(new_log)
    print(level.to_str(), msg)


def get_logs(filter_lvl_int: Optional[int]) -> List[LogDataClass]:
    all_logs: List[LogDataClass] = _runtime_logs.copy()

    if filter_lvl_int and filter_lvl_int > 0:
        filtered_logs = list(filter(lambda x: x.level.value == filter_lvl_int, all_logs))
        return filtered_logs
    else:
        return all_logs


def clear_logs():
    _runtime_logs.clear()


def get_count() -> dict:
    count_dict = dict()

    for log in _runtime_logs:
        count_dict[log.level.value] = count_dict.get(log.level.value, 0) + log.repeat

    return count_dict
