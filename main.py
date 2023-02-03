import renderer

if __name__ == "__main__":
    program        = renderer.Renderer(1920, 1080)
    program.shapes = program.Platonic_Solids()
    program.Run()