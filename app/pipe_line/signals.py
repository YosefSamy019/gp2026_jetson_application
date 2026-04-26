from scheduler.scheduler import register_queue, create_lock
from scheduler.items_queue import ItemsQueue

camera_output_queue: ItemsQueue = register_queue(ItemsQueue(name='camera_output_queue', max_n_items=1))

lens_output_queue: ItemsQueue = register_queue(ItemsQueue(name='lens_output_queue', max_n_items=1))

object_detector_yolo_queue: ItemsQueue = register_queue(ItemsQueue(name='object_detector_yolo_queue', max_n_items=1))

seatbelt_detector_yolo_queue: ItemsQueue = register_queue(
    ItemsQueue(name='seatbelt_detector_yolo_queue', max_n_items=1))

face_extractor_queue: ItemsQueue = register_queue(ItemsQueue(name='face_extractor_queue', max_n_items=1))

driver_tracker_queue: ItemsQueue = register_queue(ItemsQueue(name='driver_tracker_queue', max_n_items=1))

driver_detector_queue: ItemsQueue = register_queue(ItemsQueue(name='driver_detector_queue', max_n_items=1))

face_clipper_recognizer_queue: ItemsQueue = register_queue(
    ItemsQueue(name='face_clipper_recognizer_queue', max_n_items=1))

eye_open_close_queue: ItemsQueue = register_queue(ItemsQueue(name='eye_open_close_queue', max_n_items=1))

yawing_queue: ItemsQueue = register_queue(ItemsQueue(name='yawing_queue', max_n_items=1))

head_pose_queue: ItemsQueue = register_queue(ItemsQueue(name='head_pose_queue', max_n_items=1))

face_recognition_queue: ItemsQueue = register_queue(ItemsQueue(name='face_recognition_queue', max_n_items=1))

trip_status_queue: ItemsQueue = register_queue(ItemsQueue(name='trip_status_queue', max_n_items=1))

speaker_queue: ItemsQueue = register_queue(ItemsQueue(name='speaker_queue', max_n_items=None))

violations_queue: ItemsQueue = register_queue(ItemsQueue(name='violations_queue', max_n_items=None))

mcu_network_queue: ItemsQueue = register_queue(ItemsQueue(name='mcu_network_queue', max_n_items=None))

gpu_yolo_lock = create_lock('gpu_yolo_lock')
