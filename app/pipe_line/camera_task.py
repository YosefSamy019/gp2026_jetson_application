import cv2
import app.pipe_line.signals as signals
import app.pipe_line.timing as timing
import time
import mcal.logs as logs
import os

from scheduler.task import Task


class CameraTask(Task):
    def __init__(self):
        super().__init__(
            name='CameraTask',
            periodicity=timing.CAMERA_TASK_SLEEP_TIME
        )

    def start(self):
        computer_name = os.environ.get('COMPUTERNAME')

        if computer_name == "YOSEF-SA":
            # Youssef Laptop
            camera_path = r"D:\GP\dataset\videos\distraction\gA_4_s1_2019-03-13T10;36;15+01;00_rgb_face.mp4"
            camera_path = 0
        elif computer_name == 'DESKTOP-17FURUT':
            # Yahia Laptop
            camera_path = 1
        else:
            # Linux Board
            camera_path = 0

        logs.add_log(f"Current Computer Name: {computer_name}", logs.LogLevel.INFO)
        logs.add_log(f"Selected Camera Path: {camera_path}", logs.LogLevel.INFO)

        self.cap = cv2.VideoCapture(camera_path)

        while not self.cap.isOpened():
            self.cap = cv2.VideoCapture(camera_path)
            logs.add_log("Camera not opened", logs.LogLevel.ERROR)
            time.sleep(1)

        logs.add_log("Camera opened successfully", logs.LogLevel.INFO)

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            logs.add_log("Camera read failed", logs.LogLevel.ERROR)
            time.sleep(1)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            signals.camera_output_queue.put({
                "raw_img": frame,
            })

        time.sleep(timing.CAMERA_TASK_SLEEP_TIME)
