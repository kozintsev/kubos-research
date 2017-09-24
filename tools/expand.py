

from PyQt5 import QtCore

from OCC import gp, BRepPrimAPI, BRepBuilderAPI, TopoDS


from lib.vec import vec

from tools.tool import Tool

from exceptions_ import InvalidInputException



class Extrude(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['E&xpand', 'E&xtrude']
        self.steps = 2
        self.input_types = ['object', 'point']
        self.icon = 'cad-extrude'
        self.shortcut = 'Ctrl+E'
        self.help = ['Pick an object to extrude. It will be extruded '
                     'othogonally to the active plane',
                     'Determine the height of extrusion']

        self.reset()

    def preview(self, input, direction):
        if self.step == 0:
            from OCC import TopExp, TopAbs, BRep

            exp = TopExp.TopExp_Explorer(input, TopAbs.TopAbs_VERTEX)
            v1 = TopoDS.topods_Vertex(exp.Current())
            v1_ = BRep.BRep_Tool.Pnt(TopoDS.TopoDS_Vertex(v1))
            # TODO: 0.3: finish: automatically determine orthogonal direction
            # from
            #   input
            self.previous_data = [input, direction]
            try:
                wire = TopoDS.TopoDS_Wire(input)
                print(dir(wire))
            except:
                pass
            return ()
        elif self.step == 1:
            object, dir_ = self.previous_data[:]

            dirvec = [0, 0, 0]
            dirvec[dir_] = input[dir_]
            if dirvec == [0, 0, 0]:
                raise InvalidInputException
            self.remove = [self.previous_data[0]]
            self._final = [BRepPrimAPI.BRepPrimAPI_MakePrism(
                                object, gp.gp_Vec(*dirvec)).Shape()]
            return self._final


class Fill(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['E&xpand', '&Fill']
        self.steps = 1
        self.input_types = ['object']
        self.icon = 'edit-fill'
        self.shortcut = ''
        self.help = ['Pick a planar curve to fill it']

        self.reset()

    def preview(self, input, direction):
        try:
            wire = TopoDS.TopoDS_wire(input)
        except RuntimeError:
            raise InvalidInputException
        face = BRepBuilderAPI.BRepBuilderAPI_MakeFace(wire).Face()
        self.remove = [input]
        self._final = [face]
        return self._final


class Rotate(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['E&xpand', '&Rotate']
        self.steps = 2
        self.input_types = ['object', 'point']
        self.icon = 'cad-revolve'
        self.shortcut = ''
        self.help = ['Pick a curve or a surface',
                     'Select the axis to rotate about']

        self.reset()

    def preview(self, input, direction):
        if self.step == 0:
            self.previous_data = [input]
            return []
        elif self.step == 1:
            object = self.previous_data[0]
            dirvec = vec(0, 0, 0)
            dirvec[direction] = 1
            axis = gp.gp_Ax1(input, dirvec.to_gp_Dir())
            self.remove = [self.previous_data[0]]
            self._final = [BRepPrimAPI.BRepPrimAPI_MakeRevol(
                                                object, axis).Shape()]
            return self._final

toolbar_area = QtCore.Qt.LeftToolBarArea
toolbar_visible = True

list = [Extrude(), Rotate(), Fill()]
