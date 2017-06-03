from __future__ import absolute_import,division,print_function,unicode_literals

from OCC import BRepAlgoAPI, BRepPrimAPI, gp
from OCC import TopoDS
from lib.subshapes import subshapes

cube = BRepPrimAPI.BRepPrimAPI_MakeBox(
            gp.gp_Pnt(-10000, -10000, -10000), 20000, 20000, 20000).Solid()

def copy(shape):
    """Return a copy of the shape that does not reference the original shape"""
    new = BRepAlgoAPI.BRepAlgoAPI_Common(shape, cube).Shape()
    comp = TopoDS.TopoDS_compound(new)
    return subshapes(comp, shape.ShapeType())[0]
