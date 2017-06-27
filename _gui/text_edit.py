

from PyQt5.Qt import QPlainTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize


class TextEdit(QPlainTextEdit):
    """A Text edit widget which is set up for Python code editing"""
    def __init__(self, *args):
        QPlainTextEdit.__init__(self, *args)

        self.setMaximumWidth(655)

        font = QFont('')
        font.setFamily('Courier')
        font.setStyleHint(QFont.Monospace)
        font.setPointSize(10)
        self.setFont(font)

    def sizeHint(self):
        # This function would return (256, 192) by default.
        # The viewer widget returns (-1, -1), which would
        # make it much bigger.
        # This change will make the text edit are wide enough for 79
        # characters (as specified in PEP 8)
        return QSize(655, -1)
