# -*- coding: UTF-8 -*-
from os import path as _path

from data import appdata as _appdata

from lib.cadappqt import CadAppQt as _CadAppQt

from PyQt4.QtGui import QIcon as _QIcon

class KubosApp(_CadAppQt):

    def __init__(self, *args, **kwargs):

        try:
            appdir = kwargs.pop('appdir')
        except KeyError:
            pass

        _CadAppQt.__init__(self)

        # set application directory
        _appdata.set('APPDIR', appdir)

        # Search for icons in './icons/kubos'.
        if _appdata.get('APPDIR') is not None:
            ip = _QIcon.themeSearchPaths() + [_path.join(_appdata.get('APPDIR'), 'icons')]
            _QIcon.setThemeSearchPaths(ip)
            _QIcon.setThemeName('kubos')
        if _appdata.get('mode'):
            if _QIcon.hasThemeIcon('kubos-' + _appdata.get('mode')):
                _appdata.set('icon', _QIcon.fromTheme('kubos-' + _appdata.get('mode')))
            else:
                _appdata.set('icon', _QIcon.fromTheme('kubos'))
        else:
            _appdata.set('icon', _QIcon.fromTheme('kubos'))

        _appdata.set('AUTHORS', 'Marko Knöbl')
        _appdata.set('VERSION', '0.2b1')

        from doc import doc_ctrl
        self.doc = doc_ctrl
        # 'win' cannot be imported before creating a QApplication
        from gui import win
        self.win = win
        self.update_title()
        self.viewer = win.viewer_3d

    def run(self):

        import std_events

        self._menu_bar = self.win.menuBar()
        self._menus = {}
        self._actiongroups = {}

        self._toolbars = {}

        self.win.showMaximized()
        # second initialization step for the viewer - must be called once
        # the window is being shown
        self.win.viewer_3d.init2()

        if _appdata.get('mode') != 'script':
            self.win.viewer_3d.grid = True

        if _appdata.get('mode') in ['test', 'standard']:
            self.show_statusbar()

        std_events.filename_changed.connect(self.update_title)
        std_events.dirty_changed.connect(self.update_title)

        std_events.new_step_activated.connect(self.update_status)

        if _appdata.get('mode') == 'script' and _appdata.get('filename'):
            from actions import script
            script.load(_appdata.get('filename'))
        elif _appdata.get('filename'):
            self.doc.open(_appdata.get('filename'))
            std_events.document_modified.emit()

        if _appdata.get('mode') in ['standard', 'test']:
            self.load_actions('actions.file')
            self.load_actions('actions.edit')
            self.load_tools('tools.select')
            self.load_tools('tools.primitives')
            self.load_tools('tools.transform')
            self.load_tools('tools.expand')
            self.load_tools('tools.delete')
            self.load_tools('tools.boolean')
            self.load_actions('actions.view')
            self.load_actions('actions.option')
            self.load_actions('actions.help')
            self.load_tools('tools.bezier')
            self.load_tools('tools.roof')
            if _appdata.get('mode') == 'test':
                self.load_actions('actions.module')
                self.load_actions('actions.test')
                self.load_tools('tools.test')
                self.load_actions('actions.unit_test')
                self.load_actions('actions.my_actions')
        elif _appdata.get('mode') == 'viewer':
            self.load_actions('actions.file')
            self.load_actions('actions.view')
            self.load_actions('actions.module')
        elif _appdata.get('mode') == 'minimal':
            self.load_actions('actions.module')
        elif _appdata.get('mode') == 'script':
            self.load_actions('actions.script')
            self.load_actions('actions.view')
            self.load_actions('actions.help')

    def update_title(self):
        """Update the window title"""
        dirty_marker = '*' if _appdata.get('dirty') else ''
        filename = _path.basename(_appdata.get('filename')) or 'Unnamed'
        self.win.setWindowTitle('{0}{1} - {2}'.format(
                filename, dirty_marker, _appdata.get('APPLICATION_NAME')))

    def update_status(self):
        """Update the text in the status bar"""
        import active_tool
        if _appdata.get('mode') not in ['standard', 'test']:
            return
        name = active_tool.active_tool.menu[-1].replace('&', '')
        help = active_tool.active_tool.help[active_tool.active_tool.step]
        message = name + ' Tool: ' + help
        self._message_area.show_message(message)

    def show_statusbar(self):
        from lib.message_area import MessageArea
        self._message_area = MessageArea()
        self.win.statusBar().addWidget(self._message_area)
