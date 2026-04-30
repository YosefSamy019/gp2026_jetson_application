from constants import look_up_keys
from network.models.models import ViolationDataModel
from scheduler.task import Task
import app.pipe_line.signals as signals


class ObserverTask(Task):

    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

    def update(self):
        self._observe_face_detection()
        self._observe_face_recognition()
        self._observe_eye_status()
        self._observe_head_pose()
        self._observe_yawing()
        self._observe_seatbelt()
        self._observe_objects()

    def _observe_face_detection(self):
        get_seconds, get_last_val = signals.face_extractor_queue.monitor_attribute('face_found')

        if get_seconds > 3 and get_last_val == False:
            signals.speaker_queue.put(look_up_keys.KEY_DRIVER_NOT_DETECTED)

    def _observe_face_recognition(self):
        get_seconds, get_last_val = signals.face_clipper_recognizer_queue.monitor_attribute('driver_id')

        if get_seconds < 0.1 and get_last_val is not None:
            signals.speaker_queue.put(look_up_keys.KEY_GREETING)

    def _observe_eye_status(self):
        get_seconds, get_last_val = signals.eye_open_close_queue.monitor_attribute('is_eye_close')

        if get_seconds > 5 and get_last_val == True:
            signals.speaker_queue.put(look_up_keys.KEY_DRIVER_DROWSY)

    def _observe_head_pose(self):
        get_seconds, get_last_val = signals.head_pose_queue.monitor_attribute('is_front')

        if get_seconds > 5 and get_last_val == False:
            signals.speaker_queue.put(look_up_keys.KEY_DRIVER_DISTRACTED)

    def _observe_yawing(self):
        get_seconds, get_last_val = signals.yawing_queue.monitor_attribute('is_yawing')

        if get_seconds > 5 and get_last_val == True:
            signals.speaker_queue.put(look_up_keys.KEY_DRIVER_DROWSY)

    def _observe_seatbelt(self):
        get_seconds, get_last_val = signals.seatbelt_detector_yolo_queue.monitor_attribute('is_seatbelt_off')

        if get_seconds > 1 and get_last_val == True:
            signals.speaker_queue.put(look_up_keys.KEY_DRIVER_SEATBELT)

        if get_seconds > 5 and get_last_val == True:
            signals.violations_queue.put(
                ViolationDataModel(
                    violation_type='Seatbelt off',
                )
            )

    def _observe_objects(self):
        any_gun_detected_get_seconds, any_gun_detected_get_last_val = signals.object_detector_yolo_queue.monitor_attribute(
            'any_gun_detected')
        any_cellphone_detected_get_seconds, any_cellphone_detected_get_last_val = signals.object_detector_yolo_queue.monitor_attribute(
            'any_cellphone_detected')
        any_food_detected_get_seconds, any_food_detected_get_last_val = signals.object_detector_yolo_queue.monitor_attribute(
            'any_food_detected')
        any_smoke_detected_get_seconds, any_smoke_detected_get_last_val = signals.object_detector_yolo_queue.monitor_attribute(
            'any_smoke_detected')

        # ------------------------------
        if any_gun_detected_get_seconds > 0.1 and any_gun_detected_get_last_val == True:
            signals.speaker_queue.put(look_up_keys.KEY_WEAPON_DETECTED)

        if any_cellphone_detected_get_seconds > 0.5 and any_cellphone_detected_get_last_val == True:
            signals.speaker_queue.put(look_up_keys.KEY_DRIVER_USING_PHONE)

        if any_food_detected_get_seconds > 0.5 and any_food_detected_get_last_val == True:
            signals.speaker_queue.put(look_up_keys.KEY_DRIVER_FOOD)

        if any_smoke_detected_get_seconds > 0.5 and any_smoke_detected_get_last_val == True:
            signals.speaker_queue.put(look_up_keys.KEY_DRIVER_SMOKING)

        # ------------------------------

        if any_gun_detected_get_seconds > 1 and any_gun_detected_get_last_val == True:
            signals.violations_queue.put(
                ViolationDataModel(
                    violation_type='Gun',
                )
            )

        if any_cellphone_detected_get_seconds > 1 and any_cellphone_detected_get_last_val == True:
            signals.violations_queue.put(
                ViolationDataModel(
                    violation_type='Cellphone',
                )
            )

        if any_food_detected_get_seconds > 5 and any_food_detected_get_last_val == True:
            signals.violations_queue.put(
                ViolationDataModel(
                    violation_type='Food',
                )
            )

        if any_smoke_detected_get_seconds > 1 and any_smoke_detected_get_last_val == True:
            signals.violations_queue.put(
                ViolationDataModel(
                    violation_type='Smoke',
                )
            )
