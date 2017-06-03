

import imp

from OCC import BRepPrimAPI, TopAbs
from PyQt4 import QtGui

import doc
from lib import gp_
from data import appdata
from lib.action import Action
from gui import viewer_3d
from gui import win
from doc import doc_ctrl
from std_events import document_modified


def sphere1_():
    import random
    shape = BRepPrimAPI.BRepPrimAPI_MakeSphere(
                    gp_.gp_Pnt_([0, 0, random.random() * 7]), 1).Shape()
    doc.doc_ctrl.add(shape)
sphere1 = Action(sphere1_, ('Te&sts', '&Sphere1'))

from OCC import GC, BRepBuilderAPI


def segment_():

    p0 = gp_.gp_Pnt_([0, 0, 0])
    p1 = gp_.gp_Pnt_([1, 1, 1])
    a = GC.GC_MakeSegment(p0, p1).Value()
    print(type(a))
    print(dir(a.GetObject()))
    final = BRepBuilderAPI.BRepBuilderAPI_MakeEdge(a).Shape()
    print(type(final))
    print(dir(final.TShape().GetObject()))
    print(dir(final))
segment = Action(segment_, ('Te&sts', 'S&egment'))


def select_vertex_action():
    viewer_3d.context.CloseLocalContext()
    viewer_3d.context.OpenLocalContext()
    viewer_3d.context.ActivateStandardMode(TopAbs.TopAbs_SOLID)
select_vertex = Action(select_vertex_action, ('Te&sts', 'Select &Vertex'))


def select_shape_action():
    viewer_3d.context.CloseLocalContext()
    viewer_3d.context.OpenLocalContext()
    viewer_3d.context.ActivateStandardMode(TopAbs.TopAbs_VERTEX)
select_shape = Action(select_shape_action, ('Te&sts', 'Select &Shape'))


def list_data_():
    for key, value in appdata.__dict__.items():
        if not key.startswith('__'):
            print(key, ':\n    ', value)
list_data = Action(list_data_, ('Te&sts', 'List &Data'))


def list_children_():
    from lib import label_util
    import doc
    print(label_util.child_list(doc.doc_ctrl.top_label))
list_children = Action(list_children_, ('Te&sts', 'List &Children'))


def remove_random_():
    doc.doc_ctrl.remove_random()
remove_random = Action(remove_random_, ('Te&sts', 'Remove &Random'))

n = 0


def select_next_():
    global n
    doc.doc_ctrl.select_by_number(n)
    n += 1
select_next = Action(select_next_, ('Te&sts', 'Select &Next'))


def remove_selected_():
    doc.doc_ctrl.remove_selected()
remove_selected = Action(remove_selected_, ('Te&sts', '&Remove Selected'),
                          icon='edit-delete')

toolbar_visible = False

list = (segment, sphere1, select_vertex, select_shape, list_data, remove_random,
        select_next, remove_selected, list_children)
