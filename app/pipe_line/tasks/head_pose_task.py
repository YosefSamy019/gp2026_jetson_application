from app.pipe_line.models.models import HeadPoseTaskOutput
from scheduler.scheduler import *
import app.pipe_line.signals as signals
import models.head_pose as head_pose


class HeadPoseTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

    def update(self):
        driver_detector_out = signals.driver_detector_queue.get_last()

        if driver_detector_out is None or driver_detector_out.face_points_flattened is None:
            signals.head_pose_queue.put(
                HeadPoseTaskOutput(
                    is_front=None,
                    is_right=None,
                    is_left=None,
                    probability=None,
                    is_head_detected=False
                )
            )

            return

        cur_class, cur_prop = head_pose.head_pose_model(driver_detector_out.face_points_flattened)

        signals.head_pose_queue.put(
            HeadPoseTaskOutput(
                is_front=cur_class == 'front',
                is_right=cur_class == 'right',
                is_left=cur_class == 'left',
                probability=cur_prop,
                is_head_detected=True
            )
        )
