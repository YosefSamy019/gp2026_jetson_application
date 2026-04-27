import cv2
import numpy as np

from app.pages.camera.components.base_component import OverlayComponent
import app.pipe_line.signals as signals
from app.ui_constants import RGBColor


class LowerLeftComponent(OverlayComponent):
    def process_frame(self, frame: np.ndarray, **params) -> np.ndarray:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        y_offset = 30
        line_gap = 35
        y_bottom_padding = 30

        texts_to_draw = []
        colors = []

        face_clipper_recognizer_task_out = signals.face_clipper_recognizer_queue.get_last()
        if face_clipper_recognizer_task_out is not None:
            if face_clipper_recognizer_task_out.driver_id is not None:
                texts_to_draw.append(f"Driver ID: {face_clipper_recognizer_task_out.driver_id}")
                colors.append(RGBColor.SKY_BLUE.value)

                texts_to_draw.append(f"Driver Name: {face_clipper_recognizer_task_out.driver_name}")
                colors.append(RGBColor.SKY_BLUE.value)

                texts_to_draw.append(f"Driver Age: {face_clipper_recognizer_task_out.driver_age}")
                colors.append(RGBColor.SKY_BLUE.value)

            elif face_clipper_recognizer_task_out.driver_id is None:
                texts_to_draw.append(f"Driver: NOT-DETECTED")
                colors.append(RGBColor.RED.value)

        # Draw Panel
        h, w, _ = frame.shape

        panel_w = 300
        panel_h = 40 * len(texts_to_draw)
        alpha = 0.5

        x_start = 0
        y_start = h - panel_h - y_bottom_padding

        x_end = panel_w
        y_end = h - y_bottom_padding

        frame[y_start:y_end, x_start:x_end,] = frame[y_start:y_end, x_start:x_end,] * (1 - alpha) + alpha * np.array(
            RGBColor.GRAY_DARK.value)

        # Put texts
        for i, x in enumerate(texts_to_draw):
            cv2.putText(frame,
                        x,
                        (25, y_start + y_offset + i * line_gap),
                        font, font_scale,
                        colors[i],
                        thickness)

        return frame
