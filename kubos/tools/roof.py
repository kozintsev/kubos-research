from __future__ import absolute_import,division,print_function,unicode_literals

from .tool import Tool
from ..lib.boolean import intersection
from ..lib.vec import vec
from ..lib.subshapes import subshapes
from ..lib.gp_ import gp_Pnt_
from OCC.TopAbs import TopAbs_EDGE, TopAbs_VERTEX
from OCC import gp, BRepPrimAPI

class Roof(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.menu = ['Te&st', '&Roof']
        self.steps = 1
        self.input_types = ['object']
        self.help = ['Select a polygon to build a roof over it']
        self.icon = 'cad-roof'

        self.reset()

    # about 1 h
    def preview(self, input, direction):
        veclist = []
        for edge in subshapes(input, TopAbs_EDGE):
            vertices = subshapes(edge, TopAbs_VERTEX)
            vec_ = gp_Pnt_(vertices[0]) - gp_Pnt_(vertices[1])
            veclist.append(vec_)

        prisms = []
        for vec_ in veclist:
            vec_ = vec_ * (1/vec_.length())*100
            v = vec(vec_[1], -vec_[0], 100)

            prism = BRepPrimAPI.BRepPrimAPI_MakePrism(input, 
                        gp.gp_Vec(v[0], v[1], v[2])).Shape()
            prisms.append(prism)

        p = prisms.pop()
        for p_ in prisms:
            p = intersection(p, p_)[0]

        self._final = [p]
        return self._final

toolbar_visible = False

list = [Roof()]
