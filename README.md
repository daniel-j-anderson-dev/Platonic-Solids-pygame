# Platonic-Solids-pygame
Render and manipulate orthographic 3D wireframe objects

rotations are calculated using quaterions

vertices are lists of 3 numbers
edges are pairs vertex indices 

All solids are controlled together

controls:

    lshift:     All rotations will be about global axes while held

    w/s:        controls x-axis rotation
    a/d:        controls y-axis rotation
    q/e:        controls z-axis rotation
    space:      rotates in all three axes while held

    up/down:    controls y position
    left/right: controls x position
    PgUp/PGDwn: controls z position (unused in orthographic projection)

    0:          resets all shape positions and rotations