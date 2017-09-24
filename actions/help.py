# -*- coding: UTF-8 -*-



from PyQt5 import QtCore, QtGui, QtWidgets

from lib.action import Action

from data import appdata

from gui import win



class AboutDlg(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle('About {0}'.format(appdata.get('APPLICATION_NAME')))
        layout = QtWidgets.QVBoxLayout()

        logo_label = QtWidgets.QLabel()
        logo_label.setPixmap(appdata.get('icon').pixmap(128))
        logo_label.setAlignment(QtCore.Qt.AlignCenter)

        text = ('<b><h1>{0} {1}</h1></b><br>'
                '(C) {2}<br>'
                'CAD icons (C) FreeCAD contributors<br><br>'
                'Thanks go to the developers of:<br>'
                'Python<br>OpenCASCADE, pythonOCC<br>Qt, PyQt')
        text = text.format(appdata.get('APPLICATION_NAME'),
                           appdata.get('VERSION'),
                           appdata.get('AUTHORS'))
        text_label = QtWidgets.QLabel(text)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        button_box.accepted.connect(self.close)

        for widget in [logo_label, text_label, button_box]:
            layout.addWidget(widget)
        self.setLayout(layout)

about_dlg = AboutDlg(win)
menu = ['&Help', '&About {0}'.format(appdata.get('APPLICATION_NAME'))]
open_about_dlg = Action(about_dlg.show, menu, icon='kubos')

class KnownIssues(QtWidgets.QDialog):
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setWindowTitle('Known issues - {0} {1}'.format(
                    appdata.get('APPLICATION_NAME'), appdata.get('VERSION')))
        layout = QtWidgets.QVBoxLayout()

        text = (
          'Kubos is still in a relatively early stage of development.\n\n'
          'The following issues are known to the developer (and are '
          'being worked on):\n\n'
          '• Object colors will not be loaded / saved\n'
          '• Importing large objects (with coordinate values exceeding '
          '  10000) will result in incomplete objects\n'
          '• Intersecting curves will only yield one intersection point\n'
          '• Computing the intersection of curves will lead to incorrect '
          '  results if the curves do not intersect.\n'
          '• Loading of models that contain independent faces or edges '
          '  does not work')
        
        text_label = QtWidgets.QLabel(text)
        text_label.setWordWrap(True)
        text_label.setFixedWidth(400)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        button_box.accepted.connect(self.close)

        for widget in [text_label, button_box]:
            layout.addWidget(widget)
        self.setLayout(layout)

known_issues = KnownIssues(win)
open_known_issues = Action(known_issues.show, ['&Help', '&Known Issues'])

whats_this = Action(QtWidgets.QWhatsThis.enterWhatsThisMode,
                    ['&Help', "&What's This?"], icon='help-contextual',
                    shortcut=QtGui.QKeySequence.WhatsThis)

toolbar_visible = False
toolbar_area = QtCore.Qt.TopToolBarArea

list = [open_about_dlg, open_known_issues, whats_this]
