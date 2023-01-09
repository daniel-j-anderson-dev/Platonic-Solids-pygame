import pygame as pg
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

    def DrawPerspective(self):

        self.screen.fill(pg.Color('white'))
        for shape in self.shapes:
            shape.DrawPerspective(self.screen, self.camera, self.ORIGIN)

    def Draw(self):

        self.screen.fill(pg.Color('white'))
        for shape in self.shapes:
            shape.Draw(self.screen, self.ORIGIN)

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

        for shape in self.shapes:

            if self.keys[pg.K_LEFT]:
                shape.position[0] += -self.speed  # TRANSLATE
            if self.keys[pg.K_RIGHT]:
                shape.position[0] += self.speed
            if self.keys[pg.K_DOWN]:
                shape.position[1] += self.speed
            if self.keys[pg.K_UP]:
                shape.position[1] += -self.speed
            if self.keys[pg.K_PAGEUP]:
                shape.position[2] += self.speed
            if self.keys[pg.K_PAGEDOWN]:
                shape.position[2] += -self.speed
            if self.keys[pg.K_s]:
                shape.Rotate((1, 0, 0), -self.delta_theta)  # ROTATE
            if self.keys[pg.K_w]:
                shape.Rotate((1, 0, 0),  self.delta_theta)
            if self.keys[pg.K_d]:
                shape.Rotate((0, 1, 0), -self.delta_theta)
            if self.keys[pg.K_a]:
                shape.Rotate((0, 1, 0),  self.delta_theta)
            if self.keys[pg.K_e]:
                shape.Rotate((0, 0, 1), -self.delta_theta)
            if self.keys[pg.K_q]:
                shape.Rotate((0, 0, 1),  self.delta_theta)
            if self.keys[pg.K_SPACE]:
                self.Rotate()

    def Rotate(self):  # rotates shapes along (1/sqrt(3), 1/sqrt(3), 1/sqrt(3)) = (1,1,1)/|(1,1,1)|

        for shape in self.shapes:

            shape.Rotate((0.57735026919, 0.57735026919,
                         0.57735026919), self.delta_theta/13)

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

        is_orthographic = True
        while True:

            self.keys = pg.key.get_pressed()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    is_orthographic = not is_orthographic

            """if self.keys[pg.K_RETURN]:
                is_orthographic = not is_orthographic"""

            self.Input()

            if is_orthographic:
                self.Draw()
            else:
                self.DrawPerspective()

            self.Update()
            self.Handle_Events()


if __name__ == "__main__":
    program = Renderer()                          # init render
    program.shapes = program.Platonic_Solids()    # populate objects to be rendered
    program.Run()                                 # Render objects
