import numpy as np
import pandas as pd
import re
from assets.head_pose_model_function.model_function import score
import constants.assets_manager as assets_manager

selected_features = None

HEAD_POSE_CLS = ['front', 'right', 'left']


def init():
    global selected_features
    with open(assets_manager.HEAD_POSE_POINTS_PATH, "r", encoding="utf-8") as f:
        # remove empty lines
        selected_features = [line.strip().lower() for line in f.readlines() if line.strip()]


def normalize(face_vector):
    # Reshape to Nx2
    points = face_vector.reshape(-1, 2).copy()  # writable

    # Remove position (translation invariance)
    centroid = points.mean(axis=0)
    points -= centroid

    # Remove scale (size invariance)
    max_dist = np.linalg.norm(points, axis=1).max()
    points /= max_dist

    # Flatten back to 1D
    normalized_vector = points.flatten()

    return normalized_vector


def head_pose_model(face_mesh):
    global selected_features
    features = []

    indices = [int(re.findall(r'\d+', f)[0]) * 2 + (0 if f.startswith('x') else 1) for f in selected_features]

    features = [face_mesh[i] if i < len(face_mesh) else 0.0 for i in indices]

    df = pd.DataFrame([features])

    # Predict
    x_input = np.array(features).ravel()
    x_input = x_input.copy()
    x_input = x_input.ravel()  # shape: (N,)
    x_norm = normalize(x_input)  # shape: (N,)
    pred_probs = score(x_norm)

    class_number = int(np.argmax(pred_probs))

    cur_class = HEAD_POSE_CLS[class_number]
    cur_prop = np.max(pred_probs)

    return cur_class, cur_prop
