import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk

import app.pipe_line.signals as signals
import mcal.logs as logs
import app.pipe_line.timing as timing
import mediapipe as mp

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
        main_fram_hook._cam_label.pack(padx=0, pady=0, expand=True)

    try:
        lens_output = signals.lens_output_queue.get_immediate()
        frame = lens_output.get("processed_img") if lens_output else np.zeros((640, 480, 3), dtype=np.uint8)

        frame = _edit_frame(frame)
        frame = _resize_for_frame(frame, main_fram_hook._cam_label)

        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(img)

        main_fram_hook._cam_label.configure(image=img_tk)
        main_fram_hook._cam_label.image = img_tk

    except Exception as e:

        logs.add_log(f"Error show_cam_window: {e}", logs.LogLevel.ERROR)

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
    yaw_data = signals.yawing_queue.get_immediate(fallback_value={})
    head_data = signals.head_pose_queue.get_immediate(fallback_value={})
    eye_data = signals.eye_open_close_queue.get_immediate(fallback_value={})
    face_data = signals.face_extractor_queue.get_immediate(fallback_value={})
    driver_data = signals.face_clipper_recognizer_queue.get_immediate(fallback_value={})
    seatbelt_data = signals.seatbelt_detector_yolo_queue.get_immediate(fallback_value={})
    object_data = signals.object_detector_yolo_queue.get_immediate(fallback_value={})

    yaw_class = yaw_data.get("class", "N/A")
    yaw_flag = yaw_data.get("yawing_flag", False)
    yaw_prob = yaw_data.get("prob", 0.0)

    head_class = head_data.get("class", "N/A")
    head_prob = head_data.get("prob", 0.0)

    eye_class = eye_data.get("class", "N/A")
    eye_avg = eye_data.get("avg", 0.0)

    driver_id = driver_data.get("id", "Unknown")

    raw_land_marks = face_data.get("raw_land_marks") if face_data else None

    seatbelt_no_boxes_detected = seatbelt_data.get("no_boxes_detected", False)
    with_seatbelt_flag = seatbelt_data.get("with_seatbelt_flag", False)
    without_seatbelt_flag = seatbelt_data.get("without_seatbelt_flag", False)
    without_seatbelt_flag = seatbelt_data.get("without_seatbelt_flag", False)
    all_with_seatbelt_list = seatbelt_data.get("all_with_seatbelt_list", [])
    all_without_seatbelt_list = seatbelt_data.get("all_without_seatbelt_list", [])

    detected_objects = object_data.get("value", [])

    # =============================
    # Draw Face Mesh
    # =============================
    if raw_land_marks is not None:
        mp_drawing.draw_landmarks(
            image=frame_rgb,
            landmark_list=raw_land_marks,
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

    # Draw WITH seatbelt boxes (Green)
    for box in all_with_seatbelt_list:
        x1 = box.get("x1", 0)
        y1 = box.get("y1", 0)
        x2 = box.get("x2", 0)
        y2 = box.get("y2", 0)
        score = box.get("score", 0)

        cv2.rectangle(frame_rgb, (x1, y1), (x2, y2),
                      (0, 255, 0), 2)

        cv2.putText(frame_rgb,
                    f"Seatbelt({score})",
                    (x1, max(20, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2)

    # Draw WITHOUT seatbelt boxes (Red)
    for box in all_without_seatbelt_list:
        x1 = box.get("x1", 0)
        y1 = box.get("y1", 0)
        x2 = box.get("x2", 0)
        y2 = box.get("y2", 0)
        score = box.get("score", 0)

        cv2.rectangle(frame_rgb, (x1, y1), (x2, y2),
                      (0, 0, 255), 2)

        cv2.putText(frame_rgb,
                    f"NO Seatbelt({score})",
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

    for obj in detected_objects:
        x1 = obj.get("x1", 0)
        y1 = obj.get("y1", 0)
        x2 = obj.get("x2", 0)
        y2 = obj.get("y2", 0)
        class_name = obj.get("class", "Unknown")
        score = obj.get("score", 0)

        color = object_colors.get(class_name, default_color)

        cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame_rgb,
                    f"{class_name.capitalize()}({score})",
                    (x1, max(20, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2)

    # Determine overall status
    if seatbelt_no_boxes_detected:
        seatbelt_status_text = "NO DRIVER DETECTED"
        seatbelt_status_color = (150, 150, 150)

    elif without_seatbelt_flag:
        seatbelt_status_text = "NOT WEARING SEATBELT"
        seatbelt_status_color = (0, 0, 255)

    elif with_seatbelt_flag:
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
    cv2.putText(frame_rgb,
                f"Yawning      : {yaw_class} ({yaw_prob:.2f})",
                (25, y_offset),
                font, font_scale,
                status_color(yaw_flag),
                thickness)

    cv2.putText(frame_rgb,
                f"Head Pose    : {head_class} ({head_prob:.2f})",
                (25, y_offset + line_gap),
                font, font_scale,
                (255, 255, 255),
                thickness)

    cv2.putText(frame_rgb,
                f"Eye Status   : {eye_class} (avg: {eye_avg:.2f})",
                (25, y_offset + 2 * line_gap),
                font, font_scale,
                (255, 255, 255),
                thickness)

    cv2.putText(frame_rgb,
                f"Driver ID    : {driver_id}",
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
