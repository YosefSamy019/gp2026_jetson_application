import datetime
from typing import List

from app.pipe_line.models.models import _SingleObjectsDetectorTaskOutput, ObjectsDetectorTaskOutput
from mcal import logs
import app.pipe_line.signals as signals
import time
import models.objects as objects
import app.pipe_line.timing as timing
from constants import look_up_keys
from network.models.models import ViolationDataModel
from scheduler.task import Task


class ObjectDetectorTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

    def update(self):

        lens_out = signals.lens_output_queue.get_last()
        trip_status = signals.trip_status_queue.get_last()

        if any(x is None for x in (trip_status, lens_out)):
            return

        with signals.gpu_yolo_lock:
            results = objects.objects_model(lens_out.clean_img)

        output_list: List[_SingleObjectsDetectorTaskOutput] = []

        for result in results:
            class_name = result['class']
            x1, y1, x2, y2 = result['box']
            score = result['score']

            output_list.append(
                _SingleObjectsDetectorTaskOutput(
                    object_name=class_name,
                    object_xyxy=(x1, y1, x2, y2),
                    object_probability=score
                )
            )

        signals.object_detector_yolo_queue.put(
            ObjectsDetectorTaskOutput(
                objects_list=output_list,
                any_gun_detected=any([x.object_name == 'gun' for x in output_list]),
                any_cellphone_detected=any([x.object_name == 'cellphone' for x in output_list]),
                any_food_detected=any([x.object_name == 'food' for x in output_list]),
                any_smoke_detected=any([x.object_name == 'smoke' for x in output_list]),
            )
        )
