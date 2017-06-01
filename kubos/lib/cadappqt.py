from __future__ import absolute_import,division,print_function,unicode_literals

# set the PyQt APIs to version 2 (this must be done before
from sip import setapi
try:
    for api in ['QDate', 'QDateTime', 'QString', 'QVariant', 'QTextStream',
                'QTime', 'QUrl']:
        setapi(api, 2)
except ValueError:
    raise StandardError("Kubos or the Kubos library can only be used with "+
                        "version 2 of the PyQt API. Use 'sip.setapi' to "+
                        "change the API before importing from PyQt or import "+
                        "CadAppQt before importing anything from PyQt")


import sys
try:
    import importlib as _importlib
except ImportError:
    # for Python 2.6
    from lib import importlib as _importlib

from PyQt4.QtGui import QApplication as _QApplication
from PyQt4 import QtCore as _QtCore
from PyQt4.QtGui import QActionGroup as _QActionGroup

class CadAppQt(object):
    """Base class for CAD applications using the Qt framework.
    
    The QApplication itself can be accessed as 'self._qapp'.
    """

    def __init__(self):
        self._qapp = _QApplication(sys.argv)
        # Initializing a QApplication changes the system locale for
        # the running program - resetting to default ('C')
        from locale import setlocale, LC_ALL
        # setlocale(LC_ALL, b'C')

    def load_action(self, action, toolbar_area=_QtCore.Qt.TopToolBarArea,
                    toolbar_visible=True):
        category = action.category
        if category not in self._menus:
            # add an empty menu to the menu bar
            self._menus[category] = self._menu_bar.addMenu(category)
            self.add_toolbar(category, toolbar_area, toolbar_visible)
        self._toolbars[category].addAction(action)
        self._menus[category].addAction(action)

        group = action.group
        if group is not None:
            if group not in self._actiongroups:
                self._actiongroups[group] = _QActionGroup(self.win)
            self._actiongroups[group].addAction(action)

    def add_action(self, *args, **kwargs):
        self.load_action(*args, **kwargs)

    def add_toolbar(self, name, area, visible=False):
        """Add an empty toolbar.

        The toolbar can be accessed as self._toolbars[name].
        It is placed at 'area', which must be a Qt ToolBarArea specifier."""
        toolbar = self.win.addToolBar(name)
        self.win.addToolBar(area, toolbar)
        toolbar.setVisible(visible)
        self._toolbars[name] = toolbar

    def load_actions(self, name):
        """Load a group of actions into the menu.
        'name' must be the name of a module in the package 'actions'
        >>>self.win.load_actions('edit')
        """
        module = _importlib.import_module(name)
        try:
            toolbar_area = module.toolbar_area
        except AttributeError:
            toolbar_area = _QtCore.Qt.TopToolBarArea
        try:
            toolbar_visible = module.toolbar_visible
        except AttributeError:
            toolbar_visible = False
        for action in module.list:
            self.load_action(action, toolbar_area, toolbar_visible)

    def load_tools(self, name):
        """Load a group of tools into the menu.
        'name' must be the name of a module in the package 'tools'
        """
        module = _importlib.import_module(name)
        for tool in module.list:
            self.load_action(tool.action, _QtCore.Qt.LeftToolBarArea,
                             module.toolbar_visible)


    def exec_(self, *args, **kwargs):
        self._qapp.exec_(*args, **kwargs)
