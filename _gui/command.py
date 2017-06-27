from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDockWidget, QLineEdit

from lib import gp_
import std_events
from data import appdata
import active_tool


class CommandDockWidget(QDockWidget):

    def __init__(self, parent=None):
        QDockWidget.__init__(self, 'Command')
        self.setWhatsThis(
            'Command input\n\n'
            'Enter the coordinates of a point.\n'
            'Use the keys X, Y and Z to mark the corresponding coordinate '
            'value\n\n'
            'shortcut: C')
        self.line_edit = LineEdit()
        self.setWidget(self.line_edit)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)


class LineEdit(QLineEdit):

    def __init__(self):
        QLineEdit.__init__(self)
        self._previous_command_input = None

        std_events.input_changed.connect(self.update_command)

    def sizeHint(self):
        return QSize(120, 15)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            std_events.input_accepted.emit()
        elif event.key() in [Qt.Key_X, Qt.Key_Y, Qt.Key_Z]:
            # TODO: 1.0: don't include leading spaces
            if self.text().count(',') == 2:
                i0 = self.text().find(',')
                i1 = self.text().rfind(',')
                i2 = len(self.text())
                if event.key() == Qt.Key_X:
                    self.setSelection(0, i0)
                elif event.key() == Qt.Key_Y:
                    self.setSelection(i0 + 1, i1 - i0 - 1)
                elif event.key() == Qt.Key_Z:
                    self.setSelection(i1 + 1, i2 - i1 - 1)
        # TODO: 0.3: Esc quits operation even when the command box is active
        elif (Qt.Key_0 <= event.key() <= Qt.Key_9
              or event.key() in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Space,
                                 Qt.Key_Comma, Qt.Key_Period, Qt.Key_Minus,
                                 Qt.Key_Backspace, Qt.Key_Delete]
              or event.key() == Qt.Key_A and event.modifiers() ==
                             Qt.ControlModifier):
            QLineEdit.keyPressEvent(self, event)
            self._update_input_point()
        else:
            event.ignore()

    def _update_input_point(self):
        # Update the application-wide input point from the input in the command
        #   box
        try:
            input = gp_.gp_Pnt_([float(a) for a in self.text().split(',')])
        except ValueError:
            return
        except NotImplementedError:  # command line has only one or two entries
            return
        except TypeError:  # command line is empty
            return
        self._previous_command_input = input
        appdata.set('input', input)

    def update_command(self):
        """Update the text in the command field.

        This function is called when the input point was changed through mouse
        movement"""
        if (active_tool.active_tool.input_type == 'point' and
              appdata.get('input') is not None):
            # If the input point was changed by typing in the command field
            #   no further change is required
            if self._previous_command_input != appdata.get('input'):
                command = '{0:.2f}, {1:.2f}, {2:.2f}'.format(
                                    *appdata.get('input'))
                self.setText(command)
        else:
            self.setText('')
