import datetime
import io
import random

import cv2
import numpy as np
import requests
from PIL import Image, ImageTk

from app.pipe_line.models.models import FaceClipperRecognizerTaskOutput
from mcal import logs
from mcal import runtime_cache
import app.pipe_line.signals as signals
from scheduler.task import Task


class FaceClipperRecognizerTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

        self.driver_last_candidate_id = None

        self.should_detect_driver = True
        self.pad_ratio = 0.3
        self.up_shift_ratio = 0.15

    def update(self):
        driver_tracker_out = signals.driver_tracker_queue.get_last()

        driver_has_changed = driver_tracker_out is None or driver_tracker_out.driver_candidate_id != self.driver_last_candidate_id

        if driver_has_changed:
            self.should_detect_driver = True
            self.driver_last_candidate_id = driver_tracker_out.driver_candidate_id

            signals.face_clipper_recognizer_queue.put(
                FaceClipperRecognizerTaskOutput(
                    driver_id=None,
                    driver_name=None,
                    driver_age=None,
                    driver_image_url=None,
                )
            )

        if self.should_detect_driver:
            self._detect_driver()

    def _detect_driver(self):
        is_front_get_seconds, is_front_get_last_val = signals.head_pose_queue.monitor_attribute('is_front')
        driver_detector_out = signals.driver_detector_queue.get_last()

        if driver_detector_out is None:
            return

        if is_front_get_seconds > 2 and is_front_get_last_val == True:
            # get the face region and get face region
            original_frame = driver_detector_out.img
            original_mask = driver_detector_out.face_points_flattened

            if original_mask is not None:
                clipped_face = self._get_clipped_face(
                    original_mask=original_mask,
                    original_frame=original_frame
                )

                driver_id, driver_name, driver_age, driver_image_url = self._call_face_recognition_model(clipped_face)

                signals.face_clipper_recognizer_queue.put(
                    FaceClipperRecognizerTaskOutput(
                        driver_id=driver_id,
                        driver_name=driver_name,
                        driver_age=driver_age,
                        driver_image_url=driver_image_url,
                    )
                )

                self._load_driver_img(driver_image_url)

                cv2.imwrite(f"snapshot/d_{driver_id}.png", cv2.cvtColor(clipped_face, cv2.COLOR_RGB2BGR))

                self.should_detect_driver = False

    def _get_clipped_face(self, original_mask, original_frame):
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

        shift_y = int(self.up_shift_ratio * (y_max - y_min))
        y_min = max(0, y_min - shift_y)
        y_max = max(0, y_max - shift_y)

        x_min, y_min, x_max, y_max = self._react_to_square(x_min, y_min, x_max, y_max)

        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(w, x_max)
        y_max = min(h, y_max)

        clipped_face = original_frame[y_min:y_max, x_min:x_max]
        clipped_face = cv2.resize(clipped_face, (160, 160))

        return clipped_face

    def _load_driver_img(self, img_url):
        try:
            if not runtime_cache.has_key(img_url):
                response = requests.get(img_url)
                image_data = Image.open(io.BytesIO(response.content))
                image_data = image_data.resize((240, 240))
                runtime_cache.set_value(img_url, image_data)
        except Exception as e:
            logs.add_log('Could not load driver image', logs.LogLevel.ERROR)

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

    def _call_face_recognition_model(self, clipped_face):
        driver_id = random.randint(0, 1000)
        driver_name = 'Yosef Samy'
        driver_age = 23
        driver_image_url = r"https://statcdn.fandango.com/MPX/image/NBCU_Fandango/938/171/BabyDriver_OS_OG.jpg"

        return driver_id, driver_name, driver_age, driver_image_url
