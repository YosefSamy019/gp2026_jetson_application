from app.pages.base.scrollable_nav_base_page import ScrollableNavigationBasePage

import customtkinter as ctk
import mcal.cache as cache


class SettingsPage(ScrollableNavigationBasePage):
    def __init__(self, parent, controller, loop_periodicity: float):
        super().__init__(parent, controller, loop_periodicity)

        ctk.CTkLabel(
            self.container,
            text="Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(padx=15, pady=(15, 10), anchor="w")

        # ----------------

        self.dark_light_switch = ctk.CTkSwitch(
            self.container,
            text="Dark / Light Mode",
            command=lambda: self._on_click()
        )
        self.dark_light_switch.pack(padx=15, pady=(5, 15), anchor="w")

        # ----------------

        self.font_size_label = ctk.CTkLabel(self.container, text="None",
                                            font=ctk.CTkFont(size=14, weight="bold"))
        self.font_size_label.pack(padx=15, pady=(10, 5), anchor="w")

        self.font_size_slider = ctk.CTkSlider(
            self.container,
            from_=0.3,
            to=1.5,
        )
        self.font_size_slider.bind("<ButtonRelease-1>", lambda e: self._on_click())
        self.font_size_slider.pack(padx=15, pady=(5, 15), anchor="w")

        # ----------------

        self.speaker_speed_label = ctk.CTkLabel(self.container, text=f"None",
                                                font=ctk.CTkFont(size=14, weight="bold"))
        self.speaker_speed_label.pack(padx=15, pady=(10, 5), anchor="w")

        self.speaker_speed_slider = ctk.CTkSlider(
            self.container,
            from_=100,
            to=200,
        )
        self.speaker_speed_slider.bind("<ButtonRelease-1>", lambda e: self._on_click())
        self.speaker_speed_slider.pack(padx=15, pady=(5, 15), anchor="w")

        # ----------------

        self.speaker_volume_label = ctk.CTkLabel(self.container,
                                                 text=f"None",
                                                 font=ctk.CTkFont(size=14, weight="bold"))
        self.speaker_volume_label.pack(padx=15, pady=(10, 5), anchor="w")

        self.speaker_volume_slider = ctk.CTkSlider(
            self.container,
            from_=0,
            to=1,
        )
        self.speaker_volume_slider.bind("<ButtonRelease-1>", lambda e: self._on_click())
        self.speaker_volume_slider.pack(padx=15, pady=(5, 15), anchor="w")

        self.speaker_volume_slider.get()

        # ----------------

        self._load_cache()

    def loop(self):
        pass

    def _load_cache(self, include_all=True):
        speaker_speed = cache.get_value('Speaker speed', fallback=150, return_type=float)
        speaker_volume = cache.get_value('speaker volume level', fallback=0.7, return_type=float)
        theme_mode = cache.get_value('sw mode', fallback=0, return_type=int)
        ui_scale = cache.get_value('ui scale', fallback=0.9, return_type=float)

        if theme_mode == 0:
            self.dark_light_switch.deselect()
        else:
            self.dark_light_switch.select()

        self.font_size_label.configure(text=f"Font Size ({ui_scale * 100:0.2f})")
        self.speaker_speed_label.configure(text=f"Speak Spead ({speaker_speed:0.2f})")
        self.speaker_volume_label.configure(text=f"Speak Volume ({speaker_volume:0.2f})")

        if include_all:
            self.font_size_slider.set(ui_scale)
            self.speaker_speed_slider.set(speaker_speed)
            self.speaker_volume_slider.set(speaker_volume)

    def _on_click(self):
        cache.set_value('Speaker speed', self.speaker_speed_slider.get())
        cache.set_value('speaker volume level', self.speaker_volume_slider.get())
        cache.set_value('sw mode', self.dark_light_switch.get())
        cache.set_value('ui scale', self.font_size_slider.get())
        self._load_cache(include_all=False)
        self.adjust_theme()
