from __future__ import absolute_import,division,print_function,unicode_literals

from OCC import TopExp
from OCC import TopAbs
from OCC import TopoDS


def subshapes(shape, shapetype):
    """Return a list of subshapes of the specified type"""
    # TODO: Return a generator instead of a list
    convertor = _convertors[shapetype]
    shapelist = []
    exp = TopExp.TopExp_Explorer(shape, shapetype)
    while exp.More():
        shapelist.append(convertor(exp.Current()))
        exp.Next()
    return shapelist

_convertors = {TopAbs.TopAbs_VERTEX: TopoDS.TopoDS_vertex,
               TopAbs.TopAbs_EDGE: TopoDS.TopoDS_edge,
               TopAbs.TopAbs_WIRE: TopoDS.TopoDS_wire,
               TopAbs.TopAbs_FACE: TopoDS.TopoDS_face,
               TopAbs.TopAbs_SHELL: TopoDS.TopoDS_shell,
               TopAbs.TopAbs_SOLID: TopoDS.TopoDS_solid,
               TopAbs.TopAbs_COMPOUND: TopoDS.TopoDS_compound}
