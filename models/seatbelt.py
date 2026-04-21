from typing import Optional
import numpy as np
from ultralytics import YOLO
import constants.assets_manager as assets_manager

_seatbelt_yolo: Optional[YOLO] = None


def init():
    global _seatbelt_yolo

    _seatbelt_yolo = YOLO(
        assets_manager.SEATBELT_YOLO_MODEL_PATH  # e.g. "seatbelt_best.pt"
    )


def seatbelt_model(image: np.ndarray):
    global _seatbelt_yolo

    results = _seatbelt_yolo(image,
                             conf=0.4,  # minimum confidence
                             iou=0.5,  # NMS threshold
                             imgsz=640  # or 416 for faster speed
                             )

    detections = []

    for r in results:
        boxes = r.boxes
        if boxes is None:
            continue

        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                'score': conf,
                "class": _seatbelt_yolo.names[cls_id],
                "box": [x1, y1, x2, y2]
            })

    return detections
