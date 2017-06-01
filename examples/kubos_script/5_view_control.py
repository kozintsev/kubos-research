# This script adds an action to the application which will create an
# animation of the camera.

from __future__ import division,print_function

from app import app
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox
from lib.action import Action
from math import sin, cos

cuboid = BRepPrimAPI_MakeBox(1, 4, 5).Solid()
app.doc.add(cuboid)

def animation_():
    app.viewer.zoom = 1
    for i in range(120):
        app.viewer.eye = [sin(i/20), cos(i/20), -2+i/40]
        app.viewer.zoom *= 1.01

animation = Action(animation_, ['&View', '&Animation'])
app.load_action(animation)
