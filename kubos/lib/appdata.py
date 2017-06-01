from __future__ import absolute_import,division,print_function,unicode_literals

class Appdata(object):

    # TODO: finish documentation, clean up
    """A database with elements consisting of
    keys, values and optional setter functions
    
    >>>a = Data()
    >>>a.add('color')
    >>>a.set('color', 'red')
    >>>a.get('color')
    red
    >>>def p(value):
    ...    print('New value:', value)
    >>>a.add('length', on_set=p)
    >>>a.set('length', 3)
    New value: 3
    """
    def __init__(self):
        self._items = {}

    def add(self, name, on_set=None):
        self._items[name] = [None, on_set]

    def set(self, name, value):
        if self._items[name][1]:
            # there is a specific set function
            self._items[name][1](value)
        else:
            self._items[name][0] = value

    def sset(self, name, value):
        # silent set
        self._items[name][0] = value

    def get(self, name):
        return self._items[name][0]
