from app.pipe_line.models.models import HeadPoseTaskOutput
from mcal import logs
from scheduler.scheduler import *
import app.pipe_line.signals as signals
import models.head_pose as head_pose
import time
import app.pipe_line.timing as timing
import app.look_up_keys as look_up_keys


class HeadPoseTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

        self.head_pose_start = None
        self.DISTRACTED_THRESHOLD_SECONDS = 3

    def update(self):
        driver_detector_out = signals.driver_detector_queue.get_last()

        if driver_detector_out is None or driver_detector_out.face_points_flattened is None:
            return

        temp_vector = driver_detector_out.face_points_flattened
        cur_class, cur_prop = head_pose.head_pose_model(temp_vector)

        signals.head_pose_queue.put(
            HeadPoseTaskOutput(
                is_front=cur_class == 'front',
                is_right=cur_class == 'right',
                is_left=cur_class == 'left',
                probability=cur_prop,
            )
        )

        if cur_class != "front":
            if self.head_pose_start is None:
                self.head_pose_start = time.time()
            elif time.time() - self.head_pose_start >= self.DISTRACTED_THRESHOLD_SECONDS:

                signals.speaker_queue.put(look_up_keys.KEY_DRIVER_DISTRACTED)
        else:
            self.head_pose_start = None
