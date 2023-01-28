import pygame as pg
import math
import shape3d
import camera


class Renderer:

    def __init__(self):

        pg.init()
        self.WINDOW_SIZE = (1920, 1080)
        self.ORIGIN = [self.WINDOW_SIZE[0]//2, self.WINDOW_SIZE[1]//2, 0]
        self.FPS = 60
        self.screen = pg.display.set_mode(self.WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.shapes = []
        self.keys = pg.key.get_pressed()
        self.speed = 5
        self.delta_theta = 5
        self.camera = camera.Camera()

    def Platonic_Solids(self):

        return [shape3d.Cube([-700, -300, 0]), shape3d.Tetrahedron([-700, 300, 0]), shape3d.Dodecahedron([0, 0, 0]), shape3d.Icosahedron([700, -300, 0]), shape3d.Octahedron([700, 300, 0])]

    def rotate_point(self, point, axis, angle):

        angle = math.radians(angle)
        x, y, z = point[0], point[1], point[2]
        a, b, c, d = 1 * math.cos(angle/2), axis[0] * math.sin(
            angle/2), axis[1] * math.sin(angle/2), axis[2] * math.sin(angle/2)
        norm = math.sqrt(a*a + b*b + c*c + d*d)
        a /= norm
        b /= norm
        c /= norm
        d /= norm
        rotatedpoint = [(x*(1 - 2*c**2 - 2*d**2) + y*(2*b*c - 2*d*a) + z*(2*b*d + 2*c*a)),
                        (x*(2*b * c + 2*d*a) + y*(1 - 2*b**2 - 2*d**2) + z*(2*c*d - 2*b*a)),
                        (x*(2*b * d - 2*c*a) + y*(2*c*d + 2*b*a) + z*(1 - 2*b**2 - 2*c**2))]
        return rotatedpoint

    def rotate_point_about_another(self, point, centerOfRotation, axis, angle):

        angle = math.radians(angle)
        x, y, z = point[0] - centerOfRotation[0], point[1] - centerOfRotation[1], point[2] - centerOfRotation[2]
        a, b, c, d = 1 * math.cos(angle/2), axis[0] * math.sin(
            angle/2), axis[1] * math.sin(angle/2), axis[2] * math.sin(angle/2)
        norm = math.sqrt(a*a + b*b + c*c + d*d)
        a /= norm
        b /= norm
        c /= norm
        d /= norm
        rotatedpoint = [(x*(1 - 2*c**2 - 2*d**2) + y*(2*b*c - 2*d*a) + z*(2*b*d + 2*c*a)) + centerOfRotation[0],
                        (x*(2*b * c + 2*d*a) + y*(1 - 2*b**2 - 2*d**2) + z*(2*c*d - 2*b*a)) + centerOfRotation[1],
                        (x*(2*b * d - 2*c*a) + y*(2*c*d + 2*b*a) + z*(1 - 2*b**2 - 2*c**2)) + centerOfRotation[2]]
        return rotatedpoint

    def RotateShapes(self, axis, angle):

        for shape in self.shapes:
            rotated_vertices = []
            for vertex in shape.vertices:
                rotated_vertices.append(self.rotate_point(vertex, axis, angle))
            shape.vertices = rotated_vertices

    def RotateShapesLocal(self, axis, angle):

        for shape in self.shapes:
            rotated_vertices = []
            for vertex in shape.vertices:
                rotated_vertices.append(self.rotate_point_about_another(vertex, shape.position, axis, angle))
            shape.vertices = rotated_vertices

    def TranslateShapes(self, speed, index):
        for shape in self.shapes:
            shape.position[index] += speed

    def DrawShapes(self):

        self.screen.fill(pg.Color('white'))
        for shape in self.shapes:
            for edge in shape.edges:
                start_point = ((shape.position[0] + shape.vertices[edge[0]][0] + self.ORIGIN[0]),
                               (shape.position[1] - shape.vertices[edge[0]][1] + self.ORIGIN[1]))
                end_point   = ((shape.position[0] + shape.vertices[edge[1]][0] + self.ORIGIN[0]),
                               (shape.position[1] - shape.vertices[edge[1]][1] + self.ORIGIN[1]))
                pg.draw.line(self.screen, [0, 0, 0], start_point, end_point, 1)


    def Input(self):

        if self.keys[pg.K_i]:
            self.camera.position[0] += self.speed
        if self.keys[pg.K_k]:
            self.camera.position[0] -= self.speed
        if self.keys[pg.K_j]:
            self.camera.position[1] += self.speed
        if self.keys[pg.K_l]:
            self.camera.position[1] -= self.speed
        if self.keys[pg.K_0]:
            self.shapes = self.Platonic_Solids()                    # reset angles and pos

        if self.keys[pg.K_LEFT]:
            self.TranslateShapes(-self.speed, 0)  # TRANSLATE
        if self.keys[pg.K_RIGHT]:
            self.TranslateShapes(self.speed, 0)
        if self.keys[pg.K_DOWN]:
            self.TranslateShapes(self.speed, 1)
        if self.keys[pg.K_UP]:
            self.TranslateShapes(-self.speed, 1)
        if self.keys[pg.K_PAGEUP]:
            self.TranslateShapes(self.speed, 2)
        if self.keys[pg.K_PAGEDOWN]:
            self.TranslateShapes(-self.speed, 2)

        if not self.keys[pg.K_LSHIFT]:
            if self.keys[pg.K_s]:
                self.RotateShapes((1, 0, 0), -self.delta_theta)  # ROTATE
            if self.keys[pg.K_w]:
                self.RotateShapes((1, 0, 0),  self.delta_theta)
            if self.keys[pg.K_d]:
                self.RotateShapes((0, 1, 0), -self.delta_theta)
            if self.keys[pg.K_a]:
                self.RotateShapes((0, 1, 0),  self.delta_theta)
            if self.keys[pg.K_e]:
                self.RotateShapes((0, 0, 1), -self.delta_theta)
            if self.keys[pg.K_q]:
                self.RotateShapes((0, 0, 1),  self.delta_theta)
            if self.keys[pg.K_SPACE]:
                self.RotateShapes((1/math.sqrt(3), 1/math.sqrt(3), 1/math.sqrt(3)), self.delta_theta)

        else:
            if self.keys[pg.K_s]:
                self.RotateShapesLocal((1, 0, 0), -self.delta_theta)  # ROTATE
            if self.keys[pg.K_w]:
                self.RotateShapesLocal((1, 0, 0),  self.delta_theta)
            if self.keys[pg.K_d]:
                self.RotateShapesLocal((0, 1, 0), -self.delta_theta)
            if self.keys[pg.K_a]:
                self.RotateShapesLocal((0, 1, 0),  self.delta_theta)
            if self.keys[pg.K_e]:
                self.RotateShapesLocal((0, 0, 1), -self.delta_theta)
            if self.keys[pg.K_q]:
                self.RotateShapesLocal((0, 0, 1),  self.delta_theta)
            if self.keys[pg.K_SPACE]:
                self.RotateShapesLocal((1/math.sqrt(3), 1/math.sqrt(3), 1/math.sqrt(3)), self.delta_theta)

    def Handle_Events(self):

        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                pg.quit()
                exit()

    def Update(self):

        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()
        self.clock.tick(self.FPS)

    def Run(self):

        while True:

            self.keys = pg.key.get_pressed()
            self.Input()
            self.DrawShapes()
            self.Update()
            self.Handle_Events()


if __name__ == "__main__":
    program = Renderer()                          # init render
    program.shapes = program.Platonic_Solids()    # populate objects to be rendered
    program.Run()                                 # Render objects
