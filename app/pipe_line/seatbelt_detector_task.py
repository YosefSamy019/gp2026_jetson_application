from mcal import logs
import app.pipe_line.signals as signals

import time
import models.seatbelt as seatbelt
import app.pipe_line.timing as timing

import app.look_up_keys as look_up_keys


def seatbelt_detector_task():
    previous_trip_status = None
    can_use_violation_queue = 1
    SEATBELT_THRESHOLD_SECONDS = 3
    SEATBELT_THRESHOLD_VIOLATIONS_SECONDS = 10

    seatbelt_start = None

    while True:

        with_seatbelt_flag = False
        without_seatbelt_flag = False
        all_with_seatbelt_list = []
        all_without_seatbelt_list = []

        try:
            frame = signals.lens_output_queue.get()["processed_img"]

            trip_status = signals.trip_status_queue.get()

            if trip_status != previous_trip_status and trip_status != 0:
                can_use_violation_queue = 1
                previous_trip_status = trip_status

            with signals.gpu_yolo_lock:
                results = seatbelt.seatbelt_model(frame)

            for result in results:
                class_name = result['class']
                x1, y1, x2, y2 = result['box']
                score = result['score']

                with_seatbelt_flag = with_seatbelt_flag or (class_name == "seatbelt")
                without_seatbelt_flag = without_seatbelt_flag or (
                        class_name == "no seat belt" or class_name == "no seatbelt")

                if class_name == "seatbelt":
                    all_with_seatbelt_list.append({
                        "class": class_name,
                        "x1": int(x1),
                        "y1": int(y1),
                        "x2": int(x2),
                        "y2": int(y2),
                        "score": score
                    })
                elif class_name == "no seatbelt" or class_name == "no seat belt":
                    all_without_seatbelt_list.append({
                        "class": "no seatbelt",
                        "x1": int(x1),
                        "y1": int(y1),
                        "x2": int(x2),
                        "y2": int(y2),
                        "score": score
                    })

                if without_seatbelt_flag:
                    logs.add_log("Someone without seatbelt has been detected", logs.LogLevel.WARNING)
                if class_name == "no seatbelt" or class_name == "no seat belt":
                    if seatbelt_start is None:
                        seatbelt_start = time.time()

                    if time.time() - seatbelt_start >= SEATBELT_THRESHOLD_SECONDS:
                        signals.speaker_queue.put(look_up_keys.KEY_DRIVER_SEATBELT)

                    if time.time() - seatbelt_start >= SEATBELT_THRESHOLD_VIOLATIONS_SECONDS:
                        if can_use_violation_queue == 1:
                            signals.violations_queue.put({
                                "time": time.time(),
                                "image": frame,
                                "class": "no seatbelt"
                            })

                            can_use_violation_queue = 0
                else:
                    seatbelt_start = None

            signals.seatbelt_detector_yolo_queue.put(
                {
                    "all_with_seatbelt_list": all_with_seatbelt_list,
                    "all_without_seatbelt_list": all_without_seatbelt_list,
                    "with_seatbelt_flag": with_seatbelt_flag,
                    "without_seatbelt_flag": without_seatbelt_flag,
                    "no_boxes_detected": len(all_with_seatbelt_list) + len(all_without_seatbelt_list) == 0,
                })

        except Exception as e:
            raise e
            logs.add_log(f"seatbelt_detector_task: error {e}", logs.LogLevel.ERROR)

        time.sleep(timing.SEATBELT_DETECTOR_TASK_SLEEP_TIME)
