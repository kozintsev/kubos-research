

from OCC import BRepAlgoAPI, BRepAlgo, TopoDS, TopAbs
from OCC.BRep import BRep_Tool
from OCC.GeomAPI import GeomAPI_ExtremaCurveCurve
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeVertex

from exceptions_ import ConstructionError
from lib.subshapes import subshapes


def intersection(a, b):

    if set([a.ShapeType(), b.ShapeType()]) <= set([TopAbs.TopAbs_WIRE, TopAbs.TopAbs_EDGE]):
        # TODO: check if the computed point is within the bounded part of
        # the curves
        l = []
        for c0 in subshapes(a, TopAbs.TopAbs_EDGE):
            c0_ = BRep_Tool.Curve(c0)[0]
            for c1 in subshapes(b, TopAbs.TopAbs_EDGE):
                c1_ = BRep_Tool.Curve(c1)[0]
                # TODO: use IntTools_EdgeEdge
                #  or IntTools_BeanBeanIntersector
                u = GeomAPI_ExtremaCurveCurve(c0_, c1_)
                par = u.LowerDistanceParameters()[0]
                pnt = c0_.GetObject().Value(par)
                l.append(BRepBuilderAPI_MakeVertex(pnt).Vertex())
        return l

    c = BRepAlgoAPI.BRepAlgoAPI_Common(a, b).Shape()
    comp = TopoDS.topods_Compound(c)
    # get the subshape of the compound:
    types = set([a.ShapeType(), b.ShapeType()])
    # compound = 0
    # compsolid = 1
    # solid = 2
    # shell = 3
    # face = 4
    # wire = 5
    # edge = 6
    # vertex = 7
    # shape = 8
    if types == set([TopAbs.TopAbs_FACE]):
        return [subshapes(comp, TopAbs.TopAbs_FACE)[0]]
    elif types == set([TopAbs.TopAbs_FACE, TopAbs.TopAbs_SOLID]):
        return [subshapes(comp, TopAbs.TopAbs_SHELL)[0]]
    elif types == set([TopAbs.TopAbs_SOLID]):
        return [subshapes(comp, TopAbs.TopAbs_SOLID)[0]]
    elif types == set([TopAbs.TopAbs_SHELL]):
        return [subshapes(comp, TopAbs.TopAbs_EDGE)[0]]
    else:
        raise ConstructionError()


def union(a, b):

    if set([a.ShapeType(), b.ShapeType()]) <= set([TopAbs.TopAbs_EDGE,
                                                   TopAbs.TopAbs_WIRE]):
        from lib import wirebuilder
        wire = wirebuilder.join([a, b])
        return [wire]

    # BRepAlgoAPI_Fuse does not work correctly here: It returns the difference
    # instead of the fuse
    c = BRepAlgo.BRepAlgo_Fuse(a, b).Shape()
    comp = TopoDS.topods_Compound(c)
    # get the subshape of the compound:
    if set([a.ShapeType(), b.ShapeType()]) == set([TopAbs.TopAbs_FACE]):
        return subshapes(comp, TopAbs.TopAbs_FACE)
    elif set([a.ShapeType(), b.ShapeType()]) == set([TopAbs.TopAbs_SOLID]):
        return subshapes(comp, TopAbs.TopAbs_SOLID)
    else:
        raise ConstructionError()


def difference(a, b):
    # using BRepAlgoAPI wold cause some problems here
    c = BRepAlgo.BRepAlgo_Cut(a, b).Shape()
    comp = TopoDS.topods_Compound(c)
    # get the subshape of the compound:
    if set([a.ShapeType(), b.ShapeType()]) == set([TopAbs.TopAbs_FACE]):
        return subshapes(comp, TopAbs.TopAbs_FACE)
    elif set([a.ShapeType(), b.ShapeType()]) == set([TopAbs.TopAbs_SOLID]):
        return subshapes(comp, TopAbs.TopAbs_SOLID)
    else:
        raise ConstructionError()
