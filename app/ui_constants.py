from enum import Enum


class PagesKeys(Enum):
    IntroPage = 1
    CameraPage = 2
    CachePage = 3
    DriverPage = 4
    LogsPage = 5
    NetworkPage = 6
    SchedulerPage = 7
    SettingsPage = 8


from enum import Enum


class RGBColor(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)

    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)
    BROWN = (165, 42, 42)

    LIME = (0, 255, 128)
    SKY_BLUE = (135, 206, 235)
    GOLD = (255, 215, 0)

    DARK_RED = (139, 0, 0)
    DARK_GREEN = (0, 100, 0)
    DARK_BLUE = (0, 0, 139)

    TEAL = (0, 128, 128)
    NAVY = (0, 0, 128)
    OLIVE = (128, 128, 0)


UI_INTRO_DELAY = 0.001
UI_CAMERA_DELAY = 0.010  # TODO check jitter delays
UI_CACHE_DELAY = 0.100
UI_DRIVER_DELAY = 0.100
UI_LOGS_DELAY = 0.100
UI_NETWORK_DELAY = 0.100
UI_SCHEDULER_DELAY = 0.050
UI_SETTINGS_DELAY = 0.100
