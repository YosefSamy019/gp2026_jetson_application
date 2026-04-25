from mcal import logs
import app.pipe_line.signals as signals
import time
import cv2
import app.pipe_line.timing as timing
import scheduler.scheduler as scheduler
from scheduler.task import Task


class LensSoftwareTask(Task):
    def __init__(self):
        super().__init__(
            name='LensSoftwareTask',
            periodicity=timing.LENS_TASK_SLEEP_TIME
        )

    def start(self):
        pass

    def update(self):
        raw_img = signals.camera_output_queue.get()["raw_img"]
        if raw_img is not None:
            frame = cv2.flip(raw_img, 1)

            # todo missing [DIP]

            signals.lens_output_queue.put({
                "raw_img": raw_img,
                "processed_img": frame,
            })
