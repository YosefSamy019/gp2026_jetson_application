import threading
import time
from typing import List

from scheduler.many_items_queue import ManyItemsQueue
from scheduler.single_item_queue import SingleItemQueue
from scheduler.task import Task

# CODE
_tasks_list: List[Task] = []
_locks_list = []
_queue_list = []


def create_lock(name):
    global _locks_list

    if name not in list(map(lambda t: t[0], _locks_list)):
        lock = threading.Lock()
        _locks_list.append((name, lock))
        return lock
    else:
        return None


def create_queue(name, is_volatile: bool):
    global _queue_list

    if name not in list(map(lambda t: t[0], _queue_list)):
        q = SingleItemQueue(is_volatile)
        _queue_list.append((name, q))
        return q
    else:
        return None


def create_list_queue(name):
    global _queue_list

    if name not in list(map(lambda t: t[0], _queue_list)):
        q = ManyItemsQueue()
        _queue_list.append((name, q))
        return q
    else:
        return None


def create_task(task: Task):
    global _tasks_list

    task_thread = threading.Thread(target=lambda: task.engine(), daemon=True, name=task.name)
    _tasks_list.append(task)
    task_thread.start()


def get_report():
    return_dict = dict()

    return_dict['tasks'] = [
        f"Task: {x.name}\n"
        f"\t-periodicity={x.get_avg_periodicity():0.3f}"
        for x in _tasks_list
    ]

    return_dict['locks'] = [
        f"Lock: {x[0]}\n"
        f"\t-state={x[1].locked()}"
        for x in _locks_list
    ]

    return_dict['queues'] = [
        f"Queue: {x[0]}\n"
        f"\t-content_len={x[1].len()}"
        for x in _queue_list
    ]

    return return_dict
