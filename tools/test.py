

from OCC import BRepBuilderAPI, GC

from lib import gp_
from tools.tool import Tool


class Test1(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.menu = 'Te&sts', '&TestTool1'
        self.steps = 1
        self.input_types = ['point']
        self.icon = ''
        self.shortcut = ''
        self.help = ''

        self.reset()

    def preview(self, input, direction):
        point = input
        if self.step == 0 and point is not None:
            point1 = gp_.gp_Pnt_([0, 0, 0])
            a = GC.GC_MakeSegment(point1, point).Value()
            self._final = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(a).Shape()
            return self._final,

toolbar_visible = False

list = [Test1()]
