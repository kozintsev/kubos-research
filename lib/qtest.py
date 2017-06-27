"""Simplified unit tests for PyQt"""



# FIXME: don't import app
from app import app

from PyQt5.QtTest import QTest
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, QPoint


def init(window, time_=.5):
    """Initialize this module by passing a window object"""
    global win
    win = window
    global time
    time = time_


def mouse_move(target):
    """moves the mouse cursor to the coordinates of 'target' by a continous
    movement.  Coordinates are relative to the main window"""
    pos = win.mapFromGlobal(QCursor.pos())
    start = [pos.x(), pos.y()]
    n = max(int(time * 25), 5)
    for i in range(0, n + 1):
        pos = [start[j] + (target[j] - start[j]) / n * i for j in range(2)]
        widget = app._qapp.widgetAt(QCursor.pos()) or win
        QTest.mouseMove(
             widget, win.mapToGlobal(widget.mapFromGlobal(QPoint(*pos))), time)


def mouse_press(widget, button=Qt.LeftButton, modifier=Qt.NoModifier):
    widget = app._qapp.widgetAt(QCursor.pos())
    pos = widget.mapFromGlobal(QCursor.pos())
    QTest.mousePress(widget, button, modifier, pos)


def mouse_click(button=Qt.LeftButton, modifier=Qt.NoModifier):
    widget = app._qapp.widgetAt(QCursor.pos())
    pos = widget.mapFromGlobal(QCursor.pos())
    QTest.mouseClick(widget, button, modifier, pos)


def click_at(pos, button=Qt.LeftButton, modifier=Qt.NoModifier):
    # WORKAROUND: call the move command twice to get to the correct location
    mouse_move(pos)
    mouse_move(pos)
    mouse_click(button, modifier)
