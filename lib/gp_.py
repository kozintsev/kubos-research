from __future__ import absolute_import,division,print_function,unicode_literals

from OCC.gp import gp_Pnt
from OCC import TopoDS
from OCC.BRep import BRep_Tool

from lib.vec import vec

class point(object):
    def __init__(self, pnt):
        if isinstance(pnt, (list, tuple)):
            self._coord = list(pnt)
        elif isinstance(pnt, gp_Pnt):
            self._coord = [pnt.X(), pnt.Y(), pnt.Z()]
        elif isinstance(pnt, TopoDS.TopoDS_Vertex):
            pnt = BRep_Tool.Pnt(pnt)
            self._coord = [pnt.X(), pnt.Y(), pnt.Z()]
        elif isinstance(pnt, TopoDS.TopoDS_Shape):
            pnt = BRep_Tool.Pnt(TopoDS.TopoDS_vertex(pnt))
            self._coord = [pnt.X(), pnt.Y(), pnt.Z()]
        else:
            raise TypeError

    def __eq__(self, other):
        if type(self) == type(other):
            return self._coord == other._coord
        elif isinstance(other, gp_Pnt):
            return self.to_gp_Pnt().IsEqual(other, 0)
        else:
            return False

    def __ne__(self, other):
        return not(self == other)

    def __sub__(self, other):
        return [self[i] - other[i] for i in range(3)]

    def __getitem__(self, index):
        if isinstance(index, int):
            if -3 <= index <= 2:
                return self._coord[index]
            else:
                raise IndexError('Coordinate index out of range')
        elif isinstance(index, slice):
            raise NotImplementedError
        else:
            raise TypeError

    def __setitem__(self, index, value):
        if isinstance(index, int):
            if -3 <= index <= 2:
                self._coord[index] = value
            else:
                raise IndexError('Coordinate index out of range')
        elif isinstance(index, slice):
            raise NotImplementedError
        else:
            raise TypeError

    def __str__(self):
        return 'point({0})'.format(self._coord)

    def __repr__(self):
        return self.__str__()

    # probably make this type immutable and add a @lru_cache for this
    def to_gp_Pnt(self):
        return gp_Pnt(*self._coord)


class gp_Pnt_(gp_Pnt):
    """This is an extension of the gp_Pnt class.

    It provides a constructor that accepts lists and other types
    and allows accessing coordinate values through indices and slices
    as well as comparisons for equality
    >>> gp_Pnt_([4, 5, 42])
    gp_Pnt_([4.0, 5.0, 42.0])
    """

    def __init__(self, pnt):
        if isinstance(pnt, (list, tuple)):
            gp_Pnt.__init__(self, *pnt)
        elif isinstance(pnt, vec):
            gp_Pnt.__init__(self, *pnt)
        elif isinstance(pnt, gp_Pnt):
            gp_Pnt.__init__(self, pnt)
        elif isinstance(pnt, TopoDS.TopoDS_Vertex):
            # convert to type "gp_Pnt"
            gp_Pnt.__init__(self, BRep_Tool.Pnt(pnt))
        elif isinstance(pnt, TopoDS.TopoDS_Shape):
            gp_Pnt.__init__(self, BRep_Tool.Pnt(TopoDS.TopoDS_vertex(pnt)))
        else:
            raise TypeError

    def __eq__(self, other):
        if type(self) == type(other):
            return self.IsEqual(other, 0)
        else:
            return False

    def __ne__(self, other):
        return not(self == other)

    def __sub__(self, other):
        return vec(self[i] - other[i] for i in range(3))

    def __getitem__(self, index):
        if index in [0, -3]:
            return self.X()
        elif index in [1, -2]:
            return self.Y()
        elif index in [2, -1]:
            return self.Z()
        elif isinstance(index, slice):
            return [self[i] for i in range(index.start or 0, index.stop or 3)]
        else:
            # this is needed for unpacking
            raise IndexError

    def __setitem__(self, index, value):
        if index == 0:
            self.SetX(value)
        elif index == 1:
            self.SetY(value)
        elif index == 2:
            self.SetZ(value)
        elif isinstance(index, slice):
            stop = index.stop or 3
            start = index.start or 0
            if start <= 0 < stop:
                self.SetX(value[0 - start])
            if start <= 1 < stop:
                self.SetY(value[1 - start])
            if start <= 2 < stop:
                self.SetZ(value[2 - start])

    def __repr__(self):
        return 'gp_Pnt_({0})'.format(str(self[0:3]))
