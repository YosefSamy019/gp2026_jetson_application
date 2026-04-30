from app.pipe_line.models.models import DriverDetectorTaskOutput
from constants import look_up_keys
from mcal import logs
import app.pipe_line.signals as signals
import time
import app.pipe_line.timing as timing
from scheduler.task import Task


class DriverDetectorTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

    def start(self):
        pass

    def update(self):
        face_extractor_out = signals.face_extractor_queue.get_last()

        if face_extractor_out is None:
            return

        signals.driver_detector_queue.put(
            DriverDetectorTaskOutput(
                img=face_extractor_out.img,
                face_found=face_extractor_out.face_found,
                face_points_matrix=face_extractor_out.face_points_matrix,
                face_points_flattened=face_extractor_out.face_points_flattened,
                raw_land_marks=face_extractor_out.raw_land_marks
            )
        )
