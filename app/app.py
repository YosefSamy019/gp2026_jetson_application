import cv2
from PIL import Image, ImageTk
import customtkinter as ctk

import mcal.cache as cache

import app.upper_logic as up
import app.view.camera_view as camera_view
import app.view.logs_view as logs_view
import app.view.scheduler_view as scheduler_view
import app.view.network_tracer_view as network_tracer_view
import app.view.show_cache_view as cache_view
import app.view.setting_view as setting_view
import app.view.driver_view as driver_view
from mcal import logs
import constants.assets_manager as assets_manager

main_frame_hook: ctk.CTkScrollableFrame = None
root: ctk.CTk = None

display_cam_frame: ctk.BooleanVar = None

def play_intro(root, callback):
    splash = ctk.CTkFrame(root)
    splash.place(relx=0, rely=0, relwidth=1, relheight=1)
    splash.lift()

    video_label = ctk.CTkLabel(splash, text="")
    video_label.pack(expand=True, fill="both")

    cap = cv2.VideoCapture(assets_manager.INTRO_VIDEO_PATH)

    placeholder_img = ctk.CTkImage(
        light_image=Image.new("RGB", (10, 10)),
        dark_image=Image.new("RGB", (10, 10)),
        size=(10, 10)
    )

    video_label.configure(image=placeholder_img)
    video_label.image = placeholder_img

    def update_frame():
        ret, frame = cap.read()

        if not ret:
            cap.release()
            splash.destroy()
            callback()
            return

        w = max(root.winfo_width(), 1)
        h = max(root.winfo_height(), 1)

        frame = cv2.resize(frame, (w, h))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        pil_img = Image.fromarray(frame)

        img = ctk.CTkImage(
            light_image=pil_img,
            dark_image=pil_img,
            size=(w, h)
        )

        video_label.configure(image=img)
        video_label.image = img

        root.after(30, update_frame)

    update_frame()


def app_run():
    global root, main_frame_hook, main_frame_hook, display_cam_frame

    root = ctk.CTk()
    root.geometry('600x500')
    root.title('Smart Driver Monitor')

    def start_main_app():
        global root, main_frame_hook, main_frame_hook, display_cam_frame

        root.grid_columnconfigure(0, weight=9)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        display_cam_frame = ctk.BooleanVar()

        if bool(cache.get_value('sw mode', 0, float)):
            ctk.set_appearance_mode('light')
        else:
            ctk.set_appearance_mode('dark')

        ctk.set_default_color_theme('green')

        # ctk.set_window_scaling(cache.get_value('ui scale', 0, float))
        ctk.set_widget_scaling(cache.get_value('ui scale', 1, float))

        side_bar_frame = ctk.CTkScrollableFrame(
            root,
            width=160,
            corner_radius=12
        )

        main_frame = ctk.CTkScrollableFrame(
            root,
            corner_radius=12
        )

        main_frame_hook = main_frame

        main_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        side_bar_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        # Button 1
        sidebar_title = ctk.CTkLabel(
            side_bar_frame,
            text="Menu",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cam_btn = ctk.CTkButton(side_bar_frame, text='Show Camera', command=lambda: page_transition(camera_view))
        driver_btn = ctk.CTkButton(side_bar_frame, text='Driver', command=lambda: page_transition(driver_view))
        logs_btn = ctk.CTkButton(side_bar_frame, text='Show Logs', command=lambda: page_transition(logs_view))
        scheduler_btn = ctk.CTkButton(side_bar_frame, text='Open Scheduler',
                                      command=lambda: page_transition(scheduler_view))
        network_history_btn = ctk.CTkButton(side_bar_frame, text='Trace Network',
                                            command=lambda: page_transition(network_tracer_view))
        cache_btn = ctk.CTkButton(side_bar_frame, text='Show Cache', command=lambda: page_transition(cache_view))
        setting_btn = ctk.CTkButton(side_bar_frame, text='Setting', command=lambda: page_transition(setting_view))

        sidebar_title.pack(padx=10, pady=(15, 10))
        cam_btn.pack(padx=10, pady=(5, 5), fill='x')
        driver_btn.pack(padx=10, pady=(5, 5), fill='x')
        logs_btn.pack(padx=10, pady=5, fill='x')
        scheduler_btn.pack(padx=10, pady=5, fill='x')
        network_history_btn.pack(padx=10, pady=5, fill='x')
        cache_btn.pack(padx=10, pady=5, fill='x')
        setting_btn.pack(padx=10, pady=5, fill='x')

        # as initial
        up.upper_awake(root)

        cache_view.init()
        network_tracer_view.init()
        scheduler_view.init()
        logs_view.init()
        driver_view.init()

        page_transition(new_page=camera_view)

    play_intro(root, start_main_app)

    root.mainloop()


def page_transition(new_page):
    if new_page is camera_view:
        display_cam_frame.set(True)
    else:
        display_cam_frame.set(False)

    for widget in main_frame_hook.winfo_children():
        widget.destroy()

    if new_page is camera_view:
        camera_view.show_cam_window(
            root=root,
            main_fram_hook=main_frame_hook,
            display_cam_frame=display_cam_frame
        )

    elif new_page is driver_view:
        driver_view.show_driver_window(
            root=root,
            main_frame_hook=main_frame_hook,
        )

    elif new_page is logs_view:
        logs_view.show_logs_window(
            root=root,
            main_fram_hook=main_frame_hook,
        )

    elif new_page is scheduler_view:
        scheduler_view.show_scheduler_window(
            root=root,
            main_frame_hook=main_frame_hook,
        )

    elif new_page is network_tracer_view:
        network_tracer_view.show_network_history_window(
            root=root,
            main_frame_hook=main_frame_hook,
        )

    elif new_page is cache_view:
        cache_view.show_cache_window(
            root=root,
            main_frame_hook=main_frame_hook,
        )

    elif new_page is setting_view:
        setting_view.show_settings_window(
            root=root,
            main_fram_hook=main_frame_hook,

        )

    else:
        logs.add_log("Transition unhandled {}".format(new_page), logs.LogLevel.ERROR)
