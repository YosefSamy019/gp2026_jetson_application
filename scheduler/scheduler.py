import threading
from typing import List, TypeVar

from scheduler.task import Task
from scheduler.items_queue import ItemsQueue

# CODE
_tasks_list: List[Task] = []
_locks_list = []
_queue_list: List[ItemsQueue] = []


def create_lock(name):
    global _locks_list

    if name not in list(map(lambda t: t[0], _locks_list)):
        lock = threading.Lock()
        _locks_list.append((name, lock))
        return lock
    else:
        return None


T = TypeVar("T")


def register_queue(item_queue: ItemsQueue[T]) -> ItemsQueue[T]:
    global _queue_list

    _queue_list.append(item_queue)
    return item_queue


def register_task(task: Task):
    global _tasks_list

    task_thread = threading.Thread(target=lambda: task.engine(), daemon=True, name=task.name)
    _tasks_list.append(task)
    task_thread.start()


def get_report():
    return_dict = dict()

    return_dict['tasks'] = [
        f"Task: {x.name}\n"
        f"\t-periodicity={x.get_avg_periodicity():0.3f}#{x.get_exact_periodicity():0.3f}"
        for x in _tasks_list
    ]

    return_dict['locks'] = [
        f"Lock: {x[0]}\n"
        f"\t-state={x[1].locked()}"
        for x in _locks_list
    ]

    return_dict['queues'] = [
        f"Queue: {x.get_name()}\n"
        f"\t-length={len(x)}#{x.max_n_items}"
        for x in _queue_list
    ]

    return return_dict
