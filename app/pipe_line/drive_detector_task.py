from mcal import logs
import app.pipe_line.signals as signals
import time
import app.look_up_keys as look_up_keys
import app.pipe_line.timing as timing


def driver_detector_task():
    while True:
        try:
            face_points_matrix = signals.face_extractor_queue.get()["face_points_matrix"]
            face_points_flattened = signals.face_extractor_queue.get()["face_points_flattened"]

            signals.driver_detector_queue.put({
                "face_points_matrix": face_points_matrix,
                "face_points_flattened": face_points_flattened,
            })

            if face_points_matrix is None:
                logs.add_log(f"Driver is not detected", logs.LogLevel.WARNING)
                signals.speaker_queue.put(look_up_keys.KEY_DRIVER_NOT_DETECTED)


        except Exception as e:
            logs.add_log(f"driver_detector: error {e}", logs.LogLevel.ERROR)

        time.sleep(timing.DRIVER_DETECT_TASK_SLEEP_TIME)
