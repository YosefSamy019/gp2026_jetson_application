import customtkinter as ctk

from mcal import cache


def show_settings_window(
        root: ctk.CTk,
        main_fram_hook: ctk.CTkScrollableFrame,
):
    switch_var = ctk.IntVar(value=cache.get_value('sw mode', 0, float))
    font_size_var = ctk.DoubleVar(value=cache.get_value('ui scale', 1, float))
    speaker_speed = ctk.IntVar(value=cache.get_value('speaker speed', 150, float))
    speaker_volume = ctk.DoubleVar(value=cache.get_value('speaker volume level', 0.1, float))

    def sw_on_change(_, __, ___):
        new_val = switch_var.get()
        ctk.set_appearance_mode('light' if new_val == 1 else 'dark')
        cache.set_value('sw mode', new_val)

    switch_var.trace_add("write", sw_on_change)

    # Header
    ctk.CTkLabel(
        main_fram_hook,
        text="Settings",
        font=ctk.CTkFont(size=18, weight="bold")
    ).pack(padx=15, pady=(15, 10), anchor="w")

    # Card container
    card = ctk.CTkFrame(
        main_fram_hook,
        corner_radius=12
    )
    card.pack(padx=15, pady=10, fill="x")
    card_2 = ctk.CTkFrame(
        main_fram_hook,
        corner_radius=12
    )
    card_2.pack(padx=15, pady=10, fill="x")

    card_3 = ctk.CTkFrame(
        main_fram_hook,
        corner_radius=12
    )
    card_3.pack(padx=15, pady=10, fill="x")

    # Card title
    ctk.CTkLabel(
        card,
        text="Appearance",
        font=ctk.CTkFont(size=14, weight="bold")

    ).pack(padx=15, pady=(15, 5), anchor="w")

    ctk.CTkSwitch(
        card,
        text="Dark / Light Mode",
        variable=switch_var
    ).pack(padx=15, pady=(5, 15), anchor="w")

    # Slider
    font_label = ctk.CTkLabel(card, text=f"Font Size ({font_size_var.get():0.2f})",
                              font=ctk.CTkFont(size=14, weight="bold"))
    font_label.pack(padx=15, pady=(10, 5), anchor="w")

    font_label_speaker_speed = ctk.CTkLabel(card_2, text=f"Speaker Speed ({speaker_speed.get():0.2f})",
                              font=ctk.CTkFont(size=14, weight="bold"))
    font_label_speaker_speed.pack(padx=15, pady=(10, 5), anchor="w")

    font_label_speaker_volume = ctk.CTkLabel(card_3, text=f"Speaker Volume ({speaker_volume.get():0.2f})",
                                            font=ctk.CTkFont(size=14, weight="bold"))
    font_label_speaker_volume.pack(padx=15, pady=(10, 5), anchor="w")

    font_size_slider = ctk.CTkSlider(
        card,
        variable=font_size_var,
        from_=0.5,
        to=1.5,
        command=lambda _: font_label.configure(text=f"Font Size ({font_size_var.get():0.2f})")
    )
    font_size_slider.pack(padx=15, pady=(5, 15), anchor="w")

    speaker_speed_slider = ctk.CTkSlider(
        card_2,
        variable=speaker_speed,
        from_=100,
        to=200,
        command=lambda _: font_label_speaker_speed.configure(text=f"Speaker Speed ({speaker_speed.get():0.2f})")
    )
    speaker_speed_slider.pack(padx=15, pady=(5, 15), anchor="w")

    speaker_volume_slider = ctk.CTkSlider(
        card_3,
        variable=speaker_volume,
        from_=0,
        to=1,
        command=lambda _: font_label_speaker_volume.configure(text=f"Speaker Volume({speaker_volume.get():0.2f})")
    )
    speaker_volume_slider.pack(padx=15, pady=(5, 15), anchor="w")

    # Action to perform when finished sliding
    def on_slider_release(event):
        new_val = font_size_slider.get()
        ctk.set_widget_scaling(new_val)
        cache.set_value('ui scale', f"{new_val:0.2f}")

    # Bind mouse release event
    font_size_slider.bind("<ButtonRelease-1>", on_slider_release)


    # Action to perform when finished sliding
    def on_slider_speaker_speed(event):
        new_val = speaker_speed_slider.get()
        cache.set_value('speaker speed', f"{new_val:0.2f}")

    # Bind mouse release event
    speaker_speed_slider.bind("<ButtonRelease-1>", on_slider_speaker_speed)

    def on_slider_speaker_volume(event):
        new_val = speaker_volume_slider.get()
        cache.set_value('speaker volume level', f"{new_val:0.2f}")

    # Bind mouse release event
    speaker_volume_slider.bind("<ButtonRelease-1>", on_slider_speaker_volume)
