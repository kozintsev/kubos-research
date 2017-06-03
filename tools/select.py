

from tools.tool import Tool


class Select(Tool):

    def __init__(self):
        Tool.__init__(self)
        self.menu = ['&Edit', '&Select']
        self.steps = 1
        self.icon = 'edit-select'
        self.input_types = ['object']
        self.input_type = self.input_types[0]
        self.help = ['Selction Tool']
        self.shortcut = 'Esc'

        self.reset()

    def preview(self, input, direction):
        return []

    # override the default 'next_step' method
    def next_step(self):
        pass

toolbar_visible = True

select = Select()

list = [select]
