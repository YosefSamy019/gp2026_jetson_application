from dataclasses import dataclass
from typing import List, Tuple, Optional

import numpy as np


@dataclass(frozen=True)
class CameraTaskOutput:
    raw_img: np.ndarray


@dataclass(frozen=True)
class LensTaskOutput:
    clean_img: np.ndarray


@dataclass(frozen=True)
class FaceExtractorTaskOutput:
    img: np.ndarray
    face_found: bool
    face_points_matrix: Optional[np.ndarray]
    face_points_flattened: Optional[np.ndarray]
    raw_land_marks: Optional[np.ndarray]
    face_rect_xyxy: Optional[Tuple[int, int, int, int]]


@dataclass(frozen=True)
class DriverDetectorTaskOutput:
    img: np.ndarray
    face_found: bool
    face_points_matrix: Optional[np.ndarray]
    face_points_flattened: Optional[np.ndarray]
    raw_land_marks: Optional[np.ndarray]


@dataclass(frozen=True)
class EyeOpenCloseTaskOutput:
    is_eye_detected: bool
    ear_avg: Optional[float]
    is_eye_open: Optional[bool]
    is_eye_close: Optional[bool]


@dataclass(frozen=True)
class YawingTaskOutput:
    is_yawning_detected: bool
    is_yawing: Optional[bool]
    is_yawing_probability: Optional[float]


@dataclass(frozen=True)
class HeadPoseTaskOutput:
    is_head_detected: bool
    is_front: Optional[bool]
    is_right: Optional[bool]
    is_left: Optional[bool]
    probability: Optional[float]


@dataclass(frozen=True)
class DriverTrackerTaskOutput:
    driver_has_changed: bool


@dataclass(frozen=True)
class DriverTrackerTaskOutput:
    driver_candidate_id: int


@dataclass(frozen=True)
class FaceClipperRecognizerTaskOutput:
    driver_id: Optional[int]
    driver_name: Optional[str]
    driver_age: Optional[int]
    driver_image_url: Optional[str]


@dataclass(frozen=True)
class SeatbeltDetectorTaskOutput:
    is_seatbelt_on: Optional[bool]
    is_seatbelt_off: Optional[bool]
    probability: Optional[float]
    is_no_detection: bool
    object_xyxy: Optional[Tuple[int, int, int, int]]


@dataclass(frozen=True)
class _SingleObjectsDetectorTaskOutput:
    object_name: str
    object_xyxy: Tuple[int, int, int, int]
    object_probability: float


@dataclass(frozen=True)
class ObjectsDetectorTaskOutput:
    objects_list: List[_SingleObjectsDetectorTaskOutput]
