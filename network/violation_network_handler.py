import os
import time
from typing import List

import cv2

from app.pipe_line import timing
from app.pipe_line import signals
from mcal import logs
from network.models.models import ViolationDataModel
from scheduler import scheduler
import mcal.wifi as wifi
from scheduler.task import Task
import app.pipe_line.signals as signal


# Code
def init():
    scheduler.register_task(ViolationNetworkSession(
        name='ViolationNetworkSession',
        periodicity=timing.VIOLATION_NETWORK_TASK_SLEEP_TIME
    ))


class ViolationNetworkSession(Task):
    PATH = 'violations'

    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

        self.unready_violations_batch: List[ViolationDataModel] = []
        self.ready_violations_batch: List[ViolationDataModel] = []

        os.makedirs(self.PATH, exist_ok=True)

    def update(self):
        # Read queue
        self.unready_violations_batch.extend(signals.violations_queue.pop_all())

        # Fill null images
        self._fill_null_images()

        # Send to server
        self._send_violation()

    def _fill_null_images(self):
        if len(self.unready_violations_batch) > 0:
            face_extractor_out = signal.face_extractor_queue.get_last()
            if face_extractor_out is not None:
                image = face_extractor_out.img

                for i in range(len(self.unready_violations_batch)):
                    self.unready_violations_batch[i].image = image

                self._move_to_ready()

    def _move_to_ready(self):
        if len(self.unready_violations_batch) > 0:
            self.ready_violations_batch.extend(self.unready_violations_batch)
            self.unready_violations_batch.clear()
            self._delete_repeated_violations()

    def _delete_repeated_violations(self):
        i = 0
        while i < len(self.ready_violations_batch):
            j = i + 1
            while j < len(self.ready_violations_batch):
                if self.ready_violations_batch[j].violation_type == self.ready_violations_batch[i].violation_type:
                    self.ready_violations_batch.pop(j)
                    j = j
                else:
                    j += 1

            i += 1

    def _send_violation(self):
        if len(self.ready_violations_batch) == 0:
            return

        violation_sample = self.ready_violations_batch.pop(0)

        logs.add_log(
            f"Violation Send: {violation_sample.violation_type}",
            logs.LogLevel.WARNING
        )

        cv2.imwrite(
            os.path.join(
                self.PATH,
                f'{violation_sample.violation_type}.png'
            ),
            cv2.cvtColor(violation_sample.image, cv2.COLOR_RGB2BGR)
        )
