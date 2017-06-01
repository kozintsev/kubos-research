from __future__ import absolute_import,division,print_function,unicode_literals

from .data import appdata
from ._gui import main_win

win = main_win.MainWindow()
viewer_3d = win.viewer_3d
if appdata.get('mode') in ['standard', 'test']:
    command_dock_widget = win.command_dock_widget
    tool_options_dock = win.tool_options_dock
    object_details_dock = win.object_details_dock
elif appdata.get('mode') == 'script':
    editor = win.editor
