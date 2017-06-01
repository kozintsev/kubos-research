# This script adds a cuboid to the current document

from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox

cuboid = BRepPrimAPI_MakeBox(3, 4, 5).Solid()

SHAPES = [cuboid]
