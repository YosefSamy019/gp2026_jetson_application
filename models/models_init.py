import models.eye as eye
import models.head_pose as head_pose
import models.objects as objects
import models.seatbelt as seatbelt
import models.yawing as yawing


def models_init():
    eye.init()
    # face_model.init()
    head_pose.init()
    objects.init()
    seatbelt.init()
    yawing.init()
