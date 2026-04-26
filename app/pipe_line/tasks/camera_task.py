import cv2
import app.pipe_line.signals as signals
import app.pipe_line.timing as timing
import time
import mcal.logs as logs
import os

from app.pipe_line.models.models import CameraTaskOutput
from scheduler.task import Task


class CameraTask(Task):
    PATHS_DICT = {
        # "YOSEF-SA": r"D:\GP\dataset\videos\distraction\gA_4_s1_2019-03-13T10;36;15+01;00_rgb_face.mp4",
        "YOSEF-SA": 0,
        "DESKTOP-17FURUT": 0,
    }

    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

        self.cap = None
        self.computer_name = os.environ.get('COMPUTERNAME')
        self.camera_path = self.PATHS_DICT.get(self.computer_name)
        logs.add_log(f"Selected Camera Path: {self.camera_path}", logs.LogLevel.INFO)

    def update(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.camera_path)

        if not self.cap.isOpened():
            logs.add_log("Camera is not not opened", logs.LogLevel.ERROR)
            return

        ret, frame = self.cap.read()

        if not ret:
            logs.add_log("Camera read failed", logs.LogLevel.ERROR)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            signals.camera_output_queue.put(
                CameraTaskOutput(
                    raw_img=frame
                )
            )
