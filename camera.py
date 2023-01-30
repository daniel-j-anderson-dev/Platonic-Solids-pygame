import quaternion
class Camera:
    def __init__(self):

        self.position     = [0, 0, 0]
        self.orientation  = quaternion.Quaternion.axisAngle([0, 0, 1], 0)
        self.viewportDist = 100

    def __init__(self, position):
        self.position = [position[0], position[1], position[2]]
        self.orientation  = quaternion.Quaternion.axisAngle([0, 0, 1], 0)
        self.viewportDist = 100

    # def __init__(self, position, orientation, viewportDist):
    #     self.position     = position
    #     self.orientation  = orientation
    #     self.viewportDist = viewportDist
