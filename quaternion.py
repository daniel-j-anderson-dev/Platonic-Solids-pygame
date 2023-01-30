import math

class Quaternion:

    def __init__(self, *args):
        
        # __init__(self, q) copy contructor
        if len(args) == 1:
            q = args[0]
            self.w = q.w
            self.x = q.x
            self.y = q.y
            self.z = q.z

        # __init__(self, axis, angle) axis angle -> quat
        elif len(args) == 2:
            angle       = math.radians(args[1])
            axis        = args[0]
            self.w      =       1 * math.cos(angle/2)
            self.x      = axis[0] * math.sin(angle/2)
            self.y      = axis[1] * math.sin(angle/2)
            self.z      = axis[2] * math.sin(angle/2)

        # __init__(self, x, y, z) point -> quat
        elif len(args) == 3:
            self.w = 0
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]

        # __init__(self, w, x, y, z) components of quat -> quat
        elif len(args) == 4: 
            self.w = args[0]
            self.x = args[1]
            self.y = args[2]
            self.z = args[3]


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