import time
from app.pipe_line import timing
from app.pipe_line import signals
from mcal import logs
from mcal import wifi
from scheduler import scheduler


# Code
def init():
    scheduler.create_task(cloud_network_session_task, "cloud_network_session_task")


def cloud_network_session_task():
    get_current_time_function = lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    device_id: int = 1  # Dont change forever

    btn_status: bool = False

    location_long: float = 0.0
    location_lat: float = 0.0

    flame_sensor: bool = False
    temperature: float = 0.0

    rotation_x: float = 0.0
    rotation_y: float = 0.0
    rotation_z: float = 0.0

    while True:
        try:
            # get data from sensors
            mcu_data = signals.mcu_network_queue.get()

            current_timestamp = get_current_time_function()

            rotation_x = mcu_data.get("rotation_x", None)
            rotation_y = mcu_data.get("rotation_y", None)
            rotation_z = mcu_data.get("rotation_z", None)

            location_long = mcu_data.get("location_long", None)
            location_lat = mcu_data.get("location_lat", None)

            flame_sensor = mcu_data.get("flame_sensor", None)
            temperature = mcu_data.get("temperature", None)
            btn_status = mcu_data.get("btn_status", None)

            # call wifi endpoints

        except Exception as e:
            logs.add_log(f"cloud_network_session_task: error {e}", logs.LogLevel.ERROR)

        time.sleep(timing.CLOUD_NETWORK_TASK_SLEEP_TIME)
