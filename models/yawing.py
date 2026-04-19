from assets.yawing_model_function.internal_model import predict_yawing_prop
import constants.assets_manager as assets_manager

selected_indices = None


def init():
    global selected_indices
    with open(assets_manager.YAWNING_POINTS_PATH, "r") as f:
        selected_feature = [str(line).strip().lower() for line in f.readlines()]
        selected_indices = [2 * int(feature[1:]) + int(feature[0] == 'y') for feature in selected_feature]


def yawing_model(face_mesh):
    # Extract selected points for the model
    selected_points = face_mesh[selected_indices]

    #  prediction
    yawning_prob = predict_yawing_prop(selected_points)
    return yawning_prob
