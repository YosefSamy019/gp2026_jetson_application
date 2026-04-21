from __future__ import annotations

from typing import List

import customtkinter as ctk
import app.upper_logic as up
import mcal.logs as logs
from mcal.logs import LogLevel

_output_val = ''
txt_label: ctk.CTkLabel | None = None
btns_list: List[ctk.CTkButton] = []

btn_texts_list = ["All", "Info", "Warning", "Error"]


def init():
    global txt_label, _output_val
    up.variable_logs.trace_add("write", _output_parser)
    up.variable_logs.trace_add("write", _update_btn_texts)


def _output_parser(_, __, ___):
    if txt_label and txt_label.winfo_exists():
        value = up.variable_logs.get()
        txt_label.configure(text=value)


def _update_btn_texts(_, __, ___):
    global txt_label

    count_dict: dict = logs.get_count()
    all_logs_count = sum(count_dict.values())

    for i, btn in enumerate(btns_list):
        if not btn.winfo_exists():
            continue

        if i == 0:
            btn.configure(text=f"{btn_texts_list[i]} ({all_logs_count})")
        else:
            btn.configure(text=f"{btn_texts_list[i]} ({count_dict.get(i, 0)})")


def _get_btn_color(btn_id) -> str:
    if btn_id == up.variable_logs_filter.get():
        return "green"
    else:
        return "gray"


def _filter_btn_command(btn_id):
    up.variable_logs_filter.set(btn_id)
    for i, btn in enumerate(btns_list):
        if not btn.winfo_exists():
            continue
        btn.configure(fg_color=_get_btn_color(i))


def show_logs_window(
        root: ctk.CTk,
        main_fram_hook: ctk.CTkScrollableFrame
):
    global txt_label
    btns_list.clear()

    # ---- Buttons Frame (Horizontal Layout) ----
    btn_frame = ctk.CTkFrame(main_fram_hook)
    btn_frame.pack(padx=10, pady=5, fill="x")

    btn0 = ctk.CTkButton(btn_frame, text="Clear", fg_color="red",
                         command=lambda: logs.clear_logs())
    btn0.pack(side="left", padx=5, pady=5, expand=True, fill="x")

    btn1 = ctk.CTkButton(btn_frame, text=btn_texts_list[0], fg_color=_get_btn_color(0),
                         command=lambda: _filter_btn_command(0))
    btn1.pack(side="left", padx=5, pady=5, expand=True, fill="x")
    btns_list.append(btn1)

    btn2 = ctk.CTkButton(btn_frame, text=btn_texts_list[1], fg_color=_get_btn_color(1),
                         command=lambda: _filter_btn_command(LogLevel.INFO.value))
    btn2.pack(side="left", padx=5, pady=5, expand=True, fill="x")
    btns_list.append(btn2)

    btn3 = ctk.CTkButton(btn_frame, text=btn_texts_list[2], fg_color=_get_btn_color(2),
                         command=lambda: _filter_btn_command(LogLevel.WARNING.value))
    btn3.pack(side="left", padx=5, pady=5, expand=True, fill="x")
    btns_list.append(btn3)

    btn4 = ctk.CTkButton(btn_frame, text=btn_texts_list[3], fg_color=_get_btn_color(3),
                         command=lambda: _filter_btn_command(LogLevel.ERROR.value))
    btn4.pack(side="left", padx=5, pady=5, expand=True, fill="x")
    btns_list.append(btn4)

    # ---- Text Label ----
    txt_label = ctk.CTkLabel(
        main_fram_hook,
        text="init...",
        font=ctk.CTkFont(size=22),
        justify="left",
        anchor="w"  # align text to left
    )
    txt_label.pack(padx=10, pady=10, fill='x')
