from PIL import ImageTk

import customtkinter as ctk

from app.pages.base.scrollable_nav_base_page import ScrollableNavigationBasePage
from app.pipe_line.signals import face_clipper_recognizer_queue
from mcal import runtime_cache


class DriverPage(ScrollableNavigationBasePage):
    def __init__(self, parent, controller, loop_periodicity: float):
        super().__init__(parent, controller, loop_periodicity)

        # Driver image on top
        self._img_label = ctk.CTkLabel(self.container, text="No Image", width=120, height=120, corner_radius=60)
        self._img_label.pack(pady=(10, 10))

        # Info labels
        self._txt_id_label = ctk.CTkLabel(self.container, text="ID: init...", font=ctk.CTkFont(size=18))
        self._txt_id_label.pack(anchor="w", padx=15, pady=5)

        self._txt_name_label = ctk.CTkLabel(self.container, text="Name: init...", font=ctk.CTkFont(size=18))
        self._txt_name_label.pack(anchor="w", padx=15, pady=5)

        self._txt_age_label = ctk.CTkLabel(self.container, text="Age: init...", font=ctk.CTkFont(size=18))
        self._txt_age_label.pack(anchor="w", padx=15, pady=5)

    def loop(self):
        clipper_recognizer_out = face_clipper_recognizer_queue.get_last()

        if clipper_recognizer_out is None:
            return

        self._txt_id_label.configure(
            text=f"ID: {clipper_recognizer_out.driver_id}"
        )

        self._txt_name_label.configure(
            text=f"Name: {clipper_recognizer_out.driver_name}"
        )

        self._txt_age_label.configure(
            text=f"Age: {clipper_recognizer_out.driver_age}"
        )

        if clipper_recognizer_out.driver_image_url is not None:
            img_data = runtime_cache.get_value(clipper_recognizer_out.driver_image_url)
            if img_data is not None:
                photo = ImageTk.PhotoImage(img_data)
                self._img_label.configure(image=photo, text='')
                self._img_label.image = photo  # keep reference
