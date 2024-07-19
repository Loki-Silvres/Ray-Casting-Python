import math
from settings import *

def normalizeAngle(angle):
    angle = angle % (2 * math.pi)
    if angle <= 0:
        angle = (2 * math.pi) + angle
    return angle