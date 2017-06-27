

from lib.doc_ctrl import DocCtrl

from PyQt5.QtCore import Qt

from data import appdata
import std_events
import active_tool


class KubosDoc(DocCtrl):
    """Document Controller for Kubos

    This class manages a "TDocStd_Document" which is accessible through
    "self.document"."""

    def __init__(self):
        DocCtrl.__init__(self)
        std_events.input_accepted.connect(self.on_input_accepted)
        self._selection = None

    def remove_random(self):
        """Remove a random shape from the document (for testing)"""
        import random
        label = random.choice(list(self._label_dict.values()))

        with self.open_command():
            self._shape_tool.RemoveComponent(label)
        std_events.document_modified.emit()

    def select_by_number(self, number):
        a = list(self._label_dict.values())
        label = a[number % len(a)]
        if self._selection:
            self.set_color(self._selection, [0, 0, 1])
        self._selection = label
        self.set_color(label, [1, 0, 0])
        self._selection = label
        std_events.document_modified.emit()

    def remove_selected(self):
        with self.open_command():
            self._shape_tool.RemoveComponent(self._selection)
        std_events.document_modified.emit()

    def on_input_accepted(self):
        """Handle the "input_accepted" event"""
        from gui import tool_options_dock
        if not appdata.get('input_valid'):
            std_events.invalid_input_accepted.emit()
            return
        # Check if this is the last step
        if active_tool.active_tool.step + 1 < active_tool.active_tool.steps:
            std_events.step_finished.emit()
        else:
            # Get the final shapes and add them to the document
            shapes = active_tool.active_tool.final()
            with self.open_command():
                for shape in shapes:
                    self.add(shape)
                if tool_options_dock.copy_checkbox.checkState()==Qt.Unchecked:
                    for shape in active_tool.active_tool.remove:
                        self.remove(shape)
            std_events.document_modified.emit()
            active_tool.active_tool.reset()
            std_events.construction_finished.emit()

# some features are not needed for the script mode (e.g. interactive input)
#  - use the simpler DocCtrl in that case
if appdata.get('mode') != 'script':
    doc_ctrl = KubosDoc()
else:
    doc_ctrl = DocCtrl()
