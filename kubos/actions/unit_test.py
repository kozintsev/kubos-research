"""These tests are used to check functionality.  They were written for KDE4 and
a window size of 900x600 and might not work on other configurations"""

from __future__ import absolute_import,division,print_function,unicode_literals

from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from ..gui import win
from ..lib.action import Action
from ..lib import qtest

# initialize the qtest module
qtest.init(win)


def cube_diagonal_():
    QTest.keyPress(win.viewer_3d, Qt.Key_P, Qt.AltModifier)
    qtest.click_at([250, 180])
    qtest.click_at([210, 440])
    qtest.click_at([650, 400])
    QTest.keyPress(win, Qt.Key_X, Qt.AltModifier)
    qtest.click_at([400, 50])
    qtest.click_at([400, 400])
    QTest.keyPress(win, Qt.Key_Space, Qt.NoModifier)
    qtest.click_at([700, 100])
    QTest.keyPress(win, Qt.Key_G, Qt.ControlModifier)
    qtest.click_at([215, 440])
    QTest.keyPress(win, Qt.Key_Space)
    QTest.keyPress(win, Qt.Key_Space)
    qtest.click_at([660, 90])
cube_diagonal = Action(cube_diagonal_, ('&Unit Tests', 'Cube &Diagonal'))


def u_bahn_():
    # cube
    QTest.keyPress(win.viewer_3d, Qt.Key_B, Qt.ControlModifier)
    qtest.mouse_move([350, 320])
    QTest.keyPress(win.viewer_3d, Qt.Key_C, Qt.NoModifier, 100)
    QTest.keyPress(win.command_dock_widget.line_edit, Qt.Key_Z, Qt.NoModifier)
    QTest.keyPress(win.command_dock_widget.line_edit, Qt.Key_Minus,
                   Qt.NoModifier)
    QTest.keyPress(win.command_dock_widget.line_edit, Qt.Key_1, Qt.NoModifier)
    QTest.keyPress(win.command_dock_widget.line_edit, Qt.Key_Return,
                   Qt.NoModifier)
    qtest.mouse_move([430, 320])
    QTest.keyPress(win.command_dock_widget.line_edit, Qt.Key_Return,
                   Qt.NoModifier)
    qtest.click_at([430, 330])
    # sphere
    qtest.click_at([120, 10])
    qtest.click_at([120, 130])
    qtest.click_at([390, 320])
    qtest.click_at([430, 320])
    # intersection
    qtest.click_at([200, 10])
    qtest.click_at([200, 55])
    qtest.click_at([390, 320])
    qtest.click_at([370, 330])
    # delete
    qtest.click_at([200, 10])
    qtest.click_at([200, 30])
    qtest.click_at([390, 320])
    qtest.click_at([360, 320])
    QTest.keyPress(win.viewer_3d, Qt.Key_Escape, Qt.NoModifier)
u_bahn = Action(u_bahn_, ('&Unit Tests', '&U-Bahn'))


def view_control_():
    qtest.click_at([250, 15])
    qtest.click_at([250, 30])
view_control = Action(view_control_, ('&Unit Tests', '&View control'))

toolbar_visible = True

list = [cube_diagonal, u_bahn, view_control]
