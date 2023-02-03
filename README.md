# Platonic-Solids-pygame
Render and manipulate orthographic 3D wireframe objects

rotations are calculated using quaterions
translations are not handled properly yet
    (translations are relative to the screen instead of the axes)

vertices are lists of 3 numbers
edges are pairs vertex indices 

All solids are controlled together

negative half axis is dashed
x-axis is red
y-axis is green
z-axis is blue

controls:

    lshift:     All rotations will be about global axes while held

    w/s:        controls x-axis rotation
    a/d:        controls y-axis rotation
    q/e:        controls z-axis rotation
    space:      rotates in all three axes while held

    up/down:    controls y position
    left/right: controls x position
    PgUp/PGDwn: controls z position

    0:          resets all shape positions and rotations