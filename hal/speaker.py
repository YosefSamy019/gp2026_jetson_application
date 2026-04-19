# Speaker TTS
import pyttsx3
from mcal import cache
#from typing import Optional


# engine: Optional[pyttsx3.Engine] = None


def init():
    pass
    # global engine
    # engine = pyttsx3.init()
    # engine.setProperty('rate', 150)  # Speech speed
    # engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)


def speaker(text):
    speaker_speed = cache.get_value('speaker speed', 150, float)
    speaker_volume = cache.get_value('speaker volume level', 0.1, float)

    engine = pyttsx3.init()
    engine.setProperty('rate', speaker_speed)  # Speech speed
    engine.setProperty('volume', speaker_volume)  # Volume level (0.0 to 1.0)

    engine.say(text)

    engine.runAndWait()
    engine.stop()
    engine.endLoop()
