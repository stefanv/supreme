import numpy as N
from ctypes import c_int

from numpy.testing import set_local_path, restore_path
set_local_path('../..')
import supreme.config as SC
restore_path()

_lib = N.ctypeslib.load_library('libsupreme_',__file__)

array_1d_double = N.ctypeslib.ndpointer(dtype=N.double,ndim=1,flags='CONTIGUOUS')
array_2d_double = N.ctypeslib.ndpointer(dtype=N.double,ndim=2,flags='CONTIGUOUS')
array_1d_int = N.ctypeslib.ndpointer(dtype=N.intc,ndim=1,flags='CONTIGUOUS')

# Define libsupreme API

# Albert's ctypes pattern
libsupreme_api = {
   'npnpoly' : (None,
                [c_int, array_1d_double, array_1d_double,
                 c_int, array_1d_double, array_1d_double,
                 array_1d_int]),
   'variance_map' : (None,
                     [c_int, c_int, array_2d_double, array_2d_double,
                      c_int, c_int]),
    }

def register_api(lib,api):
    import inspect
    parent_frame = inspect.currentframe().f_back
    for f, (restype, argtypes) in api.iteritems():
        func = getattr(lib, f)
        func.restype = restype
        func.argtypes = argtypes
        parent_frame.f_locals[f] = func
    parent_frame.f_locals['__all__'] = api.keys()

register_api(_lib,libsupreme_api)

# Python wrappers for libsupreme functions

def _atype(arrays, types):
    """Return contiguous arrays of given types.

    arrays - list of input arrays
    types - list of corresponding types
    
    """
    return [N.ascontiguousarray(A).astype(T) for A,T in zip(arrays,types)]

def npnpoly(x_vertices, y_vertices, x_points, y_points):
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
