import models.eye as eye
import models.head_pose as head_pose
import models.objects as objects
import models.seatbelt as seatbelt
import models.yawing as yawing
import onnxruntime as ort
import mcal.logs as logs


def models_init():
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
