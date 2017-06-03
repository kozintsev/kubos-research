

from threading import Timer

from PyQt4.QtGui import QLabel
from PyQt4.QtCore import QSize


class MessageArea(QLabel):

    """An area for showing messages in the status bar."""
    def __init__(self):
        QLabel.__init__(self)
        self.setIndent(4)
        self._temp_message = ''
        self._message = ''
        self._std_style = self.styleSheet()

    def sizeHint(self):
        return QSize(4000, 20)

    def show_message(self, message):
        self.setText(message)
        self._message = message

    def show_temp_message(self, message):
        self.setText(message)
        # Background color taken from Dolphin
        self.setStyleSheet('QLabel { background-color : rgb(232, 187, 187);}')
        Timer(2, self._clear_temp_message).start()

    def _clear_temp_message(self):
        self.setText(self._message)
        self.setStyleSheet(self._std_style)
