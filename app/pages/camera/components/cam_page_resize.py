import cv2
import numpy as np

from app.pages.camera.components.base_component import OverlayComponent
import app.pipe_line.signals as signals
from app.ui_constants import RGBColor


class ResizeComponent(OverlayComponent):

    def process_frame(self, frame: np.ndarray, **params) -> np.ndarray:
        target_w, target_h = params['window_size']

        if target_w <= 1 or target_h <= 1:
            return frame

        h, w = frame.shape[:2]

        # Compute scale (keep aspect ratio)
        scale = min(target_w / w, target_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)

        # Resize image
        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # Create black canvas (letterbox)
        canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)

        # Center the image
        x_offset = (target_w - new_w) // 2
        y_offset = (target_h - new_h) // 2

        canvas[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized

        return canvas
