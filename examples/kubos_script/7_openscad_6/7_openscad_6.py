from __future__ import print_function,division,unicode_literals,absolute_import

from OCC.BRepPrimAPI import *
from OCC.BRepAlgoAPI import *
from OCC.gp import *

import imp
import os

l = 5
h = .5

script = imp.load_source('script', os.path.dirname(__file__) + '/rbox.py')

cube = script.rounded_box([l, l, l], h)

for pos in [[l/2, 0, 0],
            [l/5, l/2, -l/5], [-l/5, l/2, l/5],
            [l/4, l/4, -l/2], [-l/4, -l/4, -l/2], [0, 0, -l/2],
            [l/4, l/4, l/2], [l/4, -l/4, l/2], [-l/4, -l/4, l/2],
            [-l/4, l/4, l/2],
            [l/4, -l/2, l/4], [-l/4, -l/2, l/4], [-l/4, -l/2, -l/4],
            [l/4, -l/2, -l/4], [0, -l/2, 0],
            [-l/2, l/5, l/4], [-l/2, l/5, 0], [-l/2, l/5, -l/4],
            [-l/2, -l/5, l/4], [-l/2, -l/5, 0], [-l/2, -l/5, -l/4]]:
    hole = BRepPrimAPI_MakeSphere(gp_Pnt(*pos), h).Solid()
    cube = BRepAlgoAPI_Cut(cube, hole).Shape()

SHAPES = [cube]