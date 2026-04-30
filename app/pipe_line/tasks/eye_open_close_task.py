from app.pipe_line.models.models import EyeOpenCloseTaskOutput
from constants import look_up_keys
from scheduler.scheduler import *
import app.pipe_line.signals as signals
import models.eye as eye
import time


class EyeOpenCloseTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

    def update(self):
        driver_detector_out = signals.driver_detector_queue.get_last()

        if driver_detector_out is None or driver_detector_out.face_points_flattened is None:
            signals.eye_open_close_queue.put(
                EyeOpenCloseTaskOutput(
                    ear_avg=None,
                    is_eye_open=None,
                    is_eye_close=None,
                    is_eye_detected=False,
                )
            )
            return

        temp_vector = driver_detector_out.face_points_flattened

        ear_avg = eye.eye_model(temp_vector)

        eye_flag = (ear_avg < 0.25)

        signals.eye_open_close_queue.put(
            EyeOpenCloseTaskOutput(
                ear_avg=ear_avg,
                is_eye_open=not eye_flag,
                is_eye_close=eye_flag,
                is_eye_detected=True,
            )
        )
