import numpy as np
from PIL import Image, ImageTk

import customtkinter as ctk

import app.pipe_line.signals as signals
from app.pages.base.stacked_nav_base_page import StackedNavigationBasePage
from app.pages.camera.components.cam_page_face_mesh import FaceMeshComponent
from app.pages.camera.components.cam_page_lower_left_panel import LowerLeftComponent
from app.pages.camera.components.cam_page_objects_detects import ObjectDetectComponent
from app.pages.camera.components.cam_page_red_alert import RedAlertComponent
from app.pages.camera.components.cam_page_upper_left_panel import UpperLeftComponent
from app.pages.camera.components.cam_page_resize import ResizeComponent
from app.pages.camera.components.cam_page_seatbelt_detects import SeatbeltDetectComponent
from app.pages.camera.components.cam_page_snack_bar import SnackBarComponent


class CameraPage(StackedNavigationBasePage):
    SEATBELT_UNKNOWN = "UNKNOWN"

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

        self.transformations = [
            RedAlertComponent(),
            SeatbeltDetectComponent(),
            ObjectDetectComponent(),
            FaceMeshComponent(),
            ResizeComponent(),
            UpperLeftComponent(),
            LowerLeftComponent(),
            SnackBarComponent(),
        ]

    def loop(self):
        frame = self._fetch_img()
        target_w = self.container.winfo_width()
        target_h = self.container.winfo_height()

        for transformation in self.transformations:
            frame = transformation.process_frame(
                frame=frame,
                window_size=(target_w, target_h)
            )

        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img_tk)

    def _fetch_img(self):
        face_extractor_out = signals.face_extractor_queue.get_last()
        if face_extractor_out is not None:
            frame = np.copy(face_extractor_out.img)
        else:
            frame = np.zeros((640, 480, 3), dtype=np.uint8)

        return frame
