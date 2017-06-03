

from lib.event import Event

filename_changed = Event()
dirty_changed = Event()
grid_changed = Event()
input_changed = Event()
input_accepted = Event()
construction_finished = Event()
step_finished = Event()
# Is emitted when a new tool is activated or a step was finished
new_step_activated = Event()
new_tool_activated = Event()
document_modified = Event()
# Is emitted when the input is accepted when it was invalid
invalid_input_accepted = Event()
selection_changed = Event()
