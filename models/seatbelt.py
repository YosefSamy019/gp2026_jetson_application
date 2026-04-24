from typing import Optional

import numpy as np
from models.base_yolo import YOLODetector
import constants.assets_manager as assets_manager

_seatbelt_yolo: Optional[YOLODetector] = None


def init():
    global _seatbelt_yolo
    # _seatbelt_yolo = YOLODetector(
    #     model_path=assets_manager.SEATBELT_YOLO_MODEL_PATH,
    #     classes_path=assets_manager.SEATBELT_YOLO_CLASSES_PATH,
    # )


def seatbelt_model(image: np.ndarray):
    global _seatbelt_yolo
    return []

    # detections = _seatbelt_yolo(image)
    # return detections
