import time
import re
from app.pipe_line import timing
from mcal import logs
from scheduler import scheduler
from mcal.serial_comm import read_buffer
import app.pipe_line.signals as signals


# Code
def init():
    scheduler.create_task(mcu_network_session_task, "mcu_network_session_task")


def mcu_network_session_task():
    global_t_val = 0
    global_f_val = 0
    global_a_val = 0
    global_last_receive_time = time.time()
    global_slave_active = False
    trip_state_counter = 1

    current_buffer = ""

    gen = read_buffer()

    while True:
        try:
            # Read Buffer
            character = next(gen)
            if character:
                current_buffer += character
                current_buffer = current_buffer.strip()
                global_last_receive_time = time.time()

            # Check the buffer
            if len(current_buffer) > 0 and current_buffer[-1] == "[":
                # Bad Data
                current_buffer = ""

            # Decompose the buffer
            if len(current_buffer) > 0 and current_buffer[-1] == "]":
                decomposed_values = _decompose_buffer(current_buffer)
                current_buffer = ""
                global_t_val = decomposed_values.get("T", global_t_val)
                global_f_val = decomposed_values.get("F", global_f_val)
                global_a_val = decomposed_values.get("A", global_a_val)

            # Slave Active
            global_slave_active = (time.time() - global_last_receive_time) < 1.0
            if not global_slave_active:
                logs.add_log(f"network_session_task: Receiver is not responding", logs.LogLevel.ERROR)

            # Send data to queue
            signals.mcu_network_queue.put(
                {
                    "T": global_t_val,
                    "F": global_f_val,
                    "A": global_a_val,
                    "buffer": current_buffer,
                    "last_receive_time": global_last_receive_time,
                    "time_gone_from_last_receive": time.time() - global_last_receive_time,
                    "slave_active": global_slave_active,
                }
            )

            signals.trip_status_queue.put(trip_state_counter)
            trip_state_counter += 1

        except Exception as e:
            logs.add_log(f"mcu_network_session_task: error {e}", logs.LogLevel.ERROR)

        time.sleep(timing.MCU_NETWORK_TASK_SLEEP_TIME)


def _decompose_buffer(txt: str):
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
