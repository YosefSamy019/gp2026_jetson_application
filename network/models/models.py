import datetime
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ViolationDataModel:
    create_time: datetime.datetime
    image: np.ndarray
    violation_type: str


@dataclass(frozen=True)
class MCUNetworkDataModel:
    T: float
    F: float
    A: float
    buffer: str
    last_receive_time: float
    time_gone_from_last_receive: float
    slave_active: bool
