import pygame as pg
import math
import shape3d
import quaternion

class Renderer:

    def __init__(self, window_width, window_height):

        pg.init()
        self.ORIGIN      = (window_width//2, window_height//2, 0)
        self.FPS         = 60
        self.screen      = pg.display.set_mode((window_width, window_height))
        self.clock       = pg.time.Clock()
        self.keys        = pg.key.get_pressed()
        self.shapes      = []
        self.axes        = self.Axes()
        self.speed       = 5
        self.angle       = 1

    def Axes(self):
        return [shape3d.xAxis(self.ORIGIN),
                shape3d.yAxis(self.ORIGIN),
                shape3d.zAxis(self.ORIGIN)]

    def Platonic_Solids(self):

        return [shape3d.Cube        ([-450 + self.ORIGIN[0], -150 + self.ORIGIN[1], 0]),
                shape3d.Tetrahedron ([-450 + self.ORIGIN[0],  150 + self.ORIGIN[1], 0]),
                shape3d.Dodecahedron([   0 + self.ORIGIN[0],    0 + self.ORIGIN[1], 0]),
                shape3d.Icosahedron ([ 450 + self.ORIGIN[0], -150 + self.ORIGIN[1], 0]),
                shape3d.Octahedron  ([ 450 + self.ORIGIN[0],  150 + self.ORIGIN[1], 0])]

    def RotatePoint(self, point, axis, angle):
        
        rotation      = quaternion.Quaternion(axis, angle)
        original      = quaternion.Quaternion(point[0], point[1], point[2])
        product       = rotation.inverse() * original * rotation
        rotated_point = [product.x, product.y, product.z]
        return rotated_point

    def RotatePointAboutAnother(self, point, centerOfRotation, axis, angle):

        difference    = [point[0] - centerOfRotation[0], point[1] - centerOfRotation[1], point[2] - centerOfRotation[2]]
        rotated_point = self.RotatePoint(difference, axis, angle)
        sum           = [rotated_point[0] + centerOfRotation[0], rotated_point[1] + centerOfRotation[1], rotated_point[2] + centerOfRotation[2]]
        return sum

    def RotateShapeLocal(self, shape, axis, angle):

        rotated_vertices = []
        for vertex in shape.vertices:
            
            rotated_vertex = self.RotatePointAboutAnother(vertex, shape.position, axis, angle)
            rotated_vertices.append(rotated_vertex) 

        return rotated_vertices

    def RotateShapeAboutPoint(self, shape, centerOfRotation, axis, angle):

        rotated_vertices = []
        for vertex in shape.vertices:

            rotated_vertex = self.RotatePointAboutAnother(vertex, centerOfRotation, axis, angle)
            rotated_vertices.append(rotated_vertex)

        shape.position = self.RotatePointAboutAnother(shape.position, centerOfRotation, axis, angle)
        return rotated_vertices

    def RotateShapesLocal(self, axis, angle):

        for shape in self.shapes:

            shape.vertices = self.RotateShapeLocal(shape, axis, angle)

    def RotateShapesAboutPoint(self, centerOfRotation, axis, angle):
 
        for shape in self.shapes:

            shape.vertices = self.RotateShapeAboutPoint(shape, centerOfRotation, axis, angle)

    def RotateAxes(self, centerOfRotation, axis, angle):

        for shape in self.axes:

            shape.vertices = self.RotateShapeLocal(shape, axis, angle)

    # Make this relative to axis not relative to screen
    def TranslateShape(self, shape, axis):     # 0 = x, 1 = y, 2 = z
        
        shape.position[0] += axis[0]
        shape.position[1] += axis[1]
        shape.position[2] += axis[2]
        for vertex in shape.vertices:

            vertex[0] += axis[0]
            vertex[1] += axis[1] 
            vertex[2] += axis[2] 

    def TranslateShapes(self, axis):
        
        for shape in self.shapes:

            self.TranslateShape(shape, axis)    

    def DrawPoint(self, color, point):

        pg.draw.circle(self.screen, color, (point[0], point[1]), 5)

    def DrawDashedLine(self, color, startPoint, endPoint, dashLength):

        segments = []
        distance = math.sqrt(startPoint[0] * startPoint[0] + 
                             startPoint[1] * startPoint[1])

        numSegments = int(distance / dashLength)

        for i in range(numSegments):
            x = int(startPoint[0] + (i * dashLength) * (endPoint[0] - startPoint[0]) / distance)
            y = int(startPoint[1] + (i * dashLength) * (endPoint[1] - startPoint[1]) / distance)
            segments.append([x, y])
        
        for i in range(0, len(segments) - 1, 2):

                pg.draw.line(self.screen, color, segments[i], segments[i + 1], 8)

    def ClearScreen(self):

        square_size = 50

        # Set the colors for the squares
        color1 = pg.Color('darkgray')
        color2 = pg.Color('gray')

        # Fill the screen with the checkerboard pattern
        for row in range(0, self.screen.get_height(), square_size):
            for col in range(0, self.screen.get_width(), square_size):
                if (row + col) % (2 * square_size) < square_size:
                    color = color1
                else:
                    color = color2
                pg.draw.rect(self.screen, color, pg.Rect(col, row, square_size, square_size))
        # self.screen.fill(pg.Color('white'))

    def DrawAxes(self):

        for axis in self.axes:

            if  axis.name == 'xAxis':
                color = pg.Color('white')
            elif axis.name == 'yAxis':
                color = pg.Color('pink')
            elif axis.name == 'zAxis':
                color = pg.Color('purple')


            for edge in axis.edges:

                startPoint = (axis.vertices[edge[0]][0], axis.vertices[edge[0]][1])
                endPoint   = (axis.vertices[edge[1]][0], axis.vertices[edge[1]][1])

                #pg.draw.line(self.screen, color, startPoint, endPoint, 8)
                self.DrawDashedLine(color, startPoint, endPoint, 10)
        
        self.DrawPoint(pg.Color('black'), self.ORIGIN)

    def DrawShape(self, shape):

        for edge in shape.edges:
            startPoint = (shape.vertices[edge[0]][0], shape.vertices[edge[0]][1])
            endPoint   = (shape.vertices[edge[1]][0], shape.vertices[edge[1]][1])

            pg.draw.line(self.screen, pg.Color('green'), startPoint, endPoint, 5)

            self.DrawPoint(pg.Color('red'), startPoint)
            self.DrawPoint(pg.Color('red'), endPoint)

    def DrawShapes(self):

        for shape in self.shapes:
            
            self.DrawShape(shape)

    def HandleInput(self):

        if self.keys[pg.K_0]:
            self.shapes = self.Platonic_Solids()
            self.axes   = self.Axes() 

        if self.keys[pg.K_LEFT]:
            self.TranslateShapes((-self.speed, 0, 0))  # TRANSLATE
        if self.keys[pg.K_RIGHT]:
            self.TranslateShapes(( self.speed, 0, 0))
        if self.keys[pg.K_DOWN]:
            self.TranslateShapes((0,  self.speed, 0))
        if self.keys[pg.K_UP]:
            self.TranslateShapes((0, -self.speed, 0))
        if self.keys[pg.K_PAGEUP]:
            self.TranslateShapes((0, 0,  self.speed))
        if self.keys[pg.K_PAGEDOWN]:
            self.TranslateShapes((0, 0, -self.speed))

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
            if self.keys[pg.K_w]:
                self.RotateShapesAboutPoint(self.ORIGIN, (1, 0, 0), -self.angle)
                self.RotateAxes(self.ORIGIN, (1, 0, 0), -self.angle)
            if self.keys[pg.K_s]:
                self.RotateShapesAboutPoint(self.ORIGIN, (1, 0, 0),  self.angle)
                self.RotateAxes(self.ORIGIN, (1, 0, 0), self.angle)
            if self.keys[pg.K_d]:
                self.RotateShapesAboutPoint(self.ORIGIN, (0, 1, 0), -self.angle)
                self.RotateAxes(self.ORIGIN, (0, 1, 0), -self.angle)
            if self.keys[pg.K_a]:
                self.RotateShapesAboutPoint(self.ORIGIN, (0, 1, 0),  self.angle)
                self.RotateAxes(self.ORIGIN, (0, 1, 0),  self.angle)
            if self.keys[pg.K_q]:
                self.RotateShapesAboutPoint(self.ORIGIN, (0, 0, 1), -self.angle)
                self.RotateAxes(self.ORIGIN, (0, 0, 1), -self.angle)
            if self.keys[pg.K_e]:
                self.RotateShapesAboutPoint(self.ORIGIN, (0, 0, 1),  self.angle)
                self.RotateAxes(self.ORIGIN, (0, 0, 1),  self.angle)
            if self.keys[pg.K_SPACE]:
                self.RotateShapesAboutPoint(self.ORIGIN, (1, -1, 1), 1)
                self.RotateAxes(self.ORIGIN, (1, -1, 1), 1)

    def HandleEvents(self):

        self.keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                pg.quit()
                exit()
        
        self.HandleInput()

    def Update(self):

        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()
        self.clock.tick(self.FPS)

    def Run(self):
        
        while True:
            
            self.ClearScreen()

            self.DrawAxes()
            self.DrawShapes()

            self.Update()
            self.HandleEvents()

