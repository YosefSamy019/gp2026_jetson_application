from __future__ import annotations

import json
import customtkinter as ctk
import app.upper_logic as up

tasks_txt_label: ctk.CTkLabel | None = None
queues_txt_label: ctk.CTkLabel | None = None
locks_txt_label: ctk.CTkLabel | None = None


def init():
    up.variable_scheduler.trace_add("write", _output_parser)


def _output_parser(_, __, ___):
    value = up.variable_scheduler.get()
    dict_values = json.loads(value)

    if tasks_txt_label and tasks_txt_label.winfo_exists():
        tasks_txt_label.configure(text="\n".join(dict_values['tasks']))

    if queues_txt_label and queues_txt_label.winfo_exists():
        queues_txt_label.configure(text="\n".join(dict_values['queues']))

    if locks_txt_label and locks_txt_label.winfo_exists():
        locks_txt_label.configure(text="\n".join(dict_values['locks']))


def _create_section_frame(parent, title) -> ctk.CTkLabel:
    frame = ctk.CTkFrame(parent, corner_radius=10)
    frame.pack(padx=10, pady=5, fill='x')

    title_label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=24, weight="bold"), anchor="w")
    title_label.pack(padx=5, pady=(5, 0), fill='x')

    text_label = ctk.CTkLabel(frame, text="init...", font=ctk.CTkFont(size=22), anchor="w", justify="left")
    text_label.pack(padx=10, pady=5, fill='x')

    return text_label


def show_scheduler_window(root: ctk.CTk, main_frame_hook: ctk.CTkScrollableFrame):
    global tasks_txt_label, queues_txt_label, locks_txt_label

    tasks_txt_label = _create_section_frame(main_frame_hook, "Tasks")
    queues_txt_label = _create_section_frame(main_frame_hook, "Queues")
    locks_txt_label = _create_section_frame(main_frame_hook, "Locks")
