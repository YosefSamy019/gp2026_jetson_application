from mcal import logs
import app.pipe_line.signals as signals
import time
import numpy as np
import app.pipe_line.timing as timing


def driver_tracker_task():
    last_x = None
    last_y = None

    while True:
        try:
            face_points_matrix = signals.driver_detector_queue.get()["face_points_matrix"]

            cur_frame_x = face_points_matrix[:,0] if face_points_matrix is not None else None
            cur_frame_y = face_points_matrix[:,1] if face_points_matrix is not None else None

            if last_x is not None and cur_frame_x is not None:
                last_pivot_x = np.mean(last_x)
                last_pivot_y = np.mean(last_y)

                cur_pivot_x = np.mean(cur_frame_x)
                cur_pivot_y = np.mean(cur_frame_y)

                dis = np.sqrt((cur_pivot_x - last_pivot_x) ** 2 + (cur_pivot_y - last_pivot_y) ** 2)

                # Todo Adjust the threshold
                if dis > 0.15:
                    signals.driver_tracker_queue.put({
                        "value": True,
                    })  # Detect the driver
                else:
                    signals.driver_tracker_queue.put({
                        "value": False,
                    })  # Dont Detect the driver

            else:
                signals.driver_tracker_queue.put({
                    "value": True,
                })  # Detect the driver

            last_x = cur_frame_x
            last_y = cur_frame_y

        except Exception as e:
            logs.add_log(f"driver_tracker: error {e}", logs.LogLevel.ERROR)

        time.sleep(timing.DRIVER_TRACKER_TASK_SLEEP_TIME)
