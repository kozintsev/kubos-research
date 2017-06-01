# This module can be used to add custom actions to Kubos

from __future__ import absolute_import,division,print_function,unicode_literals

from ..lib.action import Action


def demo_():
    from math import pi, sin, cos
    from ..gui import viewer_3d
    from OCC import BRepPrimAPI

    quader = BRepPrimAPI.BRepPrimAPI_MakeBox(3, 4, 5).Solid()
    viewer_3d.display_shape(quader)
    viewer_3d.view_mode = 'shaded'
    viewer_3d.zoom = 1
    N = 40
    for i in range(N):
        phi = i/N * pi + pi/6
        viewer_3d.eye = [sin(phi), cos(phi), phi/5]
        viewer_3d.zoom *= 1.05
demo = Action(demo_, ['M&y Actions', '&Demo'])


def doc_demo_():
    from ..doc import doc_ctrl
    from OCC import BRepPrimAPI
    quader = BRepPrimAPI.BRepPrimAPI_MakeBox(3, 4, 5).Solid()
    kugel = BRepPrimAPI.BRepPrimAPI_MakeSphere(2).Solid()
    with doc_ctrl.open_command():
        doc_ctrl.add(quader)
        doc_ctrl.set_color(quader, [0, 1, 0])
    with doc_ctrl.open_command():
        doc_ctrl.add(kugel)
        doc_ctrl.set_color(kugel, [1, 0, 0])
    #doc_ctrl.save()
doc_demo = Action(doc_demo_, ['M&y Actions', 'D&oc Demo'])

list = [demo, doc_demo]
