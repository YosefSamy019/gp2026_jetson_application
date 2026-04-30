from app.pipe_line.models.models import YawingTaskOutput
from mcal import logs
import app.pipe_line.signals as signals
import models.yawing as yawing
import time
import app.pipe_line.timing as timing
from constants import look_up_keys
from scheduler.task import Task


class YawingTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

    def update(self):
        driver_detector_out = signals.driver_detector_queue.get_last()

        if driver_detector_out is None or driver_detector_out.face_points_flattened is None:
            signals.yawing_queue.put(
                YawingTaskOutput(
                    is_yawing=None,
                    is_yawing_probability=None,
                    is_yawning_detected=False
                )
            )
            return

        temp_vector = driver_detector_out.face_points_flattened

        # Call it every 100ms with the latest face vector.
        prediction = yawing.yawing_model(temp_vector)

        is_yawing = prediction >= 0.6

        signals.yawing_queue.put(
            YawingTaskOutput(
                is_yawing=is_yawing,
                is_yawing_probability=prediction,
                is_yawning_detected=True
            )
        )
