

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


from data import appdata

from std_events import new_tool_activated

import active_tool



class ToolOptionsDock(QtWidgets.QDockWidget):

    def __init__(self, parent):
        QtWidgets.QDockWidget.__init__(self, 'Tool Options', parent)
        layout = QtWidgets.QVBoxLayout()

        tool_name = QtWidgets.QLabel('<h2>test</h2>')
        tool_icon = QtWidgets.QLabel()
        tool_icon.setPixmap(appdata.get('icon').pixmap(22))
        layout_d = QtWidgets.QHBoxLayout()
        layout_d.addWidget(tool_icon)
        layout_d.addWidget(tool_name)
        layout_d.setAlignment(tool_name, QtCore.Qt.AlignLeft)
        tool_details = QtWidgets.QLabel()
        tool_details.setLayout(layout_d)

        self.copy_checkbox = QtWidgets.QCheckBox('Always &Keep Originals')

        #layout.addWidget(tool_details)
        layout.addWidget(self.copy_checkbox)

        widget = QtWidgets.QWidget()
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
