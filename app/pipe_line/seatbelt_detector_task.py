from mcal import logs
import app.pipe_line.signals as signals

import time
import models.seatbelt as seatbelt
import app.pipe_line.timing as timing

import app.look_up_keys as look_up_keys
from scheduler.task import Task


class SeatbeltDetectorTask(Task):
    def __init__(self):
        super().__init__(
            name='SeatbeltDetectorTask',
            periodicity=timing.SEATBELT_DETECTOR_TASK_SLEEP_TIME
        )

    def start(self):
        self.previous_trip_status = None
        self.can_use_violation_queue = 1
        self.SEATBELT_THRESHOLD_SECONDS = 3
        self.SEATBELT_THRESHOLD_VIOLATIONS_SECONDS = 10
        self.seatbelt_start = None

    def update(self):
        with_seatbelt_flag = False
        without_seatbelt_flag = False
        all_with_seatbelt_list = []
        all_without_seatbelt_list = []

        frame = signals.lens_output_queue.get()["processed_img"]

        trip_status = signals.trip_status_queue.get()

        if trip_status != self.previous_trip_status and trip_status != 0:
            self.can_use_violation_queue = 1
            self.previous_trip_status = trip_status

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
                if self.seatbelt_start is None:
                    self.seatbelt_start = time.time()

                if time.time() - self.seatbelt_start >= self.SEATBELT_THRESHOLD_SECONDS:
                    signals.speaker_queue.put(look_up_keys.KEY_DRIVER_SEATBELT)

                if time.time() - self.seatbelt_start >= self.SEATBELT_THRESHOLD_VIOLATIONS_SECONDS:
                    if self.can_use_violation_queue == 1:
                        signals.violations_queue.put({
                            "time": time.time(),
                            "image": frame,
                            "class": "no seatbelt"
                        })

                        self.can_use_violation_queue = 0
            else:
                self.seatbelt_start = None

        signals.seatbelt_detector_yolo_queue.put(
            {
                "all_with_seatbelt_list": all_with_seatbelt_list,
                "all_without_seatbelt_list": all_without_seatbelt_list,
                "with_seatbelt_flag": with_seatbelt_flag,
                "without_seatbelt_flag": without_seatbelt_flag,
                "no_boxes_detected": len(all_with_seatbelt_list) + len(all_without_seatbelt_list) == 0,
            })
