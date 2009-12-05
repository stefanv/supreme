# -*- coding: utf-8 -*-

"""
Build coordinate paths from common geometric shapes.

A coordinate path is an ordered collection of coordinates,
as calculated from some parametric function.  Provided functions
include common geometric shapes, like lines, circles and Bézier
curves.

The path coordinates are discretised to the grid (always integer
values), and contain no adjacent duplicates (however, duplicates may
occur in the total path if the parametric curve crosses itself).
"""

__all__ = ['build','line','circle','spline']

import numpy as np
import supreme.config as sc

import itertools

def build(*iterables):
    """Build a coordinate-path from one or more iterable.

    Every iterator should yield coordinate tuples/arrays between (and
    including) start and end.  The points generated should be roughly
    one pixel apart, and does not need to be discretised
    (i.e. (1.41,2.06) is fine).

    """
    path = np.array([-1,-1], sc.itype)
    for i,coord in enumerate(itertools.chain(*iterables)):
        coord = np.around(np.array(coord)).astype(sc.itype)
        if np.any(coord != path[-1]):
            path = np.vstack((path,coord))

    # TODO: find neighbouring overlaps as well
    return path[1:]


def line(start,end):
    """Generate coordinates for a line."""
    start = np.array(start, dtype=sc.ftype)
    end = np.array(end, dtype=sc.ftype)
    d = np.sqrt(np.sum((start-end)**2))

    if (np.all(start == end)):
        yield end
        raise StopIteration

    for t in np.linspace(0,1,np.ceil(d)+1):
        yield (1-t)*start + t*end

def rectangle(top_corner,bottom_corner):
    """Generate coordinates for a rectangle."""
    tl = top_corner
    tr = (bottom_corner[0],top_corner[1])
    br = bottom_corner
    bl = (top_corner[0],bottom_corner[1])
    return itertools.chain(
        line(tl,tr),
        line(tr,br),
        line(br,bl),
        line(bl,tl)
        )

def circle(centre,radius):
    """Generate coordinates for a circle."""
    if radius <= 0:
        raise ValueError("Radius must be positive.")

    start = np.array(centre,dtype=sc.ftype)
    radius = sc.ftype(radius)
    d = np.ceil(2*np.pi*radius)
    thetas = np.linspace(0,2*np.pi,d)

    for t in thetas:
        yield radius*np.array([np.cos(t), np.sin(t)]) + centre

def spline(pts):
    """Generate coordinates for a cubic spline.

    A 4-dimensional (3rd order) spline is guided by a polyline through
    the provided list of points.  At least 3 points must be specified.
    """

    from supreme.lib.nurbs.Crv import Crv

    if len(pts) < 3:
        raise ValueError("At least 3 data points needed.")

    x = [c[0] for c in pts]
    y = [c[1] for c in pts]
    dx = np.diff(x)
    dy = np.diff(y)

    # Even though we will end up with d or less points, we have to sample
    # more closely, in case the spline has a high gradient.  d is therefore
    # multiplied by 2
    d = 2*np.ceil(np.sum(np.sqrt(dx**2 + dy**2)))

    cpts = np.vstack((x,y))
    knots = np.linspace(0.,1.,len(cpts[0])-1)
    knots = np.r_[0,0,knots,1,1]

    c = Crv(cpts,knots)
    points = c.pnt3D(np.linspace(0.,1,d))
    for p in np.transpose(points):
        x,y = p[:-1]
        yield x,y
