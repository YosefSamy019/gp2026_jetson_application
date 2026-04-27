from abc import abstractmethod

import customtkinter as ctk

from app.pages.base.base_page import BasePage
from app.ui_constants import PagesKeys


class StackedNavigationBasePage(BasePage):

    def __init__(self, parent, controller, loop_periodicity: float):
        super().__init__(parent, controller, loop_periodicity)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=1)

        self._base_nav_buttons = dict()
        self.container = self._involve_nav_buttons()

    @abstractmethod
    def loop(self):
        pass

    def _involve_nav_buttons(self):
        side_bar_frame = ctk.CTkScrollableFrame(
            self,
            width=160,
            corner_radius=12
        )

        main_frame = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        side_bar_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=10)

        side_bar_frame.grid_propagate()
        main_frame.grid_propagate()

        ctk.CTkLabel(
            side_bar_frame,
            text="Menu",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=10, pady=10, fill='x')

        for i, (k, v) in enumerate(self.BUTTONS_DATA.items()):
            btn_i = ctk.CTkButton(
                side_bar_frame,
                text=k,
                fg_color='green',
                command=lambda key=k: self._base_nav_button_command(key)
            )
            btn_i.pack(padx=10, pady=10, fill='x')
            self._base_nav_buttons[k] = btn_i
        return main_frame

    def _base_nav_button_command(self, k):
        self._base_controller.navigate_to(self.BUTTONS_DATA[k])
