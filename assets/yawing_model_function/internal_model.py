
import math
import numpy as np

"""
Call "predict_yawing_prop(face_vector)" to get the yawing probability.
Call it every 100ms with the latest face vector.
"""

WINDOW_SIZE = int(2.5 * 1000 / 100)  # 2.5 seconds window

IMPORTANCE_VAL = np.linspace(1, 4, WINDOW_SIZE)
IMPORTANCE_VAL = IMPORTANCE_VAL / IMPORTANCE_VAL.sum()

_cache = []

def predict_yawing_prop(face_vector):
    global _cache

    prop = _sigmoid(_normalize(face_vector))
    
    _cache.append(prop)
    if len(_cache) > WINDOW_SIZE:
        _cache.pop(0)
    
    weighted_sum = sum(v * w for v, w in zip(_cache, IMPORTANCE_VAL))
    return weighted_sum

    
def _normalize(face_vector):
    points = face_vector.reshape(-1, 2)
    
    centroid = points.mean(axis=0)
    points = points - centroid

    max_dist = np.linalg.norm(points, axis=1).max()
    if max_dist > 1e-6:
        points = points / max_dist

    return points.flatten()


def _sigmoid(face_vector):
    z = _linear_score(face_vector)
    if z >= 0:
        ez = math.exp(-z)
        return 1.0 / (1.0 + ez)
    else:
        ez = math.exp(z)
        return ez / (1.0 + ez)


def _linear_score(input):
    return 0.7663650784293791 + input[0] * 0.8752545342622237 + input[1] * 0.6448711813119079 + input[2] * -1.11932795916674 + input[3] * -0.18446962400724984 + input[4] * 0.0757540125593169 + input[5] * -2.383871269315573 + input[6] * 0.1425316226100068 + input[7] * 2.07419149670325 + input[8] * 0.02477113595749623 + input[9] * -1.6564548224275055 + input[10] * 0.24127588460774024 + input[11] * 1.083237060390443 + input[12] * 0.8277973012732145 + input[13] * 0.5821683591474828 + input[14] * -1.0680565321032587 + input[15] * -0.1596723818027567

