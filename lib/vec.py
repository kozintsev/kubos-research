

from math import sqrt

from OCC.gp import gp_Vec, gp_Dir, gp_Pnt

class vec(object):

    def __init__(self, *args):
        if len(args) == 1:
            self._coord = list(args[0])
        elif len(args) == 3:
            self._coord = list(args)
        else:
            raise ValueError

    def __add__(self, other):
        return vec(self[i] + other[i] for i in range(3))

    def __radd__(self, other):
        return self + other

    def __eq__(self, other):
        return (self[0] == other[0] and self[1] == other[1] and
                self[2] == other[2])

    def __sub__(self, other):
        return vec(self[i] - other[i] for i in range(3))

    def __mul__(self, other):
        if not isinstance(other, (float, int)):
            raise TypeError()
        return vec(self[i] * other for i in range(3))

    def __rmul__(self, other):
        return self * other

    def __getitem__(self, index):
        return self._coord.__getitem__(index)

    def __setitem__(self, index, value):
        self._coord.__setitem__(index, value)

    def copy(self):
        return vec(self._coord)

    def cross(self, other):
        a = self
        b = other
        return vec(a[1]*b[2] - a[2]*b[1],
                   a[2]*b[0] - a[0]*b[2],
                   a[0]*b[1] - a[1]*b[0])

    def dot(self, other):
        a = self
        b = other
        return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

    def length(self):
        return sqrt(sum(self[i]**2 for i in range(3)))

    def to_gp_Pnt(self):
        return gp_Pnt(*self)

    def to_gp_Vec(self):
        return gp_Vec(*self)

    def to_gp_Dir(self):
        return gp_Dir(*self)
