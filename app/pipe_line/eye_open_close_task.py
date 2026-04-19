from mcal import logs
from scheduler.scheduler import *
import app.pipe_line.signals as signals
import models.eye as eye
import time
import app.pipe_line.timing as timing
import app.look_up_keys as look_up_keys


def eye_open_close_task():
    eye_closed_start = None
    DROWSY_THRESHOLD_SECONDS = 2
    eye_flag = 0

    while True:
        try:
            temp_vector = signals.driver_detector_queue.get()["face_points_flattened"]

            if temp_vector is not None:
                with signals.cpu_ml_lock:
                    ear_avg = eye.eye_model(temp_vector)

                # eye is close when (EAR < 0.25)
                eye_flag = (ear_avg < 0.25)

                signals.eye_open_close_queue.put({
                    "class": "Closed" if eye_flag else "Open",
                    "avg": ear_avg,
                    # TODO : will we pass eye close delta time ?!
                })

            if eye_flag:
                if eye_closed_start is None:
                    eye_closed_start = time.time()
                elif time.time() - eye_closed_start >= DROWSY_THRESHOLD_SECONDS:

                    signals.speaker_queue.put(look_up_keys.KEY_DRIVER_DROWSY)
            else:
                eye_closed_start = None



        except Exception as e:
            logs.add_log(f"eye_open_close_task: error {e}", logs.LogLevel.ERROR)

        time.sleep(timing.EYE_OPEN_CLOSE_TASK_SLEEP_TIME)
