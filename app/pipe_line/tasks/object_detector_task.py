import datetime
from typing import List

from app.pipe_line.models.models import _SingleObjectsDetectorTaskOutput, ObjectsDetectorTaskOutput
from mcal import logs
import app.pipe_line.signals as signals
import time
import models.objects as objects
import app.pipe_line.timing as timing
import app.look_up_keys as look_up_keys
from network.models.models import ViolationDataModel
from scheduler.task import Task


class ObjectDetectorTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

        self.previous_trip_status = None
        self.can_use_violation_queue_for_cellphone = 1
        self.can_use_violation_queue_for_smoke = 1
        self.can_use_violation_queue_for_food = 1

    def update(self):

        lens_out = signals.lens_output_queue.get_last()
        trip_status = signals.trip_status_queue.get_last()

        if any(x is None for x in (trip_status, lens_out)):
            return

        if trip_status != self.previous_trip_status and trip_status != 0:
            self.can_use_violation_queue_for_cellphone = 1
            self.can_use_violation_queue_for_smoke = 1
            self.can_use_violation_queue_for_food = 1
            self.previous_trip_status = trip_status

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

            if class_name == "gun":
                # TODO must pass a Dict
                signals.speaker_queue.put(look_up_keys.KEY_WEAPON_DETECTED)

                signals.violations_queue.put(
                    ViolationDataModel(
                        create_time=datetime.datetime.now(),
                        image=lens_out.clean_img,
                        violation_type=class_name
                    )
                )

            if class_name == "cellphone":
                signals.speaker_queue.put(look_up_keys.KEY_DRIVER_USING_PHONE)

                if self.can_use_violation_queue_for_cellphone == 1:
                    signals.violations_queue.put(
                        ViolationDataModel(
                            create_time=datetime.datetime.now(),
                            image=lens_out.clean_img,
                            violation_type=class_name
                        )
                    )
                    self.can_use_violation_queue_for_cellphone = 0

            if class_name == "smoke":
                signals.speaker_queue.put(look_up_keys.KEY_DRIVER_SMOKING)

                if self.can_use_violation_queue_for_smoke == 1:
                    signals.violations_queue.put(
                        ViolationDataModel(
                            create_time=datetime.datetime.now(),
                            image=lens_out.clean_img,
                            violation_type=class_name
                        )
                    )
                    self.can_use_violation_queue_for_smoke = 0

            if class_name == "food":
                signals.speaker_queue.put(look_up_keys.KEY_DRIVER_FOOD)

                if self.can_use_violation_queue_for_food == 1:
                    signals.violations_queue.put(
                        ViolationDataModel(
                            create_time=datetime.datetime.now(),
                            image=lens_out.clean_img,
                            violation_type=class_name
                        )
                    )
                    self.can_use_violation_queue_for_food = 0

            if class_name not in ["gun", "cellphone", "smoke", "food"]:
                raise ValueError(f'class {class_name} not recognized')

        signals.object_detector_yolo_queue.put(
            ObjectsDetectorTaskOutput(
                objects_list=output_list
            )
        )
