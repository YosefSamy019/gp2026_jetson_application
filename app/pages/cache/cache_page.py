import customtkinter as ctk

from app.pages.base.scrollable_nav_base_page import ScrollableNavigationBasePage
from mcal import cache


class CachePage(ScrollableNavigationBasePage):
    def __init__(self, parent, controller, loop_periodicity: float):
        super().__init__(parent, controller, loop_periodicity)

        self._widgets = dict()

    def loop(self):
        report = cache.get_report()

        for k, v in report.items():

            if k in self._widgets:
                label = self._widgets[k]
                label.configure(text=str(v))

            elif k not in self._widgets:
                row = len(self._widgets)

                # Key label (left column)
                key_label = ctk.CTkLabel(
                    self.container,
                    text=k,
                    font=ctk.CTkFont(size=15),
                    anchor="w"
                )
                key_label.grid(
                    row=row,
                    column=0,
                    sticky="w",
                    padx=15,
                    pady=6
                )

                # Value label (right column, bold)
                value_label = ctk.CTkLabel(
                    self.container,
                    text=str(v),
                    font=ctk.CTkFont(size=22, weight="bold"),
                    anchor="e"
                )
                value_label.grid(
                    row=row,
                    column=1,
                    sticky="e",
                    padx=15,
                    pady=6
                )

                self._widgets[k] = value_label
