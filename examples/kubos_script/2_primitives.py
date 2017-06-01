# Create a simple object composed of a cuboid and a sphere.
# The size of the object can be changed through the values
# of 'w' and 'h'

from __future__ import division

from OCC.BRepPrimAPI import *
from OCC.gp import gp_Pnt

w = 3
h = 4

corner = gp_Pnt(-w/2, -w/2, 0)
cuboid = BRepPrimAPI_MakeBox(corner, w, w, h).Solid()

center = gp_Pnt(0, 0, h)
sphere = BRepPrimAPI_MakeSphere(center, w/2).Solid()

SHAPES = [sphere, cuboid]
