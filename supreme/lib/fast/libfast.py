__all__ = ['nonmax','corner_detect']

import numpy as np
from ctypes import c_int, c_uint8, Structure, POINTER, pointer

import supreme.config as SC
from supreme.ext.ctype_arrays import array_2d_uchar, atype

_lib = np.ctypeslib.load_library('libfast_',__file__)

class XY(Structure):
    _fields_ = [
        ('x', c_int),
        ('y', c_int)]

libfast_api = {
    'fast_nonmax' : (POINTER(XY),
                     [array_2d_uchar, c_int, c_int,
                      POINTER(XY), c_int, c_int, POINTER(c_int)]),
    'fast_free' : (None,[POINTER(XY)]),
}

for i in range(9,13):
    libfast_api['fast_corner_detect_%s' % i] = \
             (POINTER(XY),
              [array_2d_uchar, c_int, c_int,
               c_int, POINTER(c_int)])

for f, (restype, argtypes) in libfast_api.iteritems():
    func = getattr(_lib, f)
    func.restype = restype
    func.argtypes = argtypes

def nonmax():
    raise NotImplementedError

def corner_detect(image, barrier=10, size=12):
    """Detect corners.

    Parameters
    ----------
    image : array of uint8
        Input image.
    barrier : int
        Resistance to finding nearby corners.
    size : int
        Size of operator, must be in [9,12].

    Returns
    -------
    xy : (M,) array
        The M returned coordinates, with dtype
        ``('x', int), ('y', int)``.

    """
    if size not in range(9,13):
        raise ValueError("Size must be between 9 and 12.")
    image, = atype(image,np.uint8)
    barrier = c_int(barrier)
    height,width = image.shape
    corners = c_int()
    f = getattr(_lib,"fast_corner_detect_%s" % size)
    xy = f(image,width,height,barrier,pointer(corners))
    out = np.empty(corners.value,dtype=[('x',c_int),('y',c_int)])
    for i in range(corners.value):
        val = xy[i]
        out[i] = val.x, val.y
    _lib.fast_free(xy)
    return out

