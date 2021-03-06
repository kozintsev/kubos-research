from PyQt4.QtCore import Qt, QSize
from PyQt4.QtGui import QMainWindow, QSplitter

import tools
import active_tool
from data import appdata
from doc import doc_ctrl
from _gui.command import CommandDockWidget
from _gui.object_details import ObjectDetailsDock
from _gui.viewer import KubosViewer
from _gui.tool_options import ToolOptionsDock


class MainWindow(QMainWindow):

    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self.resize(900, 640)
        self.viewer_3d = KubosViewer(doc_ctrl)

        self._splitter = QSplitter(Qt.Horizontal)

        #if appdata.get('mode') == 'script':
        from _gui.text_edit import TextEdit
        self.editor = TextEdit()
        self._splitter.addWidget(self.editor)

        self._splitter.addWidget(self.viewer_3d)

        self.setCentralWidget(self._splitter)
        self.setIconSize(QSize(22, 22))

        # if appdata.get('mode') in ['test', 'standard']:
        self.command_dock_widget = CommandDockWidget()
        self.addDockWidget(Qt.RightDockWidgetArea, self.command_dock_widget)
        #if appdata.get('mode') in ['test', 'standard']:
        self.tool_options_dock = ToolOptionsDock(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.tool_options_dock)
        self.object_details_dock = ObjectDetailsDock(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.object_details_dock)

        self.setWindowIcon(appdata.get('icon'))

    def closeEvent(self, event):
        # delayed circular import:
        import actions.file
        actions.file.quit_()
        event.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            active_tool.activate_tool(tools.select.select)
        elif event.key() == Qt.Key_C:
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
