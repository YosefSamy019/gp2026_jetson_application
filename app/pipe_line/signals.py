from network.models.models import ViolationDataModel, MCUNetworkDataModel
from scheduler.scheduler import register_queue, create_lock
from scheduler.items_queue import ItemsQueue, AttributeMonitor
from app.pipe_line.models.models import *

camera_output_queue: ItemsQueue[CameraTaskOutput] = register_queue(
    ItemsQueue[CameraTaskOutput](
        name='camera_output_queue', max_n_items=1))

lens_output_queue: ItemsQueue[LensTaskOutput] = register_queue(
    ItemsQueue[LensTaskOutput](name='lens_output_queue', max_n_items=1))

object_detector_yolo_queue: ItemsQueue[ObjectsDetectorTaskOutput] = register_queue(
    ItemsQueue[ObjectsDetectorTaskOutput](
        name='object_detector_yolo_queue',
        attribute_monitors=[
            AttributeMonitor('any_gun_detected'),
            AttributeMonitor('any_cellphone_detected'),
            AttributeMonitor('any_food_detected'),
            AttributeMonitor('any_smoke_detected'),
        ],
        max_n_items=1))

seatbelt_detector_yolo_queue: ItemsQueue[SeatbeltDetectorTaskOutput] = register_queue(
    ItemsQueue[SeatbeltDetectorTaskOutput](
        name='seatbelt_detector_yolo_queue',
        attribute_monitors=[AttributeMonitor('is_seatbelt_off'), AttributeMonitor('is_no_detection')],
        max_n_items=1))

face_extractor_queue: ItemsQueue[FaceExtractorTaskOutput] = register_queue(
    ItemsQueue[FaceExtractorTaskOutput](
        name='face_extractor_queue',
        attribute_monitors=[AttributeMonitor('face_found')],
        max_n_items=1))

driver_tracker_queue: ItemsQueue[DriverTrackerTaskOutput] = register_queue(
    ItemsQueue[DriverTrackerTaskOutput](name='driver_tracker_queue', max_n_items=1))

driver_detector_queue: ItemsQueue[DriverDetectorTaskOutput] = register_queue(
    ItemsQueue[DriverDetectorTaskOutput](name='driver_detector_queue', max_n_items=1))

face_clipper_recognizer_queue: ItemsQueue[FaceClipperRecognizerTaskOutput] = register_queue(
    ItemsQueue[FaceClipperRecognizerTaskOutput](
        name='face_clipper_recognizer_queue',
        attribute_monitors=[AttributeMonitor('driver_id')],
        max_n_items=1))

eye_open_close_queue: ItemsQueue[EyeOpenCloseTaskOutput] = register_queue(
    ItemsQueue[EyeOpenCloseTaskOutput](
        name='eye_open_close_queue',
        max_n_items=1,
        attribute_monitors=[AttributeMonitor('is_eye_close')]
    ))

yawing_queue: ItemsQueue[YawingTaskOutput] = register_queue(
    ItemsQueue[YawingTaskOutput](
        name='yawing_queue',
        attribute_monitors=[AttributeMonitor('is_yawing')],
        max_n_items=1))

head_pose_queue: ItemsQueue[HeadPoseTaskOutput] = register_queue(
    ItemsQueue[HeadPoseTaskOutput](
        name='head_pose_queue',
        attribute_monitors=[AttributeMonitor('is_front')],
        max_n_items=1))

face_recognition_queue: ItemsQueue[FaceClipperRecognizerTaskOutput] = register_queue(
    ItemsQueue[FaceClipperRecognizerTaskOutput](name='face_recognition_queue', max_n_items=1))

trip_status_queue: ItemsQueue[int] = register_queue(ItemsQueue[int](name='trip_status_queue', max_n_items=1))

speaker_queue: ItemsQueue[str] = register_queue(ItemsQueue[str](name='speaker_queue', max_n_items=None))

violations_queue: ItemsQueue[ViolationDataModel] = register_queue(
    ItemsQueue[ViolationDataModel](name='violations_queue', max_n_items=None))

mcu_network_queue: ItemsQueue[MCUNetworkDataModel] = register_queue(
    ItemsQueue[MCUNetworkDataModel](name='mcu_network_queue', max_n_items=None))

gpu_yolo_lock = create_lock('gpu_yolo_lock')
