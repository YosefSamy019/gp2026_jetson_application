import scheduler.scheduler as scheduler
import app.pipe_line.timing as timing

from app.pipe_line.tasks.camera_task import CameraTask
from app.pipe_line.tasks.face_clipper_recognizer import FaceClipperRecognizerTask
from app.pipe_line.tasks.lens_software_task import LensSoftwareTask
from app.pipe_line.tasks.observer_task import ObserverTask
from app.pipe_line.tasks.seatbelt_detector_task import SeatbeltDetectorTask
from app.pipe_line.tasks.face_extractor_task import FaceExtractorTask
from app.pipe_line.tasks.drive_detector_task import DriverDetectorTask
from app.pipe_line.tasks.driver_tracker_task import DriverTrackerTask
from app.pipe_line.tasks.eye_open_close_task import EyeOpenCloseTask
from app.pipe_line.tasks.yawing_task import YawingTask
from app.pipe_line.tasks.head_pose_task import HeadPoseTask
from app.pipe_line.tasks.speaker_task import SpeakerDetectorTask
from app.pipe_line.tasks.object_detector_task import ObjectDetectorTask


def pipeline_init():
    scheduler.register_task(CameraTask(
        name='camera_task',
        periodicity=timing.CAMERA_TASK_SLEEP_TIME,
    ))

    scheduler.register_task(LensSoftwareTask(
        name='lens_software_task',
        periodicity=timing.LENS_TASK_SLEEP_TIME,
    ))

    scheduler.register_task(ObjectDetectorTask(
        name='object_detector_task',
        periodicity=timing.OBJECTS_DETECTOR_TASK_SLEEP_TIME,
    ))

    scheduler.register_task(SeatbeltDetectorTask(
        name='seatbelt_detector_task',
        periodicity=timing.SEATBELT_DETECTOR_TASK_SLEEP_TIME,
    ))

    scheduler.register_task(FaceExtractorTask(
        name='face_extractor_task',
        periodicity=timing.FACE_EXTRACTOR_TASK_SLEEP_TIME,
    ))

    scheduler.register_task(DriverDetectorTask(
        name='driver_detector_task',
        periodicity=timing.DRIVER_DETECT_TASK_SLEEP_TIME,
    ))

    scheduler.register_task(DriverTrackerTask(
        name='driver_tracker_task',
        periodicity=timing.DRIVER_TRACKER_TASK_SLEEP_TIME,
    ))

    scheduler.register_task(FaceClipperRecognizerTask(
        name='face_clipper_recognizer_task',
        periodicity=timing.FACE_CLIPPER_RECOGNIZE_TASK_SLEEP_TIME,
    ))

    scheduler.register_task(EyeOpenCloseTask(
        name='eye_open_close_task',
        periodicity=timing.EYE_OPEN_CLOSE_TASK_SLEEP_TIME,
    ))

    scheduler.register_task(YawingTask(
        name='yawing_task',
        periodicity=timing.YAWING_TASK_SLEEP_TIME,
    ))

    scheduler.register_task(HeadPoseTask(
        name='head_pose_task',
        periodicity=timing.HEAD_POSE_TASK_SLEEP_TIME,
    ))

    scheduler.register_task(SpeakerDetectorTask(
        name='speaker_detector_task',
        periodicity=timing.SPEAKER_TASK_SLEEP_TIME,
    ))

    scheduler.register_task(ObserverTask(
        name='Observer Task',
        periodicity=timing.OBSERVER_TASK,
    ))
