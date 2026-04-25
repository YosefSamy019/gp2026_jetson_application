import models.eye as eye
import models.head_pose as head_pose
import models.objects as objects
import models.seatbelt as seatbelt
import models.yawing as yawing
import onnxruntime as ort
import mcal.logs as logs
import cv2


def models_init():
    _init_cv2()
    _init_onnx()

    eye.init()
    # face_model.init()
    head_pose.init()
    objects.init()
    seatbelt.init()
    yawing.init()


def _init_onnx():
    for item in ort.get_available_providers():
        logs.add_log("ONNX detected {}".format(item), logs.LogLevel.INFO)


def _init_cv2():
    count = cv2.cuda.getCudaEnabledDeviceCount()
    if count > 0:
        logs.add_log(f"OpenCV GPU is active! Found {count} CUDA device(s).", logs.LogLevel.INFO)
    else:
        logs.add_log("OpenCV is running on CPU only.", logs.LogLevel.INFO)
