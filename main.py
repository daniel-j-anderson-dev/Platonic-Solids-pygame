import pygame as pg
import Shape3D

class Renderer():
    def __init__(self):
        pg.init()
        self.WINDOW_SIZE    = (1920, 1080)
        self.ORIGIN         = [self.WINDOW_SIZE[0]//2, self.WINDOW_SIZE[1]//2, 0]
        self.FPS            = 60
        self.screen         = pg.display.set_mode(self.WINDOW_SIZE)
        self.clock          = pg.time.Clock()
        self.shapes         = []
        self.keys           = pg.key.get_pressed()
        self.speed          = 5
        self.delta_theta    = 5

    def Platonic_Solids(self):
        return [Shape3D.Cube(), Shape3D.Tetrahedron(), Shape3D.Dodecahedron(), Shape3D.Icosahedron(), Shape3D.Octahedron()]

    def Draw(self):
        for shape in self.shapes:
            self.screen.fill(pg.Color('white'))
            for shape in self.shapes:
                shape.Draw(self.screen, self.ORIGIN)

    def Input(self):
        for shape in self.shapes:
            if self.keys[pg.K_LEFT]:     shape.position[0]  += -self.speed            #TRANSLATE
            if self.keys[pg.K_RIGHT]:    shape.position[0]  +=  self.speed
            if self.keys[pg.K_DOWN]:     shape.position[1]  +=  self.speed
            if self.keys[pg.K_UP]:       shape.position[1]  += -self.speed
            if self.keys[pg.K_PAGEUP]:   shape.position[2]  +=  self.speed
            if self.keys[pg.K_PAGEDOWN]: shape.position[2]  += -self.speed
            if self.keys[pg.K_s]:        shape.Rotate((1,0,0), -self.delta_theta)      #ROTATE
            if self.keys[pg.K_w]:        shape.Rotate((1,0,0),  self.delta_theta)
            if self.keys[pg.K_d]:        shape.Rotate((0,1,0), -self.delta_theta)
            if self.keys[pg.K_a]:        shape.Rotate((0,1,0),  self.delta_theta)
            if self.keys[pg.K_e]:        shape.Rotate((0,0,1), -self.delta_theta)
            if self.keys[pg.K_q]:        shape.Rotate((0,0,1),  self.delta_theta)
            if self.keys[pg.K_SPACE]:    self.Rotate()
    
    def Rotate(self):#rotates along (1/sqrt(3), 1/sqrt(3), 1/sqrt(3)) = (1,1,1)/|(1,1,1)|
        for shape in self.shapes:
            shape.Rotate((0.57735026919 ,0.57735026919 ,0.57735026919 ), self.delta_theta/13)

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
            self.Rotate()
            self.Draw()
            self.Update()
            self.Handle_Events()
                
if __name__ == "__main__":
  program = Renderer()                          # init render
  program.shapes = program.Platonic_Solids()    # populate objects to be rendered
  program.Run()                                 # Render objects