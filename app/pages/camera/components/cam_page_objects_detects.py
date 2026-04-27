import cv2
import numpy as np

from app.pages.camera.components.base_component import OverlayComponent
import app.pipe_line.signals as signals
from app.ui_constants import RGBColor


class ObjectDetectComponent(OverlayComponent):
    OBJECTS_COLORS = {
        "gun": RGBColor.RED.value,
        "cellphone": RGBColor.ORANGE.value,
        "smoke": RGBColor.DARK_GREEN.value,
        "food": RGBColor.YELLOW.value,
    }

    def process_frame(self, frame: np.ndarray, **params) -> np.ndarray:
        object_detector_task_out = signals.object_detector_yolo_queue.get_last()
        if object_detector_task_out is None:
            return frame

        for obj in object_detector_task_out.objects_list:
            x1, y1, x2, y2 = obj.object_xyxy

            color = ObjectDetectComponent.OBJECTS_COLORS.get(obj.object_name, RGBColor.BLACK.value)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            cv2.putText(frame,
                        f"{obj.object_name.capitalize()} ({obj.object_probability})",
                        (x1, max(20, y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2)
        return frame
