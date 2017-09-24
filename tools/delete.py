

from PyQt5 import QtCore

from tools.tool import Tool



class Delete(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Edit', '&Delete']
        self.icon = 'edit-delete'
        self.shortcut = 'Ctrl+D'
        self.steps = 1
        self.input_types = ['object']
        self.help = ['Click on an object to delete it']

        self.reset()

    def preview(self, input, direction):
        self.remove = [input]
        return []

toolbar_area = QtCore.Qt.LeftToolBarArea
toolbar_visible = True

list = [Delete()]
