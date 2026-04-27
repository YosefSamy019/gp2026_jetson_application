from typing import List

from app.pages.base.scrollable_nav_base_page import ScrollableNavigationBasePage
import mcal.logs as logs
import customtkinter as ctk


class LogsPage(ScrollableNavigationBasePage):
    BTN_TXT_LIST = ["All", "Info", "Warning", "Error"]

    def __init__(self, parent, controller, loop_periodicity: float):
        super().__init__(parent, controller, loop_periodicity)

        self.selected_button_idx = 0

        # ---- Buttons Frame  ----
        self.main_btns_frame = ctk.CTkFrame(self.container)
        self.main_btns_frame.pack(padx=10, pady=5, fill="x")
        self.buttons = []

        # -------------
        self.clear_btn = ctk.CTkButton(self.main_btns_frame, text='Clear', fg_color='RED',
                                       width=5,
                                       command=lambda: self._clean_btn_command())
        self.clear_btn.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        # -------------

        for i, type_txt in enumerate(self.BTN_TXT_LIST):
            self.btn_i = ctk.CTkButton(self.main_btns_frame, text=self.BTN_TXT_LIST[i], fg_color=self._get_btn_color(i),
                                       width=5,
                                       command=lambda i=i: self._filter_btn_command(i))
            self.btn_i.pack(side="left", padx=5, pady=5, expand=True, fill="x")
            self.buttons.append(self.btn_i)

        # ---- Text Label ----
        self.txt_label = ctk.CTkLabel(
            self.container,
            text="init...",
            font=ctk.CTkFont(size=22),
            justify="left",
            anchor="w"  # align text to left
        )
        self.txt_label.pack(padx=10, pady=10, fill='x')

    def loop(self):
        count_dict: dict = logs.get_count()
        all_logs_count = sum(count_dict.values())

        for i, btn in enumerate(self.buttons):
            if i == 0:
                btn.configure(text=f"{self.BTN_TXT_LIST[i]} ({all_logs_count})")
            else:
                btn.configure(text=f"{self.BTN_TXT_LIST[i]} ({count_dict.get(i, 0)})")

        logs_list: List[logs.LogDataClass] = logs.get_logs(self.selected_button_idx)
        self.txt_label.configure(text="\n".join(map(str, logs_list)))

    def _get_btn_color(self, btn_id) -> str:
        if btn_id == self.selected_button_idx:
            return "green"
        else:
            return "gray"

    def _filter_btn_command(self, btn_id):
        self.selected_button_idx = btn_id

        for i, btn in enumerate(self.buttons):
            btn.configure(
                fg_color=self._get_btn_color(i)
            )

    def _clean_btn_command(self):
        logs.clear_logs()
        self.loop()
