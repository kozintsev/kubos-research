from __future__ import division

from OCC.BRepPrimAPI import *
from OCC.gp import *
from copy import deepcopy
from lib.vec import vec

def centered_box(l1, l2, l3):
    corner = gp_Pnt(-l1/2, -l2/2, -l3/2)
    return BRepPrimAPI_MakeBox(corner, l1, l2, l3).Solid()

def cylinder(start, end, radius):
    dir = end - start
    cyl = BRepPrimAPI_MakeCylinder(
            gp_Ax2(gp_Pnt(*start), gp_Dir(*dir)), radius, dir.length()).Solid()
    return cyl

shapes = []

def rounded_box(size, radius):

    l1 = size[0] - 2*radius
    l2 = size[1] - 2*radius
    l3 = size[2] - 2*radius

    shapes.extend([centered_box(l1, l2, size[2]), centered_box(l1, size[1], l3),
                   centered_box(size[0], l2, l3)])

    for corner in [vec(l1/2, l2/2, l3/2), vec(l1/2, -l2/2, -l3/2),
                   vec(-l1/2, l2/2, -l3/2), vec(-l1/2, -l2/2, l3/2)]:
        for i in range(3):
            corner_ = deepcopy(corner)
            corner_[i] *= -1
            shapes.append(cylinder(corner, corner_, radius))

    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            for s3 in [-1, 1]:
                sphere = BRepPrimAPI_MakeSphere(
                    gp_Pnt(s1*l1/2, s2*l2/2, s3*l3/2), radius).Solid()
                shapes.append(sphere)

    a = shapes.pop()
    for shape in shapes:
        a = BRepAlgoAPI_Fuse(a, shape).Shape()
    return a
    
