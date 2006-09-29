import numpy as N
from ctypes import *

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
                     [array_2d_double, c_int, c_int,
                      array_2d_double]),
    }

def register_api(lib,api):
    import inspect
    for f, (restype, argtypes) in api.iteritems():
        func = getattr(lib, f)
        func.restype = restype
        func.argtypes = argtypes
        inspect.currentframe().f_locals[f] = func
    inspect.currentframe().f_locals['__all__'] = api.keys()

register_api(_lib,libsupreme_api)
#__all__ = libsupreme_api.keys()

# Python wrappers for libsupreme functions

def npnpoly(xvert,yvert,xpoint,ypoint):
   xi = N.ascontiguousarray(xvert.astype(N.double))
   yi = N.ascontiguousarray(yvert.astype(N.double))
   x = N.ascontiguousarray(xpoint)
   y = N.ascontiguousarray(ypoint)
   out = N.empty(len(x),dtype=N.int_)
   
   _lib.npnpoly(len(xi), xi, yi,
                len(x), x, y,
                out)
   return out
