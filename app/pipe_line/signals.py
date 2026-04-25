from scheduler.scheduler import *

camera_output_queue = create_queue('camera_output_queue', False)
lens_output_queue = create_queue('lens_output_queue', False)
object_detector_yolo_queue = create_queue('object_detector_yolo_queue', False)
seatbelt_detector_yolo_queue = create_queue('seatbelt_detector_yolo_queue', False)
face_extractor_queue = create_queue('face_extractor_queue', False)
driver_tracker_queue = create_queue('driver_tracker_queue', False)
driver_detector_queue = create_queue('driver_detector_queue', True)
face_clipper_recognizer_queue = create_queue('face_clipper_recognizer_queue', False)
eye_open_close_queue = create_queue('eye_open_close_queue', False)
yawing_queue = create_queue('yawing_queue', False)
head_pose_queue = create_queue('head_pose_queue', False)
face_recognition_queue = create_queue('head_pose_queue', True)  # Todo Revise this
trip_status_queue = create_queue('trip_status_queue', False)

speaker_queue = create_list_queue('speaker_queue')
violations_queue = create_list_queue('violations_queue')

mcu_network_queue = create_queue('mcu_network_queue', False)

gpu_yolo_lock = create_lock('gpu_yolo_lock')
cpu_ml_lock = create_lock('cpu_ml_lock')
