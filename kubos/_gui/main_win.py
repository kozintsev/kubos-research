from __future__ import absolute_import,division,print_function,unicode_literals

from PyQt4 import QtCore, QtGui

from .. import tools
from .. import active_tool
from ..data import appdata
from ..doc import doc_ctrl
from .command import CommandDockWidget
from .object_details import ObjectDetailsDock
from .viewer import KubosViewer
from .tool_options import ToolOptionsDock
from .. import actions as _actions


class MainWindow(QtGui.QMainWindow):

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.resize(900, 640)
        self.viewer_3d = KubosViewer(doc_ctrl)

        self._splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)

        if appdata.get('mode') == 'script':
            from .text_edit import TextEdit
            self.editor = TextEdit()
            self._splitter.addWidget(self.editor)

        self._splitter.addWidget(self.viewer_3d)

        self.setCentralWidget(self._splitter)
        self.setIconSize(QtCore.QSize(22, 22))

        if appdata.get('mode') in ['test', 'standard']:
            self.command_dock_widget = CommandDockWidget()
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea,
                               self.command_dock_widget)
        if appdata.get('mode') in ['test', 'standard']:
            self.tool_options_dock = ToolOptionsDock(self)
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea,
                               self.tool_options_dock)
            self.object_details_dock = ObjectDetailsDock(self)
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea,
                               self.object_details_dock)

        self.setWindowIcon(appdata.get('icon'))

    def closeEvent(self, event):
        # delayed circular import:
        _actions.file.quit_()
        event.ignore()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            active_tool.activate_tool(tools.select.select)
        elif event.key() == QtCore.Qt.Key_C:
            self.command_dock_widget.line_edit.setFocus()
        else:
            event.ignore()

    def update_status(self):
        """Update the text in the status bar"""
        if appdata.get('mode') not in ['standard', 'test']:
            return
        name = active_tool.active_tool.menu[-1].replace('&', '')
        help = active_tool.active_tool.help[active_tool.active_tool.step]
        message = name + ' Tool: ' + help
        self._message_area.show_message(message)
