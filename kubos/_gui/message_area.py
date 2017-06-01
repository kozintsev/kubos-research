from __future__ import absolute_import,division,print_function,unicode_literals

from ..lib.message_area import MessageArea as MessageArea_
from ..std_events import invalid_input_accepted


class MessageArea(MessageArea_):

    def __init__(self):
        MessageArea_.__init__(self)
        invalid_input_accepted.connect(self.show_invalid_input_warning)

    def show_invalid_input_warning(self):
        self.show_temp_message('Invalid Input')
