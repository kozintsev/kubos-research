

from OCC import TopExp
from OCC import TopAbs
from OCC import TopoDS

def get_key(d, value):
    for k, v in d.items():
        if v is value:
            return k


def subshapes(shape, shapetype):
    """Return a list of subshapes of the specified type"""
    # TODO: Return a generator instead of a list
    convertor = _convertors[shapetype]
    shapelist = []
    exp = TopExp.TopExp_Explorer(shape, shapetype)
    while exp.More():
        v = exp.Current()
        t = type(v)
        i = id(v)
        # v2 = convertor(exp.Current())
        k = get_key(_convertors, t)
        shapelist.append(v)
        exp.Next()
    return shapelist


_convertors = {TopAbs.TopAbs_VERTEX: TopoDS.TopoDS_Vertex,
              TopAbs.TopAbs_EDGE: TopoDS.TopoDS_Edge,
               TopAbs.TopAbs_WIRE: TopoDS.TopoDS_Wire,
              TopAbs.TopAbs_FACE: TopoDS.TopoDS_Face,
               TopAbs.TopAbs_SHELL: TopoDS.TopoDS_Shell,
               TopAbs.TopAbs_SOLID: TopoDS.TopoDS_Solid,
               TopAbs.TopAbs_COMPOUND: TopoDS.TopoDS_Compound,
               TopAbs.TopAbs_SHAPE: TopoDS.TopoDS_Shape}
