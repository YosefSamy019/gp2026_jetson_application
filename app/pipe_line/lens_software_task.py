from mcal import logs
import app.pipe_line.signals as signals
import time
import cv2
import app.pipe_line.timing as timing


def lens_software_task():
    while True:
        try:
            raw_img = signals.camera_output_queue.get()["raw_img"]

            frame = cv2.flip(raw_img, 1)

            # todo missing [DIP]

            signals.lens_output_queue.put({
                "raw_img": raw_img,
                "processed_img": frame,
            })

        except Exception as e:
            logs.add_log(f"lens_software_task: error {e}", logs.LogLevel.ERROR)

        time.sleep(timing.LENS_TASK_SLEEP_TIME)
