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

    The polygon must be closed, i.e. x_vertices[0] == x_vertices[-1].

    Returns a boolean array of length len(x_points).
    
    """
    xi,yi,x,y = _atype([x_vertices,y_vertices,
                        x_points,y_points],[N.double]*4)
    
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
