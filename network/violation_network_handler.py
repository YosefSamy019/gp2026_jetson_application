import time
from app.pipe_line import timing
from app.pipe_line import signals
from mcal import logs
from scheduler import scheduler
import mcal.wifi as wifi
from scheduler.task import Task


# Code
def init():
    scheduler.register_task(ViolationNetworkSession())


class ViolationNetworkSession(Task):
    def __init__(self):
        super().__init__(
            name='ViolationNetworkSession',
            periodicity=timing.VIOLATION_NETWORK_TASK_SLEEP_TIME
        )

    def start(self):
        self.violations_batch = []

    def update(self):
        # Read queue
        self.violations_batch.extend(signals.violations_queue.get_all())

        # Send
        if len(self.violations_batch) > 0:
            violation_sample = self.violations_batch.pop(0)

            # Send to server
            violation_class = violation_sample['class']
            violation_image = violation_sample['image']
            violation_time = violation_sample['time']

            logs.add_log(f"Violation Send: {violation_class}, {violation_time}", logs.LogLevel.WARNING)

            # TODO In case of failure, restore the sample
            if False:
                self.violations_batch.append(violation_sample)
