

import math

from PyQt4.QtCore import Qt
from OCC import gp, TopLoc, GC, BRepBuilderAPI

from lib.vec import vec
from lib import gp_
from lib import copy_geom

from tools.tool import Tool
from exceptions_ import InvalidInputException


class Translate(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Transform', '&Tanslate']
        self.steps = 3
        self.input_types = ['object', 'point', 'point']
        self.icon = 'transform-move'
        self.shortcut = 'Ctrl+T'
        self.help = ['Pick the object to Translate',
                     'Enter the start point',
                     'Enter the target point']

        self.reset()

    def preview(self, input, direction):
        if self.step == 0:
            self.previous_data = [input]
            return []
        elif self.step == 1:
            self.previous_data = [self.previous_data[0], input]
            return []
        elif self.step == 2:
            object, point0 = self.previous_data
            vector = input - point0
            tr = gp.gp_Trsf()
            tr.SetTranslation(vector.to_gp_Vec())
            loc = TopLoc.TopLoc_Location(tr)
            t = object.Moved(loc)
            self.remove = [self.previous_data[0]]
            self._final = [copy_geom.copy(t)]
            return self._final


class Rotate(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Transform', '&Rotate']
        self.steps = 4
        self.input_types = ['object', 'point', 'point', 'point']
        self.icon = 'transform-rotate'
        self.shortcut = 'Ctrl+R'
        self.help = ['Pick the object to rotate',
                     'Enter the axis of rotation',
                     'Enter a point to determine the start of the rotation',
                     'Enter a point to determine the target of the rotation']

        self.prev_dat = {}

        self.reset()

    def preview(self, input, direction):
        if self.step == 0:
            # object to rotate
            self.prev_dat['object'] = input
            return []
        elif self.step == 1:
            # axis to rotate about
            dirvec = vec(0, 0, 0)
            dirvec[direction] = 1
            axis = gp.gp_Ax1(input, dirvec.to_gp_Dir())

            # make a copy (copy.copy does not work)
            point = gp_.gp_Pnt_(input)
            point[direction] += 2
            input[direction] -= .2
            axis_plot = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(
                            GC.GC_MakeSegment(input, point).Value()).Edge()

            self.prev_dat['point'] = input
            self.prev_dat['dirvec'] = dirvec
            self.prev_dat['axis'] = axis
            self.prev_dat['axis-plot'] = axis_plot
            return [axis_plot]
        elif self.step == 2:
            # start point
            self.prev_dat['point_start'] = input
            return [self.prev_dat['axis-plot']]
        elif self.step == 3:
            p0 = self.prev_dat['point']
            vec0 = self.prev_dat['point_start'] - p0
            vec1 = input - p0

            dirvec = self.prev_dat['dirvec']
            n0 = dirvec.cross(vec0)
            n1 = dirvec.cross(vec1)
            try:
                cos = n0.dot(n1) / (n0.length() * n1.length())
            except ZeroDivisionError:
                raise InvalidInputException
            angle = math.acos(min(max(cos, -1), 1))  # cos might be (-)1.000001

            oriented_dirvec = n0.cross(n1)
            if oriented_dirvec == vec(0, 0, 0):
                raise InvalidInputException
            axis = gp.gp_Ax1(p0, oriented_dirvec.to_gp_Dir())

            tr = gp.gp_Trsf()
            tr.SetRotation(axis, angle)
            t = self.prev_dat['object'].Moved(TopLoc.TopLoc_Location(tr))
            t = copy_geom.copy(t)
            self._final = [t]
            self.remove = [self.prev_dat['object']]
            return [t, self.prev_dat['axis-plot']]


class Mirror(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Transform', '&Mirror']
        self.steps = 1
        self.input_types = ['object']
        self.icon = 'transform-mirror'
        self.shortcut = 'Ctrl+M'
        self.help = ['Pick the object to mirror. It will be mirrored about'
                     ' the active plane.']

        self.reset()

    def preview(self, input, direction):
        assert self.step == 0
        vec_ = vec(0, 0, 0)
        vec_[direction] = 1
        tr = gp.gp_Trsf()
        tr.SetMirror(gp.gp_Ax2(gp_.gp_Pnt(0, 0, 0), vec_.to_gp_Dir()))
        # object.Moved() cannot be used here because it does not adjust
        # the surface orientation and will result in incorrect models
        t = BRepBuilderAPI.BRepBuilderAPI_Transform(input, tr).Shape()
        t = copy_geom.copy(t)
        self._final = [t]
        self.remove = [input]
        return self._final

toolbar_visible = True
toolbar_area = Qt.LeftToolBarArea

list = [Translate(), Rotate(), Mirror()]
