import sys
import math

from PyQt4 import QtCore, QtGui
from OCC.Aspect import Aspect_GDM_Lines, Aspect_GT_Rectangular
from OCC import TopAbs
from OCC.gp import gp_Ax3, gp_Dir
from OCC.Quantity import Quantity_Color

from lib.gp_ import gp_Pnt_
from lib.viewer import Viewer

from data import appdata
import std_events
import active_tool
import tools.select

# some of this module was taken from OCC.Display.OCCViewer
# It might be a good idea to look at code of that module if this one
# causes problems


class KubosViewer(Viewer):

    def __init__(self, doc):
        Viewer.__init__(self, doc)
        self.setWhatsThis('Geometry View\n\n'
                          'right mouse button: rotate\n'
                          'middle mouse button: pan\n'
                          'mouse wheel: zoom')

        self._grid = False
        self._active_plane = 2
        self._selection = []
        self.shapes = {'preview': []}
        # dictionary that associates each shape with its corresponding
        # AIS_Shape
        self.shape_dict = {}

        std_events.new_step_activated.connect(self.update_preview)
        std_events.input_changed.connect(self.update_preview)
        std_events.document_modified.connect(self.on_document_modified)

    def init2(self):
        Viewer.init2(self)
        self.eye = [0.82, 0.45, 0.36]
        self._update_grid_size()
        self.viewer.Grid().GetObject().SetColors(Quantity_Color(.9, .9, .9, 0),
                                                 Quantity_Color(.8, .8, .8, 0))

    def mouseMoveEvent(self, event):
        pos = [event.x(), event.y()]
        # Rotate
        if event.buttons() == QtCore.Qt.RightButton:
            # TODO: 1.0: 2012-08-31: rotation should not always be about the
            # origin
            phi = math.atan2(self.eye[1], self.eye[0])
            phi -= (pos[0] - self._drag_start[0]) / 200
            teta = math.acos(self.eye[2])
            teta -= (pos[1] - self._drag_start[1]) / 100
            # Avoid the angle getting less than 0 or greater than Pi
            teta = min(max(teta, 0.00001), 3.14159)
            self._drag_start = pos
            self.eye = [math.sin(teta) * math.cos(phi),
                        math.sin(teta) * math.sin(phi),
                        math.cos(teta)]
        # Pan
        elif event.buttons() == QtCore.Qt.MidButton:
            d = [pos[i] - self._drag_start[i] for i in range(2)]
            self._drag_start = pos
            self.pan([d[0], -d[1]])
        # "Geometry tool"
        elif event.buttons() == QtCore.Qt.NoButton:
            self._update_input()

    def _update_input(self):
        """Update the input based on the current position of the mouse"""
        # TODO: 0.3: Detected shape should be highlighted
        pos = self.mapFromGlobal(QtGui.QCursor.pos())
        pos = [pos.x(), pos.y()]
        if active_tool.active_tool.input_type == 'object':
            # TODO: Currently the preview is always removed and redisplayed
            # on every input change in order to avoid it being selected.
            # Make it unselectable.
            self.replace_shapes('preview', [])
            # HACK
            # iterate over all possible object types and try to select one
            #   of them:
            for selection_mode in [TopAbs.TopAbs_SOLID, TopAbs.TopAbs_SHELL,
                                   TopAbs.TopAbs_FACE, TopAbs.TopAbs_WIRE,
                                   TopAbs.TopAbs_EDGE, TopAbs.TopAbs_VERTEX]:
                self.context.CloseLocalContext()
                self.context.OpenLocalContext()
                self.context.ActivateStandardMode(selection_mode)
                self.context.MoveTo(pos[0], pos[1], self.view.GetHandle())
                if sys.platform.startswith('win'):
                    self.context.MoveTo(pos[0], pos[1], self.view.GetHandle())
                if self.context.HasDetected():
                    appdata.set('input', self.context.DetectedShape())
                    break
            else:
                appdata.set('input', None)
        else:
            self.context.CloseLocalContext()
            self.context.OpenLocalContext()
            self.context.ActivateStandardMode(TopAbs.TopAbs_VERTEX)
            self.context.MoveTo(pos[0], pos[1], self.view.GetHandle())
            if sys.platform.startswith('win'):
                # WORKAROUND: call this twice on Windows
                self.context.MoveTo(pos[0], pos[1], self.view.GetHandle())

            if self.context.HasDetected():
                a = gp_Pnt_(self.context.DetectedShape())
            elif not self.grid:
                view_point = self.view.ConvertToGrid(*pos)
                view_direction = [self.view.At()[i] - self.view.Eye()[i]
                                  for i in range(3)]
                active_direction = self.active_plane
                point = [view_point[i] - view_point[active_direction] *
                         view_direction[i]/view_direction[active_direction]
                         for i in range(3)]
                a = gp_Pnt_(point)
            else:
                a = gp_Pnt_(self.view.ConvertToGrid(*pos))
            appdata.set('input', a)

    def mousePressEvent(self, event):
        pos = [event.x(), event.y()]
        self._drag_start = pos
        if event.buttons() in [QtCore.Qt.MidButton, QtCore.Qt.RightButton]:
            # for panning or zooming: clear the preview
            self.replace_shapes('preview', [])
        elif event.buttons() == QtCore.Qt.LeftButton:
            if (active_tool.active_tool is tools.select.select and
                    appdata.get('input') is not None):
                # FIXME: 1.0: the selection will be cleared immediately after
                # this command as the active context will be closed
                self.context.Select()
                self.selection = appdata.get('input')
            else:
                std_events.input_accepted.emit()

    def mouseReleaseEvent(self, event):
        # update the input after rotating or panning the view
        self._update_input()

    def _get_active_plane(self):
        return self._active_plane
    def _set_active_plane(self, value):
        if value == self._active_plane:
            return
        if value == 2:
            axis = gp_Ax3(gp_Pnt_([0, 0, 0]), gp_Dir(0, 0, 1), gp_Dir(1, 0, 0))
        elif value == 1:
            axis = gp_Ax3(gp_Pnt_([0, 0, 0]), gp_Dir(0, 1, 0), gp_Dir(0, 0, 1))
        elif value == 0:
            axis = gp_Ax3(gp_Pnt_([0, 0, 0]), gp_Dir(1, 0, 0), gp_Dir(0, 1, 0))
        self._active_plane = value
        appdata.set('active_plane', value)
        self.viewer.SetPrivilegedPlane(axis)
        # TODO: 0.3: these should probably be called through signals
        self._update_input()
        self.update_preview()
    active_plane = property(_get_active_plane, _set_active_plane)

    def replace_shapes(self, name, new_shapes):
        """Replace a group of shapes from the display.

        Replace the shapes specified by their name with those passed to the
        function and refresh the view.
        Possible inputs for "name" are 'preview', 'construction' and
        'trihedron'.
        If "new_shapes" is empty, erase the shapes and do not replace them.
        """
        for shape in self.shapes[name]:
            self.erase_shape(shape)
        for shape in new_shapes:
            self.display_shape(shape, [0, 0, 1])
        self.shapes[name] = new_shapes
        self.repaint1()

    # TODO: turn this into a callable: viewer.get_selected()
    def _get_selection(self):
        """"List of selected objects"""
        return self._selection
    def _set_selection(self, value):
        self._selection = value
        std_events.selection_changed.emit()
    selection = property(_get_selection, _set_selection)

    def _get_grid(self):
        """Determines whether the grid is active"""
        return self._grid
    def _set_grid(self, value):
        if value != self._grid:
            self._grid = value
            if value:
                self.viewer.ActivateGrid(Aspect_GT_Rectangular,
                                         Aspect_GDM_Lines)
            else:
                self.viewer.DeactivateGrid()
            std_events.grid_changed.emit()
    grid = property(_get_grid, _set_grid)

    def _update_grid_size(self):
        """Update the grid according to the current zoom"""
        # WORKAROUND: snapping to the grid is broken for grid sizes <0.1 .
        #   Do not create any smaller grids
        zoom_level = int(round(math.log10(self.zoom)))
        size = max(10 ** -zoom_level, .1)
        self.viewer.SetRectangularGridGraphicValues(100*size, 100*size, 0)
        self.viewer.SetRectangularGridValues(0, 0, size, size, 0)

    def update_preview(self):
        """Update the preview from the current input

        Create a new preview shape from the current input and replace the
        old preview with the new shape"""
        # Input could be a point, a geometric object or "None"
        a = active_tool.preview_from_current_input()
        self.context.CloseLocalContext()
        self.replace_shapes('preview', a)
        self.context.OpenLocalContext()
        # TODO: 0.3: check if a specific selection mode should be activated

    def on_document_modified(self):
        """Handle the "document_modified" event"""
        # WORKAROUND: If the view is updated when shaded mode is active, then
        #   the mode is switched to wireframe and back to shaded, all non-solid
        #   elements are gone from the display.  So switch to wireframe mode
        #   before repainting
        self.context.CloseLocalContext()
        mode = self.view_mode
        self.view_mode = 'wireframe'
        self.repaint0()
        self.view_mode = mode
        self.context.OpenLocalContext()
