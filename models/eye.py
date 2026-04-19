import math
import constants.assets_manager as assets_manager

selected_indices = None


def init():
    global selected_indices

    with open(assets_manager.EYE_POINTS_PATH, "r", encoding="utf-8") as f:
        selected_feature = [str(line).strip().lower() for line in f.readlines()]
        selected_indices = [2 * int(feature[1:]) + int(feature[0] == 'y') for feature in selected_feature]


def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def eye_model(face_mesh):
    global selected_indices
    input_points = face_mesh[selected_indices]

    left_eye = [
        (input_points[0], input_points[1]),  # 33
        (input_points[2], input_points[3]),  # 160
        (input_points[4], input_points[5]),  # 158
        (input_points[6], input_points[7]),  # 133
        (input_points[8], input_points[9]),  # 153
        (input_points[10], input_points[11])  # 144
    ]

    # right eye: 362, 385, 387, 263, 373, 380
    right_eye = [
        (input_points[12], input_points[13]),  # 362
        (input_points[14], input_points[15]),  # 385
        (input_points[16], input_points[17]),  # 387
        (input_points[18], input_points[19]),  # 263
        (input_points[20], input_points[21]),  # 373
        (input_points[22], input_points[23])  # 380
    ]

    # calc EAR
    def ear(eye):
        A = euclidean_distance(*eye[1], *eye[5])
        B = euclidean_distance(*eye[2], *eye[4])
        C = euclidean_distance(*eye[0], *eye[3])
        return (A + B) / (2.0 * C)

    left_ear = ear(left_eye)
    right_ear = ear(right_eye)
    ear_avg = (left_ear + right_ear) / 2.0

    return ear_avg
