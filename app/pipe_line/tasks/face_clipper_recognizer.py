import io

import cv2
import numpy as np
import requests
from PIL import Image, ImageTk

from app.pipe_line.models.models import FaceClipperRecognizerTaskOutput
from mcal import logs
from mcal import runtime_cache
import app.pipe_line.signals as signals
import time
import app.pipe_line.timing as timing
from scheduler.task import Task


class FaceClipperRecognizerTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

        self.driver_last_candidate_id = None

        self.counter = 0
        self.driver_id = None
        self.pad_ratio = 0.35

    def update(self):
        driver_tracker_out = signals.driver_tracker_queue.get_last()

        driver_has_changed = driver_tracker_out is None or driver_tracker_out.driver_candidate_id != self.driver_last_candidate_id

        if driver_has_changed:
            self.driver_id = None
            self.driver_last_candidate_id = driver_tracker_out.driver_candidate_id

            signals.face_clipper_recognizer_queue.put(
                FaceClipperRecognizerTaskOutput(
                    driver_id=None,
                    driver_name=None,
                    driver_age=None,
                    driver_image_url=None,
                )
            )

        if self.driver_id is None:
            self._detect_driver()

    def _detect_driver(self):
        head_pose_out = signals.head_pose_queue.get_last()
        driver_detector_out = signals.driver_detector_queue.get_last()

        if head_pose_out is None or driver_detector_out is None:
            return

        if head_pose_out.is_front:
            # get the face region and get face region
            original_frame = driver_detector_out.img
            original_mask = driver_detector_out.face_points_flattened

            if original_mask is not None:
                h, w, _ = original_frame.shape
                x = original_mask[0::2]
                y = original_mask[1::2]

                x_min = int(np.min(x) * w)
                y_min = int(np.min(y) * h)
                x_max = int(np.max(x) * w)
                y_max = int(np.max(y) * h)

                pad_x = int(self.pad_ratio * (x_max - x_min))
                pad_y = int(self.pad_ratio * (y_max - y_min))

                x_min = max(0, x_min - pad_x)
                y_min = max(0, y_min - pad_y)
                x_max = min(w, x_max + pad_x)
                y_max = min(h, y_max + pad_y)

                x_min, y_min, x_max, y_max = self._react_to_square(x_min, y_min, x_max, y_max)

                x_min = max(0, x_min)
                y_min = max(0, y_min)
                x_max = min(w, x_max)
                y_max = min(h, y_max)

                clipped_face = original_frame[y_min:y_max, x_min:x_max]
                clipped_face = cv2.resize(clipped_face, (160, 160))

                cv2.imwrite(f"snapshot/d_{self.counter}.png", cv2.cvtColor(clipped_face, cv2.COLOR_RGB2BGR))

                # TODO Call model to get new id

                self.counter += 1
                self.driver_id = self.counter

                image_url = r"https://statcdn.fandango.com/MPX/image/NBCU_Fandango/938/171/BabyDriver_OS_OG.jpg"
                if not runtime_cache.has_key(image_url):
                    response = requests.get(image_url)
                    image_data = Image.open(io.BytesIO(response.content))
                    image_data = image_data.resize((240, 240))
                    runtime_cache.set_value(image_url, image_data)

                signals.face_clipper_recognizer_queue.put(
                    FaceClipperRecognizerTaskOutput(
                        driver_id=self.driver_id,
                        driver_name='Yosef Samy',
                        driver_age=23,
                        driver_image_url=image_url,
                    )
                )

    def _react_to_square(self, x_min, y_min, x_max, y_max):
        width = x_max - x_min
        height = y_max - y_min

        # find the difference
        diff = abs(width - height)

        if width > height:
            # height is smaller → expand y
            y_min -= diff // 2
            y_max += diff - diff // 2
        else:
            # width is smaller → expand x
            x_min -= diff // 2
            x_max += diff - diff // 2

        return x_min, y_min, x_max, y_max
