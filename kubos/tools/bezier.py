# -*- coding: UTF-8 -*-

from __future__ import absolute_import,division,print_function,unicode_literals

from OCC import BRepBuilderAPI, GC
from OCC.TColgp import TColgp_Array1OfPnt
from OCC.GeomAPI import GeomAPI_PointsToBSpline

from tools.tool import Tool

from exceptions_ import InvalidInputException

class Bspline3(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.menu = ['Te&st', 'B-Spline Curve through &3 Points']
        self.steps = 3
        self.input_types = ['point', 'point', 'point']
        self.help = ['Pick the fist point',
                     'Pick the second point',
                     'Pick the third point']
        self.icon = 'cad-bspline'

        self.reset()

    def preview(self, input, direction):
        if self.step == 0:
            self.previous_data = [input]
            return [BRepBuilderAPI.BRepBuilderAPI_MakeVertex(input).Vertex()]
        elif self.step == 1:
            point0 = self.previous_data[0]
            self.previous_data = [point0, input]
            if point0 == input:
                raise InvalidInputException
            a = GC.GC_MakeSegment(input, point0).Value()
            b = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(a).Edge()
            return [BRepBuilderAPI.BRepBuilderAPI_MakeWire(b).Wire()]
        elif self.step == 2:
            point0, point1 = self.previous_data
            if point1 == input:
                raise InvalidInputException
            pts = TColgp_Array1OfPnt(0, 2)
            pts.SetValue(0, point0)
            pts.SetValue(1, point1)
            pts.SetValue(2, input)
            a = GeomAPI_PointsToBSpline(pts).Curve()
            b = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(a).Edge()
            self._final = [BRepBuilderAPI.BRepBuilderAPI_MakeWire(b).Wire()]
            return self._final

class Bspline4(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.menu = ['Te&st', 'B-Spline Curve through &4 Points']
        self.steps = 4
        self.input_types = ['point', 'point', 'point', 'point']
        self.help = ['Pick the fist point',
                     'Pick the second point',
                     'Pick the third point',
                     'Pick the fourth point']
        self.icon = 'cad-bspline'

        self.reset()

    def preview(self, input, direction):
        if self.step == 0:
            self.previous_data = [input]
            return [BRepBuilderAPI.BRepBuilderAPI_MakeVertex(input).Vertex()]
        elif self.step == 1:
            point0 = self.previous_data[0]
            self.previous_data = [point0, input]
            if point0 == input:
                raise InvalidInputException
            a = GC.GC_MakeSegment(input, point0).Value()
            b = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(a).Edge()
            return [BRepBuilderAPI.BRepBuilderAPI_MakeWire(b).Wire()]
        elif self.step == 2:
            point0, point1 = self.previous_data[0:2]
            self.previous_data = [point0, point1, input]
            if point1 == input:
                raise InvalidInputException
            pts = TColgp_Array1OfPnt(0, 2)
            pts.SetValue(0, point0)
            pts.SetValue(1, point1)
            pts.SetValue(2, input)
            a = GeomAPI_PointsToBSpline(pts).Curve()
            b = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(a).Edge()
            return [BRepBuilderAPI.BRepBuilderAPI_MakeWire(b).Wire()]
        elif self.step == 3:
            point0, point1, point2 = self.previous_data
            if point2 == input:
                raise InvalidInputException
            pts = TColgp_Array1OfPnt(0, 3)
            pts.SetValue(0, point0)
            pts.SetValue(1, point1)
            pts.SetValue(2, point2)
            pts.SetValue(3, input)
            a = GeomAPI_PointsToBSpline(pts).Curve()
            b = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(a).Edge()
            self._final = [BRepBuilderAPI.BRepBuilderAPI_MakeWire(b).Wire()]
            return self._final

toolbar_visible = False

list = [Bspline3(), Bspline4()]
