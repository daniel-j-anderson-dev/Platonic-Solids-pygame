import pygame as pg
import math
import numpy as np
import camera
PHI = ((1 + math.sqrt(5)) / 2)
SCALE = 100


class Shape3D:
    def __init__(self, vertices, edges, name, position):
        self.vertices = vertices
        self.edges = edges
        self.position = position
        self.name = name

class Tetrahedron(Shape3D):
    def __init__(self, position):
        vertices = [[SCALE, SCALE, SCALE], [-SCALE, -SCALE, SCALE],
                    [-SCALE, SCALE, -SCALE], [SCALE, -SCALE, -SCALE]]
        edges = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
        # for vertex in vertices:
#             vertex[2] += SCALE
        super().__init__(vertices, edges, "Tetrahedron", position)


class Cube(Shape3D):
    def __init__(self, position):
        vertices = [[SCALE, SCALE, SCALE], [SCALE, SCALE, -SCALE], [SCALE, -SCALE, SCALE], [SCALE, -SCALE, -SCALE],
                    [-SCALE, SCALE, SCALE], [-SCALE, SCALE, -SCALE], [-SCALE, -SCALE, SCALE], [-SCALE, -SCALE, -SCALE]]
        edges = [[0, 1], [0, 2], [0, 4], [1, 3], [1, 5], [2, 3],
                 [2, 6], [3, 7], [4, 5], [4, 6], [5, 7], [6, 7]]
        # for vertex in vertices:
#             vertex[2] += SCALE
        super().__init__(vertices, edges, "Cube", position)


class Square(Shape3D):
    def __init__(self, position=[0, 0, 0]):  # [-700, -300, 0]):
        vertices = [[SCALE, SCALE, 0], [-SCALE, -SCALE, 0],
                    [-SCALE, SCALE, 0], [SCALE, -SCALE, 0]]
        edges = [[0, 2], [0, 3], [1, 2], [1, 3]]
        super().__init__(vertices, edges, "Square", position)


class Dodecahedron(Shape3D):
    def __init__(self, position):
        vertices = [[SCALE, SCALE, SCALE], [SCALE, SCALE, -SCALE], [SCALE, -SCALE, SCALE], [SCALE, -SCALE, -SCALE],
                    [-SCALE, SCALE, SCALE], [-SCALE, SCALE, -SCALE], [-SCALE, -SCALE, SCALE], [-SCALE, -SCALE, -SCALE],
                    [0, SCALE/PHI, SCALE*PHI], [0, SCALE/PHI, -SCALE*PHI], [0, -SCALE /PHI, SCALE*PHI], [0, -SCALE/PHI, -SCALE*PHI],
                    [SCALE/PHI, SCALE*PHI, 0], [SCALE/PHI, -SCALE*PHI, 0], [-SCALE/PHI, SCALE*PHI, 0], [-SCALE/PHI, -SCALE*PHI, 0],
                    [SCALE*PHI, 0, SCALE/PHI], [SCALE*PHI, 0, -SCALE/PHI], [-SCALE*PHI, 0, SCALE/PHI], [-SCALE*PHI, 0, -SCALE/PHI]]
        edges = [[0, 8], [0, 12], [0, 16], [1, 9], [1, 12], [1, 17], [2, 10], [2, 13], [2, 16], [3, 11], [3, 13], [3, 17], [4, 8], [4, 14], [4, 18], [
            5, 9], [5, 14], [5, 19], [6, 10], [6, 15], [6, 18], [7, 11], [7, 15], [7, 19], [8, 10], [9, 11], [12, 14], [13, 15], [16, 17], [18, 19]]
        # for vertex in vertices:
#             vertex[2] += SCALE
        super().__init__(vertices, edges, "Dodecahedron", position)


class Icosahedron(Shape3D):
    def __init__(self, position):
        vertices = [[0, SCALE, SCALE*PHI], [0, SCALE, -SCALE*PHI], [0, -SCALE, SCALE*PHI], [0, -SCALE, -SCALE*PHI], [SCALE, SCALE*PHI, 0], [SCALE, -SCALE*PHI, 0],
                    [-SCALE, SCALE*PHI, 0], [-SCALE, -SCALE*PHI, 0], [SCALE*PHI, 0, SCALE], [SCALE*PHI, 0, -SCALE], [-SCALE*PHI, 0, SCALE], [-SCALE*PHI, 0, -SCALE]]
        edges = [[0, 2], [0, 4], [0, 6], [0, 8], [0, 10], [1, 3], [1, 4], [1, 6], [1, 9], [1, 11], [2, 5], [2, 7], [2, 8], [2, 10], [3, 5], [
            3, 7], [3, 9], [3, 11], [4, 6], [4, 8], [4, 9], [5, 7], [5, 8], [5, 9], [6, 10], [6, 11],  [7, 10], [7, 11], [8, 9], [10, 11]]
        # for vertex in vertices:
#             vertex[2] += SCALE
        super().__init__(vertices, edges, "Icosahedron", position)


class Octahedron(Shape3D):
    def __init__(self, position):
        vertices = [[SCALE, 0, 0], [-SCALE, 0, 0], [0, SCALE, 0],
                    [0, -SCALE, 0], [0, 0, SCALE], [0, 0, -SCALE]]
        edges = [[0, 2], [0, 3], [0, 4], [0, 5], [1, 2], [1, 3],
                 [1, 4], [1, 5], [2, 4], [2, 5], [3, 4], [3, 5]]
        # for vertex in vertices:
#             vertex[2] += SCALE
        super().__init__(vertices, edges, "Octahedron", position)
