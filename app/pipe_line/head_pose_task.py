from mcal import logs
from scheduler.scheduler import *
import app.pipe_line.signals as signals
import models.head_pose as head_pose
import time
import app.pipe_line.timing as timing
import app.look_up_keys as look_up_keys

class HeadPoseTask(Task):
    def __init__(self):
        super().__init__(
            name='HeadPoseTask',
            periodicity=timing.HEAD_POSE_TASK_SLEEP_TIME
        )

    def start(self):
        self.head_pose_start = None
        self.DISTRACTED_THRESHOLD_SECONDS = 3

    def update(self):
        temp_vector = signals.driver_detector_queue.get()["face_points_flattened"]

        if temp_vector is not None:
            cur_class, cur_prop = head_pose.head_pose_model(temp_vector)

            signals.head_pose_queue.put(
                {"class": cur_class,
                 "prob": cur_prop,
                 # TODO : will we pass head danger delta time ?!
                 })

            if cur_class != "front":
                if self.head_pose_start is None:
                    self.head_pose_start = time.time()
                elif time.time() - self.head_pose_start >= self.DISTRACTED_THRESHOLD_SECONDS:

                    signals.speaker_queue.put(look_up_keys.KEY_DRIVER_DISTRACTED)
            else:
                self.head_pose_start = None



