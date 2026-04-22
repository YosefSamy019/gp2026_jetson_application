import time
import numpy as np
import app.pipe_line.signals as signals
from mcal import logs

import mediapipe as mp
import app.pipe_line.timing as timing


def face_extractor_task():
    mp_face = mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1, static_image_mode=False, refine_landmarks=True
    )

    while True:
        try:
            # Get latest frame (non-blocking)
            image = signals.lens_output_queue.get()["processed_img"]

            with signals.gpu_yolo_lock:
                result = mp_face.process(image)

            if result.multi_face_landmarks:
                # Take only the first face
                face_landmarks = result.multi_face_landmarks[0]

                # Flatten landmarks into 2D numpy array

                face_array = np.array(
                    [[lm.x, lm.y] for lm in face_landmarks.landmark], dtype=np.float32
                )

                # Put face array into the queue
                signals.face_extractor_queue.put(
                    {
                        "face_points_matrix": face_array,
                        "face_points_flattened": face_array.flatten(),
                        "raw_land_marks": face_landmarks
                    })
            else:
                # No face found → put None
                signals.face_extractor_queue.put(
                    {
                        "face_points_matrix": None,
                        "face_points_flattened": None,
                        "raw_land_marks": None
                    })

        except Exception as e:
            logs.add_log(f"face_extractor_task: error {e}", logs.LogLevel.ERROR)

        time.sleep(timing.FACE_EXTRACTOR_TASK_SLEEP_TIME)
