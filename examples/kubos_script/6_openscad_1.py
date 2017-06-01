# This is a derived version of "example001" from OpenSCAD.

from __future__ import division
from OCC.BRepPrimAPI import *
from OCC.gp import *
from OCC.BRepAlgoAPI import *

def example(size, hole):

    c1 = BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(0, 0, -size/2), gp_Dir(0, 0, 1)), hole/2, size).Solid()
    c2 = BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(0, -size/2, 0), gp_Dir(0, 1, 0)), hole/2, size).Solid()
    c3 = BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(-size/2, 0, 0), gp_Dir(1, 0, 0)), hole/2, size).Solid()

    c = BRepAlgoAPI_Fuse(c1, c2).Shape()
    c = BRepAlgoAPI_Fuse(c, c3).Shape()

    s = BRepPrimAPI_MakeSphere(size/2).Solid()

    f = BRepAlgoAPI_Cut(s, c).Shape()
    return f

SHAPES = [example(5, 3), example(12, 6)]

