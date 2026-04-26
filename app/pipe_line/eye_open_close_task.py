from mcal import logs
from scheduler.scheduler import *
import app.pipe_line.signals as signals
import models.eye as eye
import time
import app.pipe_line.timing as timing
import app.look_up_keys as look_up_keys


class EyeOpenCloseTask(Task):
    def __init__(self):
        super().__init__(
            name='EyeOpenCloseTask',
            periodicity=timing.EYE_OPEN_CLOSE_TASK_SLEEP_TIME
        )

    def start(self):
        self.eye_closed_start = None
        self.DROWSY_THRESHOLD_SECONDS = 2
        self.eye_flag = 0

    def update(self):
        temp_vector = signals.driver_detector_queue.get()["face_points_flattened"]

        if temp_vector is not None:
            ear_avg = eye.eye_model(temp_vector)

            # eye is close when (EAR < 0.25)
            eye_flag = (ear_avg < 0.25)

            signals.eye_open_close_queue.put({
                "class": "Closed" if eye_flag else "Open",
                "avg": ear_avg,
                # TODO : will we pass eye close delta time ?!
            })

        if self.eye_flag:
            if self.eye_closed_start is None:
                self.eye_closed_start = time.time()
            elif time.time() - self.eye_closed_start >= self.DROWSY_THRESHOLD_SECONDS:

                signals.speaker_queue.put(look_up_keys.KEY_DRIVER_DROWSY)
        else:
            self.eye_closed_start = None
