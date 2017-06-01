# Add a cuboid which is transformed in various ways.

# The modules "lib.trsf" and "lib.vec" are used to provide simpler functions
# than the native OCC functions

from OCC.BRepPrimAPI import *
from lib.trsf import *
from lib.vec import vec
from math import pi

box = BRepPrimAPI_MakeBox(10, 2, 2).Solid()

box1 = translate(box, vec(0, -2, 0))

box2 = rotate(box, [vec(0, 0, 0), vec(0, 0, 1)], 45)

box3 = translate(
          rotate(
              shape=box,
              axis=[vec(0, 0, 0), vec(1, 0, 0)],
              angle=pi/4),
          vector=vec(0, 0, 10)
      )

SHAPES = [box1, box2, box3]