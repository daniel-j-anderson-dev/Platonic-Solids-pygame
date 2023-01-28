import numpy as np
import math


class Camera:
    def __init__(self):

        # The camera is on the negative z-axis
        self.position = [0, 0, 0]
        # The camera is pointing towards the positive z-axis
        self.orientation = [0, 0, 0, 1]
        self.viewportDist = 100
