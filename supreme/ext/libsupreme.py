import numpy as N
from ctypes import c_int, c_double, Structure, POINTER

from numpy.testing import set_local_path, restore_path
set_local_path('../..')
import supreme.config as SC
restore_path()

_lib = N.ctypeslib.load_library('libsupreme_',__file__)

array_1d_double = N.ctypeslib.ndpointer(dtype=N.double,ndim=1,flags='CONTIGUOUS')
array_2d_double = N.ctypeslib.ndpointer(dtype=N.double,ndim=2,flags='CONTIGUOUS')
array_1d_int = N.ctypeslib.ndpointer(dtype=N.intc,ndim=1,flags='CONTIGUOUS')

# Define libsupreme API

class POI(Structure):
    """Point of intersection.

    """
    _fields_ =  [("x", c_double),
                 ("y", c_double),
                 ("type", c_int)]

# Albert's ctypes pattern
libsupreme_api = {
   'npnpoly' : (None,
                [c_int, array_1d_double, array_1d_double,
                 c_int, array_1d_double, array_1d_double,
                 array_1d_int]),
   'variance_map' : (None,
                     [c_int, c_int, array_2d_double, array_2d_double,
                      c_int, c_int]),
                     
   'line_intersect' : (None,
                       [c_double, c_double, c_double, c_double,
                        c_double, c_double, c_double, c_double,
                        POINTER(POI)]),
   'poly_clip' : (int,
                  [c_int, array_1d_double, array_1d_double,
                   c_double, c_double, c_double, c_double,
                   array_1d_double, array_1d_double]),
    }

def register_api(lib,api):
    import inspect
    parent_frame = inspect.currentframe().f_back
    for f, (restype, argtypes) in api.iteritems():
        func = getattr(lib, f)
        func.restype = restype
        func.argtypes = argtypes

register_api(_lib,libsupreme_api)

# Python wrappers for libsupreme functions

def _atype(arrays, types):
    """Return contiguous arrays of given types.

    arrays - list of input arrays
    types - list of corresponding types
    
    """
    return [N.ascontiguousarray(A).astype(T) for A,T in zip(arrays,types)]

def npnpoly(x_vertices, y_vertices, x_points, y_points):
    """Calculate whether points are in a given polygon.

    Returns a boolean array of length len(x_points).
    
    """
    xi,yi,x,y = _atype([x_vertices,y_vertices,
                        x_points,y_points],[N.double]*4)

    if xi[0] != xi[-1] or yi[0] != yi[-1]:
        xi = N.append(xi,x[0])
        yi = N.append(yi,y[0])

    out = N.empty(len(x),dtype=N.intc)
    
    _lib.npnpoly(len(xi), xi, yi,
                 len(x), x, y,
                 out)
    return out

def variance_map(image, shape=(3,3)):
    """Calculate the variance map of a 2D image.

    image -- of shape MxN
    shape -- shape of window over which variance is calculated

    A window of given shape is moved over the image, and at each point
    the variance of all the pixels in the window is stored.

    """
    image = N.asarray(image).astype(N.double)
    assert image.ndim == 2, "Image must be 2-dimensional"
    window_size_rows, window_size_columns = shape
    rows, columns = image.shape
    output = N.zeros(image.shape,SC.ftype)
    _lib.variance_map(rows, columns, image, output,
                      window_size_rows, window_size_columns)
    return output

def line_intersect(x0,y0,x1,y1,
                   x2,y2,x3,y3):
    """Calculate the intersection between two lines.

    The first line runs from (x0,y0) to (x1,y1) and the second from
    (x2,y2) to (x3,y3).

    Return the point of intersection, (x,y), and its type:
      0 -- Normal intersection
      1 -- Intersects outside given segments
      2 -- Parallel
      3 -- Co-incident
    """
    x0,x1,x2,x3,y0,y1,y2,y3 = map(c_double, [x0,x1,x2,x3,y0,y1,y2,y3])
    p = POI()
    _lib.line_intersect(x0,y0,x1,y1,x2,y2,x3,y3,p)
    return (p.x,p.y), p.type

def poly_clip(x, y, xleft, xright, ytop, ybottom):
    """Clip a polygon to the given bounding box.

    x and y are 1D arrays describing the coordinates of the vertices.
    xleft, xright, ytop and ybottom specify the borders of the
    bounding box.  Note that a cartesian axis system is used such that
    the following must hold:

    x_left < x_right
    y_bottom < y_top

    The x and y coordinates of the vertices of the resulting polygon
    are returned.
    
    """
    x,y = _atype([x,y],[N.double,N.double])

    assert len(x) == len(y), "Equal number of x and y coordinates required"
    assert ytop > ybottom
    assert xleft < xright

    # close polygon if necessary
    if x[0] != x[-1] or y[0] != y[-1]:
        x = N.append(x,x[0])
        y = N.append(y,y[0])
        
    xleft,xright,ytop,ybottom = map(N.double,[xleft,xright,ytop,ybottom])

    workx = N.empty(2*len(x-1),dtype=N.double)
    worky = N.empty(2*len(x-1),dtype=N.double)
    M = _lib.poly_clip(len(x),x,y,xleft,xright,ytop,ybottom,workx,worky)
    workx[M] = workx[0]
    worky[M] = worky[0]
    return workx[:M], worky[:M]
