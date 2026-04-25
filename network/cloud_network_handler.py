import time
from app.pipe_line import timing
from app.pipe_line import signals
from mcal import logs
from mcal import wifi
from scheduler import scheduler
from scheduler.task import Task


# Code
def init():
    scheduler.create_task(CloudNetworkSessionTask())


class CloudNetworkSessionTask(Task):
    def __init__(self):
        super().__init__(
            name='CloudNetworkSessionTask',
            periodicity=timing.CLOUD_NETWORK_TASK_SLEEP_TIME
        )

    def start(self):
        self.get_current_time_function = lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        self.device_id: int = 1  # Dont change forever

        self.btn_status: bool = False

        self.location_long: float = 0.0
        self.location_lat: float = 0.0

        self.flame_sensor: bool = False
        self.temperature: float = 0.0

        self.rotation_x: float = 0.0
        self.rotation_y: float = 0.0
        self.rotation_z: float = 0.0

    def update(self):
        # get data from sensors
        mcu_data = signals.mcu_network_queue.get()

        current_timestamp = self.get_current_time_function()

        self.rotation_x = mcu_data.get("rotation_x", None)
        self.rotation_y = mcu_data.get("rotation_y", None)
        self.rotation_z = mcu_data.get("rotation_z", None)

        self.location_long = mcu_data.get("location_long", None)
        self.location_lat = mcu_data.get("location_lat", None)

        self.flame_sensor = mcu_data.get("flame_sensor", None)
        self.temperature = mcu_data.get("temperature", None)
        self.btn_status = mcu_data.get("btn_status", None)

        # call wifi endpoints
