import numpy as np

def atype(arrays, types):
    """Return contiguous arrays of given types.

    arrays - list of input arrays
    types - list of corresponding types

    """
    out = ()
    try:
        za = zip(arrays,types)
    except:
        za = [(arrays,types)]

    out = ()
    for A,T in za:
        out += np.ascontiguousarray(A,T),

    return out

array_1d_double = np.ctypeslib.ndpointer(dtype=np.double, ndim=1,
                                         flags='CONTIGUOUS')

array_2d_double = np.ctypeslib.ndpointer(dtype=np.double, ndim=2,
                                         flags='CONTIGUOUS')

array_1d_int = np.ctypeslib.ndpointer(dtype=np.intc, ndim=1,
                                      flags='CONTIGUOUS')

array_2d_int = np.ctypeslib.ndpointer(dtype=np.intc, ndim=2,
                                      flags='CONTIGUOUS')

array_1d_uchar = np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1,
                                        flags='CONTIGUOUS')

array_2d_uchar = np.ctypeslib.ndpointer(dtype=np.uint8, ndim=2,
                                        flags='CONTIGUOUS')
