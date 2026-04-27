import cv2
from PIL import Image, ImageTk

import time
from app.pages.base.base_page import BasePage
import customtkinter as ctk

from app.ui_constants import PagesKeys
from constants import assets_manager


class IntroPage(BasePage):
    def __init__(self, parent, controller, loop_periodicity: float):
        super().__init__(parent, controller, loop_periodicity)

        self.video_label = ctk.CTkLabel(self.container, text="")
        self.video_label.pack(expand=True, fill="both")

        self.cap = cv2.VideoCapture(assets_manager.INTRO_VIDEO_PATH)


        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.fps <= 0: self.fps = 30
        self.frame_delay = 1.0 / self.fps
        self.last_update_time = time.time()

        self.video_finished = False

    def loop(self):
        if self.video_finished:
            return


        current_time = time.time()
        if current_time - self.last_update_time < self.frame_delay:
            return

        ret, frame = self.cap.read()

        if not ret:
            self.cap.release()
            self.video_finished = True
            self.controller.navigate_to(PagesKeys.CameraPage)
            self.controller.start_pipeline()
            return


        self.last_update_time = current_time


        w = self.container.winfo_toplevel().winfo_width()
        h = self.container.winfo_toplevel().winfo_height()

        frame_h, frame_w = frame.shape[:2]
        scale = max(w / frame_w, h / frame_h)
        new_w = int(frame_w * scale)
        new_h = int(frame_h * scale)

        frame = cv2.resize(frame, (new_w, new_h))

        x_start = (new_w - w) // 2
        y_start = (new_h - h) // 2
        frame = frame[y_start:y_start + h, x_start:x_start + w]

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame))

        self.video_label.configure(image=img)
        self.video_label.image = img

    def on_page_reinvoke(self):
        pass
