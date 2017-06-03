from data import appdata
from _gui.main_win import MainWindow

win = MainWindow()
viewer_3d = win.viewer_3d
if appdata.get('mode') in ['standard', 'test']:
    command_dock_widget = win.command_dock_widget
    tool_options_dock = win.tool_options_dock
    object_details_dock = win.object_details_dock
elif appdata.get('mode') == 'script':
    editor = win.editor
