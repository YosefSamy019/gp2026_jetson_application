import torch

import models.eye as eye
import models.head_pose as head_pose
import models.objects as objects
import models.seatbelt as seatbelt
import models.yawing as yawing
import mcal.logs as logs


def models_init():
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            logs.add_log(f"GPU {i}: {torch.cuda.get_device_name(i)}", logs.LogLevel.INFO)
    else:
        logs.add_log("No GPU found, using CPU", logs.LogLevel.WARNING)

    eye.init()
    # face_model.init()
    head_pose.init()
    objects.init()
    seatbelt.init()
    yawing.init()
