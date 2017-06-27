

from OCC import BRepBuilderAPI, GC, gp, Geom
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.gp import gp_Pnt
from PyQt4 import QtCore

from .tool import Tool
from exceptions_ import InvalidInputException
from lib.vec import vec


class Point(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Primitives', '&Point']
        self.steps = 1
        self.input_types = ['point']

        self.help = ['Pick the location of the point']
        self.icon = 'cad-point'
        self.shortcut = 'Ctrl+P'

        self.reset()

    def preview(self, input_pnt, direction):
        assert self.step == 0
        preview = BRepBuilderAPI.BRepBuilderAPI_MakeVertex(input_pnt).Vertex()
        self._final = [preview]
        return self._final


class Segment(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Primitives', 'Se&gment']
        self.steps = 2
        self.input_types = ['point', 'point']

        self.help = ['Enter the start point', 'Enter the end point']
        self.icon = 'cad-segment'
        self.shortcut = 'Ctrl+G'

        self.reset()

    def preview(self, inp, direction):
        if self.step == 0:
            self.previous_data = [inp]
            return [BRepBuilderAPI.BRepBuilderAPI_MakeVertex(inp).Vertex()]
        elif self.step == 1:
            point0 = self.previous_data[0]
            # checking if the previous points are identical: This is necessary
            # before continuing in order to avoid a crash on Windows
            if point0 == inp:
                raise InvalidInputException
            a = GC.GC_MakeSegment(inp, point0).Value()
            b = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(a).Edge()
            self._final = [BRepBuilderAPI.BRepBuilderAPI_MakeWire(b).Wire()]
            return self._final


class Line(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Primitives', '&Line']
        self.steps = 2
        self.input_types = ['point', 'point']

        self.help = ['Enter the first point on the line',
                     'Enter the second point on the line']
        self.icon = 'cad-line'
        self.shortcut = 'Ctrl+L'

        self.reset()

    def preview(self, inp, direction):
        if self.step == 0:
            self.previous_data = [inp]
            return [BRepBuilderAPI.BRepBuilderAPI_MakeVertex(inp).Vertex()]
        elif self.step == 1:
            point0 = self.previous_data[0]
            # checking if the previous points are identical: This is necessary
            # before continuing in order to avoid a crash on Windows
            if point0 == inp:
                raise InvalidInputException
            point1 = inp
            dir_ = point1 - point0
            len = dir_.length()
            p0 = point0 + 1000/len * dir_
            p1 = point0 - 1000/len * dir_
            a = GC.GC_MakeSegment(p0.to_gp_Pnt(), p1.to_gp_Pnt()).Value()
            b = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(a).Edge()
            self._final = [BRepBuilderAPI.BRepBuilderAPI_MakeWire(b).Wire()]
            return self._final


class Circle(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Primitives', '&Circle']
        self.steps = 2
        self.input_types = ['point', 'point']

        self.help = ['Enter the center of the circle',
                     'Enter a point to determine the radius of the '
                     'circle. Change the active plane to set its orientation.']
        self.icon = 'cad-circle'

        self.reset()

    def preview(self, inp, direction):
        if self.step == 0:
            self.previous_data = [inp]
            return [BRepBuilderAPI.BRepBuilderAPI_MakeVertex(inp).Vertex()]
        elif self.step == 1:
            point0 = self.previous_data[0]
            # checking if the previous points are identical: This is necessary
            # before continuing in order to avoid a crash on Windows
            if point0 == inp:
                raise InvalidInputException
            dirvec = vec(0, 0, 0)
            dirvec[direction] = 1
            axis = gp.gp_Ax2(point0, dirvec.to_gp_Dir())

            d = point0 - inp
            d[direction] = 0
            dist = d.length()

            a = Geom.Geom_Circle(axis, dist).GetHandle()
            b = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(a).Edge()
            c = BRepBuilderAPI.BRepBuilderAPI_MakeWire(b).Wire()
            self._final = [c]
            return self._final


class Disk(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Primitives', '&Disk']
        self.steps = 2
        self.input_types = ['point', 'point']

        self.help = ['Enter the center of the disk',
                     'Enter a point to determine the radius of the '
                     'disk. Change the active plane to set its orientation.']
        self.icon = 'cad-disk'

        self.reset()

    def preview(self, inp, direction):
        if self.step == 0:
            self.previous_data = [inp]
            return [BRepBuilderAPI.BRepBuilderAPI_MakeVertex(inp).Vertex()]
        elif self.step == 1:
            point0 = self.previous_data[0]
            point1 = inp
            # checking if the previous points are identical: This is necessary
            # before continuing in order to avoid a crash on Windows
            if point0 == point1:
                raise InvalidInputException
            dirvec = vec(0, 0, 0)
            dirvec[direction] = 1
            axis = gp.gp_Ax2(point0, dirvec.to_gp_Dir())

            d = point0 - inp
            d[direction] = 0
            dist = d.length()

            a = Geom.Geom_Circle(axis, dist).GetHandle()
            b = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(a).Edge()
            c = BRepBuilderAPI.BRepBuilderAPI_MakeWire(b).Wire()
            d = BRepBuilderAPI.BRepBuilderAPI_MakeFace(c).Face()
            self._final = [d]
            return self._final


class Rectangle(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Primitives', '&Rectangle']
        self.steps = 2
        self.input_types = ['point', 'point']

        self.help = ['Enter one vertex of the rectangle',
                     'Enter the opposite vertex of the rectangle. '
                     'The rectangle will be parallel to the active plane']
        self.icon = 'cad-rectangle'

        self.reset()

    def preview(self, inp, direction):
        if self.step == 0:
            self.previous_data = [inp]
            return [BRepBuilderAPI.BRepBuilderAPI_MakeVertex(inp).Vertex()]
        elif self.step == 1:
            point0 = self.previous_data[0]
            point1 = inp
            point1[direction] = point0[direction]
            if (point1[direction-1] == point0[direction-1] or
                point1[direction-2] == point0[direction-2]):
                raise InvalidInputException
            points = []
            # add two other corners:
            for i in range(3):
                if i != direction:
                    point = point0[:]
                    point[i] = point1[i]
                    points.append(point)
            points.insert(1, point0)
            points.insert(3, point1)

            builder = BRepBuilderAPI.BRepBuilderAPI_MakePolygon()
            for pnt in points:
                builder.Add(gp.gp_Pnt(*pnt))
            builder.Build()
            builder.Close()
            polygon = builder.Wire()

            face = BRepBuilderAPI.BRepBuilderAPI_MakeFace(polygon).Face()
            self._final = [face]
            return self._final


class RegularPolygon(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Primitives', 'R&egular Polygon']
        self.steps = 2
        self.input_types = ['point', 'point']

        self.help = ['Enter the center of the polygon',
                     'Enter a vertex of the polygon. '
                     'The polygon will be parallel to the active plane']
        self.icon = 'cad-regular_polygon'

        self.reset()


class Sphere(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Primitives', '&Sphere']
        self.steps = 2
        self.input_types = ['point', 'point']

        self.help = ['Enter the center of the sphere',
                     "Enter a point on the sphere's surface"]
        self.icon = 'cad-sphere'

        self.reset()

    def preview(self, inp, direction):
        if self.step == 0:
            self.previous_data = [inp]
            return [BRepBuilderAPI.BRepBuilderAPI_MakeVertex(inp).Vertex()]
        elif self.step == 1:
            center = self.previous_data[0]
            radius = (center - inp).length()
            if not radius:
                raise InvalidInputException
            self._final = [BRepPrimAPI_MakeSphere(center, radius).Solid()]
            return self._final

toolbar_area = QtCore.Qt.LeftToolBarArea
toolbar_visible = True

list = [Point(), Segment(), Line(), Circle(), Disk(), Rectangle(), Sphere()]
