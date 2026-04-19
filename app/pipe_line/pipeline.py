import scheduler.scheduler as scheduler

from app.pipe_line.camera_task import camera_task
from app.pipe_line.face_clipper_recognizer import face_clipper_recognizer_task
from app.pipe_line.lens_software_task import lens_software_task
from app.pipe_line.seatbelt_detector_task import seatbelt_detector_task
from app.pipe_line.face_extractor_task import face_extractor_task
from app.pipe_line.drive_detector_task import driver_detector_task
from app.pipe_line.driver_tracker_task import driver_tracker_task
# from app.pipe_line.face_clipper_task import
from app.pipe_line.eye_open_close_task import eye_open_close_task
from app.pipe_line.yawing_task import yawing_task
from app.pipe_line.head_pose_task import head_pose_task
from app.pipe_line.speaker_task import speaker_task
from app.pipe_line.object_detector_task import object_detector_task


def pipeline_init():
    scheduler.create_task(camera_task, "Camera Task")
    scheduler.create_task(lens_software_task, "Lens Software Task")
    scheduler.create_task(object_detector_task, "Object Detector Task")
    scheduler.create_task(seatbelt_detector_task, "Seatbelt Detector Task")
    scheduler.create_task(face_extractor_task, "Face Extractor Task")
    scheduler.create_task(driver_detector_task, "Driver Detector Task")
    scheduler.create_task(driver_tracker_task, "Driver Tracker Task")
    scheduler.create_task(face_clipper_recognizer_task, "Face Clipper Recognizer Task")
    scheduler.create_task(eye_open_close_task, "Eye Open Close Task")
    scheduler.create_task(yawing_task, "Yawing Task")
    scheduler.create_task(head_pose_task, "Head Pose Task")
    scheduler.create_task(speaker_task, "Speaker Task")
