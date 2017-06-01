from __future__ import absolute_import,division,print_function,unicode_literals

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict  # on Python 2.6
from contextlib import contextmanager
import os
import shutil

from OCC import XCAFApp, TDocStd, XCAFDoc, TopLoc, gp
from OCC.TCollection import TCollection_ExtendedString
from OCC.Quantity import Quantity_Color
from OCC import TopoDS, TopAbs
from OCC.STEPControl import STEPControl_AsIs

from ..lib import tempfile_
from ..lib.subshapes import subshapes
from ..std_events import document_modified


class ShapeToolCtrl(object):

    # FIXME: This was formerly part of /doc.py and doesn't work at the moment

    def __init__(self, shape_tool):
        self._shape_tool = shape_tool

    def add_shape(self, shape, make_assembly=True, make_prepare=True):
        # this can be used instead of "shape_tool.AddShape" and should provide
        # the same functionality.
        from OCC import TNaming
        # equivalent of "XCAFDoc_ShapeTool::addShape"
        new_label = doc_ctrl.top_label.NewChild()
        builder = TNaming.TNaming_Builder(new_label)
        builder.Generated(shape)
        return new_label


class DocCtrl(object):
    """Generic document controller.

    This class manages a "TDocStd_Document" which is accessible through
    "self.document"."""""
    def __init__(self):
        # is the document empy and unmodified?
        self.isnew = True

        # dictionary which associates each shape label with a component label
        self._label_dict = OrderedDict()

        h_doc = TDocStd.Handle_TDocStd_Document()
        XCAFApp.GetApplication().GetObject().NewDocument(
                        TCollection_ExtendedString(b'MDTV-CAF'), h_doc)

        # type: OCC.TDocStd.TDocStd_Document
        self.document = h_doc.GetObject()
        self.document.SetUndoLimit(30)

        # label: [0:1]
        main_label = self.document.Main()
        self.main_label = main_label

        # type: XCAFDoc_ShapeTool
        self._shape_tool = (XCAFDoc.XCAFDoc_DocumentTool.ShapeTool(main_label).
                            GetObject())
        # type: XCAFDoc_ColorTool
        self._color_tool = (XCAFDoc.XCAFDoc_DocumentTool.ColorTool(main_label).
                            GetObject())

        # label: [0:1:1:1]
        self.top_label = self._shape_tool.NewShape()
        new_lbl = self.top_label.NewChild()

        # default location for objects
        self._loc = TopLoc.TopLoc_Location(gp.gp_Trsf())

    def open(self, file):
        """Open a STEP file"""
        try:
            # for pythonOCC 0.5
            from OCC.Utils.DataExchange.STEP import STEPImporter
        except ImportError:
            # for pythonOCC 0.6
            from OCC.DataExchange.STEP import STEPImporter
        # Remove all existing shapes
        self.clear()

        # WORKAROUND: There would be problems if we import from a filename with
        #   non-ASCII characters in it. In ordert to avoid this, we move the
        #   file to a temporary loaction with only ASCII characters and read
        #   it from there. Corresponding OCCT bug report:
        #   http://tracker.dev.opencascade.org/view.php?id=22484
        with tempfile_.TemporaryDirectory() as tempdir:
            tfile = os.path.join(tempdir, 'importfile.stp')
            shutil.copy(file, tfile)
            importer = STEPImporter(bytes(tfile))
            importer.read_file()
            shapes = importer._shapes[0]  # TODO: import other shapes too?
            comp = TopoDS.TopoDS_compound(shapes)
            # The second argument of this function determines the shape type.
            #   If it is TopoDS_compound only one shape
            #   containing the others will be loaded.
            for compound in subshapes(comp, TopAbs.TopAbs_COMPOUND):
                for shape in subshapes(compound, TopAbs.TopAbs_SOLID):
                    from ..lib import copy_geom
                    # FIXME: This is a very ugly workaround, get rid of it:
                    #    Each shape is copied before adding it to the document
                    #    Otherwise the method get_comp_label would not find
                    #    the label of this shape so it could not be removed
                    #    from the document again
                    shape = copy_geom.copy(shape)
                    self.add(shape)


    def save(self, file):
        """Save to a file in STEP format"""
        from OCC.STEPCAFControl import STEPCAFControl_Writer
        writer = STEPCAFControl_Writer()
        writer.Transfer(self.document.GetHandle(), STEPControl_AsIs)
        # WORKAROUND: See comment for function 'open'
        with tempfile_.TemporaryDirectory() as tempdir:
            tfile = bytes(os.path.join(tempdir, 'exportfile.stp'))
            status = writer.Write(tfile)
            assert status == 1
            shutil.move(tfile, file)

    @contextmanager
    def open_command(self):
        self.document.OpenCommand()
        yield
        self.document.CommitCommand()
        # TODO: probably emit signal "document_modified"

    def undo(self):
        self.document.Undo()

    def redo(self):
        self.document.Redo()

    def add(self, shape, color=[0, 0, 1]):
        """Add a shape to the document"""
        shape_label = self._shape_tool.AddShape(shape, False)
        comp_label = self._shape_tool.AddComponent(self.top_label, shape_label,
                                                   self._loc)
#        print(self._shape_tool.IsReference(shape_label))
#        print(self._shape_tool.IsReference(comp_label))
#        print(self._shape_tool.IsTopLevel(shape_label))
#        print(self._shape_tool.IsTopLevel(comp_label))
        # The following command could replace the previous two, but then there
        # would be no way to access "shape_label"
        #   comp_label = self._shape_tool.AddComponent(self.top_label, shape,
        #                                              False)
        # the color can be set on either 'shape_label' or 'comp_label' with the
        # same effect
        self.set_color(shape_label, color)
        self._label_dict[shape_label] = comp_label
        self.isnew = False
        document_modified.emit()

    def remove(self, shape):
        """Remove a shape from the document"""
        comp_label = self.get_comp_label(shape)
        self._shape_tool.RemoveComponent(comp_label)

    def get_shape_label(self, shape):
        return self._shape_tool.FindShape(shape)

    def get_comp_label(self, shape):
        """Return the label of the component corresponding to the given shape
        """
        shape_label = self._shape_tool.FindShape(shape)
        for sl in self._label_dict:
            if sl.IsEqual(shape_label):
                return self._label_dict[sl]
        else:
            raise LookupError

    def set_color(self, label, color):
        color = Quantity_Color(color[0], color[1], color[2], 0)
        self._color_tool.SetColor(label, color, XCAFDoc.XCAFDoc_ColorGen)

    def clear(self):
        """Remove all shapes from the document"""
        for comp in self._label_dict.values():
            self._shape_tool.RemoveComponent(comp)
        self._label_dict.clear()
        document_modified.emit()
