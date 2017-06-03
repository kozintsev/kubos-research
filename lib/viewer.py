

import sys, os
import ctypes.util
import threading
import math

from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from OCC import V3d
from OCC.Quantity import Quantity_Color, Quantity_NOC_BLACK
from OCC import TPrsStd
from OCC.XCAFPrs import XCAFPrs_Driver_GetID
from OCC.Aspect import Aspect_TOTP_RIGHT_LOWER
from OCC.Visualization import Display3d
from OCC.AIS import AIS_Shaded, AIS_Shape, AIS_WireFrame
from OCC.TopoDS import TopoDS_Shape

from lib.vec import vec



if sys.platform != 'win32' and not 'CSF_GraphicShr' in os.environ:
    # Taken from OCC.Display.OCCViewer
    os.environ['CSF_GraphicShr'] = ctypes.util.find_library('TKOpenGl')

class Viewer(QtGui.QWidget):
    
    def __init__(self, doc):
        QtGui.QWidget.__init__(self)
        if sys.platform != 'win32' and 'DISPLAY' not in os.environ:
            raise Exception('The DISPLAY environment variable is not set.')
        self._inited = False
        # enable mouse tracking even if no button is pressed
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.WheelFocus)
        self.setAttribute(Qt.WA_PaintOnScreen)
        self.setAttribute(Qt.WA_NoSystemBackground)

        self._view_mode = 'shaded'
        self._zoom = 0.0333

        self.doc = doc

    def init2(self):
        """Perform the second initialization step. This should be done
        once the viewer is shown."""
        self._display = Display3d()
        # TODO: on Linux, self.winId returns a 'long' - if this is similar on
        # other platforms, conversion to int may not be neccessary
        idd = int(self.winId())
        self._display.Init(int(self.winId()))
        # types: AIS_InteractiveContext, V3d_View, V3d_Viewer
        self.context = self._display.GetContext().GetObject()
        self.view = self._display.GetView().GetObject()
        self.viewer = self._display.GetViewer().GetObject()

        self._inited = True
        # display the trihedron in the bottom right corner
        self.view.TriedronDisplay(Aspect_TOTP_RIGHT_LOWER, Quantity_NOC_BLACK,
                                  0.08,  V3d.V3d_WIREFRAME)
        self.view.SetBackgroundColor(Quantity_Color(1, 1, 1, 0))
        self.context.SetDisplayMode(AIS_Shaded)

        # Initialize and delete default lights
        # todo: fix later becase crasher
        # self.viewer.InitActiveLights()
        # for i in range(2):
        #     self.viewer.DelLight(self.viewer.ActiveLight())
        #     self.viewer.NextActiveLights()

        # ambient light
        self.add_light(V3d.V3d_AmbientLight(self.viewer.GetHandle()))

        # directional lights
        dl_1 = V3d.V3d_DirectionalLight(self.viewer.GetHandle())
        dl_2 = V3d.V3d_DirectionalLight(self.viewer.GetHandle())
        dl_1.SetDirection(2, 1, 3)
        dl_2.SetDirection(-2, -1, -3)
        self.add_light(dl_1)
        self.add_light(dl_2)

        self.zoom *= 60

        TPrsStd.TPrsStd_AISViewer_New(self.doc.top_label,
                                      self.context.GetHandle())
        # type: OCC.TPrsStd.TPrsStd_ASIPresentation
        # this is needed for updating the view with _ais_pres.Display(True)
        self._ais_pres = TPrsStd.TPrsStd_AISPresentation_Set(
            self.doc.top_label, XCAFPrs_Driver_GetID()).GetObject()

    def paintEvent(self, event):
        if self._inited:
            self.viewer.Redraw()

    def paintEngine(self):
        return None

    def resizeEvent(self, event):
        if self._inited:
            if sys.platform.startswith('linux'):
                # WORKAROUND: Calling MustBeResized without delay on Linux will
                #   update the view according to the previous size.
                threading.Timer(0.01, self.view.MustBeResized).start()
            else:
                self.view.MustBeResized()

    def wheelEvent(self, event):
        self.zoom *= 1.001**event.delta()

    def _get_zoom(self):
        return self._zoom
    def _set_zoom(self, value):
        if 0.013 < value < 4000:
            self.view.SetZoom(value / self._zoom)
            self._zoom = value
            self._update_grid_size()
    zoom = property(_get_zoom, _set_zoom)

    def pan(self, d):
        self.view.Pan(d[0], d[1])

    # TODO: rename to 'viewdir'
    def _get_eye(self):
        return self._eye
    def _set_eye(self, value):
        value = vec(value)
        value = value*(1/value.length())
        self.view.SetEye(*value)
        if value[0] == value[1] == 0:
            # this is the only case where the orientation of the view is
            #   ambiguous. Setting it so the y-Axis is horizontal
            self.view.SetTwist(math.pi / 2)
        else:
            # make the z-Axis vertical
            self.view.SetTwist(0)
        self._eye = value
    eye = property(_get_eye, _set_eye)

    def repaint0(self):
        """Recompute the visualization of the document and of all other
        displayed shapes."""
        self._ais_pres.Display(True)
        self.view.Redraw()

    def repaint1(self):
        """Recompute the visualization of all displayed shapes which are not
        part of the document (e.g. the preview)"""
        # self.view.Redraw()

    def add_light(self, light):
        """Adds a light to the viewer. Does nothing if the light is already
        present."""
        self.viewer.SetLightOn(light.GetHandle())

    def display_shape(self, shape, color=[.5, .5, .5]):
        """Display a shape with a specified color"""
        # this is only used internally in this class;
        # externally it is always called through "replace_shapes"
        if not isinstance(shape, TopoDS_Shape):
            raise TypeError(
                'cannot display objects of type {0}'.format(type(shape)))
        if not isinstance(color, (list, tuple)):
            raise TypeError
        color = Quantity_Color(color[0], color[1], color[2], 0)
        ais_shape = AIS_Shape(shape)
        self.context.SetColor(ais_shape.GetHandle(), color, 0)
        # pass False if viewer should not be updated
        self.context.Display(ais_shape.GetHandle(), True)
        self.shape_dict[shape] = ais_shape
        # TODO: return ais_shape?

    def erase_shape(self, shape):
        if shape not in self.shape_dict:
            raise Exception('shape not in shape_dict')
        self.context.Erase(self.shape_dict.pop(shape).GetHandle())

    def _get_view_mode(self):
        """"Style in which the view is presented ("wireframe" or "shaded")"""
        return self._view_mode
    def _set_view_mode(self, value):
        self._view_mode = value
        if value == 'shaded':
            self.context.SetDisplayMode(AIS_Shaded)
        elif value == 'wireframe':
            self.context.SetDisplayMode(AIS_WireFrame)
    view_mode = property(_get_view_mode, _set_view_mode)
