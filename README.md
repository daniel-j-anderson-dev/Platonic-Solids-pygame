# Platonic-Solids-pygame
Render and manipulate orthographic 3D wireframe objects

rotations are calculated using quaterions

vertices are lists of 3 numbers
edges are pairs vertex indices 

camera is on the negative z-axis pointing towards the origin
near plane is centered on the z axis 100 units away from camera
far plane is cetered on the z axis and 100 units further than the near plane 

All solids are controlled together

controls:

    w/s:        controls y-axis rotation
    a/d:        controls x-axis rotation
    q/e:        controls z-axis rotation
    space:      rotates in all three axes while held

    up/down:    controls x position
    left/right: controls y position
    PgUp/PGDwn: controls z position (unused in orthographic projection)

    Return:     perspective projection while held. Orthographic otherwise

    0:          resets all shape positions and rotations

    UNUSED:
    i/k:        move camera y position
    j/l:        move camera x position