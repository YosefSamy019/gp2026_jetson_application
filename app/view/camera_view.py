import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk

import app.pipe_line.signals as signals
import mcal.logs as logs
import app.pipe_line.timing as timing
import mediapipe as mp

from app.pipe_line.signals import face_clipper_recognizer_queue

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def _widget_alive(widget):
    try:
        return widget.winfo_exists()
    except:
        return False


def show_cam_window(
        root: ctk.CTk,
        main_fram_hook: ctk.CTkScrollableFrame,
        display_cam_frame: ctk.BooleanVar,
):
    # Stop if flag off or frame destroyed
    if not display_cam_frame.get() or not _widget_alive(main_fram_hook):
        return

    # Create label if missing or destroyed
    if (not hasattr(main_fram_hook, "_cam_label") or
            not _widget_alive(main_fram_hook._cam_label)):
        main_fram_hook._cam_label = ctk.CTkLabel(main_fram_hook, text="")
        main_fram_hook._cam_label.configure(width=640, height=480)
        main_fram_hook._cam_label.pack(padx=10, pady=10, expand=True)

    try:
        lens_output = signals.lens_output_queue.get_last()
        if lens_output is not None:
            frame = lens_output.clean_img
        else:
            frame = np.zeros((640, 480, 3), dtype=np.uint8)

        frame = _edit_frame(frame)
        frame = _resize_for_frame(frame, main_fram_hook._cam_label)

        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(img)

        main_fram_hook._cam_label.configure(image=img_tk)
        main_fram_hook._cam_label.image = img_tk

    except Exception as e:
        raise e
        logs.add_log(f"Error show_cam_window: {e}", logs.LogLevel.ERROR)

    # Schedule next frame ONLY if still alive
    if display_cam_frame.get() and _widget_alive(main_fram_hook):
        root.after(timing.UI_UPDATE_SLEEP_TIME, lambda: show_cam_window(root, main_fram_hook, display_cam_frame))


def _resize_for_frame(frame, frame_widget):
    if frame is None:
        return None

    frame_widget.update_idletasks()

    target_w = frame_widget.winfo_width()
    target_h = frame_widget.winfo_height()

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


def _edit_frame(frame_rgb):
    if frame_rgb is None:
        return None

    frame_rgb = np.copy(frame_rgb)
    h, w = frame_rgb.shape[:2]

    # =============================
    # Get signals safely
    # =============================
    yawning_task_out = signals.yawing_queue.get_last()
    head_pose_task_out = signals.head_pose_queue.get_last()
    eye_task_out = signals.eye_open_close_queue.get_last()
    face_extractor_task_out = signals.face_extractor_queue.get_last()
    face_clipper_recognizer_task_out = signals.face_clipper_recognizer_queue.get_last()
    seatbelt_task_out = signals.seatbelt_detector_yolo_queue.get_last()
    object_detector_task_out = signals.object_detector_yolo_queue.get_last()

    # =============================
    # Draw Face Mesh
    # =============================
    if face_extractor_task_out is not None and face_extractor_task_out.raw_land_marks:
        mp_drawing.draw_landmarks(
            image=frame_rgb,
            landmark_list=face_extractor_task_out.raw_land_marks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
        )

    # =============================
    # Create Transparent Info Panel
    # =============================
    overlay = frame_rgb.copy()
    panel_width = 420
    panel_height = 200

    cv2.rectangle(overlay, (10, 10), (panel_width, panel_height),
                  (20, 20, 20), -1)

    alpha = 0.6
    cv2.addWeighted(overlay, alpha, frame_rgb, 1 - alpha, 0, frame_rgb)

    # =============================
    # Seatbelt Data
    # =============================

    seatbelt_status_text = "UNKNOWN"
    seatbelt_status_color = (200, 200, 200)

    # Draw WITHOUT seatbelt boxes (Red)
    if seatbelt_task_out is not None and not seatbelt_task_out.is_no_detection:
        x1, y1, x2, y2 = seatbelt_task_out.object_xyxy

        cv2.rectangle(frame_rgb, (x1, y1), (x2, y2),
                      (0, 0, 255), 2)

        temp_txt = 'Seatbelt detected' if seatbelt_task_out.is_seatbelt_on else "No-Seatbelt detected"

        cv2.putText(frame_rgb,
                    f"{temp_txt}({seatbelt_task_out.probability})",
                    (x1, max(20, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2)
    # =============================
    # object Data
    # =============================
    object_colors = {
        "gun": (0, 0, 255),  # Red
        "cellphone": (255, 165, 0),  # orange
        "smoke": (150, 150, 150),  # gray
        "food": (0, 255, 255)  # yellow
    }

    default_color = (255, 255, 255)  # White for any unknown class

    if object_detector_task_out is not None:
        for obj in object_detector_task_out.objects_list:
            x1, y1, x2, y2 = obj.object_xyxy

            color = object_colors.get(obj.object_name, default_color)
            cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame_rgb,
                        f"{obj.object_name.capitalize()}({obj.object_probability})",
                        (x1, max(20, y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2)

    if seatbelt_task_out is None or seatbelt_task_out.is_no_detection:
        seatbelt_status_text = "NO DRIVER DETECTED"
        seatbelt_status_color = (150, 150, 150)

    elif seatbelt_task_out.is_seatbelt_off:
        seatbelt_status_text = "NOT WEARING SEATBELT"
        seatbelt_status_color = (0, 0, 255)

    elif seatbelt_task_out.is_seatbelt_on:
        seatbelt_status_text = "WEARING SEATBELT"
        seatbelt_status_color = (0, 255, 0)

    # =============================
    # Text Styling
    # =============================
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    y_offset = 40
    line_gap = 35

    def status_color(flag):
        return (0, 0, 255) if flag else (0, 255, 0)

    # =============================
    # Display Data
    # =============================
    if yawning_task_out is not None:
        cv2.putText(frame_rgb,
                    f"Yawning      : {yawning_task_out.is_yawing} ({yawning_task_out.is_yawing_probability:.2f})"
                    if yawning_task_out
                    else "Yawning: N/A",
                    (25, y_offset),
                    font, font_scale,
                    status_color(yawning_task_out.is_yawing),
                    thickness)

    cv2.putText(frame_rgb,
                f"Head Pose Front  : {head_pose_task_out.is_left} {head_pose_task_out.is_front} {head_pose_task_out.is_right} ({head_pose_task_out.probability:.2f})"
                if head_pose_task_out
                else "Head: N/A",
                (25, y_offset + line_gap),
                font, font_scale,
                (255, 255, 255),
                thickness)

    cv2.putText(frame_rgb,
                f"Eye Open   : {eye_task_out.is_eye_open} (avg: {eye_task_out.ear_avg:.2f})"
                if eye_task_out
                else "Eye: N/A",
                (25, y_offset + 2 * line_gap),
                font, font_scale,
                (255, 255, 255),
                thickness
                )

    cv2.putText(frame_rgb,
                f"Driver ID    : {face_clipper_recognizer_task_out.driver_id}"
                if face_clipper_recognizer_task_out
                else "Driver: N/A",
                (25, y_offset + 3 * line_gap),
                font, font_scale,
                (0, 255, 255),
                thickness)

    cv2.putText(frame_rgb,
                f"Seatbelt    : {seatbelt_status_text}",
                (25, y_offset + 4 * line_gap),
                font, font_scale,
                seatbelt_status_color,
                thickness)

    return frame_rgb
