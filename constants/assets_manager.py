import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _wrap_path(*p):
    abs_path = os.path.join(BASE_DIR, "assets", *p)
    return abs_path


INTRO_VIDEO_PATH = _wrap_path('intro.mp4')
LOOK_UP_TABLE_PATH = _wrap_path('look_up.json')

HEAD_POSE_POINTS_PATH = _wrap_path('head_pose_model_function', 'selected_features.txt')
YAWNING_POINTS_PATH = _wrap_path('yawing_model_function', 'selected_features.txt')
EYE_POINTS_PATH = _wrap_path('eye_model', 'points.txt')

OBJECTS_YOLO_MODEL_PATH = _wrap_path('objects_detection.onnx')
OBJECTS_YOLO_CLASSES_PATH = _wrap_path('objects_detection_classes.json')

SEATBELT_YOLO_MODEL_PATH = _wrap_path('seatbelt_detection.onnx')
SEATBELT_YOLO_CLASSES_PATH = _wrap_path('seatbelt_classes.json')
