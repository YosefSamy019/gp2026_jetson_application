import cv2
import numpy as np

from app.pages.camera.components.base_component import OverlayComponent
import app.pipe_line.signals as signals
from app.ui_constants import RGBColor


class SeatbeltDetectComponent(OverlayComponent):
    SEATBELT_COLORS = [RGBColor.BROWN.value, RGBColor.BLUE.value]

    def process_frame(self, frame: np.ndarray, **params) -> np.ndarray:
        seatbelt_task_out = signals.seatbelt_detector_yolo_queue.get_last()

        if seatbelt_task_out is None or seatbelt_task_out.is_no_detection:
            return frame

        x1, y1, x2, y2 = seatbelt_task_out.object_xyxy

        if seatbelt_task_out.is_seatbelt_on:
            seatbelt_color = SeatbeltDetectComponent.SEATBELT_COLORS[1]
        elif seatbelt_task_out.is_seatbelt_off:
            seatbelt_color = SeatbeltDetectComponent.SEATBELT_COLORS[0]
        else:
            seatbelt_color = RGBColor.BLACK.value

        temp_txt = 'Seatbelt' if seatbelt_task_out.is_seatbelt_on else "No-Seatbelt"
        cv2.rectangle(frame, (x1, y1), (x2, y2), seatbelt_color, 2)

        cv2.putText(frame,
                    f"{temp_txt}({seatbelt_task_out.probability})",
                    (x1, max(20, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    seatbelt_color,
                    2)

        return frame
