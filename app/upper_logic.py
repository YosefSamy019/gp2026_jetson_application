import json
from typing import List

import customtkinter as ctk
import mcal.logs as logs
import mcal.cache as cache
import scheduler.scheduler as scheduler
import app.pipe_line.pipeline as pipeline
import app.pipe_line.signals as signals
from mcal.logs import LogDataClass

# Some vars
variable_logs: ctk.StringVar = None
variable_logs_filter: ctk.IntVar = None
variable_scheduler: ctk.StringVar = None
variable_network: ctk.StringVar = None
variable_cache: ctk.StringVar = None
variable_driver: ctk.StringVar = None


def upper_awake(root: ctk.CTk):
    global variable_logs, variable_scheduler, variable_network, variable_cache, variable_logs_filter, variable_driver

    variable_logs = ctk.StringVar(value='Init ...', name='logs')
    variable_logs_filter = ctk.IntVar(value=0, name='logs_filter')
    variable_scheduler = ctk.StringVar(value='Init ...', name='scheduler')
    variable_network = ctk.StringVar(value='Init ...', name='network')
    variable_cache = ctk.StringVar(value='Init ...', name='cache')
    variable_driver = ctk.StringVar(value='Init ...', name='driver')

    pipeline.pipeline_init()

    _upper_ui_task(root)


def _upper_ui_task(root: ctk.CTk):
    _upper_ui_task_update_logs()
    root.after(100, func=lambda: _upper_ui_task(root))


def _upper_ui_task_update_logs():
    global variable_logs_filter
    # Read Logs and filter them
    logs_list: List[LogDataClass] = logs.get_logs(variable_logs_filter.get())
    variable_logs.set("\n".join(map(str, logs_list)))

    # Read cache
    variable_cache.set(str(json.dumps(cache.get_report())))

    # Read Scheduler
    variable_scheduler.set(str(json.dumps(scheduler.get_report())))

    # Read Network
    variable_network.set(str(json.dumps(signals.mcu_network_queue.get_immediate(fallback_value={}))))

    # Driver
    variable_driver.set(str(json.dumps(signals.face_clipper_recognizer_queue.get_immediate(fallback_value={}))))
