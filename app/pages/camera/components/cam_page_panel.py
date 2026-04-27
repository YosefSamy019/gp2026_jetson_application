import cv2
import numpy as np

from app.pages.camera.components.base_component import OverlayComponent
import app.pipe_line.signals as signals
from app.ui_constants import RGBColor


class PanelComponent(OverlayComponent):

    def process_frame(self, frame: np.ndarray, **params) -> np.ndarray:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        y_offset = 40
        line_gap = 35

        texts_to_draw = []
        colors = []

        yawning_task_out = signals.yawing_queue.get_last()
        if yawning_task_out is not None:
            if yawning_task_out.is_yawing:
                texts_to_draw.append(f"Yawning: Sleepy, Prob: {yawning_task_out.is_yawing_probability:0.2f}")
                colors.append(RGBColor.RED.value)
            else:
                texts_to_draw.append(f"Yawning: Awake,  Prob: {1 - yawning_task_out.is_yawing_probability:0.2f}")
                colors.append(RGBColor.DARK_GREEN.value)

        eye_task_out = signals.eye_open_close_queue.get_last()
        if eye_task_out is not None:
            if eye_task_out.is_eye_open:
                texts_to_draw.append(f"Eye: Open,  Ear-AVG: {eye_task_out.ear_avg:0.2f}")
                colors.append(RGBColor.DARK_GREEN.value)
            else:
                texts_to_draw.append(f"Eye: Close, Ear-AVG: {eye_task_out.ear_avg:0.2f}")
                colors.append(RGBColor.RED.value)

        head_pose_task_out = signals.head_pose_queue.get_last()
        if head_pose_task_out is not None:
            if head_pose_task_out.is_front:
                texts_to_draw.append(f"Head: Front,  Prob: {head_pose_task_out.probability:0.2f}")
                colors.append(RGBColor.DARK_GREEN.value)
            if head_pose_task_out.is_left:
                texts_to_draw.append(f"Head: Left,   Prob: {head_pose_task_out.probability:0.2f}")
                colors.append(RGBColor.RED.value)
            if head_pose_task_out.is_right:
                texts_to_draw.append(f"Head: Right,  Prob: {head_pose_task_out.probability:0.2f}")
                colors.append(RGBColor.RED.value)

        face_clipper_recognizer_task_out = signals.face_clipper_recognizer_queue.get_last()
        if face_clipper_recognizer_task_out is not None:
            if face_clipper_recognizer_task_out.driver_id is not None:
                texts_to_draw.append(f"Driver-ID: {face_clipper_recognizer_task_out.driver_id}")
                colors.append(RGBColor.DARK_GREEN.value)
            if face_clipper_recognizer_task_out.driver_id is None:
                texts_to_draw.append(f"Driver-ID: NOT-DETECTED")
                colors.append(RGBColor.RED.value)

        for i, x in enumerate(texts_to_draw):
            cv2.putText(frame,
                        x,
                        (25, y_offset + i * line_gap),
                        font, font_scale,
                        colors[i],
                        thickness)

        return frame
