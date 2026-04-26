import time
import re
from app.pipe_line import timing
from mcal import logs
from network.models.models import MCUNetworkDataModel
from scheduler import scheduler
from mcal.serial_comm import read_buffer
import app.pipe_line.signals as signals
from scheduler.task import Task


# Code
def init():
    scheduler.register_task(MCUNetworkTask(
        name='MCUNetworkTask',
        periodicity=timing.MCU_NETWORK_TASK_SLEEP_TIME
    ))


class MCUNetworkTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

        self.global_t_val = 0
        self.global_f_val = 0
        self.global_a_val = 0
        self.global_last_receive_time = time.time()
        self.global_slave_active = False
        self.trip_state_counter = 1

        self.current_buffer = ""

        self.gen = read_buffer()

    def update(self):
        # Read Buffer
        character = next(self.gen)
        if character:
            self.current_buffer += character
            self.current_buffer = self.current_buffer.strip()
            self.global_last_receive_time = time.time()

        # Check the buffer
        if len(self.current_buffer) > 0 and self.current_buffer[-1] == "[":
            # Bad Data
            self.current_buffer = ""

        # Decompose the buffer
        if len(self.current_buffer) > 0 and self.current_buffer[-1] == "]":
            decomposed_values = self._decompose_buffer(self.current_buffer)
            self.current_buffer = ""
            self.global_t_val = decomposed_values.get("T", self.global_t_val)
            self.global_f_val = decomposed_values.get("F", self.global_f_val)
            self.global_a_val = decomposed_values.get("A", self.global_a_val)

        # Slave Active
        self.global_slave_active = (time.time() - self.global_last_receive_time) < 1.0
        if not self.global_slave_active:
            logs.add_log(f"network_session_task: Receiver is not responding", logs.LogLevel.ERROR)

        # Send data to queue
        signals.mcu_network_queue.put(
            MCUNetworkDataModel(
                T=self.global_t_val,
                F=self.global_f_val,
                A=self.global_a_val,
                buffer=self.current_buffer,
                last_receive_time=self.global_last_receive_time,
                time_gone_from_last_receive=time.time() - self.global_last_receive_time,
                slave_active=self.global_slave_active,
            )
        )

        signals.trip_status_queue.put(self.trip_state_counter)
        self.trip_state_counter += 1

    def _decompose_buffer(self, txt: str):
        txt = txt.upper()

        t_val = re.findall(r"T:(\d+)", txt)
        f_val = re.findall(r"F:(\d+)", txt)
        a_val = re.findall(r"A:(\d+)", txt)

        data = {}
        if t_val:
            data["T"] = t_val[0]

        if f_val:
            data["F"] = f_val[0]

        if a_val:
            data["A"] = a_val[0]

        return data
