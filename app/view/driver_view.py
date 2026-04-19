import json
import customtkinter as ctk
from PIL import Image, ImageTk
import requests
import io
import app.upper_logic as up
from mcal import logs
from mcal import runtime_cache

_cache_img_urls = dict()

_txt_id_label: ctk.CTkLabel | None = None
_txt_name_label: ctk.CTkLabel | None = None
_txt_age_label: ctk.CTkLabel | None = None
_txt_img_label: ctk.CTkLabel | None = None
_driver_frame: ctk.CTkFrame | None = None


def init():
    up.variable_driver.trace_add("write", _output_parser)


def _output_parser(_, __, ___):
    value = up.variable_driver.get()
    if not value:
        return

    try:
        json_dict = json.loads(value)
    except json.JSONDecodeError:
        return

    if _txt_id_label and _txt_id_label.winfo_exists():
        _txt_id_label.configure(text=f"ID: {json_dict.get('id', 'N/A')}")

    if _txt_name_label and _txt_name_label.winfo_exists():
        _txt_name_label.configure(text=f"Name: {json_dict.get('name', 'N/A')}")

    if _txt_age_label and _txt_age_label.winfo_exists():
        _txt_age_label.configure(text=f"Age: {json_dict.get('age', 'N/A')}")

    # Update driver image
    image_url = json_dict.get("image_url")
    img_data = runtime_cache.get_value(image_url)

    if _txt_img_label and _txt_img_label.winfo_exists() and img_data:
        try:
            photo = ImageTk.PhotoImage(img_data)
            _txt_img_label.configure(image=photo, text='')
            _txt_img_label.image = photo  # keep reference
        except Exception as e:
            logs.add_log(f"Image load error: {e}", logs.LogLevel.ERROR)


def show_driver_window(root: ctk.CTk, main_frame_hook: ctk.CTkScrollableFrame):
    global _txt_id_label, _txt_name_label, _txt_age_label, _txt_img_label, _driver_frame

    # Card frame
    _driver_frame = ctk.CTkFrame(main_frame_hook, corner_radius=12, fg_color="#1f1f1f")
    _driver_frame.pack(padx=20, pady=15, fill='x')

    # Driver image on top
    _txt_img_label = ctk.CTkLabel(_driver_frame, text="No Image", width=120, height=120, corner_radius=60)
    _txt_img_label.pack(pady=(10, 10))

    # Info labels
    _txt_id_label = ctk.CTkLabel(_driver_frame, text="ID: init...", font=ctk.CTkFont(size=18))
    _txt_id_label.pack(anchor="w", padx=15, pady=5)

    _txt_name_label = ctk.CTkLabel(_driver_frame, text="Name: init...", font=ctk.CTkFont(size=18))
    _txt_name_label.pack(anchor="w", padx=15, pady=5)

    _txt_age_label = ctk.CTkLabel(_driver_frame, text="Age: init...", font=ctk.CTkFont(size=18))
    _txt_age_label.pack(anchor="w", padx=15, pady=5)
