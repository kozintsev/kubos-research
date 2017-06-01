# Adds an action to the interface of Kubos: The new action can be 
# found under "My Actions - Randsphere". It also has a toolbar icon.

from app import app
from OCC.BRepPrimAPI import *
from OCC.gp import gp_Pnt
from random import random
from lib.action import Action

def randsphere():
    m = gp_Pnt(random(), random(), random())
    k = BRepPrimAPI_MakeSphere(m, 0.2).Solid()
    app.doc.add(k)

rs = Action(randsphere, ['&My Actions', 'Randsphere'], icon='cad-sphere')
app.load_action(rs)
