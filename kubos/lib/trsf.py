from __future__ import absolute_import,division,print_function,unicode_literals

from OCC import gp
from OCC.gp import gp_Trsf, gp_Vec
from OCC.TopLoc import TopLoc_Location

def translate(shape, vector):
    tr = gp_Trsf()
    tr.SetTranslation(gp_Vec(*vector))
    loc = TopLoc_Location(tr)
    return shape.Moved(loc)

def rotate(shape, axis, angle):
    tr = gp_Trsf()
    point = axis[0]
    vec = axis[1]
    axis = gp.gp_Ax1(gp.gp_Pnt(*point), gp.gp_Dir(*vec))
    tr.SetRotation(axis, angle)
    loc = TopLoc_Location(tr)
    return shape.Moved(loc)
