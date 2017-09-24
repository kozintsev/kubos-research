

import imp

import sys

from os import path

import subprocess

import builtins


from PyQt5 import QtGui, QtWidgets

from data import appdata

from lib.action import Action

from gui import editor

from gui import win

from doc import doc_ctrl


module = None


def new_():
    """Create a new script and show it in a new window"""
    # FIXME: this does not work on Debian 7, where the python2 binary is missing
    #        use platform.distro_name to check for this case
    fname = path.join(appdata.get('APPDIR'), '__main__.pyw')
    subprocess.Popen([sys.executable, fname, '--mode', 'script'])
new = Action(new_, ['&File', '&New'], icon='document-new',
             shortcut=QtGui.QKeySequence.New)


def load(filename):
    """Load a script given its filename. This assumes that no script
    was loaded before.
    This occurs either on startup if a command line argument specifying the
    file to open was provided or when manually opening a file for the first
    time."""
    with open(filename) as file:
        st = file.read()
    editor.setPlainText(st)
    # If the file was opened after startup, 'filename' has not been set before.
    appdata.set('filename', filename)
    exec_script()


def exec_script():
    """Execute the current script and update the view accordingly."""
    # called by "load" and "refresh"
    doc_ctrl.clear()
    filename = appdata.get('filename')
    try:
        # see also: 
        # http://stackoverflow.com/questions/15082857/loading-modules-by-imp-load-source-with-same-name-resulting-merger-of-the-module
        global module
        if module is None:
            # This is the first time a scrit is opened
            module = imp.load_source('script', filename)
        else:
            module.__dict__.clear()
            for (key, value) in list({'__builtins__':builtins.__dict__,
                                 '__doc__':None,
                                 '__file__':None,
                                 '__name__':'script',
                                 '__package__':None}.items()):
                module.__dict__[key] = value
        module = imp.load_source('script', filename)
        try:
            for shape in module.SHAPES:
                # the imported script defines 'SHAPES': add all of its items
                # to the document
                doc_ctrl.add(shape)
        except AttributeError:
            pass
    except Exception as e:
        msgbox = QtWidgets.QMessageBox(win)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgbox.setText('Error while opening file')
        text = ("While trying to open the file '{0}' the following " +
                'exception was raised:\n"{1}"').format(filename, e)
        detailed = ('Exception type: {0}\n'+
                    'Exception: {1}\n'+
                    '{2}').format(*sys.exc_info())
        import traceback

        detailed = traceback.format_exc()
        msgbox.setInformativeText(text)
        msgbox.setDetailedText(detailed)
        msgbox.show()


def open_script_():
    """Show a file dialog to open an existing script."""
    examples_path = path.join(path.dirname(appdata.get('APPDIR')),
                              'examples/kubos_script')
    filename = QtWidgets.QFileDialog.getOpenFileName(
                win, 'Open Script', appdata.get('filename') or examples_path,
                'Python files (*.py)')[0]
    if not filename:
        # cancelled by the user
        return

    if appdata.get('filename') == '':
        # no file was opened in this application so far.
        # open the file right here.
        load(filename)
    else:
        # There is already an open file. Open the requested file in a new
        # window.
        fname = path.join(appdata.get('APPDIR'), '__main__.pyw')
        subprocess.Popen([sys.executable, fname, filename, '--mode', 'script'])

open_script = Action(open_script_, ['&File', '&Open Script'],
                     icon='document-open', shortcut=QtGui.QKeySequence.Open)


def save_script_as_():
    """Show a file dialog to save the opened script under a certian name."""
    filename = QtWidgets.QFileDialog.getSaveFileName(
                win, 'Save Script', appdata.get('filename'),
                'Python scripts (*.py)')[0]
    if filename:
        appdata.set('filename', filename)
        with open(filename, 'w') as script:
            script.write(editor.toPlainText())
        appdata.set('filename', filename)
        appdata.set('dirty', False)
save_script_as = Action(save_script_as_, ['&File', 'Save Script As'],
                        icon='document-save-as',
                        shortcut=QtGui.QKeySequence.SaveAs)


def save_script_():
    """Save the script. If it was not saved before, ask for a filename."""
    if not appdata.get('filename'):
        save_script_as_()
        return
    with open(appdata.get('filename'), 'w') as file:
        file.write(editor.toPlainText())
        appdata.set('dirty', False)
save_script = Action(save_script_, ['&File', '&Save Script'],
                     icon='document-save', shortcut=QtGui.QKeySequence.Save)


def refresh_():
    """Save the script, run it and display its result."""
    save_script_()
    if not appdata.get('filename'):
        # save was cancelled by the user
        return
    exec_script()
    appdata.set('dirty', False)
refresh = Action(refresh_, ['&File', 'Save and &Refresh'], icon='view-refresh',
                 shortcut=QtGui.QKeySequence.Refresh)


def export_():
    """Open a file dialog which lets the user export the document in STEP
    format"""
    fname = path.splitext(appdata.get('filename'))[0] + '.step'
    filename = QtWidgets.QFileDialog.getSaveFileName(
          win, 'Export File', fname, 'STEP files (*.stp *.step)')[0]
    if filename:
        doc_ctrl.save(appdata.get('filename'))
export = Action(export_, ['&File', 'E&xport'],
                 icon='document-export', shortcut='Ctrl+E')

toolbar_visible = True

list = [new, open_script, refresh, save_script, save_script_as, export]
