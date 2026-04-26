import scheduler.scheduler as scheduler

from app.pipe_line.camera_task import CameraTask
from app.pipe_line.face_clipper_recognizer import FaceClipperRecognizerTask
from app.pipe_line.lens_software_task import LensSoftwareTask
from app.pipe_line.seatbelt_detector_task import SeatbeltDetectorTask
from app.pipe_line.face_extractor_task import FaceExtractorTask
from app.pipe_line.drive_detector_task import DriverDetectorTask
from app.pipe_line.driver_tracker_task import DriverTrackerTask
from app.pipe_line.eye_open_close_task import EyeOpenCloseTask
from app.pipe_line.yawing_task import YawingTask
from app.pipe_line.head_pose_task import HeadPoseTask
from app.pipe_line.speaker_task import SpeakerDetectorTask
from app.pipe_line.object_detector_task import ObjectDetectorTask


def pipeline_init():
    scheduler.register_task(CameraTask())
    scheduler.register_task(LensSoftwareTask())
    scheduler.register_task(ObjectDetectorTask())
    scheduler.register_task(SeatbeltDetectorTask())
    scheduler.register_task(FaceExtractorTask())
    scheduler.register_task(DriverDetectorTask())
    scheduler.register_task(DriverTrackerTask())
    scheduler.register_task(FaceClipperRecognizerTask())
    scheduler.register_task(EyeOpenCloseTask())
    scheduler.register_task(YawingTask())
    scheduler.register_task(HeadPoseTask())
    scheduler.register_task(SpeakerDetectorTask())
