from __future__ import absolute_import,division,print_function,unicode_literals

from lib.action import Action
from gui import viewer_3d


def wireframe_():
    if viewer_3d.view_mode == 'shaded':
        viewer_3d.view_mode = 'wireframe'
    elif viewer_3d.view_mode == 'wireframe':
        viewer_3d.view_mode = 'shaded'
wireframe = Action(wireframe_, ['&View', '&Wireframe'], icon='view-wireframe',
                   checkable=True, checked=False)


def view_angled_():
    viewer_3d.eye = [0.82, 0.45, 0.36]
view_angled = Action(view_angled_, ['&View', '&Angled'], icon='view-angled',
                     shortcut='A')


def view_top_():
    viewer_3d.active_plane = 2
    viewer_3d.eye = [0, 0, 1]
view_top = Action(view_top_, ['&View', '&Top'], icon='view-top', shortcut='1')


def view_front_():
    viewer_3d.active_plane = 0
    viewer_3d.eye = [1, 0, 0]
view_front = Action(view_front_, ['&View', '&Front'], icon='view-front',
                    shortcut='2')


def view_right_():
    viewer_3d.active_plane = 1
    viewer_3d.eye = [0, 1, 0]
view_right = Action(view_right_, ['&View', '&Right'], icon='view-right',
                    shortcut='3')

toolbar_visible = True

list = [wireframe, view_angled, view_top, view_front, view_right]
