import numpy as np
import math


class Camera:
    def __init__(self):

        # The camera is on the negative z-axis
        self.position = [0, 0, -150]
        # The camera is pointing towards the positive z-axis
        self.direction = [0, 0, 1]
        # Y angle Field of view in degrees
        self.fovy = 45
        self.aspect_ratio = 1920/1080                               # HD aspect ratio
        # Distance from camera to near clipping plane
        self.dist_near = 150
        # Distance from camera to near clipping plane
        self.dist_far = 250
        self.getProjectionMatrix()

    # i need to convert these coords to the camera coord system
    def getProjectionMatrix(self):

        # fovy to radians
        fovy = math.radians(self.fovy)

        # near/far planes distances from camera
        n, f = self.dist_near, self.dist_far
        # top/bottom planes distances from camera
        t, b = n * math.tan(fovy / 2), -n * math.tan(fovy / 2)
        # right/left planes distances from camera
        r, l = t * self.aspect_ratio, b * self.aspect_ratio

        projection_matrix = np.array([
            [2*n/(r-l), 0,          (r+l)/(r-l),  0],
            [0,         2*n/(t-b),  (t+b)/(t-b),  0],
            [0,         0,         -(f+n)/(f-n), -2*f*n/(f-n)],
            [0,         0,         -1,            0]
        ])

        return projection_matrix
