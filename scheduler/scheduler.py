import threading

from scheduler.many_items_queue import ManyItemsQueue
from scheduler.single_item_queue import SingleItemQueue

# CODE
_tasks_list = []
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


def create_task(fun_code, task_name):
    global _tasks_list

    # remove dead tasks
    _tasks_list = list(filter(lambda t: t.is_alive(), _tasks_list))

    # check if the task is repeated
    if task_name not in list(map(lambda x: x.name, _tasks_list)):
        # create a task
        task = threading.Thread(target=fun_code, daemon=True, name=task_name)

        _tasks_list.append(task)
        task.start()

        return 1
    else:
        return 0


def get_report():
    return_dict = dict()

    return_dict['tasks'] = [
        f"Task: {x.name}"
        for x in _tasks_list
    ]

    return_dict['locks'] = [
        f"Lock: {x[0]}; State: {x[1].locked()}"
        for x in _locks_list
    ]

    return_dict['queues'] = [
        f"Queue: {x[0]}; Content:{x[1].len()}"
        for x in _queue_list
    ]

    return return_dict
