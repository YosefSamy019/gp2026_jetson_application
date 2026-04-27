import cv2
from PIL import Image, ImageTk

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
        self.video_finished = False

    def loop(self):
        if self.video_finished:
            return

        ret, frame = self.cap.read()

        if not ret:
            self.cap.release()
            self.video_finished = True
            self.controller.navigate_to(PagesKeys.CameraPage)
            self.controller.start_pipeline()
            return

        # Get current widget size safely
        w = self.container.winfo_toplevel().winfo_width()
        h = self.container.winfo_toplevel().winfo_height()

        # --- Maintain aspect ratio ---
        frame_h, frame_w = frame.shape[:2]

        scale = max(w / frame_w, h / frame_h)  # fill screen
        new_w = int(frame_w * scale)
        new_h = int(frame_h * scale)

        frame = cv2.resize(frame, (new_w, new_h))

        # center crop
        x_start = (new_w - w) // 2
        y_start = (new_h - h) // 2
        frame = frame[y_start:y_start + h, x_start:x_start + w]

        # convert color
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = ImageTk.PhotoImage(Image.fromarray(frame))

        self.video_label.configure(image=img)
        self.video_label.image = img

    def on_page_reinvoke(self):
        pass
