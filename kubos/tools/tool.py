from __future__ import absolute_import,division,print_function,unicode_literals

from functools import partial

from data import appdata
import active_tool
from lib.action import Action


class Tool(object):

    def __init__(self):
        self.help = []
        self.icon = ''
        self.shortcut = ''
        self.group = 'tools'
        self._action = None

    def reset(self):
        """Reset the tool to step 0"""
        self.step = 0
        self.input_type = self.input_types[0]
        self._final = []  # list of shapes which will be returned
        self.remove = []  # list of shapes which will be replaced

    def next_step(self):
        # reset the input (this is neccessary if the input type
        # will change)
        appdata.set('input', None)
        self.step += 1
        self.input_type = self.input_types[self.step]

    def final(self):
        """Return the final shape.

        By default, return self._final, which should be set by
        the method 'self.preview'.
        """
        return self._final

    def _get_action(self):
        """Return an action that can be used to activate the tool"""
        if not self._action:
            a = partial(active_tool.activate_tool, tool=self)
            self._action = Action(a, self.menu, group=self.group,
                                  icon=self.icon, shortcut=self.shortcut,
                                  checkable=True, parent=None)
        return self._action
    action = property(_get_action)
