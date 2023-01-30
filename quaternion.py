import math

class Quaternion:


    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def axisAngle(axis, angle):
        angle  = math.radians(angle)
        w      =       1 * math.cos(angle/2)
        x      = axis[0] * math.sin(angle/2)
        y      = axis[1] * math.sin(angle/2)
        z      = axis[2] * math.sin(angle/2)
        return Quaternion(w, x, y, z)

    def __add__(self, other):
        return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Quaternion(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)

    def norm(self):
        return math.sqrt(self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z)

    def normalize(self):
        return Quaternion(self.w/self.norm(), self.x/self.norm(), self.y/self.norm(), self.z/self.norm())

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self):
        return Quaternion(self.conjugate().w / (self.norm() * self.norm()),
                          self.conjugate().x / (self.norm() * self.norm()),
                          self.conjugate().y / (self.norm() * self.norm()),
                          self.conjugate().z / (self.norm() * self.norm()))

    def __mul__(self, other):
        return Quaternion(self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z,
                          self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y,
                          self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x,
                          self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w)