import math
import random

import cv2
import numpy as np

from app.pages.camera.components.base_component import OverlayComponent
from app.ui_constants import RGBColor, UI_CAMERA_DELAY


class SnackBarComponent(OverlayComponent):
    def __init__(self):
        self._init_x = -10
        self._cur_x = self._init_x
        self._delta_x = math.floor(UI_CAMERA_DELAY * 200) + 1

        self._all_display_texts = [
            "Eyes on me, AI sets you free.",
            "Wake up Doc, the road is a shock!",
            "The road is a traitor, don't meet your creator.",
            "Don't judge the face, the code was a chase.",
            "He who owns the Source, fears no force.",
            "Heavy load, long road, final code.",
            "Focus on the track, I've got your back.",
            "Safety first, before the bubble burst."
        ]
        self._cur_display_text = random.choice(self._all_display_texts)

    def process_frame(self, frame: np.ndarray, **params) -> np.ndarray:
        h, w, _ = frame.shape

        y = h - 10
        self._cur_x += self._delta_x

        if self._cur_x > w:
            self._cur_display_text = random.choice(self._all_display_texts)
            self._cur_x = self._init_x * len(self._cur_display_text)

        cv2.rectangle(frame,
                      (0, h - 30),
                      (w, h),
                      RGBColor.GRAY_DARK.value,
                      -1)

        cv2.putText(frame,
                    self._cur_display_text,
                    (self._cur_x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    RGBColor.WHITE.value,
                    2)

        return frame
