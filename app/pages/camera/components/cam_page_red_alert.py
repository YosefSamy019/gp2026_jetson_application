import math
import time

import cv2
import numpy as np

from app.pages.camera.components.base_component import OverlayComponent
from app.pipe_line import signals
from app.ui_constants import RGBColor


class RedAlertComponent(OverlayComponent):
    def __init__(self):
        self._start_time = time.time()
        self._sin_scale = math.pi
        self._color = np.array(RGBColor.RED.value, np.uint8)
        self._alpha_max_val = 0.3

    def process_frame(self, frame: np.ndarray, **params) -> np.ndarray:
        head_pose_task_out = signals.head_pose_queue.get_last()

        if head_pose_task_out is not None and not head_pose_task_out.is_front:
            angle = (time.time() - self._start_time) * self._sin_scale
            sin_out = math.sin(angle)
            alpha = (0.5 * sin_out + 0.5) * self._alpha_max_val

            frame[:, :] = (frame[:, :] * (1 - alpha) + alpha * self._color).astype(int)

        return frame
