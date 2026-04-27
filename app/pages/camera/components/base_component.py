from abc import ABC, abstractmethod

import numpy as np


class OverlayComponent(ABC):

    @abstractmethod
    def process_frame(self, frame: np.ndarray, **params) -> np.ndarray:
        raise NotImplementedError()
