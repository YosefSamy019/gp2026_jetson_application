import numpy as np

from app.pages.camera.components.base_component import OverlayComponent
import mediapipe as mp
import app.pipe_line.signals as signals


class FaceMeshComponent(OverlayComponent):

    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles


    def process_frame(self, frame: np.ndarray, **params) -> np.ndarray:
        face_extractor_out = signals.face_extractor_queue.get_last()

        if face_extractor_out is not None:
            self.mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_extractor_out.raw_land_marks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style(),
            )

        return frame
