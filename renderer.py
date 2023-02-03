import pygame as pg
import math
import shape3d
import quaternion

class Renderer:

    def __init__(self, window_width, window_height):

        pg.init()
        self.ORIGIN           = (window_width//2, window_height//2, 0)
        self.FPS              = 60
        self.screen           = pg.display.set_mode((window_width, window_height))
        self.clock            = pg.time.Clock()
        self.keys             = pg.key.get_pressed()
        self.shapes           = []
        self.axes             = self.Axes()
        self.speed            = 5
        self.angle            = 1
        self.worldOrientation = quaternion.Quaternion((0, 0, 1), 360)

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

    def RotateAxes(self, axis, angle):

        for shape in self.axes:

            shape.vertices = self.RotateShapeLocal(shape, axis, angle)

    def MoveShapeX(self):

        for shape in self.shapes:

            self.axes[0].vertices[0]

    # Make this relative to axis not relative to screen
    def TranslateShape(self, shape, axis, distance):     # 0 = x, 1 = y, 2 = z
        
        norm = math.sqrt(axis[0]*axis[0] + axis[1]*axis[1] + axis[1]*axis[1])
        newAxis = [(axis[0]/norm)*distance,
                   (axis[1]/norm)*distance,
                   (axis[2]/norm)*distance]

        shape.position[0] += newAxis[0]
        shape.position[1] += newAxis[1]
        shape.position[2] += newAxis[2]

        for vertex in shape.vertices:

            vertex[0] += newAxis[0]
            vertex[1] += newAxis[1]
            vertex[2] += newAxis[2]

    def TranslateShapes(self, axis, distance):
        
        for shape in self.shapes:

            self.TranslateShape(shape, axis, distance)    

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

                pg.draw.line(self.screen, color, segments[i], segments[i + 1], 5)

    def ClearScreen(self):

        square_size = 24

        # Fill the screen with the checkerboard pattern
        for row in range(0, self.screen.get_height(), square_size):

            for col in range(0, self.screen.get_width(), square_size):

                if (row + col) % (2 * square_size) < square_size:

                    color = pg.Color('darkgray')

                else:

                    color = pg.Color('gray')

                # self.screen.fill(pg.Color('white'))
                pg.draw.rect(self.screen, color, pg.Rect(col, row, square_size, square_size))

    def DrawAxes(self):

        for axis in self.axes:

            if  axis.name == 'xAxis':
                color = pg.Color('red')
            elif axis.name == 'yAxis':
                color = pg.Color('green')
            elif axis.name == 'zAxis':
                color = pg.Color('blue')

            for edge in axis.edges:

                startPoint = (axis.vertices[edge[0]][0], axis.vertices[edge[0]][1])
                endPoint   = (axis.vertices[edge[1]][0], axis.vertices[edge[1]][1])

                if edge[1] == 2:
                    
                    self.DrawDashedLine(color, startPoint, endPoint, 10)
                else:

                    pg.draw.line(self.screen, color, startPoint, endPoint, 5)
                    
        
        self.DrawPoint(pg.Color('black'), self.ORIGIN)

    def DrawShape(self, shape):

        for edge in shape.edges:
            startPoint = (shape.vertices[edge[0]][0], shape.vertices[edge[0]][1])
            endPoint   = (shape.vertices[edge[1]][0], shape.vertices[edge[1]][1])

            pg.draw.line(self.screen, pg.Color('white'), startPoint, endPoint, 5)

            self.DrawPoint(pg.Color('black'), startPoint)
            self.DrawPoint(pg.Color('black'), endPoint)

    def DrawShapes(self):

        for shape in self.shapes:
            
            self.DrawShape(shape)

    def HandleInput(self):

        if self.keys[pg.K_0]:
            self.shapes = self.Platonic_Solids()
            self.axes   = self.Axes() 

        xAxis = (1,0,0)
        yAxis = (0,1,0)
        zAxis = (0,0,1)

        if self.keys[pg.K_LEFT]:
            self.TranslateShapes(xAxis, -self.speed)  # TRANSLATE
        if self.keys[pg.K_RIGHT]:
            self.TranslateShapes(xAxis,  self.speed)
        if self.keys[pg.K_DOWN]:
            self.TranslateShapes(yAxis,  self.speed)
        if self.keys[pg.K_UP]:
            self.TranslateShapes(yAxis, -self.speed)
        if self.keys[pg.K_PAGEUP]:
            self.TranslateShapes(zAxis, -self.speed)
        if self.keys[pg.K_PAGEDOWN]:
            self.TranslateShapes(zAxis,  self.speed)

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
                self.RotateAxes((1, 0, 0), -self.angle)
            if self.keys[pg.K_s]:
                self.RotateShapesAboutPoint(self.ORIGIN, (1, 0, 0),  self.angle)
                self.RotateAxes((1, 0, 0), self.angle)
            if self.keys[pg.K_d]:
                self.RotateShapesAboutPoint(self.ORIGIN, (0, 1, 0), -self.angle)
                self.RotateAxes((0, 1, 0), -self.angle)
            if self.keys[pg.K_a]:
                self.RotateShapesAboutPoint(self.ORIGIN, (0, 1, 0),  self.angle)
                self.RotateAxes((0, 1, 0),  self.angle)
            if self.keys[pg.K_q]:
                self.RotateShapesAboutPoint(self.ORIGIN, (0, 0, 1), -self.angle)
                self.RotateAxes((0, 0, 1), -self.angle)
            if self.keys[pg.K_e]:
                self.RotateShapesAboutPoint(self.ORIGIN, (0, 0, 1),  self.angle)
                self.RotateAxes((0, 0, 1),  self.angle)
            if self.keys[pg.K_SPACE]:
                self.RotateShapesAboutPoint(self.ORIGIN, (1, -1, 1), 1)
                self.RotateAxes((1, -1, 1), 1)

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

