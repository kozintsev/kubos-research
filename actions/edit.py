

from PyQt4.QtGui import QKeySequence

from lib.action import Action
import std_events
from gui import viewer_3d
from doc import doc_ctrl


def undo_():
    doc_ctrl.undo()
    viewer_3d.context.CloseLocalContext()
    viewer_3d.repaint0()
    viewer_3d.context.OpenLocalContext()
    if not doc_ctrl.document.GetAvailableUndos():
        undo.setEnabled(False)
    redo.setEnabled(True)


def redo_():
    doc_ctrl.redo()
    viewer_3d.context.CloseLocalContext()
    viewer_3d.repaint0()
    viewer_3d.context.OpenLocalContext()
    if not doc_ctrl.document.GetAvailableRedos():
        redo.setEnabled(False)
    undo.setEnabled(True)


def on_doc_modified():
    redo.setEnabled(False)
    undo.setEnabled(True)
std_events.document_modified.connect(on_doc_modified)

undo = Action(undo_, ['&Edit', '&Undo'], icon='edit-undo',
              shortcut=QKeySequence.Undo, enabled=False)

redo = Action(redo_, ['&Edit', '&Redo'], icon='edit-redo',
              shortcut=QKeySequence.Redo, enabled=False)

toolbar_visible = True

list = [undo, redo]
