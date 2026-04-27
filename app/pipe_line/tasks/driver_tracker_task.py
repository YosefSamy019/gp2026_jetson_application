from app.pipe_line.models.models import DriverTrackerTaskOutput
import app.pipe_line.signals as signals
import numpy as np
from scheduler.task import Task


class DriverTrackerTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

        self.last_x = None
        self.last_y = None
        self.fake_id = 0

    def update(self):
        driver_detector_out = signals.driver_detector_queue.get_last()

        if driver_detector_out is None:
            self.fake_id += 1
        else:
            cur_frame_x = driver_detector_out.face_points_matrix[
                :, 0] if driver_detector_out.face_points_matrix is not None else None

            cur_frame_y = driver_detector_out.face_points_matrix[
                :, 1] if driver_detector_out.face_points_matrix is not None else None

            if self.last_x is not None and cur_frame_x is not None:
                last_pivot_x = np.mean(self.last_x)
                last_pivot_y = np.mean(self.last_y)

                cur_pivot_x = np.mean(cur_frame_x)
                cur_pivot_y = np.mean(cur_frame_y)

                dis = np.sqrt((cur_pivot_x - last_pivot_x) ** 2 + (cur_pivot_y - last_pivot_y) ** 2)

                # Todo Adjust the threshold
                if dis > 0.15:
                    self.fake_id += 1

            else:
                self.fake_id += 1

            self.last_x = cur_frame_x
            self.last_y = cur_frame_y

        signals.driver_tracker_queue.put(DriverTrackerTaskOutput(
            driver_candidate_id=self.fake_id
        ))
