import customtkinter as ctk
from app.pages.cache_page import CachePage
from app.pages.camera_page import CameraPage
from app.pages.driver_page import DriverPage
from app.pages.intro_page import IntroPage
from app.pages.logs_page import LogsPage
from app.pages.network_page import NetworkPage
from app.pages.scheduler_page import SchedulerPage
from app.pages.settings_page import SettingsPage
from app.pipe_line.pipeline import pipeline_init
from app.ui_constants import PagesKeys
import app.ui_constants as ui_constants
from mcal import cache


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._pipeline_status = False

        self.title('Smart Driver Monitor')
        self.geometry('600x500')

        self.load_theme()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = self._create_pages()
        self.current_page = self.pages[PagesKeys.IntroPage]

        for page_key, page in self.pages.items():
            page.grid(row=0, column=0, sticky="nsew")

        self.navigate_to(PagesKeys.IntroPage)

        self._engine()

    def load_theme(self):
        if cache.get_value('sw mode', 0, int) == 0:
            ctk.set_appearance_mode('light')
        else:
            ctk.set_appearance_mode('dark')

        ctk.set_default_color_theme('green')
        ctk.set_widget_scaling(cache.get_value('ui scale', 1.0, float))

    def _create_pages(self):
        return {
            PagesKeys.IntroPage: IntroPage(controller=self, parent=self.container,
                                           loop_periodicity=ui_constants.UI_INTRO_DELAY),

            PagesKeys.CameraPage: CameraPage(controller=self, parent=self.container,
                                             loop_periodicity=ui_constants.UI_CAMERA_DELAY),

            PagesKeys.CachePage: CachePage(controller=self, parent=self.container,
                                           loop_periodicity=ui_constants.UI_CACHE_DELAY),

            PagesKeys.DriverPage: DriverPage(controller=self, parent=self.container,
                                             loop_periodicity=ui_constants.UI_DRIVER_DELAY),

            PagesKeys.LogsPage: LogsPage(controller=self, parent=self.container,
                                         loop_periodicity=ui_constants.UI_LOGS_DELAY),

            PagesKeys.NetworkPage: NetworkPage(controller=self, parent=self.container,
                                               loop_periodicity=ui_constants.UI_NETWORK_DELAY),

            PagesKeys.SchedulerPage: SchedulerPage(controller=self, parent=self.container,
                                                   loop_periodicity=ui_constants.UI_SCHEDULER_DELAY),

            PagesKeys.SettingsPage: SettingsPage(controller=self, parent=self.container,
                                                 loop_periodicity=ui_constants.UI_SETTINGS_DELAY),
        }

    def navigate_to(self, page: PagesKeys):
        self.current_page = self.pages[page]
        self.pages[page].tkraise()

    def _engine(self):
        self.current_page.loop()
        # Convert Sec to m-Sec
        self.after(int(1000 * self.current_page.loop_periodicity), lambda: self._engine())

    def start_pipeline(self):
        if self._pipeline_status:
            return
        else:
            self._pipeline_status = True
            pipeline_init()


