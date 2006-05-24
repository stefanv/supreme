__all__ = []

import numpy as N
import supreme.config as SC
import scipy as S
S.pkgload('interpolate')

def build(g):
    """Build a coordinate-path from a generator.

    g - Generate coordinates between (and including) start and end.
        The points generated should be roughly one pixel apart, and
        must not be discretised (i.e. (1.41,2.06) is fine).
        Initialised with start and end as parameters.

    """
    path = N.array([-1,-1], SC.itype)
    for i,coord in enumerate(g):
        coord = N.around(N.array(coord)).astype(SC.itype)
        if N.any(coord != path[-1]):
            path = N.vstack((path,coord))

    # TODO: find neighbouring overlaps as well
    return path[1:]
    

def line(start,end):
    """Generate coordinates for a line."""
    start = N.array(start, dtype=SC.ftype)
    end = N.array(end, dtype=SC.ftype)
    d = N.absolute(start-end).max()

    if (N.all(start == end)):
        yield end
        raise StopIteration

    for t in N.linspace(0,1,N.ceil(d)+1):
        yield (1-t)*start + t*end

def circle(centre,radius):
    """Generate coordinates for a circle."""
    if radius <= 0:
        raise ValueError("Radius must be positive.")    

    start = N.array(centre,dtype=SC.ftype)
    radius = SC.ftype(radius)
    d = N.ceil(2*N.pi*radius)
    thetas = N.linspace(0,2*N.pi,d)

    for t in thetas:
        yield radius*N.array([N.cos(t), N.sin(t)]) + centre

def spline(pts):
    """Generate coordinates for a cubic spline.

    The spline is guided by a polyline through the provided list of
    points.
    """

    from Nurbs.Crv import Crv

    x = [c[0] for c in pts]
    y = [c[1] for c in pts]
    dx = N.diff(x)
    dy = N.diff(y)
    d = N.ceil(N.sum(N.sqrt(dx**2 + dy**2)))

    
