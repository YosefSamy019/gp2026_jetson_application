from typing import Optional

import numpy as np
from models.base_yolo import YOLODetector
import constants.assets_manager as assets_manager

_objects_model: Optional[YOLODetector] = None


def init():
    global _objects_model
    _objects_model = YOLODetector(
        model_path=assets_manager.OBJECTS_YOLO_MODEL_PATH,
        classes_path=assets_manager.OBJECTS_YOLO_CLASSES_PATH,
    )


def objects_model(image: np.ndarray):
    global _objects_model

    detections = _objects_model(image)
    return detections
