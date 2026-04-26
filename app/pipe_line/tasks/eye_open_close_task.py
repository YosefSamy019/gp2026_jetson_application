from app.pipe_line.models.models import EyeOpenCloseTaskOutput
from mcal import logs
from scheduler.scheduler import *
import app.pipe_line.signals as signals
import models.eye as eye
import time
import app.pipe_line.timing as timing
import app.look_up_keys as look_up_keys


class EyeOpenCloseTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

        self.eye_closed_start = None
        self.DROWSY_THRESHOLD_SECONDS = 2
        self.eye_flag = 0

    def update(self):
        driver_detector_out = signals.driver_detector_queue.get_last()

        if driver_detector_out is None or driver_detector_out.face_points_flattened is None:
            return

        temp_vector = driver_detector_out.face_points_flattened

        ear_avg = eye.eye_model(temp_vector)

        # eye is close when (EAR < 0.25)
        eye_flag = (ear_avg < 0.25)

        signals.eye_open_close_queue.put(
            EyeOpenCloseTaskOutput(
                ear_avg=ear_avg,
                is_eye_open=not eye_flag,
                is_eye_close=eye_flag
            )
        )

        if self.eye_flag:
            if self.eye_closed_start is None:
                self.eye_closed_start = time.time()
            elif time.time() - self.eye_closed_start >= self.DROWSY_THRESHOLD_SECONDS:
                signals.speaker_queue.put(look_up_keys.KEY_DRIVER_DROWSY)
        else:
            self.eye_closed_start = None
