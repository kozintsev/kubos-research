

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QLabel, QHBoxLayout, QVBoxLayout, QCheckBox, QWidget

from data import appdata
from std_events import new_tool_activated
import active_tool


class ToolOptionsDock(QDockWidget):

    def __init__(self, parent):
        QDockWidget.__init__(self, 'Tool Options', parent)
        layout = QVBoxLayout()

        tool_name = QLabel('<h2>test</h2>')
        tool_icon = QLabel()
        tool_icon.setPixmap(appdata.get('icon').pixmap(22))
        layout_d = QHBoxLayout()
        layout_d.addWidget(tool_icon)
        layout_d.addWidget(tool_name)
        layout_d.setAlignment(tool_name, QtCore.Qt.AlignLeft)
        tool_details = QLabel()
        tool_details.setLayout(layout_d)

        self.copy_checkbox = QCheckBox('Always &Keep Originals')

        #layout.addWidget(tool_details)
        layout.addWidget(self.copy_checkbox)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setMinimumWidth(120)
        widget.setMaximumHeight(60)
        self.setWidget(widget)

        new_tool_activated.connect(self.update)

    def update(self):
        enabled = ('object' in active_tool.active_tool.input_types)
        self.copy_checkbox.setEnabled(enabled)
        if enabled:
            self.copy_checkbox.setCheckState(Qt.Unchecked)
