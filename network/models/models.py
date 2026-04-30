import datetime
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=False)
class ViolationDataModel:
    violation_type: str
    create_time: datetime.datetime = datetime.datetime.now()
    image: np.ndarray = None


@dataclass(frozen=True)
class MCUNetworkDataModel:
    T: float
    F: float
    A: float
    buffer: str
    last_receive_time: float
    time_gone_from_last_receive: float
    slave_active: bool
