import cv2
import numpy as np
from PIL import Image, ImageTk

import customtkinter as ctk

import app.pipe_line.signals as signals
from app.pages.base.stacked_nav_base_page import StackedNavigationBasePage

import mediapipe as mp

from app.ui_constants import RGBColor


class CameraPage(StackedNavigationBasePage):
    OBJECTS_COLORS = {
        "gun": RGBColor.RED.value,
        "cellphone": RGBColor.ORANGE.value,
        "smoke": RGBColor.DARK_GREEN.value,
        "food": RGBColor.YELLOW.value,
    }

    SEATBELT_UNKNOWN = "UNKNOWN"
    SEATBELT_COLORS = [RGBColor.BROWN.value, RGBColor.BLUE.value]

    def __init__(self, parent, controller, loop_periodicity: float):
        super().__init__(parent, controller, loop_periodicity)

        # make container expandable
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(
            self.container,
            text=""
        )
        self.image_label.grid(row=0, column=0, sticky="nsew")

        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def loop(self):
        frame, raw_land_marks = self._fetch_img()
        frame = self._draw_face_mesh(frame, raw_land_marks)
        frame = self._draw_objects_boxes(frame)
        frame = self._draw_seatbelt_boxes(frame)
        frame = self._resize_frame(frame)
        frame = self._draw_panel(frame)

        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img_tk)

    def _fetch_img(self):
        face_extractor_out = signals.face_extractor_queue.get_last()
        if face_extractor_out is not None:
            frame = np.copy(face_extractor_out.img)
            raw_land_marks = face_extractor_out.raw_land_marks
        else:
            frame = np.zeros((640, 480, 3), dtype=np.uint8)
            raw_land_marks = None

        return frame, raw_land_marks

    def _resize_frame(self, frame):
        target_w = self.container.winfo_width()
        target_h = self.container.winfo_height()

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

    def _draw_face_mesh(self, frame, face_mesh):
        self.mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=face_mesh,
            connections=self.mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style(),
        )
        return frame

    def _draw_objects_boxes(self, frame):
        object_detector_task_out = signals.object_detector_yolo_queue.get_last()
        if object_detector_task_out is None:
            return frame

        for obj in object_detector_task_out.objects_list:
            x1, y1, x2, y2 = obj.object_xyxy

            color = CameraPage.OBJECTS_COLORS.get(obj.object_name, RGBColor.BLACK.value)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame,
                        f"{obj.object_name.capitalize()} ({obj.object_probability})",
                        (x1, max(20, y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2)
        return frame

    def _draw_seatbelt_boxes(self, frame):
        seatbelt_task_out = signals.seatbelt_detector_yolo_queue.get_last()

        if seatbelt_task_out is None or seatbelt_task_out.is_no_detection:
            return frame
        x1, y1, x2, y2 = seatbelt_task_out.object_xyxy

        if seatbelt_task_out.is_seatbelt_on:
            seatbelt_color = CameraPage.SEATBELT_COLORS[1]
        elif seatbelt_task_out.is_seatbelt_off:
            seatbelt_color = CameraPage.SEATBELT_COLORS[0]
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

    def _draw_panel(self, frame):
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
