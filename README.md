# Platonic-Solids-pygame
Render and manipulate orthographic 3D wireframe objects

rotations are calculated using quaterions
translations are not handled properly yet
    (translations are relative to the screen instead of the axes)

vertices are lists of 3 numbers
edges are pairs vertex indices 

All solids are controlled together

positive half axis is dashed
x-axis is red
y-axis is green
z-axis is blue

controls:

    lshift:     All rotations will be about screen axes while held

    w/s:        controls x-axis rotation
    a/d:        controls y-axis rotation
    q/e:        controls z-axis rotation
    space:      rotates in all three axes while held

    up/down:    controls position relative to x-axis
    left/right: controls position relative to y-axis
    PgUp/PGDwn: controls position relative to z-axis

    0:          resets all shape positions and rotations