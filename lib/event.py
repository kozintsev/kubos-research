


class Event():
    """Provides an event handling system.

    The implementation is very similar to Signals and Slots in PyQt, but has
    less functionality"""

    def __init__(self):
        self._slots = []

    def connect(self, function):
        self._slots.append(function)

    def emit(self, *args, **kwargs):
        for function in self._slots:
            function(*args, **kwargs)
