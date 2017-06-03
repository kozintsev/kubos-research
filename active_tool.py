from __future__ import absolute_import,division,print_function,unicode_literals

from exceptions_ import InvalidInputException
from tools.select import select
import std_events
from data import appdata


def activate_tool(tool):
    appdata.set('input', None)
    global active_tool
    active_tool = tool
    active_tool.reset()
    std_events.new_tool_activated.emit()
    std_events.new_step_activated.emit()


def activate_select_tool():
    select.action.trigger()


# TODO: put these functions into the "Tool" class?

def activate_next_step():
    active_tool.next_step()
    std_events.new_step_activated.emit()


def preview_from_current_input():
    """Return the preview shapes corresponding to the current input.

    If no valid shapes can be constructed for the current input, return an
    empty list and set 'input_valid' to False."""
    if appdata.get('input') is None:
        appdata.set('input_valid', False)
        return []
    try:
        a = active_tool.preview(appdata.get('input'),
                                appdata.get('active_plane'))
    except InvalidInputException:
        appdata.set('input_valid', False)
        return []
    else:
        appdata.set('input_valid', True)
        return a

active_tool = None
activate_select_tool()

std_events.step_finished.connect(activate_next_step)
std_events.construction_finished.connect(activate_select_tool)
