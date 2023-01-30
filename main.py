import pygame as pg
import shape3d
# import camera
import quaternion


class Renderer:

    def __init__(self):

        pg.init()
        self.WINDOW_SIZE = (1920, 1080)
        self.ORIGIN = (self.WINDOW_SIZE[0]//2, self.WINDOW_SIZE[1]//2, 0)
        self.FPS = 60
        self.screen = pg.display.set_mode(self.WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.shapes = []
        self.keys = pg.key.get_pressed()
        self.speed = 5
        self.angle = 5
        # self.camera = camera.Camera(self.ORIGIN)
        self.axes = [shape3d.xAxis(self.ORIGIN), shape3d.yAxis(self.ORIGIN), shape3d.zAxis(self.ORIGIN)]
        self.displaySolids = True

    def Platonic_Solids(self):

        return [shape3d.Cube        ([-700 + self.ORIGIN[0], -300 + self.ORIGIN[1], 0]),
                shape3d.Tetrahedron ([-700 + self.ORIGIN[0],  300 + self.ORIGIN[1], 0]),
                shape3d.Dodecahedron([   0 + self.ORIGIN[0],    0 + self.ORIGIN[1], 0]),
                shape3d.Icosahedron ([ 700 + self.ORIGIN[0], -300 + self.ORIGIN[1], 0]),
                shape3d.Octahedron  ([ 700 + self.ORIGIN[0],  300 + self.ORIGIN[1], 0])]

    def rotate_point(self, point, axis, angle):
        
        rotation      = quaternion.Quaternion(axis, angle)
        original      = quaternion.Quaternion(point[0], point[1], point[2])
        product       = rotation.inverse() * original * rotation
        rotated_point = [product.x, product.y, product.z]
        return rotated_point

    def rotate_point_about_another(self, point, centerOfRotation, axis, angle):

        difference    = [point[0] - centerOfRotation[0],
                         point[1] - centerOfRotation[1],
                         point[2] - centerOfRotation[2]]

        rotated_point = self.rotate_point(difference, axis, angle)

        sum           = [rotated_point[0] + centerOfRotation[0],
                         rotated_point[1] + centerOfRotation[1],
                         rotated_point[2] + centerOfRotation[2]]

        return sum

    def RotateShapesLocal(self, axis, angle):

        for shape in self.shapes:

            rotated_vertices = []
            for vertex in shape.vertices:
                
                rotated_vertex = self.rotate_point_about_another(vertex, shape.position, axis, angle)
                rotated_vertices.append(rotated_vertex) 

            shape.vertices = rotated_vertices

    def RotateShapesAboutPoint(self, centerOfRotation, axis, angle):
 
        for shape in self.shapes:

            rotated_vertices = []
            for vertex in shape.vertices:

                rotated_vertex = self.rotate_point_about_another(vertex, centerOfRotation, axis, angle)
                rotated_vertices.append(rotated_vertex)

            shape.position = self.rotate_point_about_another(shape.position, centerOfRotation, axis, angle)
            shape.vertices = rotated_vertices

    def TranslateShapes(self, speed, index):
        
        for shape in self.shapes:

            for vertex in shape.vertices:

                vertex[index] += speed  
                
            shape.position[index] += speed

    def DrawPoint(self, color, point):

        pg.draw.circle(self.screen, color, (point[0], point[1]), 5)

    def ClearScreen(self):

        self.screen.fill(pg.Color('white'))

    def DrawAxes(self):

        for axis in self.axes:

            for edge in axis.edges:

                start_point = (axis.vertices[edge[0]][0], axis.vertices[edge[0]][1])
                end_point   = (axis.vertices[edge[1]][0], axis.vertices[edge[1]][1])

                pg.draw.line(self.screen, pg.Color('black'), start_point, end_point, 1)

    def DrawShapes(self):

        for shape in self.shapes:

            for edge in shape.edges:

                start_point = (shape.vertices[edge[0]][0], shape.vertices[edge[0]][1])
                end_point   = (shape.vertices[edge[1]][0], shape.vertices[edge[1]][1])

                pg.draw.line(self.screen, pg.Color('black'), start_point, end_point, 1)

                self.DrawPoint(pg.Color('red'), start_point)
                self.DrawPoint(pg.Color('red'), end_point)

    def Input(self):

        if self.keys[pg.K_RSHIFT]:
            self.displaySolids = not self.displaySolids
        if self.keys[pg.K_0]:
            self.shapes  = self.Platonic_Solids() 

        if self.displaySolids:

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
                    self.RotateShapesLocal((1, 0, 0), -self.angle)
                if self.keys[pg.K_w]:
                    self.RotateShapesLocal((1, 0, 0),  self.angle)
                if self.keys[pg.K_d]:
                    self.RotateShapesLocal((0, 1, 0), -self.angle)
                if self.keys[pg.K_a]:
                    self.RotateShapesLocal((0, 1, 0),  self.angle)
                if self.keys[pg.K_e]:
                    self.RotateShapesLocal((0, 0, 1), -self.angle)
                if self.keys[pg.K_q]:
                    self.RotateShapesLocal((0, 0, 1),  self.angle)
                if self.keys[pg.K_SPACE]:
                    self.RotateShapesLocal((1, 1, 1), 1)

            else:
                if self.keys[pg.K_s]:
                    self.RotateShapesAboutPoint(self.ORIGIN, (1, 0, 0), -self.angle)
                if self.keys[pg.K_w]:
                    self.RotateShapesAboutPoint(self.ORIGIN, (1, 0, 0),  self.angle)
                if self.keys[pg.K_d]:
                    self.RotateShapesAboutPoint(self.ORIGIN, (0, 1, 0), -self.angle)
                if self.keys[pg.K_a]:
                    self.RotateShapesAboutPoint(self.ORIGIN, (0, 1, 0),  self.angle)
                if self.keys[pg.K_q]:
                    self.RotateShapesAboutPoint(self.ORIGIN, (0, 0, 1), -self.angle)
                if self.keys[pg.K_e]:
                    self.RotateShapesAboutPoint(self.ORIGIN, (0, 0, 1),  self.angle)
                if self.keys[pg.K_SPACE]:
                    self.RotateShapesAboutPoint(self.ORIGIN, (1, -1, 1), 1)

                


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
            self.ClearScreen()
            self.DrawPoint(pg.Color('black'), self.ORIGIN)
            self.DrawAxes()

            if self.displaySolids:
                self.DrawShapes()

            self.Update()
            self.Handle_Events()


if __name__ == "__main__":
    program = Renderer()                          # init render
    program.shapes = program.Platonic_Solids()    # populate objects to be rendered
    program.Run()                                 # Render objects
