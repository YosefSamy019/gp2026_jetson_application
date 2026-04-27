import customtkinter as ctk
from abc import ABC, abstractmethod

from app.ui_constants import PagesKeys


class BasePage(ctk.CTkFrame, ABC):
    BUTTONS_DATA = {
        "Camera View": PagesKeys.CameraPage,
        "Driver": PagesKeys.DriverPage,
        "Logs": PagesKeys.LogsPage,
        "Scheduler": PagesKeys.SchedulerPage,
        "Network": PagesKeys.NetworkPage,
        "Cache": PagesKeys.CachePage,
        "Settings": PagesKeys.SettingsPage,
    }

    def __init__(self, parent, controller, loop_periodicity: float):
        super().__init__(parent)
        self._base_controller = controller
        self.controller = controller
        self.loop_periodicity = loop_periodicity

        self.container = self

    @abstractmethod
    def loop(self):
        pass

    def adjust_theme(self):
        self._base_controller.load_theme()

    def create_section_text(self, title, init_val='None') -> ctk.CTkLabel:
        frame = ctk.CTkFrame(self.container, corner_radius=10)
        frame.pack(padx=10, pady=5, fill='x')

        title_label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=24, weight="bold"), anchor="w")
        title_label.pack(padx=5, pady=(5, 0), fill='x')

        text_label = ctk.CTkLabel(frame, text=init_val, font=ctk.CTkFont(size=22), anchor="w", justify="left")
        text_label.pack(padx=10, pady=5, fill='x')

        return text_label
