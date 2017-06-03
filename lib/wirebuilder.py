from __future__ import absolute_import,division,print_function,unicode_literals

from OCC.TopExp import TopExp
from OCC import TopAbs
from OCC.ShapeAnalysis import ShapeAnalysis_WireOrder
from OCC.Precision import Precision
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeWire
from OCC.BRepBuilderAPI import BRepBuilderAPI_WireDone

from lib import gp_
from lib.subshapes import subshapes


def join(list):
    """Join edges and wires to a wire.
    Raise an error if it is not possible to create a single wire"""
    # create a list of all edges (split wires)
    edges = []
    for a in list:
        if a.ShapeType() not in [TopAbs.TopAbs_EDGE, TopAbs.TopAbs_WIRE]:
            raise TypeError
        edges.extend(subshapes(a, TopAbs.TopAbs_EDGE))
    wire = _join_edges(edges)
    return wire


def _join_edges(edgelist):
    """Join edges to a wire. Raise an InvalidInputException if no single wire
    could be created"""
    wire_order = ShapeAnalysis_WireOrder(True, Precision.PConfusion())
    for edge in edgelist:
        wire_order.Add(gp_.gp_Pnt_(TopExp.FirstVertex(edge)).XYZ(),
                       gp_.gp_Pnt_(TopExp.LastVertex(edge)).XYZ())
    wire_order.Perform()
    assert wire_order.IsDone()
    wire_order.SetChains(Precision.PConfusion())

    n = wire_order.NbChains()
    # n = 1: one closed chain
    # n = 2: one open chain
    # n > 2: multiple chains
    if n > 2:
        raise RuntimeError

    start, end = wire_order.Chain(n)
    wirebuilder = BRepBuilderAPI_MakeWire()
    for i in range(start, end + 1):
        idx = abs(wire_order.Ordered(i))
        # If the edge must be reversed, idx will be negative. The reversal is
        # handled by wirebuilder
        wirebuilder.Add(edgelist[idx - 1])
        assert wirebuilder.Error() == BRepBuilderAPI_WireDone
    return wirebuilder.Wire()
