

import sys
import os
import subprocess

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from lib.action import Action
import std_events
from data import appdata
from gui import win
from doc import doc_ctrl


def new_():
    """Create a new document and show it in a new window"""
    # FIXME: this does not work on Debian 7, where the python2 binary is missing
    fname = os.path.join(appdata.get('APPDIR'), '__main__.pyw')
    subprocess.Popen([sys.executable, fname])


def open_():
    """Open a STEP file."""

    filename = QFileDialog.getOpenFileName(
                win, 'Open File', appdata.get('filename'), 'STEP files (*.stp *.step)')
    if not filename:
        # cancelled by the user
        return

    if doc_ctrl.isnew:
        # the current document is still empty -
        # open file in active window
        doc_ctrl.open(filename)
        std_events.document_modified.emit()
        appdata.set('filename', filename)
        appdata.set('dirty', False)
    else:
        # open file in new window
        # FIXME: this does not work on Debian 7, see comment above
        fname = os.path.join(appdata.get('APPDIR'), '__main__.pyw')
        subprocess.Popen([sys.executable, fname, filename])


def _save():
    if appdata.get('filename'):
        doc_ctrl.save(appdata.get('filename'))
        appdata.set('dirty', False)
    else:
        _save_as()


def _save_as():
    filename = QFileDialog.getSaveFileName(
          win, 'Save File', appdata.get('filename'), 
          'STEP files (*.stp *.step)')
    if filename:
        appdata.set('filename', filename)
        doc_ctrl.save(appdata.get('filename'))
        appdata.set('dirty', False)


def quit_():
    if appdata.get('mode') == 'script':
        sys.exit()
    if appdata.get('dirty'):
        unsaved_msgbox = QMessageBox(win)
        unsaved_msgbox.setStandardButtons(
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        unsaved_msgbox.setWindowTitle('Unsaved changes - ' +
                                      appdata.get('APPLICATION_NAME'))
        unsaved_msgbox.setText('Do you want to save your changes?')
        value = unsaved_msgbox.exec_()
        if value == QMessageBox.Save:
            _save()
        elif value == QMessageBox.Discard:
            sys.exit()
    # The value of 'dirty' was probably modified by _save()
    if not appdata.get('dirty'):
        sys.exit()


def on_dirty_changed():
    save.setEnabled(appdata.get('dirty'))
std_events.dirty_changed.connect(on_dirty_changed)

new = Action(new_, ['&File', '&New'], icon='document-new',
             shortcut=QKeySequence.New)
open = Action(open_, ['&File', '&Open'], icon='document-open',
              shortcut=QKeySequence.Open)
save = Action(_save, ['&File', '&Save'], icon='document-save',
              shortcut=QKeySequence.Save)
save_as = Action(_save_as, ['&File', 'Save &As'],
                 icon='document-save-as', shortcut=QKeySequence.SaveAs)
quit = Action(quit_, ['&File', '&Quit'], icon='application-exit',
              shortcut=QKeySequence.Quit)

toolbar_visible = False

list = [new, open, save, save_as, quit]
