import pygame as pg
import math
import shape3d
import quaternion

class Renderer:

    def __init__(self, window_width, window_height):

        pg.init()
        self.window_width     = window_width
        self.window_height    = window_height
        self.ORIGIN           = (window_width//2, window_height//2, 0)
        self.FPS              = 60
        self.screen           = pg.display.set_mode((window_width, window_height))
        self.clock            = pg.time.Clock()
        self.keys             = pg.key.get_pressed()
        self.shapes           = []
        self.axes             = self.Axes()
        self.speed            = 5
        self.angle            = 1

    def Axes(self):
        if self.window_width > self.window_height:

            return [shape3d.xAxis(self.window_width),  shape3d.yAxis(self.window_width),  shape3d.zAxis(self.window_width)]
        
        else:

            return [shape3d.xAxis(self.window_height), shape3d.yAxis(self.window_height), shape3d.zAxis(self.window_height)]

    def PlatonicSolids(self):

        return [shape3d.Cube        ([-450, -150, 0]),
                shape3d.Tetrahedron ([-450,  150, 0]),
                shape3d.Dodecahedron([   0,    0, 0]),
                shape3d.Icosahedron ([ 450, -150, 0]),
                shape3d.Octahedron  ([ 450,  150, 0])]

    def RotatePoint(self, point, axis, angle):
        
        rotation      = quaternion.Quaternion(axis, angle)
        original      = quaternion.Quaternion(point[0], point[1], point[2])
        product       = rotation.inverse() * original * rotation
        rotatedPoint = [product.x, product.y, product.z]
        return rotatedPoint

    def RotateShapeLocal(self, shape, axis, angle):

        rotatedVertices = []
        for vertex in shape.vertices:
            
            rotatedVertex = self.RotatePointAboutAnother(vertex, shape.position, axis, angle)
            rotatedVertices.append(rotatedVertex) 

        return rotatedVertices

    def RotateShapesLocal(self, axis, angle):

        for shape in self.shapes:

            shape.vertices = self.RotateShapeLocal(shape, axis, angle)

    def RotatePointAboutAnother(self, point, centerOfRotation, axis, angle):

        difference    = [point[0] - centerOfRotation[0], point[1] - centerOfRotation[1], point[2] - centerOfRotation[2]]
        rotatedPoint = self.RotatePoint(difference, axis, angle)
        sum           = [rotatedPoint[0] + centerOfRotation[0], rotatedPoint[1] + centerOfRotation[1], rotatedPoint[2] + centerOfRotation[2]]
        return sum

    def RotateShapeAboutPoint(self, shape, centerOfRotation, axis, angle):

        rotatedVertices = []
        for vertex in shape.vertices:

            rotatedVertex = self.RotatePointAboutAnother(vertex, centerOfRotation, axis, angle)
            rotatedVertices.append(rotatedVertex)

        shape.position = self.RotatePointAboutAnother(shape.position, centerOfRotation, axis, angle)
        return rotatedVertices

    def RotateShapesAboutPoint(self, centerOfRotation, axis, angle):
 
        for shape in self.shapes:

            shape.vertices = self.RotateShapeAboutPoint(shape, centerOfRotation, axis, angle)

    def RotateAxes(self, axis, angle):

        for shape in self.axes:

            shape.vertices = self.RotateShapeLocal(shape, axis, angle)

    # Make this relative to axis not relative to screen
    def TranslatePoint(self, point, axis, distance):

        norm            = math.sqrt(axis[0]*axis[0] + axis[1]*axis[1] + axis[2]*axis[2])
        newAxis         = [distance*(axis[0]/norm), distance*(axis[1]/norm), distance*(axis[2]/norm)]
        translatedPoint = [point[0] + newAxis[0], point[1] + newAxis[1], point[2] + newAxis[2]]
        return translatedPoint
        
    def TranslateShape(self, shape, axis, distance):     # 0 = x, 1 = y, 2 = z


        shape.position = self.TranslatePoint(shape.position, axis, distance)

        for vertex in shape.vertices:

            vertex = self.TranslatePoint(vertex, axis, distance)

    def TranslateShapes(self, axis, distance):
        
        for shape in self.shapes:

            self.TranslateShape(shape, axis, distance)    

    def DrawDashedLine(self, color, startPoint, endPoint, dashLength):

        # # From chatgpt
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

        # self.screen.fill(pg.Color('white'))
        # From chatgpt
        squareSize = 24

        for row in range(0, self.screen.get_height(), squareSize):

            for col in range(0, self.screen.get_width(), squareSize):

                if (row + col) % (2 * squareSize) < squareSize:

                    color = pg.Color('darkgray')

                else:

                    color = pg.Color('gray')

                pg.draw.rect(self.screen, color, pg.Rect(col, row, squareSize, squareSize))

    def DrawPoint(self, color, point):

        pg.draw.circle(self.screen, color, (point[0], point[1]), 5)

    def DrawEdge(self, edgeColor, vertexColor, startPoint, endPoint):

        pg.draw.line(self.screen, edgeColor, startPoint, endPoint, 5)

        self.DrawPoint(vertexColor, startPoint)
        self.DrawPoint(vertexColor, endPoint)

    def DrawShape(self, shape):

        edgeColor   = pg.Color('white')
        vertexColor = pg.Color('black')
        for edge in shape.edges:
            startPoint = (shape.vertices[edge[0]][0] + self.ORIGIN[0], shape.vertices[edge[0]][1] + self.ORIGIN[1])
            endPoint   = (shape.vertices[edge[1]][0] + self.ORIGIN[0], shape.vertices[edge[1]][1] + self.ORIGIN[1])

            self.DrawEdge(edgeColor, vertexColor, startPoint, endPoint)

    def DrawShapes(self):

        for shape in self.shapes:
            
            self.DrawShape(shape)

    def DrawAxes(self):

        for axis in self.axes:

            if  axis.name == 'xAxis':
                color = pg.Color('red')
            elif axis.name == 'yAxis':
                color = pg.Color('green')
            elif axis.name == 'zAxis':
                color = pg.Color('blue')

            for edge in axis.edges:

                startPoint = (axis.vertices[edge[0]][0] + self.ORIGIN[0], axis.vertices[edge[0]][1] + self.ORIGIN[1])
                endPoint   = (axis.vertices[edge[1]][0] + self.ORIGIN[0], axis.vertices[edge[1]][1] + self.ORIGIN[1])

                if edge[1] == 2:
                    
                    self.DrawDashedLine(color, startPoint, endPoint, 10)
                else:

                    pg.draw.line(self.screen, color, startPoint, endPoint, 5)    
        
        self.DrawPoint(pg.Color('black'), self.ORIGIN)

    def HandleInput(self):

        if self.keys[pg.K_0]:
            self.shapes = self.PlatonicSolids()
            self.axes   = self.Axes() 

        xAxis = self.axes[0].vertices[2]
        yAxis = self.axes[1].vertices[2]
        zAxis = self.axes[2].vertices[2]

        if self.keys[pg.K_LEFT]:
            self.TranslateShapes(xAxis, self.speed)
        if self.keys[pg.K_RIGHT]:
            self.TranslateShapes(xAxis, self.speed)
        if self.keys[pg.K_DOWN]:
            self.TranslateShapes(yAxis, self.speed)
        if self.keys[pg.K_UP]:
            self.TranslateShapes(yAxis, self.speed)
        if self.keys[pg.K_PAGEUP]:
            self.TranslateShapes(zAxis, self.speed)
        if self.keys[pg.K_PAGEDOWN]:
            self.TranslateShapes(zAxis, self.speed)

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
                self.RotateShapesAboutPoint((0, 0, 0), (1, 0, 0), -self.angle)
                self.RotateAxes((1, 0, 0), -self.angle)
            if self.keys[pg.K_s]:
                self.RotateShapesAboutPoint((0, 0, 0), (1, 0, 0),  self.angle)
                self.RotateAxes((1, 0, 0), self.angle)
            if self.keys[pg.K_d]:
                self.RotateShapesAboutPoint((0, 0, 0), (0, 1, 0), -self.angle)
                self.RotateAxes((0, 1, 0), -self.angle)
            if self.keys[pg.K_a]:
                self.RotateShapesAboutPoint((0, 0, 0), (0, 1, 0),  self.angle)
                self.RotateAxes((0, 1, 0),  self.angle)
            if self.keys[pg.K_q]:
                self.RotateShapesAboutPoint((0, 0, 0), (0, 0, 1), -self.angle)
                self.RotateAxes((0, 0, 1), -self.angle)
            if self.keys[pg.K_e]:
                self.RotateShapesAboutPoint((0, 0, 0), (0, 0, 1),  self.angle)
                self.RotateAxes((0, 0, 1),  self.angle)
            if self.keys[pg.K_SPACE]:
                self.RotateShapesAboutPoint((0, 0, 0), (1, -1, 1), 1)
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