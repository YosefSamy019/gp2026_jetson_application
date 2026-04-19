# import numpy as np
# import cv2
# import tensorflow as tf
#
# # -----------------------------
# FACE_NET_PATH = r"assets/face_net/facenet_int8.tflite"
# MIN_SIMILARITY_THRESHOLD: float = 0.85  # Adjust as needed
# model = None  # TFLite interpreter
# input_details = None
# output_details = None
#
#
# # -----------------------------
# def init():
#     global model, input_details, output_details, FACE_NET_PATH
#     model = tf.lite.Interpreter(model_path=FACE_NET_PATH)
#     model.allocate_tensors()
#     input_details = model.get_input_details()
#     output_details = model.get_output_details()
#
#
# def extract_face_vector(face_image: np.ndarray) -> np.ndarray:
#     # Resize to 160x160
#     face_resized = cv2.resize(face_image, (160, 160))
#
#     # Convert to float32 and normalize to 0-1
#     face_input = face_resized.astype(np.float32) / 255.0
#
#     # Add batch dimension
#     face_input = np.expand_dims(face_input, axis=0)
#
#     # Run inference
#     model.set_tensor(input_details[0]['index'], face_input)
#     model.invoke()
#     embedding = model.get_tensor(output_details[0]['index'])[0]
#
#     # L2 normalize
#     embedding = embedding / np.linalg.norm(embedding)
#
#     return embedding
#
#
# def compute_similarity(vector1: np.ndarray, vector2: np.ndarray) -> float:
#     v1 = vector1 / np.linalg.norm(vector1)
#     v2 = vector2 / np.linalg.norm(vector2)
#     return float(np.dot(v1, v2))
