import unittest
import math

def time_to_cyclic_features(time: float) -> (float, float):
    time = time % 24
    angle = 2 * math.pi * time / 24
    sin_time = math.sin(angle)
    cos_time = math.cos(angle)
    return sin_time, cos_time
