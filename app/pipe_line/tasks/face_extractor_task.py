import time
import numpy as np
import app.pipe_line.signals as signals
from app.pipe_line.models.models import FaceExtractorTaskOutput
from mcal import logs

import mediapipe as mp
import app.pipe_line.timing as timing
from scheduler.task import Task


class FaceExtractorTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

        self.mp_face = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            static_image_mode=True,
            refine_landmarks=True
        )

    def update(self):
        # Get latest frame (non-blocking)
        lens_out = signals.lens_output_queue.get_last()

        if lens_out is None:
            return

        image = lens_out.clean_img
        h, w = image.shape[:2]

        with signals.gpu_yolo_lock:
            result = self.mp_face.process(image)

        if result.multi_face_landmarks:
            # Take only the first face
            face_landmarks = result.multi_face_landmarks[0]

            # Flatten landmarks into 2D numpy array

            face_array = np.array(
                [[lm.x, lm.y] for lm in face_landmarks.landmark], dtype=np.float32
            )

            face_rect_xyxy = (
                int(np.min(face_array[:, 0]) * w),  # X min
                int(np.min(face_array[:, 1]) * h),  # Y min
                int(np.max(face_array[:, 0]) * w),  # X max
                int(np.max(face_array[:, 1]) * h),  # Y max
            )

            # Put face array into the queue
            signals.face_extractor_queue.put(
                FaceExtractorTaskOutput(
                    img=image,
                    face_found=True,
                    face_points_matrix=face_array,
                    face_points_flattened=face_array.flatten(),
                    raw_land_marks=face_landmarks,
                    face_rect_xyxy=face_rect_xyxy
                )
            )
        else:
            # No face found → put None
            signals.face_extractor_queue.put(
                FaceExtractorTaskOutput(
                    img=image,
                    face_found=False,
                    face_points_matrix=None,
                    face_points_flattened=None,
                    raw_land_marks=None,
                    face_rect_xyxy=None,
                )
            )
