

from gui import viewer_3d
from lib.action import Action


def toggle_grid_():
    viewer_3d.grid = not viewer_3d.grid

toggle_grid = Action(toggle_grid_, ['&Options', '&Grid'], icon='view-grid',
                      checkable=True, checked=True, shortcut='#')


def switch_active_plane_():
    viewer_3d.active_plane = (viewer_3d.active_plane + 1) % 3

switch_active_plane = Action(switch_active_plane_,
                              ['&Options', 'Switch &Active Plane'],
                              shortcut='space', icon='cad-active_plane')

toolbar_visible = True

list = [toggle_grid, switch_active_plane]
