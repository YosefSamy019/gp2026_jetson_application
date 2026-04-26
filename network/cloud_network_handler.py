import time
from typing import List

from app.pipe_line import timing
from app.pipe_line import signals
from mcal import logs
from mcal import wifi
from network.models.models import MCUNetworkDataModel
from scheduler import scheduler
from scheduler.task import Task


# Code
def init():
    scheduler.register_task(CloudNetworkSessionTask(
        name='CloudNetworkSessionTask',
        periodicity=timing.CLOUD_NETWORK_TASK_SLEEP_TIME
    ))


class CloudNetworkSessionTask(Task):

    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

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
        mcu_data: List[MCUNetworkDataModel] = signals.mcu_network_queue.pop_all()
        current_timestamp = self.get_current_time_function()

        # call wifi endpoints
