from typing import Optional
import numpy as np
from ultralytics import YOLO
import constants.assets_manager as assets_manager
from mcal import logs

_objects_model: Optional[YOLO] = None


def init():
    global _objects_model

    _objects_model = YOLO(
        assets_manager.OBJECTS_YOLO_MODEL_PATH  # e.g. "yolo11n.pt" or custom .pt
    )

    logs.add_log(f"Locate Objects Detection Model on ({_objects_model.device})", logs.LogLevel.INFO)


def objects_model(image: np.ndarray):
    global _objects_model

    results = _objects_model(image,
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
                "class": _objects_model.names[cls_id],
                "confidence": conf,
                "box": [x1, y1, x2, y2]
            })

    return detections
