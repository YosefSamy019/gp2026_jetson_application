from app.pipe_line.models.models import LensTaskOutput
from mcal import logs
import app.pipe_line.signals as signals
import time
import cv2
import app.pipe_line.timing as timing
import scheduler.scheduler as scheduler
from scheduler.task import Task


class LensSoftwareTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

    def update(self):
        camera_out = signals.camera_output_queue.get_last()

        if camera_out is None:
            return

        raw_img = camera_out.raw_img
        frame = cv2.flip(raw_img, 1)

        # todo missing [DIP]

        signals.lens_output_queue.put(
            LensTaskOutput(
                clean_img=frame
            )
        )
