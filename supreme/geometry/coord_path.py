__all__ = []

import numpy as N
import supreme.config as SC

def build(g):
    """Build a coordinate-path from a generator.

    g - Generate coordinates between (and including) start and end.
        The points generated should be roughly one pixel apart, and
        must not be discretised (i.e. (1.41,2.06) is fine).
        Initialised with start and end as parameters.

    """
    path = [None]
    for i,coord in enumerate(g):
        coord = N.round_(coord)
        if N.any(coord != path[-1]):
            path.append(list(coord))

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

