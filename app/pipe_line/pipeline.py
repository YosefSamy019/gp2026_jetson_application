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
    scheduler.create_task(CameraTask())
    scheduler.create_task(LensSoftwareTask())
    scheduler.create_task(ObjectDetectorTask())
    scheduler.create_task(SeatbeltDetectorTask())
    scheduler.create_task(FaceExtractorTask())
    scheduler.create_task(DriverDetectorTask())
    scheduler.create_task(DriverTrackerTask())
    scheduler.create_task(FaceClipperRecognizerTask())
    scheduler.create_task(EyeOpenCloseTask())
    scheduler.create_task(YawingTask())
    scheduler.create_task(HeadPoseTask())
    scheduler.create_task(SpeakerDetectorTask())
