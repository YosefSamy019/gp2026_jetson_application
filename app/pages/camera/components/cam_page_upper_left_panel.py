import cv2
import numpy as np

from app.pages.camera.components.base_component import OverlayComponent
import app.pipe_line.signals as signals
from app.ui_constants import RGBColor


class UpperLeftComponent(OverlayComponent):
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
            if not yawning_task_out.is_yawning_detected:
                pass
            elif yawning_task_out.is_yawing:
                texts_to_draw.append(f"Yawning: Sleepy, Prob: {yawning_task_out.is_yawing_probability:0.2f}")
                colors.append(RGBColor.RED.value)
            else:
                texts_to_draw.append(f"Yawning: Awake,  Prob: {1 - yawning_task_out.is_yawing_probability:0.2f}")
                colors.append(RGBColor.DARK_GREEN.value)

        eye_task_out = signals.eye_open_close_queue.get_last()
        if eye_task_out is not None:
            if not eye_task_out.is_eye_detected:
                pass
            elif eye_task_out.is_eye_open:
                texts_to_draw.append(f"Eye: Open,  Ear-AVG: {eye_task_out.ear_avg:0.2f}")
                colors.append(RGBColor.DARK_GREEN.value)
            else:
                texts_to_draw.append(f"Eye: Close, Ear-AVG: {eye_task_out.ear_avg:0.2f}")
                colors.append(RGBColor.RED.value)

        head_pose_task_out = signals.head_pose_queue.get_last()
        if head_pose_task_out is not None:
            if not head_pose_task_out.is_head_detected:
                pass
            elif head_pose_task_out.is_front:
                texts_to_draw.append(f"Head: Front,  Prob: {head_pose_task_out.probability:0.2f}")
                colors.append(RGBColor.DARK_GREEN.value)
            elif head_pose_task_out.is_left:
                texts_to_draw.append(f"Head: Left,   Prob: {head_pose_task_out.probability:0.2f}")
                colors.append(RGBColor.RED.value)
            elif head_pose_task_out.is_right:
                texts_to_draw.append(f"Head: Right,  Prob: {head_pose_task_out.probability:0.2f}")
                colors.append(RGBColor.RED.value)

        seatbelt_out = signals.seatbelt_detector_yolo_queue.get_last()
        if seatbelt_out is not None:
            if seatbelt_out.is_no_detection:
                texts_to_draw.append(f"Seatbelt: NO-DETECTED")
                colors.append(RGBColor.DARK_RED.value)
            elif seatbelt_out.is_seatbelt_off:
                texts_to_draw.append(f"Seatbelt: OFF")
                colors.append(RGBColor.RED.value)
            elif seatbelt_out.is_seatbelt_on:
                texts_to_draw.append(f"Seatbelt: ON")
                colors.append(RGBColor.GREEN.value)

        # Draw Panel
        panel_w = 300
        panel_h = 40 * len(texts_to_draw)
        alpha = 0.5

        frame[:panel_h, :panel_w] = frame[:panel_h, :panel_w] * (1 - alpha) + alpha * np.array(RGBColor.GRAY_DARK.value)

        # Put texts
        for i, x in enumerate(texts_to_draw):
            cv2.putText(frame,
                        x,
                        (25, y_offset + i * line_gap),
                        font, font_scale,
                        colors[i],
                        thickness)

        return frame
