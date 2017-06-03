# -*- coding: UTF-8 -*-
from os import path as _path
import data
from lib.cadappqt import CadAppQt

from PyQt4.QtGui import QIcon as _QIcon


class KubosApp(CadAppQt):
    def __init__(self, *args, **kwargs):

        try:
            appdir = kwargs.pop('appdir')
        except KeyError:
            pass

        CadAppQt.__init__(self)

        # set application directory
        data.appdata.set('APPDIR', appdir)

        # Search for icons in './icons/kubos'.
        if data.appdata.get('APPDIR') is not None:
            ip = _QIcon.themeSearchPaths() + [_path.join(data.appdata.get('APPDIR'), 'icons')]
            _QIcon.setThemeSearchPaths(ip)
            _QIcon.setThemeName('kubos')
        if data.appdata.get('mode'):
            if _QIcon.hasThemeIcon('kubos-' + data.appdata.get('mode')):
                data.appdata.set('icon', _QIcon.fromTheme('kubos-' + data.appdata.get('mode')))
            else:
                data.appdata.set('icon', _QIcon.fromTheme('kubos'))
        else:
            data.appdata.set('icon', _QIcon.fromTheme('kubos'))

        data.appdata.set('AUTHORS', 'Marko Knöbl')
        data.appdata.set('VERSION', '0.2b1')
        # todo: off doс control
        #import doc.doc_ctrl
        #self.doc = doc.doc_ctrl
        # 'win' cannot be imported before creating a QApplication
        from gui import win
        self.win = win
        self.update_title()
        self.viewer = win.viewer_3d

    def run(self):

        from . import std_events

        self._menu_bar = self.win.menuBar()
        self._menus = {}
        self._actiongroups = {}

        self._toolbars = {}

        self.win.showMaximized()
        # second initialization step for the viewer - must be called once
        # the window is being shown
        self.win.viewer_3d.init2()

        if data.appdata.get('mode') != 'script':
            self.win.viewer_3d.grid = True

        if data.appdata.get('mode') in ['test', 'standard']:
            self.show_statusbar()

        std_events.filename_changed.connect(self.update_title)
        std_events.dirty_changed.connect(self.update_title)

        std_events.new_step_activated.connect(self.update_status)

        if data.appdata.get('mode') == 'script' and data.appdata.get('filename'):
            from .actions import script
            script.load(data.appdata.get('filename'))
        elif data.appdata.get('filename'):
            self.doc.open(data.appdata.get('filename'))
            std_events.document_modified.emit()

        if data.appdata.get('mode') in ['standard', 'test']:
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
            if data.appdata.get('mode') == 'test':
                self.load_actions('actions.module')
                self.load_actions('actions.test')
                self.load_tools('tools.test')
                self.load_actions('actions.unit_test')
                self.load_actions('actions.my_actions')
        elif data.appdata.get('mode') == 'viewer':
            self.load_actions('actions.file')
            self.load_actions('actions.view')
            self.load_actions('actions.module')
        elif data.appdata.get('mode') == 'minimal':
            self.load_actions('actions.module')
        elif data.appdata.get('mode') == 'script':
            self.load_actions('actions.script')
            self.load_actions('actions.view')
            self.load_actions('actions.help')

    def update_title(self):
        """Update the window title"""
        dirty_marker = '*' if data.appdata.get('dirty') else ''
        filename = _path.basename(data.appdata.get('filename')) or 'Unnamed'
        self.win.setWindowTitle('{0}{1} - {2}'.format(
            filename, dirty_marker, data.appdata.get('APPLICATION_NAME')))

    def update_status(self):
        """Update the text in the status bar"""
        from . import active_tool
        if data.appdata.get('mode') not in ['standard', 'test']:
            return
        name = active_tool.active_tool.menu[-1].replace('&', '')
        help = active_tool.active_tool.help[active_tool.active_tool.step]
        message = name + ' Tool: ' + help
        self._message_area.show_message(message)

    def show_statusbar(self):
        from .lib.message_area import MessageArea
        self._message_area = MessageArea()
        self.win.statusBar().addWidget(self._message_area)
