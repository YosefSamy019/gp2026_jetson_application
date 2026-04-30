import datetime

from app.pipe_line.models.models import SeatbeltDetectorTaskOutput
from constants import look_up_keys
from mcal import logs
import app.pipe_line.signals as signals

import time
import models.seatbelt as seatbelt
import app.pipe_line.timing as timing

from network.models.models import ViolationDataModel
from scheduler.task import Task


class SeatbeltDetectorTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

    def update(self):
        lens_out = signals.lens_output_queue.get_last()
        trip_status = signals.trip_status_queue.get_last()

        if any(x is None for x in (trip_status, lens_out)):
            return

        with signals.gpu_yolo_lock:
            results = seatbelt.seatbelt_model(lens_out.clean_img)

        candidate_result = self.get_candidate_result(results, lens_out.clean_img.shape)

        if candidate_result is None:
            seatbelt_object_out = SeatbeltDetectorTaskOutput(
                is_seatbelt_on=None,
                is_seatbelt_off=None,
                probability=None,
                is_no_detection=True,
                object_xyxy=None
            )
        else:
            seatbelt_object_out = SeatbeltDetectorTaskOutput(
                is_seatbelt_on=candidate_result['class'] == "seatbelt",
                is_seatbelt_off=candidate_result['class'] != "seatbelt",
                probability=candidate_result['score'],
                is_no_detection=False,
                object_xyxy=candidate_result['box']
            )

        if seatbelt_object_out.is_seatbelt_off:
            logs.add_log("Someone without seatbelt has been detected", logs.LogLevel.WARNING)

        signals.seatbelt_detector_yolo_queue.put(
            seatbelt_object_out
        )

    def get_candidate_result(self, results, img_shape):
        img_cx = img_shape[1] / 2
        img_cy = img_shape[0] / 2
        best_result = None
        min_dist = float("inf")

        for result in results:
            class_name = result['class']
            x1, y1, x2, y2 = result['box']
            score = result['score']

            # center of bounding box
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            # distance to screen center
            dist = (cx - img_cx) ** 2 + (cy - img_cy) ** 2  # no need sqrt (faster)

            if dist < min_dist:
                min_dist = dist
                best_result = result

        return best_result
