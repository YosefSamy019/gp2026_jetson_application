from mcal import logs
import app.pipe_line.signals as signals
import time
import models.objects as objects
import app.pipe_line.timing as timing
import app.look_up_keys as look_up_keys
from scheduler.task import Task


class ObjectDetectorTask(Task):
    def __init__(self):
        super().__init__(
            name='ObjectDetectorTask',
            periodicity=timing.OBJECTS_DETECTOR_TASK_SLEEP_TIME
        )

    def start(self):
        self.previous_trip_status = None
        self.can_use_violation_queue_for_cellphone = 1
        self.can_use_violation_queue_for_smoke = 1
        self.can_use_violation_queue_for_food = 1

    def update(self):
        frame = signals.lens_output_queue.get()["processed_img"]

        trip_status = signals.trip_status_queue.get()
        if trip_status != self.previous_trip_status and trip_status != 0:
            self.can_use_violation_queue_for_cellphone = 1
            self.can_use_violation_queue_for_smoke = 1
            self.can_use_violation_queue_for_food = 1
            self.previous_trip_status = trip_status

        with signals.gpu_yolo_lock:
            results = objects.objects_model(frame)

        output_list = []

        for result in results:
            class_name = result['class']
            x1, y1, x2, y2 = result['box']
            score = result['score']

            output_list.append({
                "class": class_name,
                "x1": int(x1),
                "y1": int(y1),
                "x2": int(x2),
                "y2": int(y2),
                "score": score,
            })

            if class_name == "gun":
                signals.speaker_queue.put(look_up_keys.KEY_WEAPON_DETECTED)

                signals.violations_queue.put({
                    "time": time.time(),
                    "image": frame,
                    "class": "gun"
                })

            if class_name == "cellphone":
                signals.speaker_queue.put(look_up_keys.KEY_DRIVER_USING_PHONE)

                if self.can_use_violation_queue_for_cellphone == 1:
                    signals.violations_queue.put({
                        "time": time.time(),
                        "image": frame,
                        "class": "cellphone"
                    })
                    self.can_use_violation_queue_for_cellphone = 0

            if class_name == "smoke":
                signals.speaker_queue.put(look_up_keys.KEY_DRIVER_SMOKING)
                if self.can_use_violation_queue_for_smoke == 1:
                    signals.violations_queue.put({
                        "time": time.time(),
                        "image": frame,
                        "class": "smoke"
                    })
                    self.can_use_violation_queue_for_smoke = 0

            if class_name == "food":
                signals.speaker_queue.put(look_up_keys.KEY_DRIVER_FOOD)
                if self.can_use_violation_queue_for_food == 1:
                    signals.violations_queue.put({
                        "time": time.time(),
                        "image": frame,
                        "class": "food"
                    })
                    self.can_use_violation_queue_for_food = 0

            if class_name not in ["gun", "cellphone", "smoke", "food"]:
                logs.add_log(f"object_detector_task: class {class_name} not recognized", logs.LogLevel.ERROR)

        signals.object_detector_yolo_queue.put(
            {
                "value": output_list,
            })



