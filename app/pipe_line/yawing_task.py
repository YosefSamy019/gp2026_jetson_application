from mcal import logs
import app.pipe_line.signals as signals
import models.yawing as yawing
import time
import app.pipe_line.timing as timing
import app.look_up_keys as look_up_keys
from scheduler.task import Task


class YawingTask(Task):
    def __init__(self):
        super().__init__(
            name='YawingTask',
            periodicity=timing.YAWING_TASK_SLEEP_TIME
        )

    def start(self):
        self.yawing_class = None

    def update(self):
        temp_vector = signals.driver_detector_queue.get()["face_points_flattened"]

        if temp_vector is not None:
            with signals.cpu_ml_lock:
                # Call it every 100ms with the latest face vector.
                prediction = yawing.yawing_model(temp_vector)

            yawing_flag = (prediction >= 0.6)
            self.yawing_class = ["Normal", "Yawning"][int(yawing_flag)]

            signals.yawing_queue.put(
                {"class": self.yawing_class, "prob": prediction,
                 })

        if self.yawing_class == "Yawning":
            signals.speaker_queue.put(look_up_keys.KEY_DRIVER_DROWSY)
