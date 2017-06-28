

from PyQt4 import QtGui

import std_events
from doc import doc_ctrl
# import doc
from lib.label_util import tag_list

import gui


class ObjectDetailsDock(QtGui.QDockWidget):

    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, 'Object Details')
        layout = QtGui.QVBoxLayout()

        self.tag_label = QtGui.QLabel('Tag: ')

        red = QtGui.QPushButton(QtGui.QIcon.fromTheme('red'), '')
        red.clicked.connect(self.on_red)
        orange = QtGui.QPushButton(QtGui.QIcon.fromTheme('orange'), '')
        orange.clicked.connect(self.on_orange)
        yellow = QtGui.QPushButton(QtGui.QIcon.fromTheme('yellow'), '')
        yellow.clicked.connect(self.on_yellow)
        green = QtGui.QPushButton(QtGui.QIcon.fromTheme('green'), '')
        green.clicked.connect(self.on_green)
        blue = QtGui.QPushButton(QtGui.QIcon.fromTheme('blue'), '')
        blue.clicked.connect(self.on_blue)
        purple = QtGui.QPushButton(QtGui.QIcon.fromTheme('purple'), '')
        purple.clicked.connect(self.on_purple)
        color_layout = QtGui.QGridLayout()
        color_layout.addWidget(red, 0, 0)
        color_layout.addWidget(orange, 0, 1)
        color_layout.addWidget(yellow, 0, 2)
        color_layout.addWidget(green, 0, 3)
        color_layout.addWidget(blue, 1, 0)
        color_layout.addWidget(purple, 1, 1)
        color_picker = QtGui.QLabel()
        color_picker.setLayout(color_layout)

        #layout.addWidget(self.tag_label)
        layout.addWidget(color_picker)

        widget = QtGui.QWidget()
        widget.setLayout(layout)
        widget.setMinimumWidth(180)
        widget.setMaximumHeight(100)
        self.setWidget(widget)

        std_events.selection_changed.connect(self.on_selection_changed)

    def on_selection_changed(self):
        selection = gui.viewer_3d._selection
        self.lbl = doc_ctrl.get_shape_label(selection)
        lbl_ = "s" #doc_ctrl.get_comp_label(selection)
        self.tag_label.setText('Tag:\n' + str(tag_list(self.lbl))) # + '\n' + str(tag_list(lbl_)))

    def set_color(self, color):
        """Set the color of the selected shape"""
        with doc_ctrl.open_command():
            doc_ctrl.set_color(self.lbl, color)
        std_events.document_modified.emit()

    def on_red(self):
        self.set_color([1, 0, 0])

    def on_orange(self):
        self.set_color([1, 0.4, 0])

    def on_yellow(self):
        self.set_color([1, 1, 0])

    def on_green(self):
        self.set_color([0, 1, 0])

    def on_blue(self):
        self.set_color([0, 0, 1])

    def on_purple(self):
        self.set_color([0.73, 0, 1])
