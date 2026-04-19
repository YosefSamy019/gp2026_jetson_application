import cv2
import app.pipe_line.signals as signals
import app.pipe_line.timing as timing
import time
import mcal.logs as logs
import os


def camera_task():
    if os.environ.get('COMPUTERNAME') == "YOSEF-SA":
        camera_path = r"D:\GP\dataset\videos\distraction\gA_4_s1_2019-03-13T10;36;15+01;00_rgb_face.mp4"
        camera_path = 0
    else:
        camera_path = 1

    logs.add_log(f"Selected Camera Path: {camera_path}", logs.LogLevel.INFO)

    cap = cv2.VideoCapture(camera_path)

    try:
        while not cap.isOpened():
            cap = cv2.VideoCapture(camera_path)
            logs.add_log("Camera not opened", logs.LogLevel.ERROR)
            time.sleep(1)

        logs.add_log("Camera opened successfully", logs.LogLevel.INFO)

        while True:
            ret, frame = cap.read()
            if not ret:
                logs.add_log("Camera read failed", logs.LogLevel.ERROR)
                time.sleep(1)
            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                signals.camera_output_queue.put({
                    "raw_img": frame,
                })

            time.sleep(timing.CAMERA_TASK_SLEEP_TIME)

    except Exception as e:
        logs.add_log(f"camera_task: error {e}", logs.LogLevel.ERROR)
