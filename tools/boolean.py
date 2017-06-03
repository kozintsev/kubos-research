

from PyQt4 import QtCore
from OCC import TopAbs

from lib import boolean
from tools.tool import Tool

from exceptions_ import InvalidInputException, ConstructionError


class Intersection(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Boolean', '&Intersection']
        self.icon = 'boolean-intersection'
        self.shortcut = 'Ctrl+I'
        self.steps = 2
        self.input_types = ['object', 'object']
        self.help = ['Pick the first object', 'Pick the second object']

        self.reset()

    def preview(self, input, direction):
        if self.step == 0:
            self.previous_data = [input]
            return []
        elif self.step == 1:
            shape_1 = self.previous_data[0]
            shape_2 = input
            try:
                self._final = boolean.intersection(shape_1, shape_2)
            except ConstructionError:
                raise InvalidInputException
            dim = {TopAbs.TopAbs_SOLID: 3,
                   TopAbs.TopAbs_SHELL: 2,
                   TopAbs.TopAbs_FACE: 2,
                   TopAbs.TopAbs_WIRE: 1,
                   TopAbs.TopAbs_EDGE: 1,
                   TopAbs.TopAbs_VERTEX: 0,
                   TopAbs.TopAbs_COMPOUND: None,
                   TopAbs.TopAbs_SHAPE: None}
            # Remove only those of the original shapes that have the
            # same dimensionality as the resulting shape
            self.remove = []
            for shape in [shape_1, shape_2]:
                if dim[shape.ShapeType()] == dim[self._final[0].ShapeType()]:
                    self.remove.append(shape)
            return self._final


class Difference(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Boolean', 'Dif&ference']
        self.icon = 'boolean-difference'
        self.shortcut = 'Ctrl+F'
        self.steps = 2
        self.input_types = ['object', 'object']
        self.help = ['Pick the first object', 'Pick the second object']

        self.reset()

    def preview(self, input, direction):
        if self.step == 0:
            self.previous_data = [input]
            return []
        elif self.step == 1:
            self.remove = [self.previous_data[0], input]
            self._final = boolean.difference(self.previous_data[0], input)
            return self._final


class Union(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Boolean', '&Union']
        self.icon = 'boolean-union'
        self.shortcut = 'Ctrl+U'
        self.steps = 2
        self.input_types = ['object', 'object']
        self.help = ['Pick the first object', 'Pick the second object']

        self.reset()

    def preview(self, input, direction):
        if self.step == 0:
            self.previous_data = [input]
            return []
        elif self.step == 1:
            self.remove = [self.previous_data[0], input]
            try:
                self._final = boolean.union(self.previous_data[0], input)[0:1]
            except RuntimeError:
                raise InvalidInputException
            return self._final

toolbar_area = QtCore.Qt.LeftToolBarArea
toolbar_visible = True

list = [Intersection(), Difference(), Union()]
